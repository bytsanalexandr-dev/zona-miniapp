import random
from database import unlock_achievement, has_achievement

# ── All-tier ranks ────────────────────────────────────────────────────────────
# (tier, inf_min, inf_max, name, level)
ALL_RANKS = [
    # Tier 1 — Зона (by reputation 0-100)
    (1,   0,   14,  'Петух',                  0),
    (1,  15,   29,  'Чушка',                  1),
    (1,  30,   49,  'Мужик',                  2),
    (1,  50,   64,  'Спортсмен',              3),
    (1,  65,   79,  'Авторитет',              4),
    (1,  80,   94,  'Положенец',              5),
    (1,  95,  100,  'Смотрящий',              6),
    # Tier 2 — Район (by influence)
    (2,   100,   199,  'Блатной',             7),
    (2,   200,   399,  'Бригадир района',     8),
    (2,   400,   699,  'Смотрящий за районом',9),
    (2,   700,   999,  'Крёстный отец района',10),
    # Tier 3 — Город
    (3,  1000,  2999,  'Авторитет города',    11),
    (3,  3000,  5999,  'Теневой мэр',         12),
    (3,  6000,  8999,  'Вор в законе',        13),
    (3,  9000,  9999,  'Хозяин города',       14),
    # Tier 4 — Область
    (4, 10000,  29999, 'Региональный авторитет',15),
    (4, 30000,  69999, 'Теневой губернатор',    16),
    (4, 70000,  99999, 'Хозяин области',        17),
    # Tier 5 — Страна
    (5, 100000,  299999, 'Национальный авторитет',18),
    (5, 300000,  599999, 'Теневой олигарх',       19),
    (5, 600000,  899999, 'Вор в законе всея Руси',20),
    (5, 900000,  999999, 'Теневой правитель',     21),
    # Tier 6 — Мир
    (6, 1000000,  4999999, 'Международный авторитет',22),
    (6, 5000000,  9999999, 'Теневой владыка',        23),
    (6, 10000000, 10**18,  'Хозяин мира',            24),
]

TIER_NAMES = {
    1: 'ЗОНА',
    2: 'РАЙОН',
    3: 'ГОРОД',
    4: 'ОБЛАСТЬ',
    5: 'СТРАНА',
    6: 'МИР',
}

CURRENCY_NAMES = {
    1: 'монет',
    2: 'нал',
    3: 'безнал',
    4: 'активы',
    5: 'офшоры',
    6: 'крипта',
}

# Tier unlock conditions
TIER_UNLOCK = {
    2: {'tier': 1, 'reputation': 95, 'influence': 100},
    3: {'tier': 2, 'influence': 1000},
    4: {'tier': 3, 'influence': 10000},
    5: {'tier': 4, 'influence': 100000},
    6: {'tier': 5, 'influence': 1000000},
}

