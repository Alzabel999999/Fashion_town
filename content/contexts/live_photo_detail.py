from ..serializers import PageSerializer
from .common import common_context
from garpix_catalog.serializers import LivePhotoAlbumSerializer


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    context = {
        'page_info': PageSerializer(page).data,
        'album': LivePhotoAlbumSerializer(page).data,
    }
    context.update(common_context(user, page))

    return context
