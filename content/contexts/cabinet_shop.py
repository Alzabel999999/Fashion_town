from django.conf import settings
from garpix_page.models import Page
from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context
from datetime import datetime


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')
    shop = user.profile.profile_shop

    # todo убрать заглушки
    clients_count = 1000
    products_count = 1000
    orders_count = 125
    tarif_info = {
        'expiration_date': datetime.today(),
        'description': "qqqqqqqqqqqqqqqq"
    }
    # -------------------------

    logo = settings.SITE_URL + shop.logo.url if shop.logo else '#'
    title = shop.title
    domain = shop.site.domain
    clients_page = Page.objects.filter(page_type=settings.PAGE_TYPE_SHOP_CLIENTS).first()
    products_page = Page.objects.filter(page_type=settings.PAGE_TYPE_SHOP_PRODUCTS).first()
    orders_page = Page.objects.filter(page_type=settings.PAGE_TYPE_SHOP_ORDERS).first()

    context = {
        'page_info': PageSerializer(page).data,
        'logo': logo,
        'title': title,
        'domain': domain,
        'clients_count': clients_count,
        'products_count': products_count,
        'orders_count': orders_count,
        'clients_page': clients_page.slug if clients_page else '#',
        'products_page': products_page.slug if products_page else '#',
        'orders_page': orders_page.slug if orders_page else '#',
        'tarif_info': tarif_info,
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