# Actions available per tier
ACTIONS = {
    # ── TIER 1: Physical ──────────────────────────────────────────────────────
    'gym': {
        'name': 'Качалка',                'category': 'Физическое', 'tier': 1,
        'desc': 'Тренировка с железом. +Сила, -Голод.',              'cost': 0},
    'run': {
        'name': 'Пробежка',               'category': 'Физическое', 'tier': 1,
        'desc': 'Пробежка по двору. +Здоровье, -Голод.',             'cost': 0},
    'pushups': {
        'name': 'Отжимания',              'category': 'Физическое', 'tier': 1,
        'desc': 'В камере, бесплатно.',                              'cost': 0},
    # ── TIER 1: Social ────────────────────────────────────────────────────────
    'talk': {
        'name': 'Общаться',               'category': 'Социальное', 'tier': 1,
        'desc': 'Поговорить с мужиками. +Репутация, +Настроение.',   'cost': 0},
    # ── TIER 1: Economy ───────────────────────────────────────────────────────
    'work': {
        'name': 'Работа на производстве', 'category': 'Экономика',  'tier': 1,
        'desc': 'Заработать монеты.',                                'cost': 0},
    'trade': {
        'name': 'Торговать',              'category': 'Экономика',  'tier': 1,
        'desc': 'Продать что-нибудь другим зэкам.',                  'cost': 0},
    'brew_chifir': {
        'name': 'Варить чифирь',          'category': 'Экономика',  'tier': 1,
        'desc': 'Чай на продажу (нужен набор и сахар).',             'cost': 0},
    # ── TIER 1: Vices ─────────────────────────────────────────────────────────
    'smoke': {
        'name': 'Покурить',               'category': 'Пороки',     'tier': 1,
        'desc': 'Расслабиться с сигаретой.',                         'cost': 0},
    'drink': {
        'name': 'Выпить',                 'category': 'Пороки',     'tier': 1,
        'desc': 'Глоток самогона.',                                  'cost': 0},
    'gamble': {
        'name': 'Карты',                  'category': 'Пороки',     'tier': 1,
        'desc': 'Сыграть в карты (ставка 10 монет).',                'cost': 10},
    # ── TIER 1: Self care ─────────────────────────────────────────────────────
    'wash': {
        'name': 'Помыться',               'category': 'Уход',       'tier': 1,
        'desc': 'Привести себя в порядок.',                          'cost': 0},
    'sleep_extra': {
        'name': 'Поспать',                'category': 'Уход',       'tier': 1,
        'desc': 'Дополнительный сон.',                               'cost': 0},
    'shave': {
        'name': 'Побриться',              'category': 'Уход',       'tier': 1,
        'desc': 'Побриться (нужна бритва).',                         'cost': 0},
    # ── TIER 1: Gang ──────────────────────────────────────────────────────────
    'recruit': {
        'name': 'Рекрутировать',          'category': 'Банда',      'tier': 1,
        'desc': 'Позвать в банду (нужна репутация Авторитет).',      'cost': 0},
    'collect_debt': {
        'name': 'Выбить долги',           'category': 'Банда',      'tier': 1,
        'desc': 'Послать людей за должниками.',                      'cost': 0},
    # ── TIER 1: Special ───────────────────────────────────────────────────────
    'escape_attempt': {
        'name': 'ПОБЕГ',                  'category': 'Особое',     'tier': 1,
        'desc': 'Попытаться бежать (нужны сила 80+, маршрут известен).', 'cost': 0},
    # ── TIER 2+ ───────────────────────────────────────────────────────────────
    'expand_territory': {
        'name': 'Расширить территорию',   'category': 'Империя',    'tier': 2,
        'desc': 'Захватить новый район/точку.',                      'cost': 0},
    'collect_protection': {
        'name': 'Крышевание',             'category': 'Империя',    'tier': 2,
        'desc': 'Собрать дань с подопечных.',                        'cost': 0},
    'bribe_official': {
        'name': 'Купить чиновника',       'category': 'Империя',    'tier': 2,
        'desc': 'Подкупить представителя власти.',                   'cost': 0},
    'manage_business': {
        'name': 'Управлять бизнесом',     'category': 'Империя',    'tier': 2,
        'desc': 'Принять управленческое решение.',                   'cost': 0},
    'invest': {
        'name': 'Инвестировать',          'category': 'Империя',    'tier': 3,
        'desc': 'Вложить деньги в развитие.',                        'cost': 0},
    'launder_money': {
        'name': 'Отмыть деньги',          'category': 'Империя',    'tier': 3,
        'desc': 'Легализовать криминальный доход.',                  'cost': 0},
    'political_move': {
        'name': 'Политический ход',       'category': 'Империя',    'tier': 4,
        'desc': 'Влияние через политику.',                           'cost': 0},
    'global_expansion': {
        'name': 'Глобальная экспансия',   'category': 'Империя',    'tier': 5,
        'desc': 'Выход на международные рынки.',                     'cost': 0},
    # ── Personal always available ──────────────────────────────────────────────
    'train_mind': {
        'name': 'Самообразование',        'category': 'Личное',     'tier': 1,
        'desc': 'Читать, думать, развиваться. +Интеллект.',          'cost': 0},
    'meditate': {
        'name': 'Медитация',              'category': 'Личное',     'tier': 1,
        'desc': 'Успокоиться. -Паранойя, +Настроение.',              'cost': 0},
    'lay_low': {
        'name': 'Залечь на дно',          'category': 'Личное',     'tier': 2,
        'desc': 'Снизить жару, не делать ничего подозрительного.',   'cost': 0},
    # ── TIER 1: Communications ────────────────────────────────────────────────
    'send_malyava': {
        'name': 'Передать маляву',        'category': 'Социальное', 'tier': 1,
        'desc': '+15 репутации. Стоит 5 монет.',                     'cost': 5},
    'organize_obshchak': {
        'name': 'Организовать общак',     'category': 'Банда',      'tier': 1,
        'desc': '+25 репутации. Нужно 3 члена банды.',               'cost': 0},
    # ── TIER 2: Lifestyle ─────────────────────────────────────────────────────
    'eat_cafe': {
        'name': 'Поесть в кафе',          'category': 'Уход',       'tier': 2,
        'desc': '+30 голод, +10 настроение. Стоит 25.',              'cost': 25},
    'go_banya': {
        'name': 'Сходить в баню',         'category': 'Уход',       'tier': 2,
        'desc': '+40 гигиена, +20 настроение. Стоит 40.',            'cost': 40},
    'buy_phone_new': {
        'name': 'Купить новый телефон',   'category': 'Социальное', 'tier': 2,
        'desc': '+20 репутация. Стоит 80.',                          'cost': 80},
    'find_tochka': {
        'name': 'Найти точку',            'category': 'Экономика',  'tier': 2,
        'desc': '+50 пассивного дохода в день. Стоит 100.',          'cost': 100},
    'hire_driver': {
        'name': 'Нанять водителя',        'category': 'Банда',      'tier': 2,
        'desc': 'Рекрутировать водителя в банду. Стоит 60.',         'cost': 60},
    # ── TIER 3: Premium ───────────────────────────────────────────────────────
    'restaurant': {
        'name': 'Ресторан',               'category': 'Уход',       'tier': 3,
        'desc': '+40 голод, +25 настроение. Стоит 150.',             'cost': 150},
    'nightclub': {
        'name': 'Ночной клуб',            'category': 'Социальное', 'tier': 3,
        'desc': '+35 настроение, +15 реп. Стоит 200.',               'cost': 200},
    'sauna_devochki': {
        'name': 'Сауна с девочками',      'category': 'Уход',       'tier': 3,
        'desc': '+50 настроение, +20 здоровье. Стоит 300.',          'cost': 300},
    'personal_trainer': {
        'name': 'Личный тренер',          'category': 'Физическое', 'tier': 3,
        'desc': '+15 сила. Стоит 120.',                              'cost': 120},
    'lawyer': {
        'name': 'Адвокат',                'category': 'Личное',     'tier': 3,
        'desc': '-20 жары. Стоит 500.',                              'cost': 500},
    'bribe_cop': {
        'name': 'Подкупить мента',        'category': 'Личное',     'tier': 3,
        'desc': '-15 жары. Стоит 300.',                              'cost': 300},
    # ── TIER 4: Elite ─────────────────────────────────────────────────────────
    'business_dinner': {
        'name': 'Деловой ужин',           'category': 'Социальное', 'tier': 4,
        'desc': '+30 реп, +20 влияние. Стоит 1 000.',               'cost': 1000},
    'private_doctor': {
        'name': 'Частный доктор',         'category': 'Уход',       'tier': 4,
        'desc': '+40 здоровье. Стоит 800.',                          'cost': 800},
    'guard_24_7': {
        'name': 'Охрана 24/7',            'category': 'Личное',     'tier': 4,
        'desc': '-50% риск травм на 7 дней. Стоит 2 000.',          'cost': 2000},
    'buy_deputy': {
        'name': 'Купить депутата',        'category': 'Империя',    'tier': 4,
        'desc': '-30 жары, +100 влияние. Стоит 10 000.',            'cost': 10000},
    'yacht_weekend': {
        'name': 'Яхта на выходные',       'category': 'Уход',       'tier': 4,
        'desc': '+50 настроение, +30 реп. Стоит 5 000.',            'cost': 5000},
    # ── TIER 5: Ultra ─────────────────────────────────────────────────────────
    'private_jet': {
        'name': 'Частный самолёт',        'category': 'Уход',       'tier': 5,
        'desc': '+40 настроение, +50 реп. Стоит 20 000.',           'cost': 20000},
    'personal_chef': {
        'name': 'Личный повар',           'category': 'Уход',       'tier': 5,
        'desc': '+50 голод, +30 настроение. Стоит 5 000.',          'cost': 5000},
    'buy_minister': {
        'name': 'Купить министра',        'category': 'Империя',    'tier': 5,
        'desc': '+200 влияние, -50 жары. Стоит 50 000.',            'cost': 50000},
    'spa_resort': {
        'name': 'Спа-курорт',             'category': 'Уход',       'tier': 5,
        'desc': '+60 здоровье, +40 настроение. Стоит 15 000.',      'cost': 15000},
    'press_conference': {
        'name': 'Пресс-конференция',      'category': 'Социальное', 'tier': 5,
        'desc': '+100 влияние. Стоит 30 000.',                      'cost': 30000},
    # ── TIER 6: World ─────────────────────────────────────────────────────────
    'buy_island': {
        'name': 'Купить остров',          'category': 'Империя',    'tier': 6,
        'desc': '+500 влияние. Стоит 1 000 000.',                   'cost': 1000000},
    'private_army_op': {
        'name': 'Операция армии',         'category': 'Империя',    'tier': 6,
        'desc': '+200 влияние. Стоит 100 000.',                     'cost': 100000},
    'bribe_un': {
        'name': 'Подкуп ООН',             'category': 'Империя',    'tier': 6,
        'desc': '-100 жары. Стоит 500 000.',                        'cost': 500000},
    'meet_president': {
        'name': 'Встреча с президентом',  'category': 'Империя',    'tier': 6,
        'desc': '+300 влияние. Стоит 200 000.',                     'cost': 200000},
}


