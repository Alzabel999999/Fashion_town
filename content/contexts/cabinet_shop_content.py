from django.conf import settings
from garpix_menu.models import MenuItem
from ..serializers import PageSerializer, MenuItemSerializer
from .cabinet_common import cabinet_common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    context = {
        'page_info': PageSerializer(page).data,
        'cabinet_site_config_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_CABINET_SITE_CONFIG, is_active=True), many=True).data,
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
