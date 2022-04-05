import datetime
from django.conf import settings
from garpix_page.models import Page
from ..serializers import (
    MenuItemSerializer,
    SiteConfigurationSerializer,
    RoleConfigurationSerializer,
)
from garpix_menu.models import MenuItem
from config.models import SiteConfiguration, RoleConfiguration
from user.serializers import ProfileSerializer
from garpix_catalog.models import Currency


def cabinet_common_context(user=None, page=None, currency='PLN'):

    if user is None:
        return {
            'site_configuration': SiteConfigurationSerializer(SiteConfiguration.get_solo()).data,
            'status': 'Forbidden', 'code': 403
        }

    role_config = RoleConfiguration.objects.filter(
        role=user.profile.role if user.profile.role != 0 else 1).first()

    main_page = Page.objects.filter(page_type=settings.PAGE_TYPE_HOME).first()
    breadcrumbs = get_breadcrumbs(page) if page else []
    breadcrumbs = [{'slug': main_page.slug, 'title': main_page.title}, ] + breadcrumbs
    currencies_dict = Currency.objects.all().exclude(ratio=0.0000)
    currencies = ['PLN', ] + [currency.title for currency in currencies_dict]
    cabinet_menu_items = MenuItem.objects.filter(parent=None, menu_type=settings.MENU_TYPE_CABINET, is_active=True)
    if user.profile.role in [0, 1]:
        cabinet_menu_items = cabinet_menu_items.exclude(page__page_type=settings.PAGE_TYPE_CATALOG_EXPORT)

    context = {
        'status': 'login',
        'breadcrumbs': breadcrumbs,
        'currencies': currencies,
        'site_configuration': SiteConfigurationSerializer(SiteConfiguration.get_solo()).data,
        'role_configuration': RoleConfigurationSerializer(role_config).data,
        'main_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_MAIN, is_active=True), many=True).data,
        'header_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_HEADER, is_active=True), many=True).data,
        'footer_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_FOOTER, is_active=True), many=True).data,
        'cabinet_menu': MenuItemSerializer(cabinet_menu_items, many=True).data,
        'cabinet_site_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_CABINET_SITE, is_active=True), many=True).data,
        'profile': ProfileSerializer(user.profile, context={'currency': currency}).data,
        'year': datetime.date.today().year,
    }
    return context


def get_breadcrumbs(page):
    result = []
    if page.slug and page.page_type != 0:
        obj = page
        crumb = {'title': page.title, 'slug': page.slug}
        result.append(crumb)
        while obj.parent is not None:
            crumb = {'title': obj.parent.title, 'slug': obj.parent.slug}
            result.insert(0, crumb)
            obj = obj.parent
    return result
