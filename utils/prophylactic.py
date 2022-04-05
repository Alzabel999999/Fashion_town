'''
python manage.py shell -c "from utils.prophylactic import prophylactic; prophylactic()"
python backend/manage.py shell -c "from utils.prophylactic import prophylactic; prophylactic()"
'''
from garpix_order.models import Order, OrderItem
from django.db.models import Count


def prophylactic():
    cleaning_order_items()
    cleaning_orders()


def cleaning_orders():
    print('--- orders ---')
    orders = Order.objects.annotate(items_count=Count('order_items')).filter(items_count=0)
    count = orders.count()
    for order in orders:
        if hasattr(order, 'order_payment'):
            order.order_payment.delete()
        order.delete()
    print(count, 'empty orders deleted')


def cleaning_order_items():
    print('--- order items ---')
    order_items = OrderItem.objects.filter(cart_item=None, cart_items_pack=None)
    count = order_items.count()
    order_items.delete()
    print(count, 'empty order items deleted')
