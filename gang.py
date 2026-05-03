import random
import uuid

_NAMES = [
    'Коля', 'Витёк', 'Сёма', 'Жека', 'Пашка', 'Лёха', 'Вася', 'Гриша',
    'Серёга', 'Толян', 'Борян', 'Федос', 'Димон', 'Ромка', 'Санёк',
    'Игорёк', 'Лёша', 'Стёпа', 'Миха', 'Кирюха', 'Рустам', 'Тимур',
    'Жора', 'Петро', 'Вовик', 'Слава', 'Юрик', 'Олег', 'Игорь', 'Дима',
]

# ── Member type definitions ───────────────────────────────────────────────────
MEMBER_TYPES = {
    # TIER 1 — Зона
    'shesterka': {
        'name_ru': 'Шестёрка', 'tier': 1,
        'daily_cost': 0, 'income_range': (2, 5),
        'str_range': (10, 20), 'loyalty_range': (40, 60),
        'specialty': 'earner',
        'recruit_req': {'tier': 1, 'reputation': 0},
        'recruit_cost': 0,
        'desc': 'Верный, но слабый. Приносит мелочь.',
    },
    'boyets': {
        'name_ru': 'Боец', 'tier': 1,
        'daily_cost': 5, 'income_range': (0, 0),
        'str_range': (30, 50), 'loyalty_range': (50, 70),
        'specialty': 'fighter',
        'recruit_req': {'tier': 1, 'reputation': 30},
        'recruit_cost': 20,
        'desc': 'Дерётся за тебя. Дохода не приносит.',
    },
    # TIER 2 — Район
    'ulichny': {
        'name_ru': 'Уличный', 'tier': 2,
        'daily_cost': 10, 'income_range': (20, 40),
        'str_range': (20, 40), 'loyalty_range': (40, 65),
        'specialty': 'earner',
        'recruit_req': {'tier': 2, 'influence': 100},
        'recruit_cost': 100,
        'desc': 'Работает на улице, приносит деньги.',
    },
    'smotrjashchiy_tochki': {
        'name_ru': 'Смотрящий за точкой', 'tier': 2,
        'daily_cost': 30, 'income_range': (80, 120),
        'str_range': (30, 55), 'loyalty_range': (50, 75),
        'specialty': 'manager',
        'recruit_req': {'tier': 2, 'influence': 200},
        'recruit_cost': 500,
        'desc': 'Управляет точкой. Серьёзный доход.',
        'special': 'manage_business',
    },
    'voditel': {
        'name_ru': 'Водитель', 'tier': 2,
        'daily_cost': 20, 'income_range': (0, 0),
        'str_range': (15, 30), 'loyalty_range': (45, 70),
        'specialty': 'driver',
        'recruit_req': {'tier': 2, 'influence': 150},
        'recruit_cost': 200,
        'desc': 'Нужен для некоторых операций.',
    },
    # TIER 3 — Город
    'brigadir': {
        'name_ru': 'Бригадир', 'tier': 3,
        'daily_cost': 100, 'income_range': (200, 400),
        'str_range': (50, 75), 'loyalty_range': (55, 80),
        'specialty': 'manager',
        'recruit_req': {'tier': 3, 'influence': 1000},
        'recruit_cost': 5000,
        'desc': 'Управляет 10 подчинёнными. Серьёзный человек.',
        'special': 'manage_business',
    },
    'yurist': {
        'name_ru': 'Юрист', 'tier': 3,
        'daily_cost': 200, 'income_range': (0, 0),
        'str_range': (5, 15), 'loyalty_range': (40, 65),
        'specialty': 'diplomat',
        'recruit_req': {'tier': 3, 'influence': 2000},
        'recruit_cost': 3000,
        'desc': 'Снижает жару на 2/день.',
        'special': 'reduce_heat_2',
    },
    'buhgalter': {
        'name_ru': 'Бухгалтер', 'tier': 3,
        'daily_cost': 150, 'income_range': (0, 0),
        'str_range': (5, 10), 'loyalty_range': (35, 60),
        'specialty': 'hacker',
        'recruit_req': {'tier': 3, 'influence': 1500},
        'recruit_cost': 2000,
        'desc': 'Увеличивает доход бизнесов на 15%.',
        'special': 'income_bonus_15',
    },
    # TIER 4 — Область
    'ohrannik': {
        'name_ru': 'Охранник', 'tier': 4,
        'daily_cost': 500, 'income_range': (0, 0),
        'str_range': (60, 85), 'loyalty_range': (60, 80),
        'specialty': 'fighter',
        'recruit_req': {'tier': 4, 'influence': 10000},
        'recruit_cost': 20000,
        'desc': 'Защищает бизнесы от рейдов.',
        'special': 'protect_business',
    },
    'reshala': {
        'name_ru': 'Решала', 'tier': 4,
        'daily_cost': 1000, 'income_range': (0, 0),
        'str_range': (30, 50), 'loyalty_range': (50, 75),
        'specialty': 'diplomat',
        'recruit_req': {'tier': 4, 'influence': 20000},
        'recruit_cost': 50000,
        'desc': 'Решает конфликты без стрельбы.',
        'special': 'resolve_conflicts',
    },
    'polittexhnolog': {
        'name_ru': 'Политтехнолог', 'tier': 4,
        'daily_cost': 2000, 'income_range': (0, 0),
        'str_range': (5, 15), 'loyalty_range': (40, 65),
        'specialty': 'diplomat',
        'recruit_req': {'tier': 4, 'influence': 30000},
        'recruit_cost': 100000,
        'desc': 'Управляет выборами и медиа.',
        'special': 'influence_bonus',
    },
    # TIER 5 — Страна
    'silovik': {
        'name_ru': 'Силовик', 'tier': 5,
        'daily_cost': 5000, 'income_range': (0, 0),
        'str_range': (80, 95), 'loyalty_range': (40, 60),
        'specialty': 'fighter',
        'recruit_req': {'tier': 5, 'influence': 100000},
        'recruit_cost': 500000,
        'desc': 'Государственная крыша. Серьёзная защита.',
        'special': 'heat_immunity_minor',
    },
    'deputat': {
        'name_ru': 'Депутат', 'tier': 5,
        'daily_cost': 10000, 'income_range': (0, 0),
        'str_range': (5, 15), 'loyalty_range': (30, 55),
        'specialty': 'diplomat',
        'recruit_req': {'tier': 5, 'influence': 200000},
        'recruit_cost': 2000000,
        'desc': 'Снижает жару на 10/день. Продвигает интересы.',
        'special': 'reduce_heat_10',
    },
    'general': {
        'name_ru': 'Генерал', 'tier': 5,
        'daily_cost': 20000, 'income_range': (0, 0),
        'str_range': (85, 100), 'loyalty_range': (35, 55),
        'specialty': 'fighter',
        'recruit_req': {'tier': 5, 'influence': 500000},
        'recruit_cost': 10000000,
        'desc': 'Военная защита. Разгоняет конкурентов.',
        'special': 'military_protection',
    },
    # TIER 6 — Мир
    'naemnik_unit': {
        'name_ru': 'Наёмный отряд', 'tier': 6,
        'daily_cost': 100000, 'income_range': (0, 0),
        'str_range': (80, 95), 'loyalty_range': (50, 70),
        'specialty': 'fighter',
        'recruit_req': {'tier': 6, 'influence': 1000000},
        'recruit_cost': 5000000,
        'desc': '100 бойцов-наёмников.',
    },
    'pravitelstvo': {
        'name_ru': 'Правительство страны', 'tier': 6,
        'daily_cost': 1000000, 'income_range': (5000000, 10000000),
        'str_range': (50, 70), 'loyalty_range': (25, 50),
        'specialty': 'earner',
        'recruit_req': {'tier': 6, 'influence': 5000000},
        'recruit_cost': 100000000,
        'desc': 'Контролируешь целую страну.',
        'special': 'control_nation',
    },
}