DEFAULT_STATE = {
    # Identity
    'player_name': 'Заключённый',
    'days_survived': 0,
    'skin_type': 1,

    # Personal stats (0-100)
    'health': 80,
    'strength': 35,
    'sleep': 70,
    'hunger': 70,
    'hygiene': 70,
    'mood': 55,
    'intelligence': 30,
    'charisma': 25,
    'paranoia': 10,

    # Addictions
    'addiction_cigarettes': 0,
    'addiction_alcohol': 0,
    'smoker': False,
    'drinker': False,

    # Physical
    'weight': 70.0,
    'muscle_mass': 0,
    'gym_visits': 0,

    # Tier 1 specifics
    'reputation': 10,
    'guard_favor': 50,
    'sentence_days': 365,
    'udo_hinted': False,

    # Empire
    'tier': 1,
    'influence': 0.0,
    'cash': 30.0,
    'total_assets': 0.0,
    'heat': 5,
    'respect': 0,

    # Empire collections
    'businesses': [],
    'territories': [],
    'bribed_officials': [],
    'npc_rivals': [],

    # Gang
    'gang_members': [],

    # Inventory
    'inventory': {},

    # Combat / status
    'injuries': [],
    'tattoos': [],
    'has_shiv': False,
    'has_phone': False,
    'escape_route_known': False,

    # Counters
    'fights_won': 0,
    'fights_lost': 0,
    'total_fights': 0,
    'times_snitched': 0,
    'money_earned': 0.0,
    'debt': 0,

    # Clothing
    'clothing_level': 0,
    'clothing_item': 'uniform',

    # Daily reset
    'actions_left': 3,
    'actions_used': [],

    # Log
    'event_log': [('system', 'Зона приняла тебя. Выживи.')],
    'achievements': [],

    # State
    'game_over': False,
    'ending': None,
    'pending_event': None,
}


# ── Public API ────────────────────────────────────────────────────────────────

def new_game(player_name='Заключённый'):
    state = dict(DEFAULT_STATE)
    state['player_name'] = player_name
    state['event_log'] = [('system', 'Зона приняла тебя. Выживи.')]
    state['inventory'] = {}
    state['injuries'] = []
    state['gang_members'] = []
    state['tattoos'] = []
    state['actions_used'] = []
    state['businesses'] = []
    state['territories'] = []
    state['bribed_officials'] = []
    state['npc_rivals'] = []
    state['cash'] = 30.0
    return state


def get_rank(state):
    tier = state.get('tier', 1)
    if tier == 1:
        rep = state.get('reputation', 0)
        for t, lo, hi, name, lvl in ALL_RANKS:
            if t == 1 and lo <= rep <= hi:
                return name, lvl
        return 'Мужик', 2
    else:
        inf = state.get('influence', 0)
        best = None
        for t, lo, hi, name, lvl in ALL_RANKS:
            if t == tier and lo <= inf:
                best = (name, lvl)
        if best:
            return best
        for t, lo, hi, name, lvl in ALL_RANKS:
            if t == tier:
                return name, lvl
        return 'Блатной', 7


def get_tier(state):
    return state.get('tier', 1)


def get_currency_name(tier):
    return CURRENCY_NAMES.get(tier, 'монет')


def fmt(n):
    return f'{int(n):,}'.replace(',', ' ')


def calculate_score(state):
    tier = state.get('tier', 1)
    inf = state.get('influence', 0)
    days = max(1, state.get('days_survived', 1))
    days_mod = 1 + min(2.0, days / 100.0)
    return inf * (1 + tier * 0.5) * days_mod


def get_survival_probability(state):
    health = state.get('health', 80)
    mood = state.get('mood', 50)
    hunger = state.get('hunger', 60)
    rep = state.get('reputation', 10)
    alc = state.get('addiction_alcohol', 0)
    cig = state.get('addiction_cigarettes', 0)
    gang_size = len(state.get('gang_members', []))
    heat = state.get('heat', 0)
    tier = state.get('tier', 1)

    score = (health * 0.30 + mood * 0.15 + hunger * 0.10
             + rep * 0.10 + gang_size * 3 + (tier - 1) * 10)
    score -= alc * 0.15 + cig * 0.08 + heat * 0.15
    return max(0, min(100, int(score)))


def get_daily_income_breakdown(state):
    from gang import daily_passive_income
    from economy import process_businesses_day
    gang_income = sum(m.get('daily_income', 0) for m in state.get('gang_members', []))
    passive = daily_passive_income(state)
    biz_income = sum(_biz_income_estimate(b) for b in state.get('businesses', []))
    return gang_income + passive, biz_income


def _biz_income_estimate(biz_inst):
    from economy import BUSINESSES, business_daily_income
    return int(BUSINESSES.get(biz_inst.get('template_id', ''), {}).get('base_income', 0)
               * (BUSINESSES.get(biz_inst.get('template_id', ''), {}).get('level_mult', 2)
                  ** (biz_inst.get('level', 1) - 1)))


# ── do_action ────────────────────────────────────────────────────────────────

