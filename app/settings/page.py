PAGE_TYPE_DEFAULT = 0
PAGE_TYPE_HOME = 1
PAGE_TYPE_INFO = 2
PAGE_TYPE_CATEGORY = 3
PAGE_TYPE_PRODUCT = 4
PAGE_TYPE_CATALOG = 5
PAGE_TYPE_AUTH = 6
PAGE_TYPE_REGISTRATION = 7
PAGE_TYPE_ACCOUNT = 8
PAGE_TYPE_CART = 9
PAGE_TYPE_RESET_PASS = 10
PAGE_TYPE_CHECKOUT = 11
PAGE_TYPE_ORDER_HISTORY = 12
PAGE_TYPE_WISHLIST = 13
PAGE_TYPE_COMPARSION = 14
PAGE_TYPE_SEARCH = 15
PAGE_TYPE_INFO_PAYMENT = 16
PAGE_TYPE_INFO_DELIVERY = 17
PAGE_TYPE_INFO_EXCHANGE = 18
PAGE_TYPE_INFO_JURIDICAL = 19
PAGE_TYPE_INFO_CONTACTS = 20
PAGE_TYPE_INFO_HOW_TO = 21
PAGE_TYPE_INFO_REVIEWS = 22
PAGE_TYPE_ABOUT = 23
PAGE_TYPE_LIVE_PHOTOS = 24
PAGE_TYPE_LIVE_PHOTOS_ALBUM = 25
PAGE_TYPE_NEWS = 26
PAGE_TYPE_NEWS_DETAIL = 27
PAGE_TYPE_FOR_PARTNERS = 28
PAGE_TYPE_ORDERS = 29
PAGE_TYPE_ORDER_DETAIL = 30
PAGE_TYPE_REVIEWS = 31
PAGE_TYPE_404 = 32
PAGE_TYPE_500 = 33
PAGE_TYPE_PROFILE = 34
PAGE_TYPE_NOTIFICATIONS = 35
PAGE_TYPE_BALANCE = 36
PAGE_TYPE_CATALOG_EXPORT = 37
PAGE_TYPE_SHOP = 38
PAGE_TYPE_SHOP_SETTINGS = 39
PAGE_TYPE_SHOP_REQUISITES = 40
PAGE_TYPE_SHOP_CONTENT = 41
PAGE_TYPE_SHOP_CONTENT_RETAIL_INFO = 42
PAGE_TYPE_SHOP_CONTENT_ABOUT = 43
PAGE_TYPE_SHOP_CONTENT_CONTACTS = 44
PAGE_TYPE_SHOP_CONTENT_LIVE_PHOTOS = 45
PAGE_TYPE_SHOP_CONTENT_FOOTER = 46
PAGE_TYPE_SHOP_CONTENT_DELIVERY = 47
PAGE_TYPE_SHOP_CREATE = 48
PAGE_TYPE_SHOP_PRODUCTS = 49
PAGE_TYPE_SHOP_ORDERS = 50
PAGE_TYPE_SHOP_ORDER_DETAIL = 51
PAGE_TYPE_SHOP_CLIENTS = 52
PAGE_TYPE_SHOP_PROMO = 53
PAGE_TYPE_SHOP_CLIENT_DETAIL = 54
PAGE_TYPE_LANDING = 55
PAGE_TYPE_UIKIT = 56
PAGE_TYPE_SHOP_MAIN_PAGE = 57
PAGE_TYPE_SHOP_INFO_PAGE = 58
PAGE_TYPE_SHOP_CATALOG_PAGE = 59
PAGE_TYPE_SHOP_PRODUCT_PAGE = 60
PAGE_TYPE_SHOP_ORDER_CHECKOUT_PAGE = 61
PAGE_TYPE_SHOP_ORDERS_LIST_PAGE = 62
PAGE_TYPE_SHOP_ORDER_DETAIL_PAGE = 63
PAGE_TYPE_SHOP_LIVE_PHOTO_ALBUM_PAGE = 64
PAGE_TYPE_SHOP_LIVE_PHOTOS_PAGE = 65
PAGE_TYPE_SHOP_CART_PAGE = 66
PAGE_TYPE_SHOP_MY_SHOP = 67
PAGE_TYPE_SHOP_INFO_DEFAULT = 68
PAGE_TYPE_SHOP_MOTIVATION = 69
PAGE_TYPE_SHOP_CONTENT_MAIN = 70


