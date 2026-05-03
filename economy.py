import random

# ── Tier 1 shop items ─────────────────────────────────────────────────────────
ITEMS = {
    'bread':       {'name': 'Хлеб',          'category': 'Еда',        'cost': 2,   'min_rep': 0,
                    'desc': 'Казённый хлеб.',                           'effects': {'hunger': 10}},
    'tushenka':    {'name': 'Тушняк',         'category': 'Еда',        'cost': 8,   'min_rep': 0,
                    'desc': 'Консервы — главная валюта зоны.',           'effects': {'hunger': 30, 'health': 3}},
    'sugar':       {'name': 'Сахар',          'category': 'Еда',        'cost': 3,   'min_rep': 0,
                    'desc': 'Для чифиря.',                              'effects': {'hunger': 5, 'mood': 5}},
    'chifir':      {'name': 'Чифирь',         'category': 'Еда',        'cost': 5,   'min_rep': 0,
                    'desc': 'Бодрит. Мешает спать.',                    'effects': {'mood': 20, 'sleep': -15, 'health': -2}},
    'vodka':       {'name': 'Водяра',         'category': 'Еда',        'cost': 15,  'min_rep': 0,
                    'desc': 'Самогон. Опасная радость.',                 'effects': {'mood': 30, 'addiction_alcohol': 15, 'health': -5},
                    'contraband': True},
    'papirosa':    {'name': 'Папироса',       'category': 'Курево',     'cost': 3,   'min_rep': 0,
                    'desc': 'Простая папироса.',                        'effects': {'mood': 15, 'addiction_cigarettes': 10, 'health': -1},
                    'is_cigarette': True},
    'prima':       {'name': 'Сигарета Прима', 'category': 'Курево',     'cost': 4,   'min_rep': 0,
                    'desc': 'Чуть получше папиросы.',                   'effects': {'mood': 12, 'addiction_cigarettes': 8, 'health': -1},
                    'is_cigarette': True},
    'soap':        {'name': 'Мыло',           'category': 'Гигиена',    'cost': 5,   'min_rep': 0,
                    'desc': 'Хозяйственное мыло.',                      'effects': {'hygiene': 20}},
    'toothpaste':  {'name': 'Зубная паста',   'category': 'Гигиена',    'cost': 4,   'min_rep': 0,
                    'desc': 'Зубная паста.',                            'effects': {'hygiene': 10, 'mood': 3}},
    'razor':       {'name': 'Бритва',         'category': 'Гигиена',    'cost': 6,   'min_rep': 0,
                    'desc': 'Одноразовая бритва.',                      'effects': {'hygiene': 15}},
    'tracksuit':   {'name': 'Треники',        'category': 'Одежда',     'cost': 25,  'min_rep': 30,
                    'desc': 'Спортивный костюм.',                       'effects': {'mood': 10},
                    'is_clothing': True, 'clothing_level': 1},
    'sneakers':    {'name': 'Кеды',           'category': 'Одежда',     'cost': 15,  'min_rep': 0,
                    'desc': 'Нормальные кеды.',                         'effects': {'mood': 5},
                    'is_clothing': True, 'clothing_level': 1},
    'leather_jacket': {'name': 'Кожанка',     'category': 'Одежда',     'cost': 80,  'min_rep': 60,
                    'desc': 'Авторитетный вид.',                        'effects': {'mood': 20, 'reputation': 5},
                    'is_clothing': True, 'clothing_level': 3},
    'shiv':        {'name': 'Заточка',        'category': 'Контрабанда','cost': 20,  'min_rep': 0,
                    'desc': 'Самодельный нож.',                         'effects': {},
                    'contraband': True, 'is_weapon': True},
    'phone':       {'name': 'Телефон',        'category': 'Контрабанда','cost': 100, 'min_rep': 0,
                    'desc': 'Мобила. Высокий риск.',                    'effects': {'mood': 30},
                    'contraband': True},
    'tea_set':     {'name': 'Набор для чифиря','category': 'Контрабанда','cost': 12,  'min_rep': 0,
                    'desc': 'Для варки чифиря на продажу.',              'effects': {},
                    'contraband': True},
    'bandage':     {'name': 'Бинт',           'category': 'Медицина',   'cost': 7,   'min_rep': 0,
                    'desc': 'Перевязочный материал.',                   'effects': {'health': 15}},
    'painkillers': {'name': 'Таблетки',       'category': 'Медицина',   'cost': 10,  'min_rep': 0,
                    'desc': 'Обезболивающее.',                          'effects': {'health': 10, 'mood': 5}},
}