def do_action(state, action_id):
    """Returns list of plain strings (for main.py compatibility)."""
    if state.get('game_over'):
        return ['Игра окончена.']
    if state.get('actions_left', 0) <= 0:
        return ['Действий не осталось. Нажми "Следующий день".']
    if action_id in state.get('actions_used', []):
        return ['Это действие уже выполнено сегодня.']

    action = ACTIONS.get(action_id)
    if not action:
        return ['Неизвестное действие.']

    required_tier = action.get('tier', 1)
    if state.get('tier', 1) < required_tier:
        return [f'Доступно с уровня {required_tier} ({TIER_NAMES.get(required_tier, "")}).']

    msgs = []
    inv = state.get('inventory', {})

    # ── PHYSICAL ──────────────────────────────────────────────────────────────
    if action_id == 'gym':
        state['strength'] = min(100, state.get('strength', 35) + random.randint(2, 5))
        state['muscle_mass'] = min(100, state.get('muscle_mass', 0) + 2)
        state['hunger'] = max(0, state.get('hunger', 70) - 12)
        state['sleep'] = max(0, state.get('sleep', 70) - 8)
        state['weight'] = max(60.0, state.get('weight', 70.0) - 0.3)
        state['gym_visits'] = state.get('gym_visits', 0) + 1
        msgs.append('Потренировался. +Сила, +Мышцы, -Голод')

    elif action_id == 'run':
        state['health'] = min(100, state.get('health', 80) + random.randint(3, 7))
        state['strength'] = min(100, state.get('strength', 35) + 1)
        state['hunger'] = max(0, state.get('hunger', 70) - 10)
        state['weight'] = max(60.0, state.get('weight', 70.0) - 0.25)
        msgs.append('Пробежка. +Здоровье, -Голод')

    elif action_id == 'pushups':
        state['strength'] = min(100, state.get('strength', 35) + random.randint(1, 3))
        state['muscle_mass'] = min(100, state.get('muscle_mass', 0) + 1)
        state['hunger'] = max(0, state.get('hunger', 70) - 6)
        msgs.append('Отжимания. +Сила')

    # ── SOCIAL ───────────────────────────────────────────────────────────────
    elif action_id == 'talk':
        rep_gain = random.randint(1, 4)
        mood_gain = random.randint(5, 15)
        state['reputation'] = min(100, state.get('reputation', 10) + rep_gain)
        state['mood'] = min(100, state.get('mood', 50) + mood_gain)
        state['charisma'] = min(100, state.get('charisma', 25) + 1)
        if random.random() < 0.10:
            state.setdefault('injuries', []).append({'type': 'bruise', 'severity': 1, 'days': 3})
            state['health'] = max(0, state.get('health', 80) - 10)
            msgs.append('Разговор перерос в конфликт. Получил в нос.')
        else:
            msgs.append(f'Поговорил. +{rep_gain} Реп, +{mood_gain} Настроение')

    # ── ECONOMY T1 ───────────────────────────────────────────────────────────
    elif action_id == 'work':
        earned = random.randint(3, 8)
        state['cash'] = state.get('cash', 0) + earned
        state['money_earned'] = state.get('money_earned', 0) + earned
        state['hunger'] = max(0, state.get('hunger', 70) - 8)
        state['mood'] = max(0, state.get('mood', 55) - 5)
        msgs.append(f'Отработал смену. +{earned} монет')

    elif action_id == 'trade':
        if inv:
            earned = random.randint(5, 15)
            state['cash'] = state.get('cash', 0) + earned
            state['money_earned'] = state.get('money_earned', 0) + earned
            msgs.append(f'Поторговал. +{earned} монет')
        else:
            msgs.append('Нечем торговать.')
            return msgs

    elif action_id == 'brew_chifir':
        from economy import craft_chifir
        ok, msg = craft_chifir(state)
        msgs.append(msg)
        if not ok:
            return msgs

    # ── VICES ────────────────────────────────────────────────────────────────
    elif action_id == 'smoke':
        found = next((c for c in ('papirosa', 'prima') if inv.get(c, 0) > 0), None)
        if not found:
            msgs.append('Нет сигарет.')
            return msgs
        from economy import use_item
        ok, effects, msg = use_item(state, found)
        msgs.append(msg)

    elif action_id == 'drink':
        if inv.get('vodka', 0) <= 0:
            msgs.append('Нет водки.')
            return msgs
        from economy import use_item
        ok, effects, msg = use_item(state, 'vodka')
        msgs.append(msg)
        if random.random() < 0.2:
            lost = random.randint(5, 20)
            state['cash'] = max(0, state.get('cash', 0) - lost)
            msgs.append(f'Отключился. Пропало {lost} монет.')

    elif action_id == 'gamble':
        bet = 10
        if state.get('cash', 0) < bet:
            msgs.append(f'Нужно {bet} монет.')
            return msgs
        state['cash'] = max(0, state.get('cash', 0) - bet)
        if random.random() > 0.48:
            win = bet * 2
            state['cash'] = state.get('cash', 0) + win
            state['mood'] = min(100, state.get('mood', 50) + 15)
            msgs.append(f'Выиграл {win} монет!')
        else:
            state['mood'] = max(0, state.get('mood', 50) - 10)
            msgs.append(f'Проиграл {bet} монет.')

    # ── SELF CARE ─────────────────────────────────────────────────────────────
    elif action_id == 'wash':
        if inv.get('soap', 0) > 0:
            inv['soap'] -= 1
            if inv['soap'] <= 0:
                del inv['soap']
            state['hygiene'] = min(100, state.get('hygiene', 70) + 20)
            state['mood'] = min(100, state.get('mood', 50) + 5)
            msgs.append('Помылся с мылом. +Гигиена')
        else:
            state['hygiene'] = min(100, state.get('hygiene', 70) + 5)
            msgs.append('Ополоснулся без мыла.')

    elif action_id == 'sleep_extra':
        state['sleep'] = min(100, state.get('sleep', 70) + 25)
        state['health'] = min(100, state.get('health', 80) + 5)
        state['mood'] = min(100, state.get('mood', 50) + 10)
        msgs.append('Доспал. +Сон, +Здоровье')

    elif action_id == 'shave':
        if inv.get('razor', 0) > 0:
            inv['razor'] -= 1
            if inv['razor'] <= 0:
                del inv['razor']
            state['hygiene'] = min(100, state.get('hygiene', 70) + 15)
            state['mood'] = min(100, state.get('mood', 50) + 8)
            state['shaved_today'] = True
            msgs.append('Побрился. +Гигиена')
        else:
            msgs.append('Нет бритвы.')
            return msgs

    # ── GANG ──────────────────────────────────────────────────────────────────
    elif action_id == 'recruit':
        from gang import recruit_member
        ok, msg = recruit_member(state)
        msgs.append(msg)
        if not ok:
            return msgs

    elif action_id == 'collect_debt':
        gang = state.get('gang_members', [])
        if not gang:
            msgs.append('Некому собирать долги.')
            return msgs
        earned = len(gang) * random.randint(3, 8)
        state['cash'] = state.get('cash', 0) + earned
        state['money_earned'] = state.get('money_earned', 0) + earned
        msgs.append(f'Банда выбила долги. +{fmt(earned)} монет')

    # ── ESCAPE ────────────────────────────────────────────────────────────────
    elif action_id == 'escape_attempt':
        if state.get('tier', 1) != 1:
            msgs.append('Ты уже на воле.')
            return msgs
        if not state.get('escape_route_known'):
            msgs.append('Не знаешь маршрута.')
            return msgs
        if state.get('strength', 0) < 80:
            msgs.append('Недостаточно сил (нужно 80+).')
            return msgs
        chance = 0.35
        if state.get('has_shiv'):
            chance += 0.1
        if state.get('reputation', 0) >= 50:
            chance += 0.1
        if random.random() < chance:
            state['game_over'] = False
            state['ending'] = None
            _advance_to_tier2(state)
            msgs.append('ПОБЕГ УДАЛСЯ! Ты на свободе!')
        else:
            state['health'] = max(0, state.get('health', 80) - 30)
            state['reputation'] = max(0, state.get('reputation', 0) - 15)
            state['guard_favor'] = max(0, state.get('guard_favor', 50) - 40)
            state.setdefault('injuries', []).append({'type': 'bruise', 'severity': 4, 'days': 10})
            msgs.append('Поймали. Избили. Карцер.')
        return msgs

    # ── EMPIRE ACTIONS ────────────────────────────────────────────────────────
    elif action_id == 'expand_territory':
        from economy import BUSINESSES
        cost = int(100 * (10 ** (state.get('tier', 2) - 2)))
        if state.get('cash', 0) >= cost:
            state['cash'] -= cost
            gain = random.randint(50, 200) * (state.get('tier', 2) - 1)
            state['influence'] = state.get('influence', 0) + gain
            state['reputation'] = min(100, state.get('reputation', 0) + random.randint(1, 5))
            msgs.append(f'Расширил территорию. +{fmt(gain)} влияния')
        else:
            msgs.append(f'Нужно {fmt(cost)} монет.')
            return msgs

    elif action_id == 'collect_protection':
        tier = state.get('tier', 1)
        territories = state.get('territories', [])
        base = 50 * (10 ** (tier - 2)) if tier >= 2 else 0
        collected = int(base * (1 + len(territories) * 0.2) * random.uniform(0.8, 1.2))
        if collected > 0:
            state['cash'] = state.get('cash', 0) + collected
            state['money_earned'] = state.get('money_earned', 0) + collected
            state['heat'] = min(100, state.get('heat', 0) + 0.5)
            msgs.append(f'Собрал крышевание: +{fmt(collected)}')
        else:
            msgs.append('Нечего собирать.')
            return msgs

    elif action_id == 'bribe_official':
        msgs.append('Используй вкладку Магазин → Чиновники для подкупа.')
        return msgs

    elif action_id == 'manage_business':
        businesses = state.get('businesses', [])
        maintained = [b for b in businesses if b.get('condition', 100) < 80]
        if maintained:
            b = maintained[0]
            b['condition'] = min(100, b.get('condition', 80) + 15)
            msgs.append(f'Улучшил состояние {b["name"]} до {b["condition"]:.0f}%')
        else:
            msgs.append('Все бизнесы в хорошем состоянии.')
            return msgs

    elif action_id == 'invest':
        cash = state.get('cash', 0)
        invest_min = 1000 * (10 ** (state.get('tier', 3) - 3))
        if cash >= invest_min:
            amount = invest_min
            state['cash'] -= amount
            returns = amount * random.uniform(1.1, 1.5)
            state['cash'] += returns
            profit = returns - amount
            state['money_earned'] = state.get('money_earned', 0) + profit
            msgs.append(f'Инвестировал {fmt(amount)}, прибыль +{fmt(profit)}')
        else:
            msgs.append(f'Нужно минимум {fmt(invest_min)}.')
            return msgs

    elif action_id == 'launder_money':
        cash = state.get('cash', 0)
        launder = min(cash * 0.2, 1000000)
        if launder >= 1000:
            state['cash'] -= launder
            clean = launder * 0.7
            state['cash'] += clean
            state['total_assets'] = state.get('total_assets', 0) + clean
            state['heat'] = max(0, state.get('heat', 0) - 3)
            msgs.append(f'Отмыл {fmt(launder)}: -30% комиссия, -3 жара')
        else:
            msgs.append('Недостаточно денег для отмывания.')
            return msgs

    elif action_id == 'political_move':
        cost = 100000 * (10 ** (state.get('tier', 4) - 4))
        if state.get('cash', 0) >= cost:
            state['cash'] -= cost
            inf_gain = random.randint(500, 2000) * (state.get('tier', 4) - 3)
            state['influence'] = state.get('influence', 0) + inf_gain
            state['heat'] = max(0, state.get('heat', 0) - 5)
            msgs.append(f'Политический ход. +{fmt(inf_gain)} влияния, -5 жара')
        else:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs

    elif action_id == 'global_expansion':
        cost = 10000000 * (10 ** (state.get('tier', 5) - 5))
        if state.get('cash', 0) >= cost:
            state['cash'] -= cost
            inf_gain = random.randint(10000, 50000)
            state['influence'] = state.get('influence', 0) + inf_gain
            msgs.append(f'Глобальная экспансия. +{fmt(inf_gain)} влияния')
        else:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs

    elif action_id == 'train_mind':
        state['intelligence'] = min(100, state.get('intelligence', 30) + random.randint(1, 3))
        state['mood'] = min(100, state.get('mood', 50) + 5)
        msgs.append('Самообразование. +Интеллект')

    elif action_id == 'meditate':
        state['paranoia'] = max(0, state.get('paranoia', 10) - random.randint(3, 8))
        state['mood'] = min(100, state.get('mood', 50) + 10)
        msgs.append('Медитация. -Паранойя, +Настроение')

    elif action_id == 'lay_low':
        state['heat'] = max(0, state.get('heat', 0) - random.randint(3, 8))
        state['mood'] = max(0, state.get('mood', 50) - 5)
        msgs.append('Залёг на дно. -Жара')

    # ── NEW TIER 1 ────────────────────────────────────────────────────────────
    elif action_id == 'send_malyava':
        cost = 5
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost} монет.')
            return msgs
        state['cash'] -= cost
        state['reputation'] = min(100, state.get('reputation', 10) + 15)
        msgs.append('Малява дошла. +15 репутации')

    elif action_id == 'organize_obshchak':
        if len(state.get('gang_members', [])) < 3:
            msgs.append('Нужно минимум 3 члена банды.')
            return msgs
        state['reputation'] = min(100, state.get('reputation', 10) + 25)
        state['mood'] = min(100, state.get('mood', 50) + 10)
        msgs.append('Общак поднят. +25 репутации')

    # ── NEW TIER 2 ────────────────────────────────────────────────────────────
    elif action_id == 'eat_cafe':
        cost = 25
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['hunger'] = min(100, state.get('hunger', 50) + 30)
        state['mood'] = min(100, state.get('mood', 50) + 10)
        msgs.append('Поел в кафе. +Голод, +Настроение')

    elif action_id == 'go_banya':
        cost = 40
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['hygiene'] = min(100, state.get('hygiene', 50) + 40)
        state['mood'] = min(100, state.get('mood', 50) + 20)
        msgs.append('Попарился в бане. +Гигиена, +Настроение')

    elif action_id == 'buy_phone_new':
        cost = 80
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['reputation'] = min(100, state.get('reputation', 10) + 20)
        msgs.append('Купил новый телефон. +Репутация')

    elif action_id == 'find_tochka':
        cost = 100
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['passive_income_bonus'] = state.get('passive_income_bonus', 0) + 50
        msgs.append('Нашёл точку. +50 пассивного дохода в день')

    elif action_id == 'hire_driver':
        import uuid
        from gang import MEMBER_TYPES, _NAMES, max_gang_size
        cost = 60
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        gang = state.setdefault('gang_members', [])
        cap = max_gang_size(state)
        if len(gang) >= cap:
            msgs.append(f'Банда полна ({cap} чел.).')
            return msgs
        state['cash'] -= cost
        mtype = MEMBER_TYPES['voditel']
        used_names = {m['name'] for m in gang}
        pool = [n for n in _NAMES if n not in used_names] or _NAMES
        name = random.choice(pool)
        lo_str, hi_str = mtype['str_range']
        lo_loy, hi_loy = mtype['loyalty_range']
        gang.append({
            'id': f'gm_{uuid.uuid4().hex[:8]}',
            'name': name, 'age': random.randint(18, 45),
            'type': 'voditel', 'type_name': mtype['name_ru'],
            'loyalty': random.randint(lo_loy, hi_loy),
            'strength': random.randint(lo_str, hi_str),
            'skill': random.randint(20, 80),
            'specialty': mtype['specialty'],
            'daily_cost': mtype['daily_cost'],
            'daily_income': 0, 'days_with_you': 0,
            'special': mtype.get('special'),
        })
        msgs.append(f'{name} (Водитель) нанят')

    # ── NEW TIER 3 ────────────────────────────────────────────────────────────
    elif action_id == 'restaurant':
        cost = 150
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['hunger'] = min(100, state.get('hunger', 50) + 40)
        state['mood'] = min(100, state.get('mood', 50) + 25)
        msgs.append('Отужинал в ресторане. +Голод, +Настроение')

    elif action_id == 'nightclub':
        cost = 200
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['mood'] = min(100, state.get('mood', 50) + 35)
        state['reputation'] = min(100, state.get('reputation', 10) + 15)
        msgs.append('Ночной клуб. +Настроение, +Репутация')

    elif action_id == 'sauna_devochki':
        cost = 300
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['mood'] = min(100, state.get('mood', 50) + 50)
        state['health'] = min(100, state.get('health', 80) + 20)
        msgs.append('Сауна. +Настроение, +Здоровье')

    elif action_id == 'personal_trainer':
        cost = 120
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['strength'] = min(100, state.get('strength', 35) + 15)
        msgs.append('Тренировка с личным тренером. +Сила')

    elif action_id == 'lawyer':
        cost = 500
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['heat'] = max(0, state.get('heat', 0) - 20)
        msgs.append('Адвокат поработал. -20 жары')

    elif action_id == 'bribe_cop':
        cost = 300
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {cost}.')
            return msgs
        state['cash'] -= cost
        state['heat'] = max(0, state.get('heat', 0) - 15)
        msgs.append('Мент в кармане. -15 жары')

    # ── NEW TIER 4 ────────────────────────────────────────────────────────────
    elif action_id == 'business_dinner':
        cost = 1000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['reputation'] = min(100, state.get('reputation', 10) + 30)
        state['influence'] = state.get('influence', 0) + 20
        msgs.append('Деловой ужин. +Репутация, +Влияние')

    elif action_id == 'private_doctor':
        cost = 800
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['health'] = min(100, state.get('health', 80) + 40)
        msgs.append('Частный доктор. +40 здоровья')

    elif action_id == 'guard_24_7':
        cost = 2000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['guard_active_days'] = state.get('guard_active_days', 0) + 7
        msgs.append('Охрана 24/7 на 7 дней. -50% риск травм')

    elif action_id == 'buy_deputy':
        cost = 10000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['heat'] = max(0, state.get('heat', 0) - 30)
        state['influence'] = state.get('influence', 0) + 100
        msgs.append('Депутат куплен. -30 жары, +100 влияния')

    elif action_id == 'yacht_weekend':
        cost = 5000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['mood'] = min(100, state.get('mood', 50) + 50)
        state['reputation'] = min(100, state.get('reputation', 10) + 30)
        msgs.append('Яхта на выходные. +Настроение, +Репутация')

    # ── NEW TIER 5 ────────────────────────────────────────────────────────────
    elif action_id == 'private_jet':
        cost = 20000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['mood'] = min(100, state.get('mood', 50) + 40)
        state['reputation'] = min(100, state.get('reputation', 10) + 50)
        msgs.append('Частный самолёт. +Настроение, +Репутация')

    elif action_id == 'personal_chef':
        cost = 5000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['hunger'] = min(100, state.get('hunger', 50) + 50)
        state['mood'] = min(100, state.get('mood', 50) + 30)
        msgs.append('Личный повар накормил. +Голод, +Настроение')

    elif action_id == 'buy_minister':
        cost = 50000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['influence'] = state.get('influence', 0) + 200
        state['heat'] = max(0, state.get('heat', 0) - 50)
        msgs.append('Министр куплен. +200 влияния, -50 жары')

    elif action_id == 'spa_resort':
        cost = 15000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['health'] = min(100, state.get('health', 80) + 60)
        state['mood'] = min(100, state.get('mood', 50) + 40)
        msgs.append('Спа-курорт. +Здоровье, +Настроение')

    elif action_id == 'press_conference':
        cost = 30000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['influence'] = state.get('influence', 0) + 100
        msgs.append('Пресс-конференция. +100 влияния')

    # ── NEW TIER 6 ────────────────────────────────────────────────────────────
    elif action_id == 'buy_island':
        cost = 1000000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['influence'] = state.get('influence', 0) + 500
        msgs.append('Остров куплен. +500 влияния')

    elif action_id == 'private_army_op':
        cost = 100000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['influence'] = state.get('influence', 0) + 200
        state['reputation'] = min(100, state.get('reputation', 10) + 100)
        msgs.append('Операция армии. +Влияние, +Репутация')

    elif action_id == 'bribe_un':
        cost = 500000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['heat'] = max(0, state.get('heat', 0) - 100)
        msgs.append('ООН подкуплена. -100 жары')

    elif action_id == 'meet_president':
        cost = 200000
        if state.get('cash', 0) < cost:
            msgs.append(f'Нужно {fmt(cost)}.')
            return msgs
        state['cash'] -= cost
        state['influence'] = state.get('influence', 0) + 300
        msgs.append('Встреча с президентом. +300 влияния')

    else:
        return ['Неизвестное действие.']

    state['actions_left'] = state.get('actions_left', 3) - 1
    state.setdefault('actions_used', []).append(action_id)
    return msgs


