from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context
from garpix_order.models import Order
from garpix_order.serializers import OrderSerializer


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    order = Order.objects.filter(id=page.id).first()

    context = {
        'page_info': PageSerializer(page).data,
        'order': OrderSerializer(order, context={'request': request}).data,
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