# Max gang size per tier
_MAX_GANG = {1: 12, 2: 50, 3: 200, 4: 1000, 5: 10000, 6: 999999}


def max_gang_size(state_or_rep):
    """Accept either a state dict or a rep int (backward compat with old UI)."""
    if isinstance(state_or_rep, dict):
        tier = state_or_rep.get('tier', 1)
        return _MAX_GANG.get(tier, 12)
    # Legacy: called with reputation int
    rep = int(state_or_rep)
    if rep >= 95: return 10
    if rep >= 80: return 7
    if rep >= 65: return 4
    return 0


def can_recruit(state, member_type='boyets'):
    mtype = MEMBER_TYPES.get(member_type)
    if not mtype:
        return False, 'Неизвестный тип'
    req = mtype.get('recruit_req', {})
    if state.get('tier', 1) < req.get('tier', 1):
        return False, f"Недоступно на этом уровне"
    if state.get('reputation', 0) < req.get('reputation', 0):
        return False, f"Нужна репутация {req.get('reputation', 0)}+"
    if state.get('influence', 0) < req.get('influence', 0):
        return False, f"Нужно влияние {req.get('influence', 0)}+"
    gang = state.get('gang_members', [])
    cap = max_gang_size(state)
    if len(gang) >= cap:
        return False, f'Банда полна ({cap} чел.)'
    cost = mtype.get('recruit_cost', 0)
    if state.get('cash', 0) < cost:
        return False, f"Нужно {cost} монет"
    return True, 'OK'


