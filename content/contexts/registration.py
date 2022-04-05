from ..serializers import PageSerializer
from ..models.any_pages import AnyPages
from .common import common_context
from django.conf import settings
from config.models import RoleConfiguration


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    if AnyPages.get_solo().auth_reg_image:
        image = settings.SITE_URL + AnyPages.get_solo().auth_reg_image.url
    else:
        image = '#'
    public_offers = [
        {
            'role': role_config.role,
            'public_offer': settings.SITE_URL + role_config.public_offer.url if role_config.public_offer else '#'
        } for role_config in RoleConfiguration.objects.all()
    ]

    context = {
        'page_info': PageSerializer(page).data,
        'image': image,
        'text': AnyPages.get_solo().auth_reg_text,
        'public_offers': public_offers,
    }
    context.update(common_context(user, page))

    return context