# ── Business templates (all tiers) ────────────────────────────────────────────
BUSINESSES = {
    # TIER 1
    't1_chifir_trade': {
        'name': 'Чифирный бизнес',     'tier': 1, 'cost': 50,          'base_income': 10,
        'heat_gen': 0.5,  'desc': 'Варишь и продаёшь чифирь в бараке.',
        'max_level': 3,   'level_mult': 1.8},
    't1_card_table': {
        'name': 'Картёжный стол',      'tier': 1, 'cost': 100,         'base_income': 20,
        'heat_gen': 1.0,  'desc': 'Держишь игру в карты.',
        'max_level': 3,   'level_mult': 1.8},
    't1_canteen_point': {
        'name': 'Точка в столовой',    'tier': 1, 'cost': 150,         'base_income': 30,
        'heat_gen': 0.8,  'desc': 'Продаёшь еду и сигареты в столовой.',
        'max_level': 3,   'level_mult': 1.8},
    't1_gym_control': {
        'name': 'Контроль качалки',    'tier': 1, 'cost': 200,         'base_income': 15,
        'heat_gen': 0.5,  'desc': 'Берёшь дань с качалки.',
        'max_level': 3,   'level_mult': 1.8},
    't1_contraband_channel': {
        'name': 'Канал контрабанды',   'tier': 1, 'cost': 300,         'base_income': 50,
        'heat_gen': 3.0,  'desc': 'Канал контрабанды через забор.',
        'max_level': 3,   'level_mult': 2.0},
    # TIER 2
    't2_kiosk': {
        'name': 'Ларёк',               'tier': 2, 'cost': 500,         'base_income': 50,
        'heat_gen': 0.3,  'desc': 'Небольшой киоск на районе.',
        'max_level': 5,   'level_mult': 2.0},
    't2_market': {
        'name': 'Рынок',               'tier': 2, 'cost': 2000,        'base_income': 200,
        'heat_gen': 0.5,  'desc': 'Рынок под твоим контролем.',
        'max_level': 5,   'level_mult': 2.0},
    't2_carwash': {
        'name': 'Автомойка',           'tier': 2, 'cost': 3000,        'base_income': 300,
        'heat_gen': 0.4,  'desc': 'Автомойка — отмывает и деньги.',
        'max_level': 5,   'level_mult': 2.0},
    't2_nightclub': {
        'name': 'Ночной клуб',         'tier': 2, 'cost': 8000,        'base_income': 800,
        'heat_gen': 1.5,  'desc': 'Центр теневых сходок.',
        'max_level': 5,   'level_mult': 2.0},
    't2_drug_point': {
        'name': 'Наркоточка',          'tier': 2, 'cost': 1000,        'base_income': 400,
        'heat_gen': 4.0,  'desc': 'Рискованно, но прибыльно.',
        'max_level': 5,   'level_mult': 2.2},
    't2_slot_machines': {
        'name': 'Игровые автоматы',    'tier': 2, 'cost': 1500,        'base_income': 250,
        'heat_gen': 1.0,  'desc': 'Нелегальные автоматы.',
        'max_level': 5,   'level_mult': 2.0},
    # TIER 3
    't3_gas_station': {
        'name': 'Заправка',            'tier': 3, 'cost': 20000,       'base_income': 2000,
        'heat_gen': 0.2,  'desc': 'Легальная заправка.',
        'max_level': 5,   'level_mult': 2.0},
    't3_restaurant': {
        'name': 'Ресторан',            'tier': 3, 'cost': 15000,       'base_income': 1500,
        'heat_gen': 0.1,  'desc': 'Ресторан — место встреч.',
        'max_level': 5,   'level_mult': 2.0},
    't3_casino': {
        'name': 'Казино',              'tier': 3, 'cost': 50000,       'base_income': 8000,
        'heat_gen': 2.0,  'desc': 'Казино — мечта авторитета.',
        'max_level': 5,   'level_mult': 2.2},
    't3_construction': {
        'name': 'Строительная фирма',  'tier': 3, 'cost': 40000,       'base_income': 5000,
        'heat_gen': 0.3,  'desc': 'Откаты и господряды.',
        'max_level': 5,   'level_mult': 2.0},
    't3_loan_shark': {
        'name': 'Ростовщик',           'tier': 3, 'cost': 10000,       'base_income': 3000,
        'heat_gen': 1.5,  'desc': 'Кредиты под дикие проценты.',
        'max_level': 5,   'level_mult': 2.0},
    # TIER 4
    't4_factory': {
        'name': 'Завод',               'tier': 4, 'cost': 500000,      'base_income': 50000,
        'heat_gen': 0.1,  'desc': 'Производственное предприятие.',
        'max_level': 5,   'level_mult': 2.0},
    't4_mall': {
        'name': 'ТРЦ',                 'tier': 4, 'cost': 300000,      'base_income': 30000,
        'heat_gen': 0.1,  'desc': 'Торгово-развлекательный центр.',
        'max_level': 5,   'level_mult': 2.0},
    't4_bank': {
        'name': 'Банк',                'tier': 4, 'cost': 1000000,     'base_income': 150000,
        'heat_gen': 0.5,  'desc': 'Региональный банк.',
        'max_level': 5,   'level_mult': 2.0},
    't4_media': {
        'name': 'Медиахолдинг',        'tier': 4, 'cost': 200000,      'base_income': 20000,
        'heat_gen': -1.0, 'desc': 'СМИ снижают репутационные риски.',
        'max_level': 5,   'level_mult': 2.0},
    't4_agro': {
        'name': 'Агрохолдинг',         'tier': 4, 'cost': 400000,      'base_income': 40000,
        'heat_gen': 0.05, 'desc': 'Земля кормит.',
        'max_level': 5,   'level_mult': 2.0},
    # TIER 5
    't5_state_bank': {
        'name': 'Государственный банк','tier': 5, 'cost': 10000000,    'base_income': 1500000,
        'heat_gen': 0.5,  'desc': 'Контроль над госбанком.',
        'max_level': 3,   'level_mult': 2.0},
    't5_oil_company': {
        'name': 'Нефтяная компания',   'tier': 5, 'cost': 50000000,    'base_income': 8000000,
        'heat_gen': 0.3,  'desc': 'Нефтяная корпорация.',
        'max_level': 3,   'level_mult': 2.0},
    't5_airline': {
        'name': 'Авиакомпания',        'tier': 5, 'cost': 20000000,    'base_income': 3000000,
        'heat_gen': 0.1,  'desc': 'Собственная авиакомпания.',
        'max_level': 3,   'level_mult': 2.0},
    't5_media_empire': {
        'name': 'Медиаимперия',        'tier': 5, 'cost': 15000000,    'base_income': 2000000,
        'heat_gen': -3.0, 'desc': 'Полный контроль над нацСМИ.',
        'max_level': 3,   'level_mult': 2.0},
    # TIER 6
    't6_offshore_bank': {
        'name': 'Офшорный банк',       'tier': 6, 'cost': 100000000,   'base_income': 20000000,
        'heat_gen': 1.0,  'desc': 'Офшорный банк на Каймановых о-вах.',
        'max_level': 3,   'level_mult': 2.0},
    't6_cartel': {
        'name': 'Международный картель','tier': 6,'cost': 500000000,   'base_income': 100000000,
        'heat_gen': 5.0,  'desc': 'Глобальная наркосеть.',
        'max_level': 3,   'level_mult': 2.0},
    't6_corporation': {
        'name': 'Транснац. корпорация','tier': 6, 'cost': 1000000000,  'base_income': 200000000,
        'heat_gen': 0.5,  'desc': 'Легальная корпорация мирового масштаба.',
        'max_level': 3,   'level_mult': 2.0},
    't6_island': {
        'name': 'Личный остров',       'tier': 6, 'cost': 2000000000,  'base_income': 500000000,
        'heat_gen': -10.0,'desc': 'Остров-государство. Своя юрисдикция.',
        'max_level': 1,   'level_mult': 1.0},
}

