from ..serializers import PageSerializer
from ..models.any_pages import AnyPages
from .common import common_context
from django.conf import settings


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    if AnyPages.get_solo().auth_reg_image:
        image = settings.SITE_URL + AnyPages.get_solo().auth_reg_image.url
    else:
        image = '#'

    context = {
        'page_info': PageSerializer(page).data,
        'image': image,
        'text': AnyPages.get_solo().auth_reg_text,
    }
    context.update(common_context(user, page))

    return context
