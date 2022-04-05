from celery.schedules import crontab
from celery.task import periodic_task
from ..models import Product
import datetime


def periodic_decorator():
    return periodic_task(run_every=crontab(hour=1, minute=0))


@periodic_decorator()
def update_products_task():
    delta = datetime.timedelta(days=7)
    for product in Product.objects.all():
        if product.created_at.date() + delta < datetime.datetime.now().date() and product.is_new:
            product.is_new = False
            product.save()
            print(f'товар №{product.id} - теперь не новинка')
