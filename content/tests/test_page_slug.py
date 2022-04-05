from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest
from garpix_page.models import Page
from django.conf import settings


class SlugPageViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/content/page/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_page = Page.objects.create(title='hhggqq', page_type=settings.PAGE_TYPE_INFO)


class SlugPageTest(SlugPageViewTest):

    def test_get_page_by_slug(self):
        slug = self.some_page.slug
        response = self.client.get(f'{self.URL}{slug}', data={"slug": "hhggqq"})
        self.assertEqual(response.status_code, 200)
