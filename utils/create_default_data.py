'''
----- common
python backend/manage.py shell -c "from utils.create_default_data import clear_all; clear_all()"
python backend/manage.py shell -c "from utils.create_default_data import create_default_data; create_default_data()"
----- delete
python backend/manage.py shell -c "from utils.create_default_data import clear_pages; clear_pages()"
python backend/manage.py shell -c "from utils.create_default_data import clear_menu; clear_menu()"
python backend/manage.py shell -c "from utils.create_default_data import create_banners; create_banners()"
----- create
python backend/manage.py shell -c "from utils.create_default_data import create_pages; create_pages()"
python backend/manage.py shell -c "from utils.create_default_data import create_menus; create_menus()"
python backend/manage.py shell -c "from utils.create_default_data import create_banners; create_banners()"
'''

from content.models.banner import Banner
from garpix_menu.models import MenuItem
from garpix_page.models import Page
from django.conf import settings
from .default_data import pages, menu, banners
from config.models import SiteConfiguration


def create_default_data():
    create_pages()
    create_site_config_pages()
    create_menus()
    create_banners()


def create_pages():
    for item in pages:
        print(item)
        parent_page = Page(title=item['title'], slug=item['url'], page_type=item['type'], )
        parent_page.save()
        parent_page.sites.set([1])
        parent_page.save()
        if item['children']:
            for child_item in item['children']:
                child_page = Page(title=child_item['title'], slug=child_item['url'], page_type=child_item['type'],
                                  parent=parent_page)
                child_page.save()
                child_page.sites.set([1])
                child_page.save()


def create_menus():
    url = '/'
    for menu_type, menus_in_type in menu.items():
        i = 1
        for parent_menu in menus_in_type:
            new_parent_menu = MenuItem.objects.create(
                title_for_admin=parent_menu['title'], title=parent_menu['title'],
                menu_type=menu_type, page=Page.objects.filter(page_type=parent_menu['page_type']).first(), sort=i)
            i += 1
            if parent_menu['children']:
                for child_menu in parent_menu['children']:
                    new_child_menu = MenuItem.objects.create(
                        title_for_admin=child_menu['title'], title=child_menu['title'],
                        menu_type=menu_type, page=Page.objects.filter(page_type=child_menu['page_type']).first(),
                        sort=i, parent=new_parent_menu)
                    i += 1


def create_banners():
    url = '/'
    for banner_type, banners_list in banners.items():
        for order_index, banner in banners_list.items():
            new_banner = Banner(title=banner['title'], content=banner['content'], footnote=banner['footnote'],
                                url=url, banner_type=banner_type, ordering=order_index)
            new_banner.save()


'''
python backend/manage.py shell -c "from utils.create_default_data import create_site_config_pages; create_site_config_pages()"
'''
def create_site_config_pages():
    config = SiteConfiguration.get_solo()
    config.page_type_cart = Page.objects.filter(page_type=9).order_by('id').first()
    config.page_type_account = Page.objects.filter(page_type=8).order_by('id').first()
    config.page_type_auth = Page.objects.filter(page_type=6).order_by('id').first()
    config.page_type_reg = Page.objects.filter(page_type=7).order_by('id').first()
    config.page_type_reset_pass = Page.objects.filter(page_type=10).order_by('id').first()
    config.page_type_checkout = Page.objects.filter(page_type=11).order_by('id').first()
    config.page_type_order_history = Page.objects.filter(page_type=12).order_by('id').first()
    config.page_type_wishlist = Page.objects.filter(page_type=13).order_by('id').first()
    config.page_type_comparsion = Page.objects.filter(page_type=14).order_by('id').first()
    config.page_type_search = Page.objects.filter(page_type=15).order_by('id').first()
    config.page_type_catalog = Page.objects.filter(page_type=5).order_by('id').first()
    config.page_type_news = Page.objects.filter(page_type=26).order_by('id').first()
    config.page_type_reviews = Page.objects.filter(page_type=22).order_by('id').first()
    config.page_type_live_photos = Page.objects.filter(page_type=24).order_by('id').first()
    config.page_type_404 = Page.objects.filter(page_type=32).order_by('id').first()
    config.page_type_500 = Page.objects.filter(page_type=33).order_by('id').first()
    config.save()


# очистка
def clear_all():
    clear_pages()
    clear_menu()
    clear_banners()


def clear_pages():
    Page.objects.all().delete()


def clear_menu():
    MenuItem.objects.all().delete()


def clear_banners():
    Banner.objects.all().delete()
