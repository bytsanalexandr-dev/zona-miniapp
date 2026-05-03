TERRITORY_DEFS = [
    # Ring 1: Район (10) — tier_req 2
    {'id':'r1_1',  'name':'Южный район',        'ring':1,'segment':0, 'tier_req':2,'income':100,    'capture_cost':500},
    {'id':'r1_2',  'name':'Северный район',      'ring':1,'segment':1, 'tier_req':2,'income':100,    'capture_cost':500},
    {'id':'r1_3',  'name':'Западный район',      'ring':1,'segment':2, 'tier_req':2,'income':100,    'capture_cost':500},
    {'id':'r1_4',  'name':'Восточный район',     'ring':1,'segment':3, 'tier_req':2,'income':100,    'capture_cost':500},
    {'id':'r1_5',  'name':'Центральный район',   'ring':1,'segment':4, 'tier_req':2,'income':150,    'capture_cost':600},
    {'id':'r1_6',  'name':'Портовый район',      'ring':1,'segment':5, 'tier_req':2,'income':120,    'capture_cost':500},
    {'id':'r1_7',  'name':'Заводской район',     'ring':1,'segment':6, 'tier_req':2,'income':130,    'capture_cost':500},
    {'id':'r1_8',  'name':'Рыночный район',      'ring':1,'segment':7, 'tier_req':2,'income':110,    'capture_cost':500},
    {'id':'r1_9',  'name':'Крим. квартал',       'ring':1,'segment':8, 'tier_req':2,'income':200,    'capture_cost':700},
    {'id':'r1_10', 'name':'Торговый квартал',    'ring':1,'segment':9, 'tier_req':2,'income':160,    'capture_cost':600},
    # Ring 2: Город (8) — tier_req 3
    {'id':'r2_1',  'name':'Северный город',      'ring':2,'segment':0, 'tier_req':3,'income':1000,   'capture_cost':3000},
    {'id':'r2_2',  'name':'Портовый город',      'ring':2,'segment':1, 'tier_req':3,'income':1200,   'capture_cost':3500},
    {'id':'r2_3',  'name':'Промышленный город',  'ring':2,'segment':2, 'tier_req':3,'income':1500,   'capture_cost':4000},
    {'id':'r2_4',  'name':'Курортный город',     'ring':2,'segment':3, 'tier_req':3,'income':900,    'capture_cost':3000},
    {'id':'r2_5',  'name':'Финансовый центр',    'ring':2,'segment':4, 'tier_req':3,'income':2000,   'capture_cost':5000},
    {'id':'r2_6',  'name':'Столичный округ',     'ring':2,'segment':5, 'tier_req':3,'income':1800,   'capture_cost':5000},
    {'id':'r2_7',  'name':'Академгородок',       'ring':2,'segment':6, 'tier_req':3,'income':800,    'capture_cost':2500},
    {'id':'r2_8',  'name':'Военный город',       'ring':2,'segment':7, 'tier_req':3,'income':1100,   'capture_cost':3500},
    # Ring 3: Область (6) — tier_req 4
    {'id':'r3_1',  'name':'Западная область',    'ring':3,'segment':0, 'tier_req':4,'income':10000,  'capture_cost':30000},
    {'id':'r3_2',  'name':'Восточная область',   'ring':3,'segment':1, 'tier_req':4,'income':10000,  'capture_cost':30000},
    {'id':'r3_3',  'name':'Северный регион',     'ring':3,'segment':2, 'tier_req':4,'income':12000,  'capture_cost':35000},
    {'id':'r3_4',  'name':'Южный регион',        'ring':3,'segment':3, 'tier_req':4,'income':11000,  'capture_cost':30000},
    {'id':'r3_5',  'name':'Нефтяной регион',     'ring':3,'segment':4, 'tier_req':4,'income':20000,  'capture_cost':50000},
    {'id':'r3_6',  'name':'Аграрный регион',     'ring':3,'segment':5, 'tier_req':4,'income':8000,   'capture_cost':25000},
    # Ring 4: Страна (4) — tier_req 5
    {'id':'r4_1',  'name':'Западная страна',     'ring':4,'segment':0, 'tier_req':5,'income':100000, 'capture_cost':300000},
    {'id':'r4_2',  'name':'Восточная страна',    'ring':4,'segment':1, 'tier_req':5,'income':100000, 'capture_cost':300000},
    {'id':'r4_3',  'name':'Северная страна',     'ring':4,'segment':2, 'tier_req':5,'income':150000, 'capture_cost':400000},
    {'id':'r4_4',  'name':'Южная страна',        'ring':4,'segment':3, 'tier_req':5,'income':120000, 'capture_cost':350000},
    # Ring 5: Мир (3) — tier_req 6
    {'id':'r5_1',  'name':'Западный континент',  'ring':5,'segment':0, 'tier_req':6,'income':1000000,'capture_cost':3000000},
    {'id':'r5_2',  'name':'Восточный континент', 'ring':5,'segment':1, 'tier_req':6,'income':1000000,'capture_cost':3000000},
    {'id':'r5_3',  'name':'Центральный океан',   'ring':5,'segment':2, 'tier_req':6,'income':2000000,'capture_cost':5000000},
]

PLAYER_COLORS = [
    '#ff4444', '#4488ff', '#44dd44', '#ffdd44', '#ff44ff',
    '#44ffff', '#ff8844', '#8844ff', '#44ff88', '#ff4488',
]

TOTAL_TERRITORIES = len(TERRITORY_DEFS)  # 31

def get_territory_def(tid: str):
    return next((t for t in TERRITORY_DEFS if t['id'] == tid), None)
