from ..serializers import PageSerializer
from .common import common_context
from config.models import RoleConfiguration


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    info_payment = list(RoleConfiguration.objects.all().values('role', 'payment_info'))

    context = {
        'page_info': PageSerializer(page).data,
        'info_payment': info_payment,
    }
    context.update(common_context(user, page))

    return context
