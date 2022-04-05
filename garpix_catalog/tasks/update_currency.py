from celery.schedules import crontab
from celery.task import periodic_task
from ..models import Currency


def periodic_decorator():
    return periodic_task(run_every=crontab(minute=0, hour=0))


@periodic_decorator()
def update_currency_task():
    Currency.get_currencies_from_bank()
