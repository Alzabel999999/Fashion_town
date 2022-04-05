from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context
from django.conf import settings
from garpix_order.models import Order


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    statuses = []
    for s in settings.CHOICE_ORDER_STATUSES:
        statuses.append({
            'status': s[0],
            'title': s[1],
            'count': Order.objects.filter(profile__user=user, status=s[0]).count()
        })

    context = {
        'page_info': PageSerializer(page).data,
        'statuses': statuses,
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