# Official bribe types
OFFICIALS = {
    'cop': {
        'name_template': 'Капитан {name}', 'tier': 2,
        'cost': 500, 'daily_cost': 50,
        'bonus_type': 'heat_reduction', 'bonus_value': 5,
        'desc': 'Снижает жару на 5 ед./день.',
    },
    'judge': {
        'name_template': 'Судья {name}', 'tier': 3,
        'cost': 20000, 'daily_cost': 500,
        'bonus_type': 'case_dismissal', 'bonus_value': 1,
        'desc': 'Закрывает уголовные дела.',
    },
    'deputy': {
        'name_template': 'Депутат {name}', 'tier': 4,
        'cost': 100000, 'daily_cost': 2000,
        'bonus_type': 'heat_reduction', 'bonus_value': 10,
        'desc': 'Снижает жару на 10 ед./день.',
    },
    'minister': {
        'name_template': 'Министр {name}', 'tier': 5,
        'cost': 1000000, 'daily_cost': 10000,
        'bonus_type': 'heat_immunity', 'bonus_value': 50,
        'desc': 'Гос. защита: иммунитет к жаре до 50.',
    },
    'fsb_general': {
        'name_template': 'Генерал {name}', 'tier': 5,
        'cost': 5000000, 'daily_cost': 50000,
        'bonus_type': 'heat_reduction', 'bonus_value': 20,
        'desc': 'Снижает жару на 20 ед./день.',
    },
}

