from django.http import Http404, HttpResponse
# from django.contrib.sitemaps import GenericSitemap
from .models import SiteConfiguration
# from django.utils.timezone import now


def robots_txt(request):
    config = SiteConfiguration.get_solo()
    if config.robots_txt:
        return HttpResponse(config.robots_txt)
    raise Http404


def sitemap_view():
    return {}
