from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context
from user.models import User
from user.serializers import ShopUserSerializer


def context(request, *args, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')
    client_id = int(request.GET.get('client_id', 0))
    client = User.objects.filter(id=client_id).first()

    context = {
        'page_info': PageSerializer(page).data,
        'client_id': client_id,
        'client': ShopUserSerializer(client).data if client else None
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