# ── advance_day ───────────────────────────────────────────────────────────────

def advance_day(state):
    """Main daily tick. Returns list of (kind, msg) tuples."""
    if state.get('game_over'):
        return []

    msgs = []
    day = state.get('days_survived', 0) + 1
    state['days_survived'] = day
    tier = state.get('tier', 1)

    print(f'[DAY {day}] Tier:{tier} Inf:{state.get("influence",0):.0f} '
          f'Cash:{state.get("cash",0):.0f} Heat:{state.get("heat",0):.0f} '
          f'Gang:{len(state.get("gang_members",[]))} Biz:{len(state.get("businesses",[]))}')

    # 1. STAT DECAY
    state['hunger']  = max(0, state.get('hunger', 70) - 12)
    state['sleep']   = max(0, state.get('sleep', 70) - 18)
    state['hygiene'] = max(0, state.get('hygiene', 70) - 7)
    state['mood']    = max(0, min(100, state.get('mood', 55) - 4))

    if state['hunger'] <= 5:
        state['health'] = max(0, state.get('health', 80) - 10)
        state['strength'] = max(0, state.get('strength', 35) - 2)
        msgs.append(('danger', '⚠ Голод подрывает здоровье!'))
    if state['sleep'] <= 10:
        state['mood'] = max(0, state.get('mood', 50) - 15)
        state['strength'] = max(0, state.get('strength', 35) - 2)
        msgs.append(('danger', '⚠ Хроническое недосыпание.'))
    if state.get('hygiene', 70) <= 5:
        state['health'] = max(0, state.get('health', 80) - 5)
        msgs.append(('danger', '⚠ Грязь вызывает болезни.'))

    # Weight
    hunger_val = state.get('hunger', 60)
    muscle = state.get('muscle_mass', 0)
    gym_today = 'gym' in state.get('actions_used', []) or 'run' in state.get('actions_used', [])
    if hunger_val > 70 and muscle < 30 and not gym_today:
        state['weight'] = min(120.0, state.get('weight', 70.0) + 0.1)
    elif hunger_val < 30:
        state['weight'] = max(55.0, state.get('weight', 70.0) - 0.15)

    # Paranoia creep at high tiers
    if tier >= 3 and random.random() < 0.1:
        state['paranoia'] = min(100, state.get('paranoia', 10) + 1)

    # 2. ADDICTIONS
    _process_addictions(state, msgs)

    # 3. INJURIES
    injuries = state.get('injuries', [])
    state['injuries'] = [dict(inj, days=inj['days'] - 1)
                         for inj in injuries if inj.get('days', 1) - 1 > 0]

    # 4. BUSINESS INCOME
    if state.get('businesses'):
        from economy import process_businesses_day
        biz_msgs, total_biz = process_businesses_day(state)
        msgs.extend(biz_msgs)
        if total_biz > 0:
            msgs.append(('result', f'🏪 Бизнесы принесли {fmt(total_biz)}/день'))

    # 5. OFFICIALS
    if state.get('bribed_officials'):
        from economy import process_officials_day
        heat_red = process_officials_day(state)
        if heat_red > 0:
            state['heat'] = max(0, state.get('heat', 0) - heat_red)

    # 6. GANG
    from gang import process_gang_day, daily_passive_income
    gang_msgs = process_gang_day(state)
    msgs.extend(gang_msgs)

    passive = daily_passive_income(state)
    passive += state.get('passive_income_bonus', 0)
    if passive > 0:
        state['cash'] = state.get('cash', 0) + passive
        state['money_earned'] = state.get('money_earned', 0) + passive
        msgs.append(('result', f'💰 Пассивный доход: +{fmt(passive)}'))

    # 7. HEAT SYSTEM
    _process_heat(state, msgs)

    # 8. RANDOM EVENT
    if random.random() < _event_chance(state):
        from events import pick_event, apply_auto_event
        event = pick_event(state)
        if event:
            if event.get('choices'):
                state['pending_event'] = event
            else:
                event_msgs = apply_auto_event(state, event)
                msgs.extend(event_msgs)

    # 9. NPC RIVALS
    if tier >= 2 and random.random() < 0.05:
        _npc_rival_action(state, msgs)

    # 10. HEAT NATURAL DECAY
    if 'lay_low' in state.get('actions_used', []):
        state['heat'] = max(0, state.get('heat', 0) - 2)

    # 11. INFLUENCE GAIN
    _update_influence(state, msgs)

    # 12. TIER ADVANCEMENT
    tier_msg = _check_tier_advancement(state)
    if tier_msg:
        msgs.append(('win', tier_msg))

    # 13. RESET DAILY
    state['actions_left'] = 3
    state['actions_used'] = []
    state.pop('shaved_today', None)
    if state.get('guard_active_days', 0) > 0:
        state['guard_active_days'] -= 1
        state['heat'] = max(0, state.get('heat', 0) - 2)

    # 14. ACHIEVEMENTS
    _check_achievements(state)

    # 15. LEADERBOARD
    _update_leaderboard_sync(state)

    # Keep log trimmed
    log = state.get('event_log', [])
    if len(log) > 200:
        state['event_log'] = log[-200:]

    return msgs


