import os


CLIENT_ID = '3832701'#os.getenv('CLIENT_ID', '')
CLIENT_SECRET = '34BMt7NI'#os.getenv('CLIENT_SECRET', '')


# delivery types

DELIVERY_TYPE_POLAND_POST = 'poland_post'
DELIVERY_TYPE_POLAND_CDEK = 'poland_cdek'
DELIVERY_TYPE_RUSSIA_POST = 'russian_post'
DELIVERY_TYPE_RUSSIA_SDEK = 'russian_cdek'
DELIVERY_TYPE_POST = 'post'
DELIVERY_TYPE_CDEK = 'cdek'
DELIVERY_TYPE_CARGO_WITH_DOCS = 'cargo_with_docs'
DELIVERY_TYPE_CARGO_WITHOUT_DOCS = 'cargo_without_docs'
DELIVERY_TYPE_CARGO_FIVE_KG = 'Five_kg'

DELIVERY_TYPES = {
    DELIVERY_TYPE_POLAND_POST: {
        'title': 'Почта Польши',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_POLAND_CDEK: {
        'title': 'СДЭК Польши',
        'need_passport': True,
        'class': ''
    },
    DELIVERY_TYPE_RUSSIA_POST: {
        'title': 'Почта России',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_RUSSIA_SDEK: {
        'title': 'СДЭК России',
        'need_passport': True,
        'class': ''
    },
    DELIVERY_TYPE_CARGO_WITH_DOCS: {
        'title': 'КАРГО (с документами)',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_CARGO_WITHOUT_DOCS: {
        'title': 'КАРГО (без доккументов)',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_CDEK: {
        'title': 'СДЭК',
        'need_passport': True,
        'class': ''
    },
    DELIVERY_TYPE_POST: {
        'title': 'Почта',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_CARGO_FIVE_KG: {
        'title': 'Больше пяти кг.',
        'need_passport': False,
        'class': ''
    },
}

CHOICE_DELIVERY_TYPES = [(k, v['title']) for k, v in DELIVERY_TYPES.items()]

"""DELIVERY_TYPE_POLAND_POST = 'poland_post'
DELIVERY_TYPE_POLAND_CDEK = 'poland_cdek'
DELIVERY_TYPE_RUSSIA_POST = 'russian_post'
DELIVERY_TYPE_RUSSIA_SDEK = 'russian_cdek'
DELIVERY_TYPE_POST = 'post'
DELIVERY_TYPE_CDEK = 'cdek'
DELIVERY_TYPE_CARGO_WITH_DOCS = 'cargo_with_docs'
DELIVERY_TYPE_CARGO_WITHOUT_DOCS = 'cargo_without_docs'
DELIVERY_TYPE_CARGO_FIVE_KG = '5_kg'

DELIVERY_TYPES = {
    DELIVERY_TYPE_CARGO_WITH_DOCS: {
        'title': 'КАРГО (с документами)',
    },
    DELIVERY_TYPE_CARGO_WITHOUT_DOCS: {
        'title': 'КАРГО (без доккументов)',
    },
    DELIVERY_TYPE_CARGO_FIVE_KG: {
        'title': 'Больше 5 кг.',
    },
    DELIVERY_TYPE_CDEK: {
        'title': 'СДЭК',
        'need_passport': True,
        'class': ''
    },
    DELIVERY_TYPE_POST: {
        'title': 'Почта',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_POLAND_POST: {
        'title': 'Почта Польши',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_POLAND_CDEK: {
        'title': 'СДЭК Польши',
        'need_passport': True,
        'class': ''
    },
    DELIVERY_TYPE_RUSSIA_POST: {
        'title': 'Почта России',
        'need_passport': False,
        'class': ''
    },
    DELIVERY_TYPE_RUSSIA_SDEK: {
        'title': 'СДЭК России',
        'need_passport': True,
        'class': ''
    },
    }

CHOICE_DELIVERY_TYPES = [(k, v['title']) for k, v in DELIVERY_TYPES.items()]"""
# payment types

PAYMENT_TYPE_ONLINE = 'online'
PAYMENT_TYPE_BALANCE = 'balance'

PAYMENT_TYPES = {
    PAYMENT_TYPE_ONLINE: {
        'title': 'Онлайн',
        'class': ''
    },
    PAYMENT_TYPE_BALANCE: {
        'title': 'Списание с баланса',
        'class': ''
    },
}

CHOICE_PAYMENT_TYPES = [(k, v['title']) for k, v in PAYMENT_TYPES.items()]


# order status types

'''
0 Заказ не оформлен
1 Ожидается оплата
2 Принят в работу
3 Заказ выкуплен
4 Упаковка заказа
5 Ожидается оплата за доставку
6 Доставка оплачена
7 Заказ отправлен
8 Закрыт
9 Отмена заказа
10 Возврат
'''
ORDER_STATUS_UNFORMED = 'unformed'  # 0 Заказ не оформлен
ORDER_STATUS_PAYMENT_WAITING = 'payment_waiting'  # 1 Ожидается оплата
ORDER_STATUS_IN_PROCESS = 'in_process'  # 2 Принят в работу
ORDER_STATUS_REDEEMED = 'redeemed'  # 3 Заказ выкуплен
ORDER_STATUS_PACKAGING = 'packaging'  # 4 Упаковка заказа
ORDER_STATUS_DELIVERY_PAYMENT_WAITING = 'delivery_payment_waiting'  # 5 Ожидается оплата за доставку
ORDER_STATUS_DELIVERY_PAID = 'delivery_paid'  # 6 Доставка оплачена
ORDER_STATUS_SENDED = 'sended'  # 7 Заказ отправлен
ORDER_STATUS_CLOSED = 'closed'  # 8 Закрыт
ORDER_STATUS_CANCELED = 'canceled'  # 9 Отмена заказа
ORDER_STATUS_RETURN = 'return'  # 10 Возврат

ORDER_STATUSES = {
    ORDER_STATUS_UNFORMED: {
        'title': 'Заказ не оформлен',
        'available_statuses': [],
    },
    ORDER_STATUS_PAYMENT_WAITING: {
        'title': 'Ожидается оплата',
        'available_statuses': [],
    },
    ORDER_STATUS_IN_PROCESS: {
        'title': 'Принят в работу',
        'available_statuses': [],
    },
    ORDER_STATUS_REDEEMED: {
        'title': 'Заказ выкуплен',
        'available_statuses': [],
    },
    ORDER_STATUS_PACKAGING: {
        'title': 'Упаковка заказа',
        'available_statuses': [],
    },
    ORDER_STATUS_DELIVERY_PAYMENT_WAITING: {
        'title': 'Ожидается оплата за доставку',
        'available_statuses': [],
    },
    ORDER_STATUS_DELIVERY_PAID: {
        'title': 'Доставка оплачена',
        'available_statuses': [],
    },
    ORDER_STATUS_SENDED: {
        'title': 'Заказ отправлен',
        'available_statuses': [],
    },
    ORDER_STATUS_CLOSED: {
        'title': 'Закрыт',
        'available_statuses': [],
    },
    ORDER_STATUS_CANCELED: {
        'title': 'Отмена заказа',
        'available_statuses': [],
    },
    ORDER_STATUS_RETURN: {
        'title': 'Возврат',
        'available_statuses': [],
    },
}
CHOICE_ORDER_STATUSES = [(k, v['title']) for k, v in ORDER_STATUSES.items()]


# order item status types

'''
1 Ожидается оплата
2 Товар оплачен
3 Товар заказан
4 Товар выкуплен
5 Товар на упаковке
6 Товар отправлен
7 Замена товара
8 Отмена товара
9 В сборе
'''
ORDER_ITEM_STATUS_PAYMENT_WAITING = 'payment_waiting'  # 1 Ожидается оплата
ORDER_ITEM_STATUS_PAID = 'paid'  # 2 Товар оплачен
ORDER_ITEM_STATUS_ORDERED = 'ordered'  # 3 Товар заказан
ORDER_ITEM_STATUS_REDEEMED = 'redeemed'  # 4 Товар выкуплен
ORDER_ITEM_STATUS_PACKAGING = 'packaging'  # 5 Товар на упаковке
ORDER_ITEM_STATUS_SENDED = 'sended'  # 6 Товар отправлен
ORDER_ITEM_STATUS_REPLACEMENT = 'replacement'  # 7 Замена товара
ORDER_ITEM_STATUS_CANCELED = 'canceled'  # 8 Отмена товара
ORDER_ITEM_STATUS_COLLECTION = 'collection' # В сборе

ORDER_ITEM_STATUSES = {
    ORDER_ITEM_STATUS_PAYMENT_WAITING: {
        'title': 'Ожидается оплата',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_PAID: {
        'title': 'Товар оплачен',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_ORDERED: {
        'title': 'Товар заказан',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_REDEEMED: {
        'title': 'Товар выкуплен',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_PACKAGING: {
        'title': 'Товар на упаковке',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_SENDED: {
        'title': 'Товар отправлен',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_REPLACEMENT: {
        'title': 'Замена товара',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_CANCELED: {
        'title': 'Отмена товара',
        'available_statuses': [],
    },
    ORDER_ITEM_STATUS_COLLECTION: {
        'title': 'В сборе',
        'available_statuses': [],
    },
}
CHOICE_ORDER_ITEM_STATUSES = [(k, v['title']) for k, v in ORDER_ITEM_STATUSES.items()]
