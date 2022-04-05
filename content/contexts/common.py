import datetime
from django.conf import settings
from garpix_page.models import Page

from user.models import Profile
from ..serializers import (
    MenuItemSerializer,
    SiteConfigurationSerializer,
    AnnounceSerializer,
    RoleConfigurationSerializer,
)
from ..models import Announce
from garpix_menu.models import MenuItem
from config.models import SiteConfiguration, RoleConfiguration
from user.serializers import ProfileSerializer
from garpix_catalog.models import Currency
from garpix_catalog.models import Product


def common_context(user=None, page=None, currency='PLN'):

    role = user.profile.role if user else 0
    status = user.status if user else 0
    role_config = RoleConfiguration.objects.filter(role=role if role != 0 else 1).first()
    main_page = Page.objects.filter(page_type=settings.PAGE_TYPE_HOME).first()
    breadcrumbs = get_breadcrumbs(page) if page else []
    breadcrumbs = [{'slug': main_page.slug, 'title': main_page.title}, ] + breadcrumbs
    currencies_dict = Currency.objects.all().exclude(ratio=0.0000)
    currencies = ['PLN', ] + [currency.title for currency in currencies_dict]
    cabinet_menu_items = MenuItem.objects.filter(parent=None, menu_type=settings.MENU_TYPE_CABINET, is_active=True)
    if role in [0, 1]:
        cabinet_menu_items = cabinet_menu_items.exclude(page__page_type=settings.PAGE_TYPE_CATALOG_EXPORT)
    context = {
        'breadcrumbs': breadcrumbs,
        'currencies': currencies,
        'site_configuration': SiteConfigurationSerializer(SiteConfiguration.get_solo()).data,
        'role_configuration': RoleConfigurationSerializer(role_config).data,
        'announce': None,
        'main_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_MAIN, is_active=True), many=True).data,
        'header_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_HEADER, is_active=True), many=True).data,
        'footer_menu': MenuItemSerializer(MenuItem.objects.filter(
            parent=None, menu_type=settings.MENU_TYPE_FOOTER, is_active=True), many=True).data,
        'cabinet_menu': MenuItemSerializer(cabinet_menu_items, many=True).data if status == 3 else [],
        'year': datetime.date.today().year
    }
    if role in [Profile.ROLE.DROPSHIPPER, Profile.ROLE.WHOLESALE]:
        announce = Announce.objects.filter(is_active=True).first()
        if announce:
            context.update({'announce': AnnounceSerializer(announce, many=False).data})
    if status != 0:
        context.update({'profile': ProfileSerializer(user.profile, context={'currency': currency}).data})
    else:
        context.update({'profile': {'role': 0, 'status': 0, }})

    return context


def get_breadcrumbs(page):
    result = []
    if page.slug and page.page_type != 0:
        obj = page
        crumb = {'title': page.title, 'slug': page.slug}
        result.append(crumb)
        while obj.parent is not None:
            filter_str = ''
            if type(obj) == Product:
                filter_str = f'?category={obj.category.id}'
            crumb = {'title': obj.parent.title, 'slug': obj.parent.slug + filter_str}
            result.insert(0, crumb)
            obj = obj.parent
    return result
