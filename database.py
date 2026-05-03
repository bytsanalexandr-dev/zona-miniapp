import os
import json
import psycopg2
import psycopg2.pool
from contextlib import contextmanager
from datetime import datetime
from typing import Optional

# Direct connection uses IPv6-only (blocked on many networks).
# Use the Supabase IPv4 connection pooler (eu-west-1, port 6543) as default.
_POOLER_URL = (
    "postgresql://postgres.fpbyrtpxntfuixuzjamr:67206720Sim!www"
    "@aws-0-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require"
)
DATABASE_URL = os.environ.get("DATABASE_URL", _POOLER_URL)

_pool: Optional[psycopg2.pool.SimpleConnectionPool] = None


def _get_pool() -> psycopg2.pool.SimpleConnectionPool:
    global _pool
    if _pool is None:
        _pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)
    return _pool


@contextmanager
def _cursor():
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


# ── Schema ────────────────────────────────────────────────────────────────────

def init_db():
    with _cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_games (
                user_id      BIGINT PRIMARY KEY,
                player_name  TEXT,
                days_survived INTEGER DEFAULT 0,
                tier         INTEGER DEFAULT 1,
                last_updated TEXT,
                data         JSONB NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                user_id      BIGINT,
                id           TEXT,
                name         TEXT,
                description  TEXT,
                unlocked_day INTEGER,
                PRIMARY KEY (user_id, id)
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                user_id        BIGINT PRIMARY KEY,
                player_name    TEXT,
                score          DOUBLE PRECISION,
                influence      DOUBLE PRECISION,
                tier           INTEGER,
                rank_name      TEXT,
                days_played    INTEGER,
                num_businesses INTEGER,
                gang_size      INTEGER,
                territories    INTEGER,
                saved_at       TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS globe_territories (
                territory_id  TEXT PRIMARY KEY,
                owner_user_id BIGINT,
                owner_name    TEXT,
                captured_at   TEXT
            )
        ''')
    print("[DB] Tables ready (PostgreSQL/Supabase)")


# ── Game state ────────────────────────────────────────────────────────────────

def save_game(user_id: int, state: dict):
    with _cursor() as cur:
        cur.execute(
            '''
            INSERT INTO user_games
                (user_id, player_name, days_survived, tier, last_updated, data)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                player_name   = EXCLUDED.player_name,
                days_survived = EXCLUDED.days_survived,
                tier          = EXCLUDED.tier,
                last_updated  = EXCLUDED.last_updated,
                data          = EXCLUDED.data
            ''',
            (
                user_id,
                state.get('player_name', 'Заключённый'),
                state.get('days_survived', 0),
                state.get('tier', 1),
                datetime.now().strftime('%d.%m.%Y %H:%M'),
                json.dumps(state, ensure_ascii=False),
            )
        )


def load_game(user_id: int) -> Optional[dict]:
    with _cursor() as cur:
        cur.execute('SELECT data FROM user_games WHERE user_id = %s', (user_id,))
        row = cur.fetchone()
        if row:
            data = row[0]
            return data if isinstance(data, dict) else json.loads(data)
    return None


def user_exists(user_id: int) -> bool:
    with _cursor() as cur:
        cur.execute('SELECT 1 FROM user_games WHERE user_id = %s', (user_id,))
        return cur.fetchone() is not None


# ── Achievements ──────────────────────────────────────────────────────────────

def unlock_achievement(user_id: int, achievement_id: str,
                       name: str, description: str, day: int):
    with _cursor() as cur:
        cur.execute(
            '''
            INSERT INTO achievements (user_id, id, name, description, unlocked_day)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id, id) DO NOTHING
            ''',
            (user_id, achievement_id, name, description, day)
        )


def get_achievements(user_id: int) -> list:
    with _cursor() as cur:
        cur.execute(
            '''SELECT id, name, description, unlocked_day
               FROM achievements
               WHERE user_id = %s
               ORDER BY unlocked_day''',
            (user_id,)
        )
        return cur.fetchall()


def has_achievement(user_id: int, achievement_id: str) -> bool:
    with _cursor() as cur:
        cur.execute(
            'SELECT 1 FROM achievements WHERE user_id = %s AND id = %s',
            (user_id, achievement_id)
        )
        return cur.fetchone() is not None


# ── Leaderboard ───────────────────────────────────────────────────────────────

def update_leaderboard(user_id: int, player_name: str, score: float,
                       influence: float, tier: int, rank_name: str,
                       days_played: int, num_businesses: int,
                       gang_size: int, territories: int):
    with _cursor() as cur:
        cur.execute(
            '''
            INSERT INTO leaderboard
                (user_id, player_name, score, influence, tier, rank_name,
                 days_played, num_businesses, gang_size, territories, saved_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                player_name    = EXCLUDED.player_name,
                score          = EXCLUDED.score,
                influence      = EXCLUDED.influence,
                tier           = EXCLUDED.tier,
                rank_name      = EXCLUDED.rank_name,
                days_played    = EXCLUDED.days_played,
                num_businesses = EXCLUDED.num_businesses,
                gang_size      = EXCLUDED.gang_size,
                territories    = EXCLUDED.territories,
                saved_at       = EXCLUDED.saved_at
            ''',
            (user_id, player_name, score, influence, tier, rank_name,
             days_played, num_businesses, gang_size, territories,
             datetime.now().strftime('%d.%m.%Y %H:%M'))
        )


def get_globe_territories() -> list:
    with _cursor() as cur:
        cur.execute('SELECT territory_id, owner_user_id, owner_name FROM globe_territories')
        return cur.fetchall()


def capture_globe_territory(territory_id: str, user_id: int, owner_name: str):
    with _cursor() as cur:
        cur.execute(
            '''INSERT INTO globe_territories (territory_id, owner_user_id, owner_name, captured_at)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (territory_id) DO UPDATE SET
                   owner_user_id = EXCLUDED.owner_user_id,
                   owner_name    = EXCLUDED.owner_name,
                   captured_at   = EXCLUDED.captured_at''',
            (territory_id, user_id, owner_name,
             datetime.now().strftime('%d.%m.%Y %H:%M'))
        )


def get_globe_top10() -> list:
    with _cursor() as cur:
        cur.execute('''
            SELECT owner_user_id, owner_name, COUNT(*) AS cnt
            FROM globe_territories
            WHERE owner_user_id IS NOT NULL
            GROUP BY owner_user_id, owner_name
            ORDER BY cnt DESC
            LIMIT 10
        ''')
        return cur.fetchall()


def get_leaderboard() -> list:
    with _cursor() as cur:
        cur.execute(
            '''SELECT user_id, player_name, score, influence, tier, rank_name,
                      days_played, num_businesses, gang_size, territories, saved_at
               FROM leaderboard
               ORDER BY score DESC
               LIMIT 10'''
        )
        return cur.fetchall()
