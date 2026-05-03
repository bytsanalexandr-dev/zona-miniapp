import random

# ─────────────────────────────────────────────────────────────────────────────
# Event format
# tier: 0=any tier, 1-6=specific tier
# choices=None → auto event (apply_auto_event)
# choices=[{text, effects, msg, ...}] → player picks
# effects keys: any state stat + 'cash_abs' for cash change, 'heat', 'influence'
# ─────────────────────────────────────────────────────────────────────────────

ALL_EVENTS = [

    # ══════════════════════════════════════════════════════════════════════════
    # TIER 1 — ЗОНА
    # ══════════════════════════════════════════════════════════════════════════
    {
        'id': 'toilet_beating', 'tier': 1, 'min_day': 1, 'max_day': 30, 'weight': 12,
        'text': 'В туалете тебя прижали двое. "Ну что, первоход, давай знакомиться."',
        'choices': [
            {'text': 'Дать отпор',
             'fight': True, 'difficulty': 35,
             'win_msg': 'Ты отбился. Смотрят по-другому.',
             'win_effects': {'reputation': 15, 'health': -10},
             'lose_msg': 'Отметелили. Но ты не сломался.',
             'lose_effects': {'reputation': 5, 'health': -25}},
            {'text': 'Отдать что есть',
             'effects': {'mood': -20, 'reputation': -10},
             'msg': 'Ты отдал хлеб и мыло. Посмеиваются.'},
        ],
    },
    {
        'id': 'cellmate_tea', 'tier': 1, 'min_day': 1, 'max_day': 20, 'weight': 10,
        'text': 'Сокамерник Витёк протягивает кружку чифиря: "Пей, брат. Здесь без этого никак."',
        'choices': [
            {'text': 'Принять чай',
             'effects': {'mood': 15, 'sleep': -10, 'addiction_cigarettes': 5, 'reputation': 3},
             'msg': '"Нормальный ты мужик." Отношения потеплели.'},
            {'text': 'Отказаться вежливо',
             'effects': {'mood': -5},
             'msg': 'Витёк кивнул. Держит дистанцию.'},
        ],
    },
    {
        'id': 'shmon', 'tier': 1, 'min_day': 3, 'max_day': None, 'weight': 8,
        'text': 'Шмон! Вертухаи врываются и переворачивают всё вверх дном.',
        'auto_effects': {'mood': -10},
        'auto_msg': 'Проверка закончилась. Камера разгромлена.',
        'contraband_risk': True,
    },
    {
        'id': 'bad_food', 'tier': 1, 'min_day': 1, 'max_day': None, 'weight': 9,
        'text': 'Пайка сегодня — помои с кусочками непонятного. Желудок скручивает.',
        'auto_effects': {'hunger': -15, 'health': -5, 'mood': -8},
        'auto_msg': 'Пришлось есть. Лучше бы не ел.',
    },
    {
        'id': 'theft', 'tier': 1, 'min_day': 2, 'max_day': 60, 'weight': 8,
        'text': 'Когда вернулся с прогулки, часть вещей пропала.',
        'auto_effects': {'mood': -15},
        'auto_msg': 'Пропали вещи. В зоне ничего твоего нет.',
        'steal_item': True,
    },
    {
        'id': 'new_fish', 'tier': 1, 'min_day': 5, 'max_day': 60, 'weight': 7,
        'text': 'Новый этап. Борзой сразу качает права: "Кто тут главный?"',
        'choices': [
            {'text': 'Ответить жёстко',
             'fight': True, 'difficulty': 40,
             'win_msg': 'Поставил на место. Все видели.',
             'win_effects': {'reputation': 12, 'health': -10},
             'lose_msg': 'Оказался крепче. Придётся отлежаться.',
             'lose_effects': {'health': -25, 'reputation': -5}},
            {'text': 'Промолчать',
             'effects': {'mood': -10, 'reputation': -5},
             'msg': 'Ты промолчал. Некоторые заметили.'},
        ],
    },
    {
        'id': 'letter_from_home', 'tier': 1, 'min_day': 7, 'max_day': None, 'weight': 6,
        'text': 'Принесли письмо. Мать пишет, что ждёт.',
        'auto_effects': {'mood': 20},
        'auto_msg': 'Читаешь дважды. Убираешь в карман — близко к сердцу.',
    },
    {
        'id': 'fight_debts', 'tier': 1, 'min_day': 5, 'max_day': 60, 'weight': 7,
        'text': 'Тёмные глаза: "Ты должен Лёхе три тушняка. Отдавай."',
        'choices': [
            {'text': 'Отдать долг (-24 монеты)',
             'effects': {'mood': -5},
             'pay_cash': 24,
             'msg': 'Рассчитался. Тему закрыли.'},
            {'text': 'Отказать — пускай попробует',
             'fight': True, 'difficulty': 45,
             'win_msg': 'Отбился. Но долг никуда не делся.',
             'win_effects': {'reputation': 8, 'health': -15},
             'lose_msg': 'Избили прямо в бараке.',
             'lose_effects': {'health': -30, 'reputation': -8, 'mood': -20}},
        ],
    },
    {
        'id': 'gambling_invite', 'tier': 1, 'min_day': 3, 'max_day': None, 'weight': 7,
        'text': 'В углу режутся в карты. "Садись, первоход."',
        'choices': [
            {'text': 'Сыграть (ставка 10 монет)',
             'gamble': True, 'bet': 10,
             'win_msg': 'Карта пошла! Поднял двадцатку.',
             'win_effects': {'mood': 20, 'reputation': 5, 'cash_rel': 20},
             'lose_msg': 'Потерял десятку.',
             'lose_effects': {'mood': -15}},
            {'text': 'Отказаться',
             'effects': {'mood': -3},
             'msg': 'Ушёл. Смеются вслед.'},
        ],
    },
    {
        'id': 'sanitar_work', 'tier': 1, 'min_day': 4, 'max_day': 40, 'weight': 6,
        'text': 'Дежурный предлагает убирать санчасть. Платят немного.',
        'choices': [
            {'text': 'Согласиться',
             'effects': {'guard_favor': 10, 'mood': -5},
             'cash_abs': 8,
             'msg': 'Отмыл всё. Получил восемь монет и кивок от вертухая.'},
            {'text': 'Отказаться',
             'effects': {'mood': 5},
             'msg': 'Своя работа западло.'},
        ],
    },
    {
        'id': 'avtoritet_offer', 'tier': 1, 'min_day': 15, 'max_day': 90,
        'weight': 8, 'req_rep_max': 64,
        'text': 'Авторитет: "Будешь на меня работать — защита и монеты."',
        'choices': [
            {'text': 'Согласиться',
             'effects': {'mood': 5, 'reputation': 5},
             'cash_abs': 15,
             'msg': 'Теперь у тебя есть крыша.'},
            {'text': 'Отказаться — сам себе хозяин',
             'effects': {'reputation': 8, 'mood': -5},
             'msg': '"Смотри," — говорит он и уходит.'},
        ],
    },
    {
        'id': 'found_contraband', 'tier': 1, 'min_day': 10, 'max_day': None, 'weight': 5,
        'text': 'В углу двора нашёл свёрток. Внутри — заточка и немного чая.',
        'choices': [
            {'text': 'Взять',
             'effects': {'mood': 10},
             'give_item': 'shiv',
             'risk': 0.15, 'risk_msg': 'Вертухай заметил. Шмон!',
             'risk_effects': {'guard_favor': -20, 'mood': -20},
             'msg': 'Припрятал. Никто не видел.'},
            {'text': 'Оставить',
             'effects': {'guard_favor': 5},
             'msg': 'Меньше проблем.'},
        ],
    },
    {
        'id': 'prison_riot', 'tier': 1, 'min_day': 30, 'max_day': None, 'weight': 4,
        'text': 'БУМ! В соседнем корпусе вспыхнул бунт. ОМОН входит в зону.',
        'choices': [
            {'text': 'Залечь',
             'effects': {'mood': -15, 'health': -5},
             'msg': 'Пересидел под шконкой. Живой.'},
            {'text': 'Воспользоваться хаосом',
             'effects': {'health': -20, 'reputation': 5},
             'cash_abs': 25,
             'risk': 0.30, 'risk_msg': 'ОМОН схватил тебя. Карцер.',
             'risk_effects': {'health': -20, 'mood': -30, 'guard_favor': -30},
             'msg': 'Нашёл кое-что брошенное.'},
        ],
    },
    {
        'id': 'snitch_opportunity', 'tier': 1, 'min_day': 14, 'max_day': None, 'weight': 6,
        'text': 'Кум вызывает тихо: "Поможешь — будут льготы."',
        'choices': [
            {'text': 'Помочь',
             'effects': {'guard_favor': 25, 'reputation': -20},
             'cash_abs': 20, 'snitch': True,
             'risk': 0.25, 'risk_msg': 'Кто-то всё узнал. Тебя называют крысой.',
             'risk_effects': {'reputation': -30, 'health': -20, 'mood': -25},
             'msg': 'Слил пару имён. Кум доволен. Совесть — нет.'},
            {'text': 'Отказаться',
             'effects': {'reputation': 10, 'mood': 10},
             'msg': '"Подумай ещё." Ты выходишь.'},
        ],
    },
    {
        'id': 'injury_accident', 'tier': 1, 'min_day': 8, 'max_day': None, 'weight': 6,
        'text': 'На производстве станок дёрнуло — рука в крови.',
        'auto_effects': {'health': -15},
        'auto_msg': 'Перевязали тряпкой. Болит, но работать заставили.',
        'add_injury': {'type': 'cut', 'severity': 2, 'days': 7},
    },
    {
        'id': 'cold_snap', 'tier': 1, 'min_day': 20, 'max_day': None, 'weight': 5,
        'text': 'Ударили морозы. В бараке почти не топят.',
        'auto_effects': {'health': -10, 'sleep': -15, 'mood': -10},
        'auto_msg': 'Спал в куртке. Утром еле встал.',
    },
    {
        'id': 'medic_visit', 'tier': 1, 'min_day': 10, 'max_day': None, 'weight': 5,
        'req_health_max': 60,
        'text': 'Тебя вызвали в санчасть. Фельдшер равнодушно: "На что жалуемся?"',
        'choices': [
            {'text': 'Попросить лечение',
             'effects': {'health': 20, 'guard_favor': -5},
             'msg': 'Дал таблеток. "Следующий."'},
            {'text': 'Отказаться — сам справлюсь',
             'effects': {'reputation': 3},
             'msg': 'Мужики кивнули уважительно.'},
        ],
    },
    {
        'id': 'card_debt', 'tier': 1, 'min_day': 10, 'max_day': None, 'weight': 5,
        'text': 'Проигрался в карты — должен двадцать монет.',
        'auto_effects': {'mood': -15},
        'auto_msg': 'Долг — это петля.',
        'add_debt': 20,
    },
    {
        'id': 'test_of_strength', 'tier': 1, 'min_day': 15, 'max_day': None, 'weight': 5,
        'text': 'Спортсмен: "Отожмись больше меня — уважу."',
        'choices': [
            {'text': 'Принять вызов',
             'strength_contest': True, 'difficulty': 55,
             'win_msg': 'Выжал больше. Уважение честное.',
             'win_effects': {'reputation': 12, 'strength': 5, 'mood': 15},
             'lose_msg': 'Проиграл по очкам.',
             'lose_effects': {'reputation': 3, 'mood': -5}},
            {'text': 'Уклониться',
             'effects': {'mood': -5},
             'msg': 'Пусть думают что хотят.'},
        ],
    },
    {
        'id': 'udo_chance', 'tier': 1, 'min_day': 60, 'max_day': None, 'weight': 5,
        'req_rep_min': 30, 'req_rep_max': 79,
        'text': '"Комиссия по УДО через месяц. Если поведение — могут выпустить."',
        'auto_effects': {'mood': 15},
        'auto_msg': 'Шанс есть. Надо не облажаться.',
        'udo_hint': True,
    },
    {
        'id': 'vorovskoy_test', 'tier': 1, 'min_day': 60, 'max_day': None, 'weight': 4,
        'req_rep_min': 50,
        'text': 'Тебя спрашивают прямо: "Как относишься к ментам?"',
        'choices': [
            {'text': '"Враги." — без колебаний',
             'effects': {'reputation': 15, 'guard_favor': -20},
             'msg': 'Старый уголовник кивает: "Правильно думаешь."'},
            {'text': 'Промолчать',
             'effects': {'reputation': 5},
             'msg': 'Тишина тоже ответ.'},
            {'text': '"По-разному бывает…"',
             'effects': {'reputation': -15, 'mood': -10},
             'msg': '"Мутный ты," — и уходит.'},
        ],
    },
    {
        'id': 'rival_gang', 'tier': 1, 'min_day': 70, 'max_day': None, 'weight': 5,
        'req_gang': True,
        'text': 'Конкурирующая группировка требует долю с твоих людей. "Или война."',
        'choices': [
            {'text': 'Заплатить дань',
             'effects': {'mood': -15, 'reputation': -10},
             'pay_cash': 30,
             'msg': 'Мир куплен. Но дорого.'},
            {'text': 'Воевать',
             'fight': True, 'difficulty': 80, 'gang_war': True,
             'win_msg': 'Отстояли территорию.',
             'win_effects': {'reputation': 20, 'health': -15},
             'lose_msg': 'Крепко потрепали.',
             'lose_effects': {'reputation': -5, 'health': -30}},
        ],
    },
    {
        'id': 'betrayal_in_gang', 'tier': 1, 'min_day': 60, 'max_day': None, 'weight': 4,
        'req_gang': True,
        'text': 'Сигнал изнутри: один из твоих водит дружбу с кумом.',
        'choices': [
            {'text': 'Разобраться лично',
             'effects': {'reputation': 15, 'health': -10},
             'remove_traitor': True,
             'msg': 'Крысу выгнали.'},
            {'text': 'Действовать через третьих',
             'effects': {'reputation': 5},
             'pay_cash': 10,
             'msg': 'Дело сделано чужими руками.'},
        ],
    },
    {
        'id': 'escape_hint', 'tier': 1, 'min_day': 90, 'max_day': None, 'weight': 3,
        'req_str_min': 65, 'req_rep_min': 40,
        'text': 'Старый зэк шепчет: "Вот слабое место в заборе. Один шанс."',
        'choices': [
            {'text': 'Изучить план',
             'effects': {'mood': 10},
             'unlock_escape': True,
             'msg': 'Запоминаешь каждую деталь.'},
            {'text': 'Отказаться',
             'effects': {'mood': -5},
             'msg': 'Может, оно и к лучшему.'},
        ],
    },
    {
        'id': 'phone_call_home', 'tier': 1, 'min_day': 10, 'max_day': None, 'weight': 7,
        'text': 'Официальный звонок домой. Слышишь голос матери.',
        'auto_effects': {'mood': 25},
        'auto_msg': '"Держись, сынок." Голос дрожит. Ты тоже.',
    },
    {
        'id': 'good_day', 'tier': 1, 'min_day': 5, 'max_day': None, 'weight': 8,
        'text': 'Странно, но сегодня всё шло нормально.',
        'auto_effects': {'mood': 15, 'hunger': 10},
        'auto_msg': 'Бывает и такое.',
    },
    {
        'id': 'tattoo_offer', 'tier': 1, 'min_day': 30, 'max_day': None, 'weight': 4,
        'req_rep_min': 35,
        'text': '"Набью татуировку по понятиям. Как надо."',
        'choices': [
            {'text': 'Согласиться (-15 монет)',
             'effects': {'mood': 15, 'reputation': 8},
             'pay_cash': 15, 'add_tattoo': True,
             'msg': 'Иголка в кожу. Рисунок навсегда.'},
            {'text': 'Отказаться',
             'effects': {},
             'msg': '"Потом, может."'},
        ],
    },
    {
        'id': 'gym_motivation', 'tier': 1, 'min_day': 10, 'max_day': None, 'weight': 5,
        'text': 'Спортсмен даёт совет как правильно тренироваться.',
        'auto_effects': {'strength': 5, 'mood': 10},
        'auto_msg': 'Новые знания. Завтра попробуешь.',
    },
    {
        'id': 'new_contraband', 'tier': 1, 'min_day': 20, 'max_day': None, 'weight': 4,
        'text': '"Есть телефон. Дорого, но своё."',
        'choices': [
            {'text': 'Купить (100 монет)',
             'pay_cash': 100, 'give_item': 'phone',
             'effects': {'reputation': 5},
             'msg': 'Телефон в кармане. Позвонил домой.'},
            {'text': 'Отказаться',
             'effects': {},
             'msg': 'Правильное решение.'},
        ],
    },
    # NEW TIER 1 EVENTS
    {
        'id': 'card_tournament', 'tier': 1, 'min_day': 20, 'max_day': None, 'weight': 4,
        'text': 'В бараке объявили турнир по картам. Ставки крупнее обычного.',
        'choices': [
            {'text': 'Участвовать (ставка 30 монет)',
             'gamble': True, 'bet': 30,
             'win_msg': 'Победил в финале! Все признали игрока.',
             'win_effects': {'reputation': 15, 'mood': 25, 'cash_rel': 90},
             'lose_msg': 'Продул всё. Тяжёлая ночь.',
             'lose_effects': {'mood': -25, 'reputation': -5}},
            {'text': 'Наблюдать',
             'effects': {'mood': 5},
             'msg': 'Запоминаешь повадки игроков.'},
        ],
    },
    {
        'id': 'hunger_strike', 'tier': 1, 'min_day': 30, 'max_day': None, 'weight': 3,
        'text': 'В соседней камере объявили голодовку. Зэки требуют улучшения условий.',
        'choices': [
            {'text': 'Поддержать голодовку',
             'effects': {'reputation': 15, 'guard_favor': -20, 'health': -10, 'hunger': -20},
             'msg': 'Солидарность. Но вертухаи тебя запомнили.'},
            {'text': 'Донести куму',
             'effects': {'guard_favor': 20, 'reputation': -20},
             'snitch': True,
             'msg': 'Кум доволен. Зэки заподозрят.'},
            {'text': 'Держаться в стороне',
             'effects': {'mood': -5},
             'msg': 'Не твоё дело.'},
        ],
    },
    {
        'id': 'etap', 'tier': 1, 'min_day': 30, 'max_day': None, 'weight': 3,
        'text': 'Этапируют в другой корпус. Всё начинается заново.',
        'auto_effects': {'reputation': -10, 'mood': -15},
        'auto_msg': 'Новые лица. Старые правила.',
    },
    {
        'id': 'amnesty_rumour', 'tier': 1, 'min_day': 60, 'max_day': None, 'weight': 4,
        'text': 'Слухи: готовят амнистию по определённым статьям. Народ взбудоражен.',
        'auto_effects': {'mood': 20},
        'auto_msg': 'Пока слухи. Но надежда — уже кое-что.',
    },
    {
        'id': 'vor_priehal', 'tier': 1, 'min_day': 50, 'max_day': None, 'weight': 3,
        'req_rep_min': 50,
        'text': 'В зону приехал Вор в законе. Проверяет порядок.',
        'choices': [
            {'text': 'Представиться, показать себя',
             'effects': {'reputation': 20, 'mood': 15},
             'msg': 'Вор кивнул. "Вижу человека."'},
            {'text': 'Держаться в тени',
             'effects': {'reputation': 5},
             'msg': 'Незаметность — тоже мудрость.'},
        ],
    },
    {
        'id': 'ponyatiya_check', 'tier': 1, 'min_day': 40, 'max_day': None, 'weight': 4,
        'req_rep_min': 40,
        'text': 'Старый уголовник проверяет тебя по понятиям. Несколько вопросов.',
        'choices': [
            {'text': 'Ответить правильно (по понятиям)',
             'strength_contest': True, 'difficulty': 45,
             'win_msg': '"Правильно думаешь. Мужик."',
             'win_effects': {'reputation': 20, 'mood': 15},
             'lose_msg': 'Замялся на вопросе. Заметили.',
             'lose_effects': {'reputation': -5, 'mood': -10}},
            {'text': 'Уклониться от разговора',
             'effects': {'reputation': -5},
             'msg': 'Трус или умный — не поняли.'},
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TIER 2 — РАЙОН
    # ══════════════════════════════════════════════════════════════════════════
    {
        'id': 't2_competitor_kiosk', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 8,
        'text': 'Конкурент открыл ларёк в двух шагах от твоего.',
        'choices': [
            {'text': 'Наехать — закрыть бизнес',
             'fight': True, 'difficulty': 50,
             'win_msg': 'Конкурент убрался. Точка твоя.',
             'win_effects': {'reputation': 10, 'heat': 5},
             'lose_msg': 'Не получилось. Конкурент укрепился.',
             'lose_effects': {'reputation': -10, 'cash_rel': -200}},
            {'text': 'Договориться — разделить рынок',
             'effects': {'mood': 5},
             'msg': 'Поделили районы. Мир без войны.'},
            {'text': 'Игнорировать',
             'effects': {'cash_rel': -100},
             'msg': 'Теряешь часть клиентов.'},
        ],
    },
    {
        'id': 't2_journalist', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 6,
        'text': 'Журналист из местной газеты нюхает вокруг твоих ларьков.',
        'choices': [
            {'text': 'Заплатить за молчание',
             'pay_cash': 500,
             'effects': {'heat': -5},
             'msg': 'Деньги решили проблему.'},
            {'text': 'Напугать',
             'fight': True, 'difficulty': 30,
             'win_msg': 'Убежал и забыл.',
             'win_effects': {'heat': -3},
             'lose_msg': 'Статья вышла. Жарко.',
             'lose_effects': {'heat': 20}},
            {'text': 'Ничего не делать',
             'effects': {'heat': 15},
             'msg': 'Статья вышла. Полиция заинтересовалась.'},
        ],
    },
    {
        'id': 't2_protection_demand', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 7,
        'text': 'ОПГ требует 20% с оборота твоих точек каждую неделю.',
        'choices': [
            {'text': 'Платить',
             'effects': {'cash_pct': -15, 'mood': -20},
             'msg': 'Платишь дань. Унизительно, но живёшь.'},
            {'text': 'Отказать — воевать',
             'fight': True, 'difficulty': 65, 'gang_war': True,
             'win_msg': 'Выстояли. Район теперь твой.',
             'win_effects': {'influence': 200, 'reputation': 25},
             'lose_msg': 'Потери. Придётся перестроиться.',
             'lose_effects': {'cash_rel': -1000, 'reputation': -15}},
        ],
    },
    {
        'id': 't2_police_check', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 8,
        'text': 'Участковый пришёл "проверить документы" на ларёк.',
        'choices': [
            {'text': 'Дать взятку (200 нал)',
             'pay_cash': 200,
             'effects': {'heat': -8, 'guard_favor': 5},
             'msg': 'Участковый ушёл довольный.'},
            {'text': 'Всё по закону — пусть проверяет',
             'effects': {'heat': 5, 'mood': -10},
             'msg': 'Придирался час. Ничего не нашёл, но запомнил.'},
        ],
    },
    {
        'id': 't2_new_crew', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Местные пацаны хотят работать на тебя. Смотрят с уважением.',
        'choices': [
            {'text': 'Взять в дело',
             'effects': {'influence': 50, 'heat': 3},
             'recruit_random': True,
             'msg': 'Пополнение в банду.'},
            {'text': 'Отказать — не время',
             'effects': {},
             'msg': 'Не сейчас.'},
        ],
    },
    {
        'id': 't2_turf_war', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 6,
        'text': 'Соседняя ОПГ захватила один из твоих районов пока ты отдыхал.',
        'choices': [
            {'text': 'Немедленно отбить',
             'fight': True, 'difficulty': 60, 'gang_war': True,
             'win_msg': 'Район отбит. Авторитет вырос.',
             'win_effects': {'reputation': 20, 'influence': 150},
             'lose_msg': 'Не смогли отбить. Потери.',
             'lose_effects': {'cash_rel': -500, 'reputation': -10}},
            {'text': 'Договориться',
             'pay_cash': 1000,
             'effects': {'mood': -15},
             'msg': 'Откупился. Сохранил лицо ценой монет.'},
        ],
    },
    {
        'id': 't2_good_contract', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Выгодный контракт на поставку — одноразовый, но жирный.',
        'auto_effects': {'mood': 15, 'influence': 100},
        'auto_msg': 'Разовая сделка принесла хорошие деньги.',
        'cash_abs': 500,
    },
    {
        'id': 't2_local_against', 'tier': 2, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Местные жители собрали подписи против твоих "заведений".',
        'choices': [
            {'text': 'Задобрить районный совет',
             'pay_cash': 300, 'effects': {'heat': -5, 'influence': 50},
             'msg': 'Проблема решена. Положительный образ.'},
            {'text': 'Игнорировать',
             'effects': {'heat': 10},
             'msg': 'Шум нарастает. Полиция начинает интересоваться.'},
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TIER 3 — ГОРОД
    # ══════════════════════════════════════════════════════════════════════════
    {
        'id': 't3_mayor_wants_cut', 'tier': 3, 'min_day': 0, 'max_day': None, 'weight': 7,
        'text': 'Мэр хочет долю с твоего казино. Намёки становятся прямыми.',
        'choices': [
            {'text': 'Платить (5 000/мес)',
             'effects': {'heat': -10, 'mood': -20},
             'pay_cash': 5000,
             'msg': 'Мэр доволен. Пока.'},
            {'text': 'Купить мэра полностью',
             'pay_cash': 50000,
             'effects': {'heat': -20, 'influence': 500},
             'msg': 'Мэр в твоём кармане. Город открыт.'},
            {'text': 'Отказать — создать врага',
             'effects': {'heat': 25, 'influence': -200},
             'msg': 'Мэр объявил войну твоему бизнесу.'},
        ],
    },
    {
        'id': 't3_newspaper_article', 'tier': 3, 'min_day': 0, 'max_day': None, 'weight': 6,
        'text': 'Известная газета опубликовала расследование о твоём бизнесе.',
        'choices': [
            {'text': 'Купить редактора',
             'pay_cash': 10000,
             'effects': {'heat': -15},
             'msg': 'Статью отозвали. Купил молчание.'},
            {'text': 'Угрожать журналисту',
             'fight': True, 'difficulty': 40,
             'win_msg': 'Журналист замолчал.',
             'win_effects': {'heat': -5},
             'lose_msg': 'Скандал усилился.',
             'lose_effects': {'heat': 30}},
        ],
    },
    {
        'id': 't3_partner_exit', 'tier': 3, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Партнёр по казино хочет выйти из бизнеса.',
        'choices': [
            {'text': 'Выкупить его долю (20 000)',
             'pay_cash': 20000,
             'effects': {'mood': 10, 'influence': 200},
             'msg': 'Казино полностью твоё.'},
            {'text': 'Отпустить и найти нового',
             'effects': {'cash_rel': -5000},
             'msg': 'Потерял доход на переходный период.'},
            {'text': 'Убедить остаться (силой)',
             'fight': True, 'difficulty': 45,
             'win_msg': 'Остался. Но смотрит искоса.',
             'win_effects': {'heat': 10},
             'lose_msg': 'Ушёл и понёс в полицию.',
             'lose_effects': {'heat': 25}},
        ],
    },
    {
        'id': 't3_casino_raid', 'tier': 3, 'min_day': 0, 'max_day': None, 'weight': 6,
        'text': 'Облава на казино. Люди в масках, мигалки.',
        'auto_effects': {'heat': 10, 'mood': -20},
        'auto_msg': 'Казино закрыто на неделю. Потери в доходе.',
        'raid_business_tier': 3,
    },
    {
        'id': 't3_politician_offer', 'tier': 3, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Депутат городского совета предлагает союз.',
        'choices': [
            {'text': 'Принять союз',
             'pay_cash': 5000,
             'effects': {'heat': -10, 'influence': 500},
             'msg': 'Политик в союзниках. Руки стали длиннее.'},
            {'text': 'Отказать',
             'effects': {'heat': 5},
             'msg': 'Депутат обиделся. Может стать проблемой.'},
        ],
    },
    {
        'id': 't3_rival_opg', 'tier': 3, 'min_day': 0, 'max_day': None, 'weight': 6,
        'text': 'Конкурирующая ОПГ уничтожила один из твоих бизнесов.',
        'auto_effects': {'heat': 15, 'mood': -25},
        'auto_msg': 'Потеря бизнеса. Нужна ответная мера.',
        'destroy_random_business': True,
    },
    {
        'id': 't3_buy_police', 'tier': 3, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Начальник полиции намекает, что 50 000 решили бы многие вопросы.',
        'choices': [
            {'text': 'Заплатить',
             'pay_cash': 50000,
             'effects': {'heat': -20, 'influence': 300},
             'msg': 'Полиция смотрит в другую сторону.'},
            {'text': 'Отказать',
             'effects': {'heat': 10},
             'msg': 'Начальник злой. Усиливает патрули.'},
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TIER 4 — ОБЛАСТЬ
    # ══════════════════════════════════════════════════════════════════════════
    {
        'id': 't4_governor_change', 'tier': 4, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Сменился губернатор. Все прежние договорённости под вопросом.',
        'choices': [
            {'text': 'Перекупить нового',
             'pay_cash': 500000,
             'effects': {'heat': -15, 'influence': 2000},
             'msg': 'Новый губернатор понял правила.'},
            {'text': 'Переждать и разобраться',
             'effects': {'cash_rel': -50000, 'heat': 15},
             'msg': 'Месяц неразберихи. Потери.'},
        ],
    },
    {
        'id': 't4_fsb_investigation', 'tier': 4, 'min_day': 0, 'max_day': None, 'weight': 4,
        'text': 'ФСБ начало разработку твоей структуры.',
        'choices': [
            {'text': 'Перекупить куратора дела',
             'pay_cash': 1000000,
             'effects': {'heat': -25},
             'msg': 'Дело закрыто. Дорого, но необходимо.'},
            {'text': 'Временно свернуть активность',
             'effects': {'cash_rel': -200000, 'heat': -10},
             'msg': 'Залёг на дно. Потери, но безопасно.'},
            {'text': 'Игнорировать',
             'effects': {'heat': 20, 'paranoia': 15},
             'msg': 'ФСБ ведёт дело дальше. Становится горячо.'},
        ],
    },
    {
        'id': 't4_factory_upgrade', 'tier': 4, 'min_day': 0, 'max_day': None, 'weight': 4,
        'text': 'Завод требует модернизации. Старое оборудование ломается.',
        'choices': [
            {'text': 'Вложить в модернизацию (100 000)',
             'pay_cash': 100000,
             'effects': {'mood': 10, 'influence': 500},
             'msg': 'Завод обновлён. Эффективность выросла.'},
            {'text': 'Заставить работать как есть',
             'effects': {'cash_rel': -20000, 'mood': -10},
             'msg': 'Постоянные поломки съедают прибыль.'},
        ],
    },
    {
        'id': 't4_raider_attack', 'tier': 4, 'min_day': 0, 'max_day': None, 'weight': 5,
        'text': 'Рейдерский захват: конкурент пытается поглотить твою компанию.',
        'choices': [
            {'text': 'Защититься через суд (50 000)',
             'pay_cash': 50000,
             'effects': {'heat': -5, 'influence': 300},
             'msg': 'Суд на твоей стороне. Рейд отбит.'},
            {'text': 'Силовой ответ',
             'fight': True, 'difficulty': 75,
             'win_msg': 'Рейдеры отступили.',
             'win_effects': {'influence': 500, 'reputation': 20},
             'lose_msg': 'Потерял часть активов.',
             'lose_effects': {'total_assets': -300000}},
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TIER 5 — СТРАНА
    # ══════════════════════════════════════════════════════════════════════════
    {
        'id': 't5_sanctions', 'tier': 5, 'min_day': 0, 'max_day': None, 'weight': 4,
        'text': 'Международные санкции ударили по твоим офшорным счетам.',
        'choices': [
            {'text': 'Перевести активы в крипту',
             'pay_cash': 2000000,
             'effects': {'cash_pct': -10, 'paranoia': 10},
             'msg': 'Активы спасены, но стало сложнее.'},
            {'text': 'Лоббировать отмену через депутатов',
             'pay_cash': 5000000,
             'effects': {'heat': -10, 'influence': 2000},
             'msg': 'Санкции ослаблены. Дорого, но работает.'},
        ],
    },
    {
        'id': 't5_assassination_attempt', 'tier': 5, 'min_day': 0, 'max_day': None, 'weight': 4,
        'text': 'Конкурент нанял киллера. Твоя охрана докладывает.',
        'choices': [
            {'text': 'Упредить — убрать конкурента первым',
             'fight': True, 'difficulty': 85,
             'win_msg': 'Угроза ликвидирована.',
             'win_effects': {'influence': 1000, 'heat': 20},
             'lose_msg': 'Покушение почти удалось. Здоровье на пределе.',
             'lose_effects': {'health': -40, 'paranoia': 20}},
            {'text': 'Уйти в подполье (1 000 000)',
             'pay_cash': 1000000,
             'effects': {'heat': -15, 'mood': -20},
             'msg': 'Переждал. Конкурент думает ты мёртв.'},
        ],
    },
    {
        'id': 't5_elections', 'tier': 5, 'min_day': 0, 'max_day': None, 'weight': 3,
        'text': 'Президентские выборы. Твой кандидат может победить с деньгами.',
        'choices': [
            {'text': 'Финансировать кандидата (1 000 000)',
             'pay_cash': 1000000,
             'effects': {'influence': 5000, 'heat': -20},
             'msg': 'Кандидат победил. Страна открыта.'},
            {'text': 'Поддержать обоих — на всякий случай',
             'pay_cash': 2000000,
             'effects': {'influence': 8000, 'heat': -30},
             'msg': 'Победитель в любом случае твой человек.'},
            {'text': 'Не вмешиваться',
             'effects': {'heat': 10},
             'msg': 'Новый президент — неизвестная переменная.'},
        ],
    },
    {
        'id': 't5_media_leak', 'tier': 5, 'min_day': 0, 'max_day': None, 'weight': 3,
        'text': 'Расследование журналиста-расследователя: документы об офшорах в прессе.',
        'choices': [
            {'text': 'Заткнуть через медиаимперию',
             'pay_cash': 3000000,
             'effects': {'heat': -20},
             'msg': 'Материал уничтожен. Журналист уволен.'},
            {'text': 'Публично опровергнуть',
             'effects': {'heat': 10, 'paranoia': 10},
             'msg': 'Скандал немного утих, но сомнения остались.'},
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TIER 6 — МИР
    # ══════════════════════════════════════════════════════════════════════════
    {
        'id': 't6_interpol', 'tier': 6, 'min_day': 0, 'max_day': None, 'weight': 4,
        'text': 'Интерпол объявил тебя в международный розыск.',
        'choices': [
            {'text': 'Подкупить куратора Интерпола',
             'pay_cash': 50000000,
             'effects': {'heat': -30, 'paranoia': 20},
             'msg': 'Дело закрыто. Дорого, но эффективно.'},
            {'text': 'Переехать на личный остров',
             'effects': {'heat': -20, 'mood': -15, 'influence': 1000},
             'msg': 'Недоступен для большинства юрисдикций.'},
        ],
    },
    {
        'id': 't6_revolution', 'tier': 6, 'min_day': 0, 'max_day': None, 'weight': 3,
        'text': 'Революция в подконтрольной стране. Новое правительство против тебя.',
        'choices': [
            {'text': 'Подавить восстание (ЧВК)',
             'pay_cash': 100000000,
             'effects': {'influence': 5000, 'heat': 15},
             'msg': 'Порядок восстановлен. Страна под контролем.'},
            {'text': 'Эвакуировать активы и сдать страну',
             'effects': {'influence': -5000, 'cash_pct': -20},
             'msg': 'Потеря территории, но активы спасены.'},
        ],
    },
    {
        'id': 't6_cartel_war', 'tier': 6, 'min_day': 0, 'max_day': None, 'weight': 4,
        'text': 'Конкурирующий картель объявил тебе войну за маршруты.',
        'choices': [
            {'text': 'Полная война (ЧВК)',
             'fight': True, 'difficulty': 90, 'gang_war': True,
             'win_msg': 'Картель уничтожен. Маршруты твои.',
             'win_effects': {'influence': 10000},
             'lose_msg': 'Серьёзные потери.',
             'lose_effects': {'cash_pct': -30, 'reputation': -20}},
            {'text': 'Разделить сферы влияния',
             'pay_cash': 500000000,
             'effects': {'influence': 3000},
             'msg': 'Мир куплен. Дорого.'},
        ],
    },
    {
        'id': 't6_cia_operation', 'tier': 6, 'min_day': 0, 'max_day': None, 'weight': 3,
        'text': 'ЦРУ начало операцию против твоей инфраструктуры.',
        'choices': [
            {'text': 'Запустить дезинформацию',
             'pay_cash': 20000000,
             'effects': {'heat': -15, 'paranoia': 20},
             'msg': 'Операция сорвана. На время.'},
            {'text': 'Привлечь союзную спецслужбу',
             'pay_cash': 100000000,
             'effects': {'heat': -30, 'influence': 5000},
             'msg': 'Противостояние спецслужб. Ты пока жив.'},
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PERSONAL / UNIVERSAL (any tier)
    # ══════════════════════════════════════════════════════════════════════════
    {
        'id': 'personal_illness', 'tier': 0, 'min_day': 10, 'max_day': None, 'weight': 4,
        'text': 'Резко заболел. Температура, слабость, всё тело ломит.',
        'choices': [
            {'text': 'Лечиться нормально',
             'pay_cash_pct': 0.005,
             'effects': {'health': 15, 'mood': -10},
             'msg': 'Вылечился. Дорого, но помогло.'},
            {'text': 'Переболеть на ногах',
             'effects': {'health': -20, 'strength': -5, 'mood': -15},
             'msg': 'Мучился неделю. Выжил, но ослаб.'},
        ],
    },
    {
        'id': 'personal_good_news', 'tier': 0, 'min_day': 5, 'max_day': None, 'weight': 6,
        'text': 'Хорошие новости с воли. Что-то хорошее случилось.',
        'auto_effects': {'mood': 20, 'paranoia': -5},
        'auto_msg': 'Настроение поднялось. Есть ради чего.',
    },
    {
        'id': 'personal_old_friend', 'tier': 0, 'min_day': 20, 'max_day': None, 'weight': 5,
        'text': 'Объявился старый друг из прошлой жизни. Хочет работать вместе.',
        'choices': [
            {'text': 'Принять в команду',
             'effects': {'mood': 15, 'reputation': 5},
             'recruit_random': True,
             'msg': 'Старый друг — проверенный человек.'},
            {'text': 'Отказать — слишком опасно',
             'effects': {'mood': -10},
             'msg': 'Он понял. Исчез.'},
        ],
    },
    {
        'id': 'personal_rat_alert', 'tier': 0, 'min_day': 30, 'max_day': None, 'weight': 4,
        'req_gang': True,
        'text': 'Кто-то из твоих людей сливает информацию властям.',
        'choices': [
            {'text': 'Найти и наказать (проверка)',
             'strength_contest': True, 'difficulty': 50,
             'win_msg': 'Нашёл крысу. Выгнал с позором.',
             'win_effects': {'heat': -10, 'reputation': 10},
             'lose_msg': 'Не смог определить кто. Паранойя растёт.',
             'lose_effects': {'paranoia': 15, 'heat': 5}},
            {'text': 'Кормить дезинформацией',
             'effects': {'paranoia': 5, 'heat': -8},
             'msg': 'Пускай несёт ложь. Умная тактика.'},
        ],
    },
    {
        'id': 'personal_addiction_crisis', 'tier': 0, 'min_day': 1, 'max_day': None, 'weight': 0,
        'req_withdrawal': True,
        'text': 'Ломка. Тело требует своё. Трясёт, пот градом.',
        'auto_effects': {'health': -15, 'mood': -25, 'strength': -10},
        'auto_msg': 'Ломка бьёт без пощады.',
    },
    {
        'id': 'personal_cooperation_offer', 'tier': 0, 'min_day': 20, 'max_day': None, 'weight': 4,
        'text': 'Неизвестный авторитет предлагает совместный бизнес.',
        'choices': [
            {'text': 'Согласиться',
             'effects': {'influence': 200, 'paranoia': 10},
             'msg': 'Новый союз. Посмотрим на что он способен.'},
            {'text': 'Проверить сначала',
             'effects': {'paranoia': -5},
             'msg': 'Осторожность не помешает.'},
            {'text': 'Отказать',
             'effects': {'mood': -5},
             'msg': 'Возможность упущена. Или угроза предотвращена.'},
        ],
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _matches(event, state):
    tier = state.get('tier', 1)
    ev_tier = event.get('tier', 0)
    if ev_tier != 0 and ev_tier != tier:
        return False

    day = state.get('days_survived', 0)
    if day < (event.get('min_day') or 0):
        return False
    if event.get('max_day') is not None and day > event['max_day']:
        return False

    if event.get('req_gang') and not state.get('gang_members'):
        return False
    if event.get('req_rep_min') and state.get('reputation', 0) < event['req_rep_min']:
        return False
    if event.get('req_rep_max') is not None and state.get('reputation', 0) > event['req_rep_max']:
        return False
    if event.get('req_str_min') and state.get('strength', 0) < event['req_str_min']:
        return False
    if event.get('req_health_max') and state.get('health', 100) > event['req_health_max']:
        return False
    if event.get('req_withdrawal'):
        cig_w = (state.get('addiction_cigarettes', 0) > 30
                 and not state.get('inventory', {}).get('papirosa')
                 and not state.get('inventory', {}).get('prima'))
        alc_w = (state.get('addiction_alcohol', 0) > 40
                 and not state.get('inventory', {}).get('vodka'))
        if not (cig_w or alc_w):
            return False
    return True


def pick_event(state):
    pool = []
    for ev in ALL_EVENTS:
        if not _matches(ev, state):
            continue
        w = ev.get('weight', 5)
        if w <= 0:
            continue
        pool.extend([ev] * w)
    return random.choice(pool) if pool else None


def apply_auto_event(state, event):
    msgs = [('event', event.get('text', ''))]
    am = event.get('auto_msg', '')
    if am:
        msgs.append(('result', am))

    for stat, val in event.get('auto_effects', {}).items():
        _apply_stat(state, stat, val)

    cash_abs = event.get('cash_abs', 0)
    if cash_abs:
        state['cash'] = state.get('cash', 0) + cash_abs
        if cash_abs > 0:
            state['money_earned'] = state.get('money_earned', 0) + cash_abs

    if event.get('steal_item'):
        inv = state.get('inventory', {})
        keys = [k for k, v in inv.items() if v > 0]
        if keys:
            stolen = random.choice(keys)
            inv[stolen] -= 1
            if inv[stolen] <= 0:
                del inv[stolen]

    if event.get('add_debt'):
        state['debt'] = state.get('debt', 0) + event['add_debt']

    if event.get('add_injury'):
        state.setdefault('injuries', []).append(dict(event['add_injury']))

    if event.get('contraband_risk'):
        has_contra = (state.get('has_shiv') or state.get('has_phone') or
                      state.get('inventory', {}).get('tea_set', 0) > 0)
        if has_contra and random.random() < 0.4:
            _confiscate(state)
            msgs.append(('danger', 'Нашли контрабанду! Конфисковали.'))

    if event.get('udo_hint'):
        state['udo_hinted'] = True

    if event.get('raid_business_tier'):
        _raid_random_business(state, event['raid_business_tier'])

    if event.get('destroy_random_business'):
        _destroy_random_business(state)

    return msgs


def resolve_choice(state, event, choice_idx):
    choices = event.get('choices', [])
    if choice_idx >= len(choices):
        return [('result', 'Неверный выбор')]
    c = choices[choice_idx]
    msgs = [('event', event.get('text', ''))]

    # Direct stat effects
    for stat, val in c.get('effects', {}).items():
        _apply_stat(state, stat, val)

    # Cash changes
    if 'cash_abs' in c:
        amt = c['cash_abs']
        state['cash'] = max(0, state.get('cash', 0) + amt)
        if amt > 0:
            state['money_earned'] = state.get('money_earned', 0) + amt

    if 'cash_rel' in c:
        amt = c['cash_rel']
        state['cash'] = max(0, state.get('cash', 0) + amt)
        if amt > 0:
            state['money_earned'] = state.get('money_earned', 0) + amt

    if 'cash_pct' in c:
        amt = int(state.get('cash', 0) * abs(c['cash_pct']))
        if c['cash_pct'] < 0:
            state['cash'] = max(0, state.get('cash', 0) - amt)
        else:
            state['cash'] = state.get('cash', 0) + amt

    if 'pay_cash' in c:
        amt = c['pay_cash']
        if state.get('cash', 0) >= amt:
            state['cash'] -= amt
        else:
            msgs.append(('danger', f'Недостаточно денег! Нужно {amt:,}'.replace(',', ' ')))

    # Fight
    if c.get('fight'):
        won = _resolve_fight(state, c)
        eff = c.get('win_effects' if won else 'lose_effects', {})
        for stat, val in eff.items():
            _apply_stat(state, stat, val)
        msgs.append(('win' if won else 'lose',
                     c.get('win_msg' if won else 'lose_msg', '')))
        if c.get('gang_war') and not won:
            _gang_lose_member(state, msgs)

    # Strength contest
    elif c.get('strength_contest'):
        score = state.get('strength', 40) + state.get('muscle_mass', 0) // 2
        won = (score + random.randint(1, 20)) >= c.get('difficulty', 50)
        eff = c.get('win_effects' if won else 'lose_effects', {})
        for stat, val in eff.items():
            _apply_stat(state, stat, val)
        msgs.append(('win' if won else 'lose',
                     c.get('win_msg' if won else 'lose_msg', '')))

    # Gamble
    elif c.get('gamble'):
        bet = c.get('bet', 10)
        if state.get('cash', 0) < bet:
            msgs.append(('result', 'Нет денег для ставки.'))
        else:
            state['cash'] -= bet
            if random.random() > 0.48:
                winnings = bet * 2
                state['cash'] += winnings
                state['money_earned'] = state.get('money_earned', 0) + winnings
                for stat, val in c.get('win_effects', {}).items():
                    _apply_stat(state, stat, val)
                msgs.append(('win', c.get('win_msg', f'Выиграл {winnings}!')))
            else:
                for stat, val in c.get('lose_effects', {}).items():
                    _apply_stat(state, stat, val)
                msgs.append(('lose', c.get('lose_msg', f'Потерял {bet}.')))

    # Give item
    if c.get('give_item'):
        item_id = c['give_item']
        if c.get('risk') and random.random() < c['risk']:
            for stat, val in c.get('risk_effects', {}).items():
                _apply_stat(state, stat, val)
            msgs.append(('danger', c.get('risk_msg', 'Попался!')))
        else:
            state.setdefault('inventory', {})[item_id] = \
                state['inventory'].get(item_id, 0) + 1
            if item_id == 'shiv':
                state['has_shiv'] = True
            if item_id == 'phone':
                state['has_phone'] = True

    if c.get('snitch'):
        state['times_snitched'] = state.get('times_snitched', 0) + 1
        if c.get('risk') and random.random() < c['risk']:
            for stat, val in c.get('risk_effects', {}).items():
                _apply_stat(state, stat, val)
            msgs.append(('danger', c.get('risk_msg', 'Раскрыт!')))

    if c.get('unlock_escape'):
        state['escape_route_known'] = True

    if c.get('add_tattoo'):
        state.setdefault('tattoos', []).append('arm_tattoo')

    if c.get('remove_traitor'):
        _remove_least_loyal(state)

    if c.get('recruit_random'):
        from gang import recruit_member
        ok, rm = recruit_member(state)
        if ok:
            msgs.append(('result', rm))

    # Regular msg
    msg_text = c.get('msg', '')
    if msg_text and not any(k in c for k in ('fight', 'gamble', 'strength_contest')):
        msgs.append(('result', msg_text))
    elif msg_text:
        msgs.append(('result', msg_text))

    return msgs


# ── Internal helpers ──────────────────────────────────────────────────────────

def _apply_stat(state, stat, val):
    if stat in ('cash', 'total_assets', 'influence', 'money_earned'):
        state[stat] = max(0, state.get(stat, 0) + val)
    elif stat == 'heat':
        state['heat'] = max(0, min(100, state.get('heat', 0) + val))
    elif stat == 'cash_pct':
        amt = int(state.get('cash', 0) * abs(val))
        state['cash'] = max(0, state.get('cash', 0) + (amt if val > 0 else -amt))
    elif stat in state:
        state[stat] = max(0, min(100, state[stat] + val))


def _resolve_fight(state, choice):
    from gang import gang_fight_bonus
    difficulty = choice.get('difficulty', 50)
    roll = (state.get('strength', 40)
            + random.randint(1, 20)
            + state.get('gym_visits', 0) // 5
            + gang_fight_bonus(state)
            + (15 if state.get('has_shiv') else 0))
    enemy = difficulty + random.randint(1, 20)
    won = roll >= enemy
    state['total_fights'] = state.get('total_fights', 0) + 1
    if won:
        state['fights_won'] = state.get('fights_won', 0) + 1
    else:
        state['fights_lost'] = state.get('fights_lost', 0) + 1
        state.setdefault('injuries', []).append({'type': 'bruise', 'severity': 2, 'days': 5})
    return won


def _confiscate(state):
    if state.get('has_shiv'):
        state['has_shiv'] = False
        state.get('inventory', {}).pop('shiv', None)
    if state.get('has_phone'):
        state['has_phone'] = False
        state.get('inventory', {}).pop('phone', None)


def _gang_lose_member(state, msgs):
    gang = state.get('gang_members', [])
    if gang:
        lost = gang.pop(random.randrange(len(gang)))
        msgs.append(('danger', f'{lost["name"]} выбыл из строя.'))


def _remove_least_loyal(state):
    gang = state.get('gang_members', [])
    if gang:
        traitor = min(gang, key=lambda m: m['loyalty'])
        gang.remove(traitor)


def _raid_random_business(state, tier):
    matching = [b for b in state.get('businesses', []) if b.get('tier', 1) <= tier]
    if matching:
        b = random.choice(matching)
        b['is_raided'] = True
        b['raid_days_left'] = random.randint(3, 7)


def _destroy_random_business(state):
    biz = state.get('businesses', [])
    if biz:
        lost = random.choice(biz)
        biz.remove(lost)
        state.setdefault('event_log', []).append(
            ('danger', f"🔥 {lost['name']} уничтожен конкурентами!")
        )
