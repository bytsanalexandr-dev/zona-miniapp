import sqlite3
import json
from datetime import datetime

DB_PATH = "zona_miniapp.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS user_games (
            user_id     INTEGER PRIMARY KEY,
            player_name TEXT,
            days_survived INTEGER DEFAULT 0,
            tier        INTEGER DEFAULT 1,
            last_updated TEXT,
            data        TEXT NOT NULL
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS achievements (
            user_id     INTEGER,
            id          TEXT,
            name        TEXT,
            description TEXT,
            unlocked_day INTEGER,
            PRIMARY KEY (user_id, id)
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
            user_id     INTEGER PRIMARY KEY,
            player_name TEXT,
            score       REAL,
            influence   REAL,
            tier        INTEGER,
            rank_name   TEXT,
            days_played INTEGER,
            num_businesses INTEGER,
            gang_size   INTEGER,
            territories INTEGER,
            saved_at    TEXT
        )''')
        conn.commit()


def save_game(user_id, state):
    data = json.dumps(state, ensure_ascii=False)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''INSERT OR REPLACE INTO user_games
               (user_id, player_name, days_survived, tier, last_updated, data)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (user_id,
             state.get('player_name', 'Заключённый'),
             state.get('days_survived', 0),
             state.get('tier', 1),
             datetime.now().strftime('%d.%m.%Y %H:%M'),
             data)
        )
        conn.commit()


def load_game(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            'SELECT data FROM user_games WHERE user_id=?', (user_id,)
        ).fetchone()
        if row:
            return json.loads(row[0])
    return None


def user_exists(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            'SELECT user_id FROM user_games WHERE user_id=?', (user_id,)
        ).fetchone()
        return row is not None


def unlock_achievement(user_id, achievement_id, name, description, day):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''INSERT OR IGNORE INTO achievements
               (user_id, id, name, description, unlocked_day)
               VALUES (?, ?, ?, ?, ?)''',
            (user_id, achievement_id, name, description, day)
        )
        conn.commit()


def get_achievements(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            '''SELECT id, name, description, unlocked_day FROM achievements
               WHERE user_id=? ORDER BY unlocked_day''',
            (user_id,)
        ).fetchall()


def has_achievement(user_id, achievement_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            'SELECT id FROM achievements WHERE user_id=? AND id=?',
            (user_id, achievement_id)
        ).fetchone()
        return row is not None


def update_leaderboard(user_id, player_name, score, influence, tier, rank_name,
                       days_played, num_businesses, gang_size, territories):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''INSERT OR REPLACE INTO leaderboard
               (user_id, player_name, score, influence, tier, rank_name, days_played,
                num_businesses, gang_size, territories, saved_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, player_name, score, influence, tier, rank_name,
             days_played, num_businesses, gang_size, territories,
             datetime.now().strftime('%d.%m.%Y %H:%M'))
        )
        conn.commit()


def get_leaderboard():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            '''SELECT user_id, player_name, score, influence, tier, rank_name,
                      days_played, num_businesses, gang_size, territories, saved_at
               FROM leaderboard ORDER BY score DESC LIMIT 10'''
        ).fetchall()
