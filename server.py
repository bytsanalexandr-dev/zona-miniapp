import os
import sys
import asyncio
import threading
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Any

sys.path.insert(0, os.path.dirname(__file__))
import database as db
import game_engine as ge
import economy
import gang as gng
import events as ev
import globe as gl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db.init_db()
        logger.info("DB initialised")
    except Exception as e:
        logger.error(f"DB init failed (will retry on first request): {e}")
    _start_bot_thread()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_BASE = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(_BASE, "static")), name="static")


# ── Request models ────────────────────────────────────────────────────────────

class NewGameBody(BaseModel):
    user_id: int
    player_name: str

class ActionBody(BaseModel):
    action_id: str
    params: Optional[dict] = None

class BuyItemBody(BaseModel):
    item_id: str
    quantity: int = 1

class BuyBusinessBody(BaseModel):
    business_id: str

class RecruitBody(BaseModel):
    member_type: Optional[str] = None

class CaptureTerritoryBody(BaseModel):
    territory_id: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_state(user_id: int):
    state = db.load_game(user_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Игра не найдена. Начни новую игру.")
    return state


def _save_and_return(user_id: int, state: dict, extra: dict = None):
    state['user_id'] = user_id
    db.save_game(user_id, state)
    payload = {"success": True, "new_state": state}
    if extra:
        payload.update(extra)
    return payload


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return FileResponse(os.path.join(_BASE, "static", "index.html"))


@app.post("/api/new_game")
def new_game(body: NewGameBody):
    state = ge.new_game(body.player_name.strip() or "Заключённый")
    state['user_id'] = body.user_id
    db.save_game(body.user_id, state)
    return {"success": True, "new_state": state}


@app.get("/api/state/{user_id}")
def get_state(user_id: int):
    state = db.load_game(user_id)
    if state is None:
        return {"exists": False}
    state['user_id'] = user_id
    return {"exists": True, "state": state}


@app.post("/api/action/{user_id}")
def do_action(user_id: int, body: ActionBody):
    state = _get_state(user_id)
    state['user_id'] = user_id

    # Handle pending event resolution
    if body.action_id == '_resolve_event':
        params = body.params or {}
        pending = state.get('pending_event')
        if pending:
            choice_idx = params.get('choice', 0)
            event_msgs = ev.resolve_choice(state, pending, choice_idx)
            state.pop('pending_event', None)
            ge._check_achievements(state)
            plain_msgs = [msg for _, msg in event_msgs]
            return _save_and_return(user_id, state, {
                "messages": plain_msgs,
                "events": event_msgs,
            })
        return _save_and_return(user_id, state, {"messages": ["Нет активного события."], "events": []})

    msgs = ge.do_action(state, body.action_id)
    return _save_and_return(user_id, state, {
        "messages": msgs,
        "events": []
    })


@app.post("/api/next_day/{user_id}")
def next_day(user_id: int):
    state = _get_state(user_id)
    state['user_id'] = user_id

    day_events = ge.advance_day(state)

    # Collect newly unlocked achievements
    new_ach = state.pop('achievements', [])

    return _save_and_return(user_id, state, {
        "day_events": day_events,
        "achievements_unlocked": new_ach,
    })


@app.post("/api/buy_item/{user_id}")
def buy_item(user_id: int, body: BuyItemBody):
    state = _get_state(user_id)
    state['user_id'] = user_id
    results = []
    for _ in range(max(1, body.quantity)):
        ok, msg = economy.buy_item(state, body.item_id)
        results.append(msg)
        if not ok:
            break
    return _save_and_return(user_id, state, {
        "success": ok,
        "message": results[-1] if results else "Ошибка"
    })


@app.post("/api/buy_business/{user_id}")
def buy_business(user_id: int, body: BuyBusinessBody):
    state = _get_state(user_id)
    state['user_id'] = user_id
    ok, msg = economy.buy_business(state, body.business_id)
    return _save_and_return(user_id, state, {"success": ok, "message": msg})


@app.post("/api/upgrade_business/{user_id}")
def upgrade_business(user_id: int, body: BuyBusinessBody):
    state = _get_state(user_id)
    state['user_id'] = user_id
    ok, msg = economy.upgrade_business(state, body.business_id)
    return _save_and_return(user_id, state, {"success": ok, "message": msg})


@app.post("/api/sell_business/{user_id}")
def sell_business(user_id: int, body: BuyBusinessBody):
    state = _get_state(user_id)
    state['user_id'] = user_id
    ok, msg = economy.sell_business(state, body.business_id)
    return _save_and_return(user_id, state, {"success": ok, "message": msg})


@app.post("/api/recruit/{user_id}")
def recruit(user_id: int, body: RecruitBody):
    state = _get_state(user_id)
    state['user_id'] = user_id
    ok, msg = gng.recruit_member(state)
    return _save_and_return(user_id, state, {"success": ok, "message": msg})


@app.post("/api/fire_member/{user_id}")
def fire_member(user_id: int, body: dict):
    state = _get_state(user_id)
    state['user_id'] = user_id
    member_id = body.get("member_id")
    gang = state.get("gang_members", [])
    before = len(gang)
    state["gang_members"] = [m for m in gang if m.get("id") != member_id]
    ok = len(state["gang_members"]) < before
    return _save_and_return(user_id, state, {
        "success": ok,
        "message": "Уволен" if ok else "Не найден"
    })


@app.post("/api/use_item/{user_id}")
def use_item(user_id: int, body: dict):
    state = _get_state(user_id)
    state['user_id'] = user_id
    item_id = body.get("item_id", "")
    ok, effects, msg = economy.use_item(state, item_id)
    return _save_and_return(user_id, state, {"success": ok, "message": msg})


@app.get("/api/leaderboard")
def leaderboard():
    rows = db.get_leaderboard()
    result = []
    for row in rows:
        uid, name, score, inf, tier, rank_name, days, bizs, gang, terr, saved = row
        result.append({
            "user_id": uid,
            "player_name": name,
            "score": score,
            "influence": inf,
            "tier": tier,
            "rank_name": rank_name,
            "days_played": days,
            "num_businesses": bizs,
            "gang_size": gang,
            "territories": terr,
            "saved_at": saved,
        })
    return {"leaderboard": result}


@app.get("/api/shop/{user_id}")
def get_shop(user_id: int):
    state = _get_state(user_id)
    state['user_id'] = user_id
    items = economy.get_shop_items(state)
    result = {}
    for item_id, item in items:
        can_buy, reason = economy.can_buy(state, item_id)
        result[item_id] = {**item, "can_buy": can_buy, "reason": reason}
    return {"items": result}


@app.get("/api/businesses/{user_id}")
def get_businesses(user_id: int):
    state = _get_state(user_id)
    state['user_id'] = user_id
    tier = state.get('tier', 1)
    owned_ids = {b['template_id'] for b in state.get('businesses', [])}
    available = {
        tid: tmpl for tid, tmpl in economy.BUSINESSES.items()
        if tmpl['tier'] <= tier and tid not in owned_ids
    }
    owned_detail = []
    for biz in state.get('businesses', []):
        tmpl = economy.BUSINESSES.get(biz['template_id'], {})
        income = int(economy.business_daily_income(biz, state))
        can_up, reason_up = economy.can_buy_business(state, biz['template_id'])
        max_lvl = tmpl.get('max_level', 5)
        if biz['level'] < max_lvl:
            upg_cost = int(tmpl.get('cost', 0) * (tmpl.get('level_mult', 2) ** biz['level']))
        else:
            upg_cost = None
        owned_detail.append({**biz, "daily_income": income, "upgrade_cost": upg_cost})
    return {"owned": owned_detail, "available": available}


# ── Globe ─────────────────────────────────────────────────────────────────────

@app.get("/api/globe_data/{user_id}")
def globe_data(user_id: int):
    _get_state(user_id)  # ensure player exists

    owned_rows = db.get_globe_territories()
    ownership  = {row[0]: {'owner_user_id': row[1], 'owner_name': row[2]} for row in owned_rows}

    top10_rows = db.get_globe_top10()
    player_colors: dict = {}
    top10 = []
    for i, (uid, uname, cnt) in enumerate(top10_rows):
        color = gl.PLAYER_COLORS[i] if i < len(gl.PLAYER_COLORS) else '#aaaaaa'
        player_colors[uid] = color
        top10.append({
            'user_id': uid, 'username': uname,
            'territory_count': cnt,
            'globe_percent': round(cnt / gl.TOTAL_TERRITORIES * 100, 1),
            'color': color,
        })
    if user_id not in player_colors:
        player_colors[user_id] = '#ffffff'

    territories = []
    for tdef in gl.TERRITORY_DEFS:
        own = ownership.get(tdef['id'], {})
        territories.append({**tdef,
                             'owner_user_id': own.get('owner_user_id'),
                             'owner_name':    own.get('owner_name')})

    my_count      = sum(1 for t in territories if t['owner_user_id'] == user_id)
    total_claimed = sum(1 for t in territories if t['owner_user_id'] is not None)

    return {
        'territories':              territories,
        'player_colors':            {str(k): v for k, v in player_colors.items()},
        'top10':                    top10,
        'current_player_percent':   round(my_count / gl.TOTAL_TERRITORIES * 100, 1),
        'total_claimed_percent':    round(total_claimed / gl.TOTAL_TERRITORIES * 100, 1),
        'my_territory_count':       my_count,
        'total_territories':        gl.TOTAL_TERRITORIES,
    }


@app.post("/api/capture_territory/{user_id}")
def capture_territory_endpoint(user_id: int, body: CaptureTerritoryBody):
    state = _get_state(user_id)
    state['user_id'] = user_id

    tdef = gl.get_territory_def(body.territory_id)
    if not tdef:
        raise HTTPException(status_code=404, detail="Территория не найдена")

    if state.get('tier', 1) < tdef['tier_req']:
        return {'success': False, 'message': f"Нужен тир {tdef['tier_req']}"}

    owned_rows = db.get_globe_territories()
    ownership  = {row[0]: row[1] for row in owned_rows}
    current_owner = ownership.get(body.territory_id)

    if current_owner == user_id:
        return {'success': False, 'message': 'Эта территория уже твоя'}

    cost = tdef['capture_cost'] * (2 if current_owner else 1)
    if state.get('influence', 0) < cost:
        n = f'{int(cost):,}'.replace(',', ' ')
        return {'success': False, 'message': f'Нужно {n} влияния'}

    state['influence'] = state.get('influence', 0) - cost
    db.save_game(user_id, state)
    db.capture_globe_territory(body.territory_id, user_id,
                               state.get('player_name', 'Игрок'))

    # Check world domination
    my_total = sum(1 for row in db.get_globe_territories() if row[1] == user_id)
    if my_total >= gl.TOTAL_TERRITORIES:
        return {'success': True, 'world_domination': True,
                'message': '🌍 МИРОВОЕ ГОСПОДСТВО! Ты захватил весь мир!',
                'new_state': state}

    return {'success': True,
            'message': f'Захвачено: {tdef["name"]}!',
            'new_state': state}


# ── Bot thread ────────────────────────────────────────────────────────────────

def _start_bot_thread():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not set – bot won't start")
        return
    t = threading.Thread(target=_run_bot, args=(token,), daemon=True)
    t.start()
    logger.info("Bot thread started")


def _run_bot(token: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        from bot import run_bot
        loop.run_until_complete(run_bot(token))
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
    finally:
        loop.close()
