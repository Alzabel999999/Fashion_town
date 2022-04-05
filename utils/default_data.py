# PAGES
pages = [
    {'type': 1, 'title': 'Главная', 'url': '', 'children': []},
    {'type': 5, 'title': 'Каталог', 'url': 'catalog', 'children': []},
    {'type': 3, 'title': 'Категория', 'url': 'category', 'children': []},
    {'type': 4, 'title': 'Товар', 'url': 'product', 'children': []},
    {'type': 2, 'title': 'Информация', 'url': 'information', 'children': [
        {'type': 16, 'title': 'Информация (оплата)', 'url': 'payment', 'children': []},
        {'type': 17, 'title': 'Информация (доставка)', 'url': 'delivery', 'children': []},
        {'type': 18, 'title': 'Информация (замена)', 'url': 'exchange', 'children': []},
        {'type': 19, 'title': 'Информация (юридическая информация)', 'url': 'juridical', 'children': []},
        {'type': 20, 'title': 'Информация (контакты)', 'url': 'contacts', 'children': []},
        {'type': 21, 'title': 'Информация (как подобрать размер)', 'url': 'how_to', 'children': []},
        {'type': 22, 'title': 'Информация (отзывы)', 'url': 'reviews', 'children': []},
    ]},
    {'type': 6, 'title': 'Авторизация', 'url': 'authorization', 'children': []},
    {'type': 7, 'title': 'Регистрация', 'url': 'registration', 'children': []},
    {'type': 8, 'title': 'ЛК', 'url': 'lk', 'children': [
        {'type': 29, 'title': 'Заказы', 'url': 'orders', 'children': []},
    ]},
    {'type': 9, 'title': 'Корзина', 'url': 'cart', 'children': []},
    {'type': 10, 'title': 'Вспомнить пароль', 'url': 'refresh_pass', 'children': []},
    {'type': 11, 'title': 'Оформление заказа', 'url': 'order', 'children': []},
    {'type': 12, 'title': 'История заказов', 'url': 'order_history', 'children': []},
    {'type': 13, 'title': 'Избранное', 'url': 'wishlist', 'children': []},
    {'type': 14, 'title': 'Сравнение', 'url': 'compare', 'children': []},
    {'type': 15, 'title': 'Поиск', 'url': 'search', 'children': []},
    {'type': 23, 'title': 'О нас', 'url': 'about', 'children': []},
    {'type': 24, 'title': 'Живые фото', 'url': 'live_photos', 'children': [
        # {'type': 25, 'title': 'Живые фото (детальная)', 'url': '', 'children': []},
    ]},
    {'type': 26, 'title': 'Новости', 'url': 'news', 'children': [
        # {'type': 27, 'title': 'Новости (детальная)', 'url': '', 'children': []},
    ]},
    {'type': 28, 'title': 'Партнерам', 'url': 'for_partners', 'children': []},
    {'type': 32, 'title': '404', 'url': '404', 'children': []},
    {'type': 33, 'title': '500', 'url': '500', 'children': []},
    {'type': 34, 'title': 'Профиль', 'url': 'profile', 'children': []},
    {'type': 35, 'title': 'Уведомления', 'url': 'notifications', 'children': []},
    {'type': 36, 'title': 'Баланс и платежи', 'url': 'balance', 'children': []},
    {'type': 37, 'title': 'Экспорт каталога', 'url': 'catalog_export', 'children': []},
]


