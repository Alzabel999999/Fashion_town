import os
from django.conf import settings
from rest_framework.test import APITestCase, APIClient
from user.models import User
from ..models import Category
from ..models import Product


# run test --- python backend/manage.py test garpix_catalog
class BaseViewTest(APITestCase):
    client = APIClient()
    module_dir = os.path.dirname(__file__)

    @staticmethod
    def create_user(username="", email="", first_name="", last_name="", password="", is_superuser=True, is_staff=True):
        """
        Create a user in the db
        :param is_staff:
        :param is_superuser:
        :param password:
        :param username:
        :param email:
        :param first_name:
        :param last_name:
        """
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                        password=password, is_superuser=is_superuser, is_staff=is_staff)

        return user

    @staticmethod
    def create_category(parent=None, title="", ordering=0):
        category = Category.objects.create(parent=parent, title=title, ordering=ordering)
        return category

    @staticmethod
    def create_product(price=0, stock=0, weight=0, extra=0, ):
        product = Product.objects.create(price=price, stock=stock, weight=weight, extra=extra,
                                         page_type=settings.PAGE_TYPE_HOME)
        return product
