from garpix_page.models import Page
from rest_framework.test import APITestCase, APIClient
from user.models import User
from ..models import Feature
from ..models import Banner
from ..models import BlogPost
from ..models import Slider
from garpix_menu.models import MenuItem


# run test --- python backend/manage.py test content

class BaseViewTest(APITestCase):
    client = APIClient()
    some_page = Page.objects.create(title='some_page')

    @staticmethod
    def create_user(username="", email="", first_name="", last_name="", password=""):
        """
        Create a user in the db
        :param password:
        :param username:
        :param email:
        :param first_name:
        :param last_name:
        """
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                        password=password)

        return user

    @staticmethod
    def create_feature(title="", ordering=0, content="", is_active=True):
        feature = Feature.objects.create(content=content, title=title, ordering=ordering,
                                         is_active=is_active)
        return feature

    @staticmethod
    def create_banner(ordering=0, is_active=True, content="", url="", target_blank=False, css_class="",
                      banner_type=None):
        banner = Banner.objects.create(ordering=ordering, is_active=is_active, content=content, url=url,
                                       target_blank=target_blank, css_class=css_class, banner_type=banner_type)
        return banner

    @staticmethod
    def create_menu_item(title="", page=None, is_active=True, url='', target_blank=True, css_class='', edition_style='',
                         is_only_for_authenticated=False):
        menu_item = MenuItem.objects.create(title=title, is_active=is_active, page=page, url=url,
                                            target_blank=target_blank, css_class=css_class, edition_style=edition_style,
                                            is_only_for_authenticated=is_only_for_authenticated)
        return menu_item

    @staticmethod
    def create_blog_post(title=""):
        blog_post = BlogPost.objects.create(title=title)

        return blog_post

    @staticmethod
    def create_slider(title=""):
        slider = Slider.objects.create(title=title)
        return slider
