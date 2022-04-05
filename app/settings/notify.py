NOTIFY_REGISTRATION_EVENT = 1
NOTIFY_FEEDBACK = 2
NOTIFY_EVENT_RESTORE_PASSWORD = 3
CONFIRM_EMAIL_EVENT = 2001
CONFIRM_PHONE_EVENT = 2002

NOTIFY_EVENTS = {
    NOTIFY_REGISTRATION_EVENT: {
        'title': 'Регистрация',
        'context_description': '--',
        'event_description': 'Регистрация',
    },
    NOTIFY_FEEDBACK: {
        'title': 'Обратная связь',
        'context_description': '{{ name }}, {{ email }}, {{ phone }}',
        'event_description': 'Обратная связь',
    },
    NOTIFY_EVENT_RESTORE_PASSWORD: {
        'title': 'сброс / восстановление пароля',
        'context_description': '{{ password_reset_key }} - ключ смены пароля,\n {{ site }} - сайт, с которого поступил запрос',
        'event_description': 'Смена пароля',
    },
    CONFIRM_EMAIL_EVENT: {
        'title': 'Подтверждение email',
        'context_description': '{{ link }} link for confirmation,\n {{ user }} - registered user',
        'event_description': 'This event used when need email confirmation',
    },
    CONFIRM_PHONE_EVENT: {
        'title': 'Подтверждение номера телефона',
        'context_description': '{{ phone_confirmation_key }} -  key for phone confirmation',
        'event_description': 'This event used when need phone confirmation',
    },
}


CHOICES_NOTIFY_EVENT = [(k, v['title']) for k, v in NOTIFY_EVENTS.items()]


NOTIFY_HELP_TEXT = """
    <h3>Переменные в письме</h3>
"""

NOTIFY_SMS_URL = "http://sms.ru/sms/send"

NOTIFY_SMS_API_ID = "1234567890"

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "1234567890"
}

SEND_SMS = False
