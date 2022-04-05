from ..serializers import PageSerializer
from .shop_common import shop_common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    context = {
        'page_info': PageSerializer(page).data,
    }
    context.update(shop_common_context(user, page))

    return context