HOME_PAGES = [PAGE_TYPE_HOME]

PAGE_TYPES = {
    PAGE_TYPE_DEFAULT: {
        'title': 'default',
        'template': '',
        'context': 'content.contexts.default.context'
    },
    PAGE_TYPE_HOME: {
        'title': 'Главная',
        'template': '',
        'context': 'content.contexts.main.context'
    },
    PAGE_TYPE_CATALOG: {
        'title': 'Каталог',
        'template': '',
        'context': 'content.contexts.catalog.context'
    },
    PAGE_TYPE_CATEGORY: {
        'title': 'Категория',
        'template': '',
        'context': 'content.contexts.category.context'
    },
    PAGE_TYPE_PRODUCT: {
        'title': 'Товар',
        'template': '',
        'context': 'content.contexts.product.context'
    },
    PAGE_TYPE_INFO: {
        'title': 'Информация',
        'template': '',
        'context': 'content.contexts.info.context'
    },
    PAGE_TYPE_AUTH: {
        'title': 'Авторизация',
        'template': '',
        'context': 'content.contexts.auth.context'
    },
    PAGE_TYPE_REGISTRATION: {
        'title': 'Регистрация',
        'template': '',
        'context': 'content.contexts.registration.context'
    },
    PAGE_TYPE_ACCOUNT: {
        'title': 'ЛК',
        'template': '',
        'context': 'content.contexts.account.context'
    },
    PAGE_TYPE_CART: {
        'title': 'Корзина',
        'template': '',
        'context': 'content.contexts.cart.context'
    },
    PAGE_TYPE_RESET_PASS: {
        'title': 'Вспомнить пароль',
        'template': '',
        'context': 'content.contexts.reset_pass.context'
    },
    PAGE_TYPE_CHECKOUT: {
        'title': 'Оформление заказа',
        'template': '',
        'context': 'content.contexts.checkout.context'
    },
    PAGE_TYPE_ORDER_HISTORY: {
        'title': 'История заказов',
        'template': '',
        'context': 'content.contexts.order_history.context'
    },
    PAGE_TYPE_WISHLIST: {
        'title': 'Избранное',
        'template': '',
        'context': 'content.contexts.wishlist.context'
    },
    PAGE_TYPE_COMPARSION: {
        'title': 'Сравнение',
        'template': '',
        'context': 'content.contexts.comparsion.context'
    },
    PAGE_TYPE_SEARCH: {
        'title': 'Поиск',
        'template': '',
        'context': 'content.contexts.search.context'
    },
    PAGE_TYPE_INFO_PAYMENT: {
        'title': 'Информация (оплата)',
        'template': '',
        'context': 'content.contexts.info_payment.context'
    },
    PAGE_TYPE_INFO_DELIVERY: {
        'title': 'Информация (доставка)',
        'template': '',
        'context': 'content.contexts.info_delivery.context'
    },
    PAGE_TYPE_INFO_EXCHANGE: {
        'title': 'Информация (замена)',
        'template': '',
        'context': 'content.contexts.info_exchange.context'
    },
    PAGE_TYPE_INFO_JURIDICAL: {
        'title': 'Информация (юридическая информация)',
        'template': '',
        'context': 'content.contexts.info_juridical.context'
    },
    PAGE_TYPE_INFO_CONTACTS: {
        'title': 'Информация (контакты)',
        'template': '',
        'context': 'content.contexts.info_contacts.context'
    },
    PAGE_TYPE_INFO_HOW_TO: {
        'title': 'Информация (как подобрать размер)',
        'template': '',
        'context': 'content.contexts.info_howto.context'
    },
    PAGE_TYPE_INFO_REVIEWS: {
        'title': 'Информация (отзывы)',
        'template': '',
        'context': 'content.contexts.info_reviews.context'
    },
    PAGE_TYPE_ABOUT: {
        'title': 'О нас',
        'template': '',
        'context': 'content.contexts.about.context'
    },
    PAGE_TYPE_LIVE_PHOTOS: {
        'title': 'Живые фото',
        'template': '',
        'context': 'content.contexts.live_photo.context'
    },
    PAGE_TYPE_LIVE_PHOTOS_ALBUM: {
        'title': 'Живые фото (детальная)',
        'template': '',
        'context': 'content.contexts.live_photo_detail.context'
    },
    PAGE_TYPE_NEWS: {
        'title': 'Новости',
        'template': '',
        'context': 'content.contexts.news.context'
    },
    PAGE_TYPE_NEWS_DETAIL: {
        'title': 'Новости (детальная)',
        'template': '',
        'context': 'content.contexts.news_detail.context'
    },
    PAGE_TYPE_FOR_PARTNERS: {
        'title': 'Партнерам',
        'template': '',
        'context': 'content.contexts.for_partners.context'
    },
    PAGE_TYPE_ORDERS: {
        'title': 'Заказы',
        'template': '',
        'context': 'content.contexts.orders.context'
    },
    PAGE_TYPE_ORDER_DETAIL: {
        'title': 'Заказ (детальная)',
        'template': '',
        'context': 'content.contexts.order_detail.context'
    },
    PAGE_TYPE_REVIEWS: {
        'title': 'Отзывы (ЛК)',
        'template': '',
        'context': 'content.contexts.cabinet_reviews.context'
    },
    PAGE_TYPE_404: {
        'title': '404',
        'template': '',
        'context': 'content.contexts.404.context'
    },
    PAGE_TYPE_500: {
        'title': '500',
        'template': '',
        'context': 'content.contexts.500.context'
    },
    PAGE_TYPE_PROFILE: {
        'title': 'Профиль',
        'template': '',
        'context': 'content.contexts.profile.context'
    },
    PAGE_TYPE_NOTIFICATIONS: {
        'title': 'Уведомления',
        'template': '',
        'context': 'content.contexts.cabinet_notifications.context'
    },
    PAGE_TYPE_BALANCE: {
        'title': 'Баланс и платежи',
        'template': '',
        'context': 'content.contexts.balance.context'
    },
    PAGE_TYPE_CATALOG_EXPORT: {
        'title': 'Экспорт каталога',
        'template': '',
        'context': 'content.contexts.cabinet_export_photo.context'
    },
    PAGE_TYPE_SHOP: {
        'title': 'Мой магазин',
        'template': '',
        'context': 'content.contexts.cabinet_shop.context'
    },
    PAGE_TYPE_SHOP_SETTINGS: {
        'title': 'Мой магазин (настройки)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_settings.context'
    },
    PAGE_TYPE_SHOP_REQUISITES: {
        'title': 'Мой магазин (реквизиты)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_requisites.context'
    },
    PAGE_TYPE_SHOP_CONTENT: {
        'title': 'Мой магазин (контент)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content.context'
    },
    PAGE_TYPE_SHOP_CONTENT_RETAIL_INFO: {
        'title': 'Мой магазин (контент - информация для розницы)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content_retail_info.context'
    },
    PAGE_TYPE_SHOP_CONTENT_ABOUT: {
        'title': 'Мой магазин (контент - о компании)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content_about.context'
    },
    PAGE_TYPE_SHOP_CONTENT_CONTACTS: {
        'title': 'Мой магазин (контент - контакты)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content_contacts.context'
    },
    PAGE_TYPE_SHOP_CONTENT_LIVE_PHOTOS: {
        'title': 'Мой магазин (контент - живые фото)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content_live_photos.context'
    },
    PAGE_TYPE_SHOP_CONTENT_FOOTER: {
        'title': 'Мой магазин (контент - футер сайта)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content_footer.context'
    },
    PAGE_TYPE_SHOP_CONTENT_DELIVERY: {
        'title': 'Мой магазин (контент - доставка)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content_delivery.context'
    },
    PAGE_TYPE_SHOP_CREATE: {
        'title': 'Мой магазин (создание)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_create.context'
    },
    PAGE_TYPE_SHOP_PRODUCTS: {
        'title': 'Мой магазин (товары)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_products.context'
    },
    PAGE_TYPE_SHOP_ORDERS: {
        'title': 'Мой магазин (заказы)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_orders.context'
    },
    PAGE_TYPE_SHOP_ORDER_DETAIL: {
        'title': 'Мой магазин (заказ - детальная страница)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_order_detail.context'
    },
    PAGE_TYPE_SHOP_CLIENTS: {
        'title': 'Мой магазин (клиенты)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_clients.context'
    },
    PAGE_TYPE_SHOP_PROMO: {
        'title': 'Мой магазин (промокоды)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_promo.context'
    },
    PAGE_TYPE_SHOP_CLIENT_DETAIL: {
        'title': 'Мой магазин (клиент - детальная страница)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_client_detail.context'
    },
    PAGE_TYPE_LANDING: {
        'title': 'Лендинг',
        'template': '',
        'context': 'content.contexts.landing.context'
    },
    PAGE_TYPE_UIKIT: {
        'title': 'UIKit',
        'template': '',
        'context': 'content.contexts.default.context'
    },
    PAGE_TYPE_SHOP_MAIN_PAGE: {
        'title': 'Главная (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_main.context'
    },
    PAGE_TYPE_SHOP_INFO_PAGE: {
        'title': 'Информация (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_info.context'
    },
    PAGE_TYPE_SHOP_CATALOG_PAGE: {
        'title': 'Каталог (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_catalog.context'
    },
    PAGE_TYPE_SHOP_PRODUCT_PAGE: {
        'title': 'Товар (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_product_detail.context'
    },
    PAGE_TYPE_SHOP_ORDER_CHECKOUT_PAGE: {
        'title': 'Оформление заказа (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_order_checkout.context'
    },
    PAGE_TYPE_SHOP_ORDERS_LIST_PAGE: {
        'title': 'Заказы (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_orders.context'
    },
    PAGE_TYPE_SHOP_ORDER_DETAIL_PAGE: {
        'title': 'Заказ - детальная (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_order_detail.context'
    },
    PAGE_TYPE_SHOP_LIVE_PHOTO_ALBUM_PAGE: {
        'title': 'Живые фото - детальная (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_live_photo_album.context'
    },
    PAGE_TYPE_SHOP_LIVE_PHOTOS_PAGE: {
        'title': 'Живые фото (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_live_photos.context'
    },
    PAGE_TYPE_SHOP_CART_PAGE: {
        'title': 'Корзина (ИМ)',
        'template': '',
        'context': 'content.contexts.shop_cart.context'
    },
    PAGE_TYPE_SHOP_MY_SHOP: {
        'title': 'Мой магазин (Описание)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_my_shop.context'
    },
    PAGE_TYPE_SHOP_INFO_DEFAULT: {
        'title': 'Мой магазин (Информация)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_info.context'
    },
    PAGE_TYPE_SHOP_MOTIVATION: {
        'title': 'Мой магазин (Мотивационный блок)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_motivation.context'
    },
    PAGE_TYPE_SHOP_CONTENT_MAIN: {
        'title': 'Мой магазин (контент - главная)',
        'template': '',
        'context': 'content.contexts.cabinet_shop_content_main.context'
    },
}

CHOICES_PAGE_TYPES = [(k, v['title']) for k, v in PAGE_TYPES.items()]

CHOICES_COMPONENT_POSITION = (
    ('DEFAULT', 'default'),
    ('INFO', 'Информация'),
    ('SIZE_SELECTION', 'Как подобрать размер'),
    ('CONTACTS', 'Контакты'),
    ('ABOUT', 'О нас'),
    ('PARTNERS', 'Партнерам'),
    ('LANDING', 'Лендинг'),
    ('DELIVERY', 'Доставка'),
)

CHOICES_COMPONENT_TEMPLATE = (
    ('--', '--'),
)

PAGINATION_DEFAULT_OBJECTS_ON_PAGE = 5

EXCLUDE_PAGE_TYPES_FROM_SEARCH = [

]