# ── Internal helpers ──────────────────────────────────────────────────────────

def _process_addictions(state, msgs):
    inv = state.get('inventory', {})
    cig_add = state.get('addiction_cigarettes', 0)
    alc_add = state.get('addiction_alcohol', 0)

    if cig_add > 0 and not state.get('smoker'):
        state['addiction_cigarettes'] = max(0, cig_add - 1)
    if alc_add > 0 and not state.get('drinker'):
        state['addiction_alcohol'] = max(0, alc_add - 1)

    has_cig = inv.get('papirosa', 0) > 0 or inv.get('prima', 0) > 0
    if cig_add > 30 and not has_cig and 'smoke' not in state.get('actions_used', []):
        state['mood'] = max(0, state.get('mood', 50) - 15)
        state['strength'] = max(0, state.get('strength', 35) - 5)
        msgs.append(('danger', '⚠ Ломка по куреву.'))
        if cig_add > 70:
            state['health'] = max(0, state.get('health', 80) - 10)

    has_alc = inv.get('vodka', 0) > 0
    if alc_add > 40 and not has_alc and 'drink' not in state.get('actions_used', []):
        state['mood'] = max(0, state.get('mood', 50) - 20)
        state['health'] = max(0, state.get('health', 80) - 8)
        msgs.append(('danger', '⚠ Ломка по алкоголю.'))
        if alc_add > 80:
            state['health'] = max(0, state.get('health', 80) - 10)
            msgs.append(('danger', '⚠ Цирроз прогрессирует.'))

    if state.get('smoker') and cig_add < 5:
        state['addiction_cigarettes'] = 5
    if state.get('drinker') and alc_add < 5:
        state['addiction_alcohol'] = 5


