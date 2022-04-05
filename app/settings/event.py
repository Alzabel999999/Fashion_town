"""
start - запускать по расписанию, доступные возможности:
Возможности по заданиям по расписанию см. в garpix_utils.schedule.check_schedule
"""
from django.utils.timezone import timedelta

EVENT_WATCHDOG_PERIOD = 15
EVENT_DEFAULT_DELAY_TIME = timedelta(hours=24)

EVENT_TYPE_EMPTY = 0
EVENT_TYPE_ONE = 1
EVENT_TYPE_TWO = 2
EVENT_TYPE_THREE = 3


EVENT_TYPES = {
    EVENT_TYPE_EMPTY: {
        'title': 'Empty Event',
        'model': 'garpix_event.models.event.Event',
        'parameters': {},
        'on_action': 'garpix_event.test_func.on_action',
        'on_success': '',
        'on_fail': '',
        'start': {
            'every_second': 6,
        }
    },
    # EVENT_TYPE_ONE: {
    #     'title': 'Event 1',
    #     'model': '',
    #     'parameters': {},
    #     'on_action': 'garpix_subscribe.views.send_email.send_weekly_mail',
    #     'on_success': '',
    #     'on_fail': '',
    #     'start': {
    #         'every_second': 6,
    #     }
    # },
}

CHOICES_EVENT_TYPES = [(k, v['title']) for k, v in EVENT_TYPES.items()]