def recruit_member(state, member_type=None):
    """Recruit a member. Falls back to tier-appropriate default if type not given."""
    tier = state.get('tier', 1)
    if member_type is None:
        if tier >= 5:
            member_type = 'silovik'
        elif tier >= 4:
            member_type = 'ohrannik'
        elif tier >= 3:
            member_type = 'brigadir'
        elif tier >= 2:
            member_type = 'ulichny'
        else:
            rep = state.get('reputation', 0)
            member_type = 'boyets' if rep >= 30 else 'shesterka'

    ok, msg = can_recruit(state, member_type)
    if not ok:
        return False, msg

    mtype = MEMBER_TYPES[member_type]
    cost = mtype.get('recruit_cost', 0)
    if cost > 0:
        state['cash'] = state.get('cash', 0) - cost

    gang = state.setdefault('gang_members', [])
    used_names = {m['name'] for m in gang}
    pool = [n for n in _NAMES if n not in used_names] or _NAMES
    name = random.choice(pool)

    lo_str, hi_str = mtype['str_range']
    lo_loy, hi_loy = mtype['loyalty_range']
    lo_inc, hi_inc = mtype['income_range']

    member = {
        'id': f'gm_{uuid.uuid4().hex[:8]}',
        'name': name,
        'age': random.randint(18, 45),
        'type': member_type,
        'type_name': mtype['name_ru'],
        'loyalty': random.randint(lo_loy, hi_loy),
        'strength': random.randint(lo_str, hi_str),
        'skill': random.randint(20, 80),
        'specialty': mtype['specialty'],
        'daily_cost': mtype['daily_cost'],
        'daily_income': random.randint(lo_inc, hi_inc),
        'days_with_you': 0,
        'special': mtype.get('special'),
    }
    gang.append(member)
    return True, f'{name} ({mtype["name_ru"]}) вступил в твою банду'


def fire_member(state, member_id):
    gang = state.get('gang_members', [])
    target = next((m for m in gang if m['id'] == member_id), None)
    if not target:
        return False, 'Участник не найден'
    gang.remove(target)
    return True, f'{target["name"]} уволен'