def _process_heat(state, msgs):
    heat = state.get('heat', 0)
    if heat <= 0:
        return
    tier = state.get('tier', 1)

    # Heat consequences
    if heat >= 95:
        if random.random() < 0.05:
            _full_crackdown(state, msgs)
    elif heat >= 85:
        if random.random() < 0.04:
            # Special operation
            businesses = state.get('businesses', [])
            if businesses:
                b = random.choice(businesses)
                b['is_raided'] = True
                b['raid_days_left'] = random.randint(5, 10)
                msgs.append(('danger', f'🚔 Силовая операция! {b["name"]} захвачен.'))
    elif heat >= 75:
        if random.random() < 0.03:
            # Arrest attempt
            escape = state.get('cash', 0) >= 5000 * tier
            if escape and tier >= 2:
                bribe = int(5000 * tier)
                state['cash'] = max(0, state.get('cash', 0) - bribe)
                state['heat'] = max(0, state.get('heat', 0) - 10)
                msgs.append(('danger', f'🚔 Попытка ареста! Откупился за {fmt(bribe)}.'))
            else:
                state['health'] = max(0, state.get('health', 80) - 20)
                state['mood'] = max(0, state.get('mood', 50) - 20)
                msgs.append(('danger', '🚔 Задержание! Тебя задержали и отпустили.'))
    elif heat >= 50:
        if random.random() < 0.02:
            # Business raid
            businesses = [b for b in state.get('businesses', []) if not b.get('is_raided')]
            if businesses:
                b = random.choice(businesses)
                b['is_raided'] = True
                b['raid_days_left'] = random.randint(2, 4)
                msgs.append(('danger', f'🚔 Облава на {b["name"]}!'))
    elif heat >= 30:
        if random.random() < 0.015:
            # Lose contraband
            if state.get('has_shiv') or state.get('has_phone'):
                from events import _confiscate
                _confiscate(state)
                msgs.append(('danger', '🔍 Проверка. Нашли контрабанду.'))


