from ..serializers import PageSerializer
from .common import common_context
from config.models import RoleConfiguration


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    info_delivery = list(RoleConfiguration.objects.all().values('role', 'delivery_condition'))

    context = {
        'page_info': PageSerializer(page).data,
        'info_delivery': info_delivery,
    }
    context.update(common_context(user, page))

    return context
