MENU_TYPE_MAIN = 'main_menu'
MENU_TYPE_HEADER = 'header_menu'
MENU_TYPE_FOOTER = 'footer_menu'
MENU_TYPE_CABINET = 'cabinet_menu'
MENU_TYPE_CABINET_SITE = 'cabinet_site_menu'
MENU_TYPE_CABINET_SITE_CONFIG = 'cabinet_site_config_menu'
MENU_TYPE_CHILD_SITE = 'child_site_menu'

MENU_TYPES = {
    MENU_TYPE_MAIN: {
        'title': 'Главное меню',
        'class': ''
    },
    MENU_TYPE_HEADER: {
        'title': 'Меню хэдера',
        'class': ''
    },
    MENU_TYPE_FOOTER: {
        'title': 'Меню футера',
        'class': ''
    },
    MENU_TYPE_CABINET: {
        'title': 'Меню в ЛК',
        'class': ''
    },
    MENU_TYPE_CABINET_SITE: {
        'title': 'Меню сайта в ЛК',
        'class': ''
    },
    MENU_TYPE_CABINET_SITE_CONFIG: {
        'title': 'Меню настройки сайта в ЛК',
        'class': ''
    },
    MENU_TYPE_CHILD_SITE: {
        'title': 'Меню дочернего сайта',
        'class': ''
    },
}

CHOICE_MENU_TYPES = [(k, v['title']) for k, v in MENU_TYPES.items()]
