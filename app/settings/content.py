BANNER_TYPE_DISABLED = 'disabled'
BANNER_TYPE_MAIN_FIRST_PAGE = 'main_page_first_page'
BANNER_TYPE_MAIN_ABOUT = 'main_page_about'
BANNER_TYPE_MAIN_FOR_PARTNER = 'main_page_for_partner'


BANNER_TYPES = {
    BANNER_TYPE_DISABLED: {
        'title': 'Не показан',
        'class': ''
    },
    BANNER_TYPE_MAIN_FIRST_PAGE: {
        'title': 'Баннеры на главную (первая страница)',
        'class': ''
    },
    BANNER_TYPE_MAIN_ABOUT: {
        'title': 'Баннер на главную (о компании)',
        'class': ''
    },
    BANNER_TYPE_MAIN_FOR_PARTNER: {
        'title': 'Баннеры на главную (для партнёров)',
        'class': ''
    },
}

CHOICE_BANNER_TYPES = [(k, v['title']) for k, v in BANNER_TYPES.items()]


SLIDER_TYPE_DISABLED = 'disabled'
SLIDER_TYPE_MAIN = 'main_page'

SLIDER_TYPES = {
    SLIDER_TYPE_DISABLED: {
        'title': 'Не показан',
        'class': ''
    },
    SLIDER_TYPE_MAIN: {
        'title': 'На главной',
        'class': ''
    },
}

CHOICE_SLIDER_TYPES = [(k, v['title']) for k, v in SLIDER_TYPES.items()]
