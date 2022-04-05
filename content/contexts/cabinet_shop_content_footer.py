from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    context = {
        'page_info': PageSerializer(page).data,
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