def _full_crackdown(state, msgs):
    msgs.append(('danger', '🚨 ПОЛНЫЙ РАЗГРОМ! Силовая операция против тебя!'))
    businesses = state.get('businesses', [])
    lost = businesses[:max(1, len(businesses) // 3)]
    for b in lost:
        b['is_raided'] = True
        b['raid_days_left'] = random.randint(10, 20)
    gang = state.get('gang_members', [])
    arrested = int(len(gang) * 0.2)
    state['gang_members'] = gang[arrested:]
    state['cash'] = max(0, state.get('cash', 0) * 0.5)
    state['heat'] = max(50, state.get('heat', 0) - 30)
    state['influence'] = max(0, state.get('influence', 0) * 0.7)
    if gang:
        msgs.append(('danger', f'  {arrested} человек арестовано.'))


def _npc_rival_action(state, msgs):
    tier = state.get('tier', 1)
    businesses = state.get('businesses', [])
    if businesses and random.random() < 0.5:
        b = random.choice(businesses)
        b['condition'] = max(0, b.get('condition', 100) - 20)
        msgs.append(('event', f'⚔ Конкуренты атаковали {b["name"]}. Состояние -{20}%.'))
    else:
        loss = int(100 * (10 ** (tier - 2))) if tier >= 2 else 0
        if loss > 0 and state.get('cash', 0) > loss:
            state['cash'] -= loss
            msgs.append(('event', f'⚔ Конкуренты перебили клиентов. -{fmt(loss)}'))


def _update_influence(state, msgs):
    tier = state.get('tier', 1)
    businesses = state.get('businesses', [])
    territories = state.get('territories', [])
    gang = state.get('gang_members', [])

    daily_gain = (
        sum(t.get('population', 10000) * 0.0001 for t in territories)
        + len(gang) * 0.5
        + len(businesses) * 5 * tier
        + state.get('reputation', 0) * 0.1
        + state.get('respect', 0) * 0.2
    )

    # At higher tiers, influence scales with income
    cash_daily = state.get('cash', 0) * 0.00001 * tier
    daily_gain += cash_daily

    daily_gain = max(0.1, daily_gain)
    state['influence'] = state.get('influence', 0) + daily_gain


def _event_chance(state):
    tier = state.get('tier', 1)
    base = 0.45
    heat_mod = state.get('heat', 0) * 0.002
    return min(0.85, base + heat_mod + (tier - 1) * 0.05)


def _check_tier_advancement(state):
    current_tier = state.get('tier', 1)
    if current_tier >= 6:
        return None

    cond = TIER_UNLOCK.get(current_tier + 1, {})
    if not cond:
        return None

    req_tier = cond.get('tier', 1)
    if current_tier < req_tier:
        return None

    if current_tier == 1:
        # T1 → T2: Смотрящий + influence 100 (from UDO, parole, or escape)
        rep_ok = state.get('reputation', 0) >= cond.get('reputation', 95)
        inf_ok = state.get('influence', 0) >= cond.get('influence', 100)
        if rep_ok and inf_ok:
            _advance_to_tier2(state)
            return '🎉 ОСВОБОЖДЁН! Добро пожаловать в РАЙОН.'
    else:
        inf_ok = state.get('influence', 0) >= cond.get('influence', 0)
        if inf_ok:
            state['tier'] = current_tier + 1
            tier_name = TIER_NAMES.get(current_tier + 1, '')
            return f'🔥 НОВЫЙ УРОВЕНЬ: {tier_name}!'
    return None


def _advance_to_tier2(state):
    state['tier'] = 2
    state['sentence_days'] = 0
    # Convert prison rep to street influence
    state['influence'] = max(100.0, state.get('reputation', 0) * 2.0)
    state['respect'] = state.get('reputation', 0) // 5
    # Spawn first NPC rival
    if not state.get('npc_rivals'):
        state['npc_rivals'].append({
            'id': 'npc_serega', 'name': 'Серёга Резаный',
            'tier': 2, 'strength': 40, 'territories': 1,
            'is_at_war': False, 'aggression': 0.25, 'wealth': 2000,
        })


def _check_achievements(state):
    day = state.get('days_survived', 0)
    rep = state.get('reputation', 0)
    tier = state.get('tier', 1)
    influence = state.get('influence', 0)
    rank_name, rank_lvl = get_rank(state)

    uid = state.get('user_id', 0)

    def award(ach_id, name, desc):
        if not has_achievement(uid, ach_id):
            unlock_achievement(uid, ach_id, name, desc, day)
            state.setdefault('achievements', []).append(ach_id)
            state.setdefault('event_log', []).append(
                ('achievement', f'🏆 Достижение: {name}')
            )

    # Tier 1
    if day == 7:   award('first_week',  'Первая неделя',  'Пережил первую неделю в зоне')
    if day == 30:  award('first_month', 'Первый месяц',   'Месяц за решёткой')
    if day == 100: award('hundred',     '100 дней',       'Пережил 100 дней')
    if day == 365: award('full_year',   'Год в зоне',     'Полный год за решёткой')
    if state.get('total_fights', 0) >= 1:
        award('first_fight', 'Первая драка', 'Первый бой')
    if state.get('smoker'):
        award('smoker',      'Первая затяжка', 'Закурил в зоне')
    if state.get('drinker'):
        award('drinker',     'Первый стакан',  'Выпил первый раз')
    if rank_lvl >= 2:  award('muzhik',      'Мужик',         'Достиг ранга Мужик')
    if rank_lvl >= 4:  award('avtoritet',   'Авторитет',     'Достиг ранга Авторитет')
    if rank_lvl >= 6:  award('smotrjashchiy','Смотрящий',    'Стал Смотрящим зоны')
    if len(state.get('gang_members', [])) >= 1:
        award('first_recruit', 'Первый боец', 'Завербовал первого')
    if state.get('cash', 0) >= 500:
        award('rich_t1',   'Богатей (зона)', 'Накопил 500 монет в зоне')
    if state.get('fights_won', 0) >= 5:
        award('five_wins', 'Боец',           'Выиграл 5 драк')
    if state.get('escape_route_known'):
        award('escape_plan','Побегушник',    'Узнал маршрут побега')
    if (day >= 30 and state.get('addiction_cigarettes', 0) == 0
            and state.get('addiction_alcohol', 0) == 0):
        award('clean', 'Чистый', 'Без зависимостей на 30-й день')
    if state.get('tattoos'):
        award('tattooed', 'Намалёванный', 'Набил татуировку')

    # Tier 2+
    if tier >= 2:
        award('tier2_unlock', 'На свободе!', 'Вышел из зоны')
        if state.get('businesses'):
            award('first_biz', 'Первый бизнес', 'Открыл первый бизнес')
        if len(state.get('businesses', [])) >= 3:
            award('three_biz', 'Три бизнеса', 'Три бизнеса одновременно')
        if any(b.get('tier', 1) == 2 for b in state.get('bribed_officials', [])):
            award('first_cop', 'Купил мента', 'Первый подкупленный чиновник')

    # Tier 3+
    if tier >= 3:
        award('tier3_unlock', 'Хозяин города', 'Вышел на городской уровень')
        if any(b.get('template_id') == 't3_casino' for b in state.get('businesses', [])):
            award('casino', 'Казино открыл', 'Открыл казино')
        if state.get('cash', 0) >= 1000000:
            award('million', 'Миллион в кармане', 'Накопил миллион')

    # Tier 4+
    if tier >= 4:
        award('tier4_unlock', 'Хозяин области', 'Региональный уровень')
        if state.get('cash', 0) >= 1000000000:
            award('billion', 'Миллиард', 'Миллиард активов')

    # Tier 5+
    if tier >= 5:
        award('tier5_unlock',  'Национальный',       'Национальный уровень')
        if len(state.get('gang_members', [])) >= 1000:
            award('army_1000', 'Частная армия 1000', '1000 бойцов')

    # Tier 6
    if tier >= 6:
        award('tier6_unlock', 'Хозяин мира', 'Мировой уровень')
        if influence >= 10000000:
            award('legend', 'ЛЕГЕНДА', 'Влияние 10 миллионов')
        if any(b.get('template_id') == 't6_island' for b in state.get('businesses', [])):
            award('island', 'Остров куплен', 'Личный остров')


def _update_leaderboard_sync(state):
    try:
        import database as db
        uid = state.get('user_id', 0)
        rank_name, _ = get_rank(state)
        score = calculate_score(state)
        db.update_leaderboard(
            user_id=uid,
            player_name=state.get('player_name', 'Игрок'),
            score=score,
            influence=state.get('influence', 0),
            tier=state.get('tier', 1),
            rank_name=rank_name,
            days_played=state.get('days_survived', 0),
            num_businesses=len(state.get('businesses', [])),
            gang_size=len(state.get('gang_members', [])),
            territories=len(state.get('territories', [])),
        )
    except Exception:
        pass
