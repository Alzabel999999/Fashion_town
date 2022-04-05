from django.conf import settings
from ..serializers import PageSerializer
from .common import common_context
from config.models import SiteConfiguration


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    config = SiteConfiguration.get_solo()

    context = {
        'page_info': PageSerializer(page).data,
        'policy': settings.SITE_URL + config.policy.url if config.policy else '#',
        'terms': settings.SITE_URL + config.terms.url if config.terms else '#',
        'order_condition': settings.SITE_URL + config.order_condition.url if config.order_condition else '#',
        'return_rules': settings.SITE_URL + config.return_rules.url if config.return_rules else '#',
    }
    context.update(common_context(user, page))

    return context
