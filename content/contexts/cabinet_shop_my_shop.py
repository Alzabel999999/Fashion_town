from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context
from datetime import datetime

def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    # todo убрать заглушки
    clients_count = 1000
    products_count = 1000
    orders_count = 125
    tarif_info = {
        'expiration_date': datetime.today(),
        'description': "qqqqqqqqqqqqqqqq"
    }
    logo = '#'
    title = 'title'
    domain = 'domain.ru'

    context = {
        'logo': logo,
        'title': title,
        'domain': domain,
        'page_info': PageSerializer(page).data,
        'clients_count': clients_count,
        'products_count': products_count,
        'orders_count': orders_count,
        'tarif_info': tarif_info,
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
