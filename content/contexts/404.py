from ..serializers import PageSerializer
from .common import common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    context = {
        'page_info': PageSerializer(page).data,
    }
    context.update(common_context(user))

    return context