_OFFICIAL_NAMES = [
    'Петров', 'Иванов', 'Сидоров', 'Кузнецов', 'Смирнов',
    'Попов', 'Соколов', 'Новиков', 'Морозов', 'Волков',
]

_biz_counter = [0]
_off_counter  = [0]


def _next_biz_id():
    _biz_counter[0] += 1
    return f'biz_{_biz_counter[0]:04d}'


def _next_off_id():
    _off_counter[0] += 1
    return f'off_{_off_counter[0]:04d}'


# ── Item helpers ──────────────────────────────────────────────────────────────

def can_buy(state, item_id):
    item = ITEMS.get(item_id)
    if not item:
        return False, 'Товар не найден'
    cash = state.get('cash', 0)
    if cash < item['cost']:
        return False, f"Недостаточно денег (нужно {fmt(item['cost'])})"
    if state.get('reputation', 0) < item.get('min_rep', 0):
        return False, f"Недостаточно репутации (нужно {item['min_rep']})"
    return True, 'OK'


def buy_item(state, item_id):
    ok, msg = can_buy(state, item_id)
    if not ok:
        return False, msg
    item = ITEMS[item_id]
    state['cash'] = state.get('cash', 0) - item['cost']
    inv = state.setdefault('inventory', {})
    inv[item_id] = inv.get(item_id, 0) + 1
    if item.get('is_weapon'):
        state['has_shiv'] = True
    if item_id == 'phone':
        state['has_phone'] = True
    if item.get('is_clothing'):
        lvl = item.get('clothing_level', 0)
        if lvl > state.get('clothing_level', 0):
            state['clothing_level'] = lvl
            state['clothing_item'] = item_id
    return True, f"Куплено: {item['name']}"