def process_gang_day(state):
    gang = state.get('gang_members', [])
    if not gang:
        return []

    msgs = []
    total_income = 0
    total_salary = 0
    to_remove = []

    for m in gang:
        m['days_with_you'] = m.get('days_with_you', 0) + 1

        # Loyalty dynamics
        if state.get('mood', 50) < 20:
            m['loyalty'] = max(0, m['loyalty'] - 5)
        if state.get('reputation', 0) > 75 or state.get('respect', 0) > 50:
            m['loyalty'] = min(100, m['loyalty'] + 1)
        if state.get('cash', 0) < 10:
            m['loyalty'] = max(0, m['loyalty'] - 4)
        if m['days_with_you'] > 30:
            m['loyalty'] = min(100, m['loyalty'] + 1)

        # Salary
        salary = m.get('daily_cost', 0)
        if salary > 0:
            if state.get('cash', 0) >= salary:
                state['cash'] -= salary
                total_salary += salary
            else:
                m['loyalty'] = max(0, m['loyalty'] - 15)

        # Income
        inc = m.get('daily_income', 0)
        if inc > 0:
            total_income += inc

        # Special bonuses
        sp = m.get('special', '')
        if sp == 'reduce_heat_2':
            state['heat'] = max(0, state.get('heat', 0) - 2)
        elif sp == 'reduce_heat_10':
            state['heat'] = max(0, state.get('heat', 0) - 10)
        elif sp == 'influence_bonus':
            state['influence'] = state.get('influence', 0) + 50

        # Loyalty events
        roll = random.random()
        if roll < 0.03:
            m['loyalty'] = min(100, m['loyalty'] + 8)
            msgs.append(('win', f'👊 {m["name"]} доказал верность'))
        elif roll < 0.05:
            m['loyalty'] = max(0, m['loyalty'] - 12)
            msgs.append(('event', f'😤 {m["name"]} что-то мутит'))

        # Betrayal check
        if m['loyalty'] < 40:
            betrayal_chance = (40 - m['loyalty']) * 0.005  # up to 10% at loyalty=20
            if m['loyalty'] < 20:
                betrayal_chance *= 2  # doubles below 20
            if random.random() < betrayal_chance:
                stolen = random.randint(10, max(50, int(state.get('cash', 100) * 0.05)))
                stolen = min(stolen, state.get('cash', 0))
                state['cash'] = max(0, state.get('cash', 0) - stolen)
                state['reputation'] = max(0, state.get('reputation', 0) - 5)
                state['heat'] = min(100, state.get('heat', 0) + 5)
                to_remove.append(m)
                msgs.append(('danger',
                    f'🐀 {m["name"]} предал тебя! Украл {stolen} и сдал полиции.'))
                continue

    for m in to_remove:
        if m in gang:
            gang.remove(m)

    if total_income > 0:
        state['cash'] = state.get('cash', 0) + total_income
        state['money_earned'] = state.get('money_earned', 0) + total_income
        msgs.append(('result', f'💰 Банда заработала {total_income:,}'.replace(',', ' ')))

    return msgs


def gang_fight_bonus(state):
    """Combat bonus from gang."""
    gang = state.get('gang_members', [])
    fighters = [m for m in gang if m.get('specialty') == 'fighter']
    return min(40, sum(m['strength'] // 10 for m in fighters))


def daily_gang_salary(state):
    return sum(m.get('daily_cost', 0) for m in state.get('gang_members', []))


def daily_passive_income(state):
    """Passive income from gang earners (separate from business income)."""
    gang = state.get('gang_members', [])
    tier = state.get('tier', 1)
    base = sum(m.get('daily_income', 0) for m in gang)

    rep = state.get('reputation', 0)
    influence = state.get('influence', 0)
    bonus = 0
    if tier == 1:
        if rep >= 95: bonus = 30
        elif rep >= 80: bonus = 15
        elif rep >= 65: bonus = 7
    else:
        if influence >= 10000: bonus = int(influence * 0.001)

    return base + bonus


def get_gang_stats(state):
    gang = state.get('gang_members', [])
    if not gang:
        return {'total': 0, 'avg_loyalty': 0, 'avg_strength': 0,
                'fighters': 0, 'earners': 0, 'total_income': 0, 'total_cost': 0}
    total = len(gang)
    avg_loy = sum(m['loyalty'] for m in gang) // total
    avg_str = sum(m['strength'] for m in gang) // total
    fighters = sum(1 for m in gang if m.get('specialty') == 'fighter')
    earners = sum(1 for m in gang if m.get('specialty') == 'earner')
    return {
        'total': total, 'avg_loyalty': avg_loy, 'avg_strength': avg_str,
        'fighters': fighters, 'earners': earners,
        'total_income': sum(m.get('daily_income', 0) for m in gang),
        'total_cost': sum(m.get('daily_cost', 0) for m in gang),
    }