# MENU
menu = {
    'header_menu': [
        {'title': 'О компании', 'page_type': 23, 'filter': '', 'children': []},
        {'title': 'Живые фото', 'page_type': 24, 'filter': '', 'children': []},
        {'title': 'Новости', 'page_type': 26, 'filter': '', 'children': []},
        {'title': 'Партнерам', 'page_type': 28, 'filter': '', 'children': []},
        {'title': 'Информация', 'page_type': 2, 'filter': '', 'children': [
            {'title': 'Оплата', 'page_type': 16, 'filter': '', 'children': []},
            {'title': 'Доставка', 'page_type': 17, 'filter': '', 'children': []},
            {'title': 'Обмен и возврат', 'page_type': 18, 'filter': '', 'children': []},
            {'title': 'Юридическая информация', 'page_type': 19, 'filter': '', 'children': []},
            {'title': 'Контакты', 'page_type': 20, 'filter': '', 'children': []},
            {'title': 'Как подобрать размер', 'page_type': 21, 'filter': '', 'children': []},
            {'title': 'Отзывы', 'page_type': 22, 'filter': '', 'children': []},
        ]},
    ],
    'main_menu': [
        {'title': 'Каталог', 'page_type': 5, 'filter': '', 'children': []},
        {'title': 'В наличии', 'page_type': 5, 'filter': '?in_stock=true', 'children': []},
        {'title': 'Новинки', 'page_type': 5, 'filter': '?is_new=true', 'children': []},
        {'title': 'Хиты', 'page_type': 5, 'filter': '?is_bestseller=true', 'children': []},
        {'title': 'Распродажа', 'page_type': 5, 'filter': '?is_closeout=true', 'children': []},
    ],
    'footer_menu': [
        {'title': 'О нас', 'page_type': 23, 'filter': '', 'children': [
            {'title': 'О компании', 'page_type': 23, 'filter': '', 'children': []},
            {'title': 'Живые фото', 'page_type': 24, 'filter': '', 'children': []},
            {'title': 'Контакты', 'page_type': 20, 'filter': '', 'children': []},
            {'title': 'Информация', 'page_type': 2, 'filter': '', 'children': []},
        ]},
        {'title': 'Купить', 'page_type': 5, 'filter': '', 'children': [
            {'title': 'Новинки', 'page_type': 5, 'filter': '?is_new=true', 'children': []},
            {'title': 'Распродажа', 'page_type': 5, 'filter': '?is_closeout=true', 'children': []},
            {'title': 'В наличии', 'page_type': 5, 'filter': '?in_stock=true', 'children': []},
            {'title': 'Хиты сезона', 'page_type': 5, 'filter': '?is_bestseller=true', 'children': []},
        ]},
    ],
    'cabinet_menu': [
        {'title': 'Профиль', 'page_type': 34, 'filter': '', 'children': []},
        {'title': 'Мои заказы', 'page_type': 29, 'filter': '', 'children': []},
        {'title': 'Уведомления', 'page_type': 35, 'filter': '', 'children': []},
        {'title': 'Баланс и платежи', 'page_type': 36, 'filter': '', 'children': []},
        {'title': 'Отзывы', 'page_type': 22, 'filter': '', 'children': []},
        {'title': 'Экспорт каталога', 'page_type': 37, 'filter': '', 'children': []},
    ]
}


# BANNERS
banners = {
    'main_page_first_page': {
        1: {
            'title': 'НОВИНКИ',
            'content': '',
            'footnote': '',
        },
        2: {
            'title': 'ХИТЫ СЕЗОНА',
            'content': '',
            'footnote': '',
        },
        3: {
            'title': 'РАСПРОДАЖА',
            'content': '',
            'footnote': '',
        },
    },
    'main_page_for_partner': {
        1: {
            'title': 'Дропшипперам',
            'content': 'Покупайте выгодно от 1 шт. \n Отправляйте напрямую своим покупателям*',
            'footnote': '*При наличии действующего интренет-магазина / точки продаж'
        },
        2: {
            'title': 'Оптовикам',
            'content': 'Покупайте по оптовой цене* \n Гибкие условия заказа*',
            'footnote': '*При наличии действующего интренет-магазина / точки продаж'
        },
    },
    'main_page_about': {
        1: {
            'title': 'О компании',
            'content': 'Fashion Town - это сервис, который упрощает ведение бизнеса в интернете '
                       'и предоставляет пользователям доступ к одежде невероятно модных брендов.'
                       'А купить ее можно не только на оптовых условиях, но и как обычный розничный покупатель!',
            'footnote': '',
        }
    }
}