def use_item(state, item_id):
    inv = state.get('inventory', {})
    if inv.get(item_id, 0) <= 0:
        return False, {}, 'Этого предмета нет в инвентаре'
    item = ITEMS.get(item_id)
    if not item:
        return False, {}, 'Неизвестный предмет'
    effects = dict(item.get('effects', {}))
    for stat, value in effects.items():
        if stat in state:
            state[stat] = max(0, min(100, state[stat] + value))
    if item['category'] == 'Еда' and 'hunger' in effects:
        state['weight'] = min(120.0, state.get('weight', 70.0) + effects['hunger'] * 0.02)
    if effects.get('addiction_cigarettes', 0) > 0:
        state['smoker'] = True
    if effects.get('addiction_alcohol', 0) > 0:
        state['drinker'] = True
    inv[item_id] -= 1
    if inv[item_id] <= 0:
        del inv[item_id]
    return True, effects, f"Использовано: {item['name']}"


def sell_item(state, item_id, quantity=1):
    inv = state.get('inventory', {})
    if inv.get(item_id, 0) < quantity:
        return False, 'Недостаточно товара'
    item = ITEMS.get(item_id)
    if not item:
        return False, 'Неизвестный товар'
    sell_price = max(1, item['cost'] // 2)
    total = sell_price * quantity
    inv[item_id] -= quantity
    if inv[item_id] <= 0:
        del inv[item_id]
    state['cash'] = state.get('cash', 0) + total
    state['money_earned'] = state.get('money_earned', 0) + total
    return True, f'Продано за {fmt(total)}'


def get_shop_items(state):
    rep = state.get('reputation', 0)
    return [(iid, item) for iid, item in ITEMS.items()
            if item.get('cost', 0) > 0 and item.get('min_rep', 0) <= rep]


def craft_chifir(state):
    inv = state.get('inventory', {})
    if inv.get('tea_set', 0) <= 0:
        return False, 'Нет набора для варки чифиря'
    if inv.get('sugar', 0) <= 0:
        return False, 'Нет сахара'
    inv['sugar'] -= 1
    if inv['sugar'] <= 0:
        del inv['sugar']
    inv['chifir'] = inv.get('chifir', 0) + 3
    return True, 'Сварил 3 порции чифиря'


# ── Business helpers ──────────────────────────────────────────────────────────

def get_available_businesses(state):
    tier = state.get('tier', 1)
    owned_ids = {b['template_id'] for b in state.get('businesses', [])}
    return [
        (bid, biz)
        for bid, biz in BUSINESSES.items()
        if biz['tier'] <= tier and bid not in owned_ids
    ]


def can_buy_business(state, template_id):
    biz = BUSINESSES.get(template_id)
    if not biz:
        return False, 'Бизнес не найден'
    if biz['tier'] > state.get('tier', 1):
        return False, f"Доступно с уровня {biz['tier']}"
    if state.get('cash', 0) < biz['cost']:
        return False, f"Нужно {fmt(biz['cost'])}"
    owned = [b for b in state.get('businesses', []) if b['template_id'] == template_id]
    if owned:
        return False, 'Уже куплено'
    return True, 'OK'


def buy_business(state, template_id):
    ok, msg = can_buy_business(state, template_id)
    if not ok:
        return False, msg
    biz = BUSINESSES[template_id]
    state['cash'] = state.get('cash', 0) - biz['cost']
    state['total_assets'] = state.get('total_assets', 0) + biz['cost']
    instance = {
        'id': _next_biz_id(),
        'template_id': template_id,
        'name': biz['name'],
        'tier': biz['tier'],
        'level': 1,
        'condition': 100,
        'manager_id': None,
        'is_raided': False,
        'raid_days_left': 0,
        'bonus_days': 0,
        'bonus_multiplier': 1.0,
        'days_owned': 0,
    }
    state.setdefault('businesses', []).append(instance)
    return True, f"Куплено: {biz['name']} (+{fmt(biz['base_income'])}/день)"


def sell_business(state, biz_id):
    businesses = state.get('businesses', [])
    target = next((b for b in businesses if b['id'] == biz_id), None)
    if not target:
        return False, 'Бизнес не найден'
    biz = BUSINESSES[target['template_id']]
    sell_price = int(biz['cost'] * (biz['level_mult'] ** (target['level'] - 1)) * 0.6)
    businesses.remove(target)
    state['cash'] = state.get('cash', 0) + sell_price
    state['total_assets'] = max(0, state.get('total_assets', 0) - sell_price)
    return True, f"Продано за {fmt(sell_price)}"


def upgrade_business(state, biz_id):
    businesses = state.get('businesses', [])
    target = next((b for b in businesses if b['id'] == biz_id), None)
    if not target:
        return False, 'Бизнес не найден'
    biz = BUSINESSES[target['template_id']]
    if target['level'] >= biz.get('max_level', 5):
        return False, 'Максимальный уровень'
    upgrade_cost = int(biz['cost'] * (biz['level_mult'] ** target['level']))
    if state.get('cash', 0) < upgrade_cost:
        return False, f"Нужно {fmt(upgrade_cost)}"
    state['cash'] = state.get('cash', 0) - upgrade_cost
    state['total_assets'] = state.get('total_assets', 0) + upgrade_cost
    target['level'] += 1
    new_income = int(biz['base_income'] * (biz['level_mult'] ** (target['level'] - 1)))
    return True, f"{biz['name']} улучшен до ур.{target['level']} (+{fmt(new_income)}/день)"


def business_daily_income(biz_instance, state):
    """Return income for one business instance for one day."""
    biz = BUSINESSES.get(biz_instance['template_id'])
    if not biz:
        return 0.0
    if biz_instance.get('is_raided'):
        return 0.0
    base = biz['base_income'] * (biz.get('level_mult', 2.0) ** (biz_instance['level'] - 1))
    cond_mult = biz_instance.get('condition', 100) / 100.0
    manager_mult = 1.2 if biz_instance.get('manager_id') else 1.0
    heat = state.get('heat', 0)
    heat_penalty = 1.0 - (heat / 200.0)
    bonus = biz_instance.get('bonus_multiplier', 1.0) if biz_instance.get('bonus_days', 0) > 0 else 1.0
    return base * cond_mult * manager_mult * heat_penalty * bonus


def business_daily_heat(biz_instance):
    biz = BUSINESSES.get(biz_instance['template_id'])
    if not biz:
        return 0.0
    return biz.get('heat_gen', 0.5) * biz_instance['level']


def process_businesses_day(state):
    """Process all businesses for one day. Returns list of (kind, msg)."""
    msgs = []
    businesses = state.get('businesses', [])
    total_income = 0.0
    total_heat = 0.0

    for biz in businesses:
        biz['days_owned'] = biz.get('days_owned', 0) + 1

        # Raid countdown
        if biz.get('is_raided') and biz.get('raid_days_left', 0) > 0:
            biz['raid_days_left'] -= 1
            if biz['raid_days_left'] <= 0:
                biz['is_raided'] = False
                msgs.append(('result', f"🏪 {biz['name']} восстановлен после рейда."))
            continue

        # Condition decay
        biz['condition'] = max(0, biz.get('condition', 100) - random.uniform(0.3, 1.2))

        # Bonus countdown
        if biz.get('bonus_days', 0) > 0:
            biz['bonus_days'] -= 1

        # Income
        income = business_daily_income(biz, state)
        total_income += income
        total_heat += business_daily_heat(biz)

        # Random business events (2% chance per business per day)
        if random.random() < 0.02:
            msgs.extend(_random_business_event(state, biz))

    if total_income > 0:
        state['cash'] = state.get('cash', 0) + total_income
        state['money_earned'] = state.get('money_earned', 0) + total_income

    state['heat'] = min(100, state.get('heat', 0) + total_heat)
    return msgs, total_income


def _random_business_event(state, biz):
    msgs = []
    roll = random.random()
    if roll < 0.20:
        biz['condition'] = max(0, biz.get('condition', 100) - 30)
        msgs.append(('danger', f"🔥 Пожар в {biz['name']}! Состояние -{30}%."))
    elif roll < 0.40:
        biz['is_raided'] = True
        biz['raid_days_left'] = random.randint(2, 5)
        state['heat'] = min(100, state.get('heat', 0) + 10)
        msgs.append(('danger', f"🚔 Облава! {biz['name']} закрыт на {biz['raid_days_left']} дн."))
    elif roll < 0.55:
        fine = int(BUSINESSES[biz['template_id']]['base_income'] * random.uniform(0.5, 2.0))
        if state.get('cash', 0) >= fine:
            state['cash'] -= fine
            msgs.append(('event', f"💸 Налоговая проверка: штраф {fmt(fine)}."))
        else:
            biz['is_raided'] = True
            biz['raid_days_left'] = 3
            msgs.append(('danger', f"⚠ Не смог заплатить штраф. {biz['name']} закрыт."))
    elif roll < 0.75:
        biz['bonus_days'] = 7
        biz['bonus_multiplier'] = 1.5
        msgs.append(('win', f"📈 Удачный месяц в {biz['name']}! +50% дохода на 7 дн."))
    else:
        biz['condition'] = min(100, biz.get('condition', 100) + 20)
        msgs.append(('result', f"🔧 Ремонт в {biz['name']}. Состояние восстановлено."))
    return msgs


# ── Officials / bribes ────────────────────────────────────────────────────────

def can_bribe_official(state, official_type):
    off = OFFICIALS.get(official_type)
    if not off:
        return False, 'Тип чиновника не найден'
    if state.get('tier', 1) < off['tier']:
        return False, f"Доступно с уровня {off['tier']}"
    already = [o for o in state.get('bribed_officials', []) if o['type'] == official_type]
    if already:
        return False, 'Уже куплен'
    if state.get('cash', 0) < off['cost']:
        return False, f"Нужно {fmt(off['cost'])}"
    return True, 'OK'


def bribe_official(state, official_type):
    ok, msg = can_bribe_official(state, official_type)
    if not ok:
        return False, msg
    off = OFFICIALS[official_type]
    state['cash'] = state.get('cash', 0) - off['cost']
    name = random.choice(_OFFICIAL_NAMES)
    instance = {
        'id': _next_off_id(),
        'type': official_type,
        'name': off['name_template'].format(name=name),
        'daily_cost': off['daily_cost'],
        'bonus_type': off['bonus_type'],
        'bonus_value': off['bonus_value'],
        'days_held': 0,
    }
    state.setdefault('bribed_officials', []).append(instance)
    return True, f"Куплен: {instance['name']} (-{fmt(off['daily_cost'])}/день)"


def process_officials_day(state):
    """Pay officials and apply bonuses. Returns heat reduction."""
    officials = state.get('bribed_officials', [])
    heat_reduction = 0.0
    to_remove = []
    for off in officials:
        off['days_held'] = off.get('days_held', 0) + 1
        daily = off.get('daily_cost', 0)
        if state.get('cash', 0) >= daily:
            state['cash'] -= daily
            bt = off.get('bonus_type', '')
            bv = off.get('bonus_value', 0)
            if bt == 'heat_reduction':
                heat_reduction += bv
            elif bt == 'heat_immunity':
                state['heat'] = min(state.get('heat', 0), bv)
        else:
            to_remove.append(off)
    for off in to_remove:
        officials.remove(off)
        state.setdefault('event_log', []).append(
            ('danger', f"💸 {off['name']} ушёл — не смог заплатить.")
        )
    return heat_reduction


def fmt(n):
    """Format number with space as thousands separator."""
    return f'{int(n):,}'.replace(',', ' ')
