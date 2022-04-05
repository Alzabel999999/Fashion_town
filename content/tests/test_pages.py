from rest_framework.test import APIClient
from .base import BaseViewTest
from garpix_page.models import Page
from django.conf import settings


class PagesTest(BaseViewTest):

    def setUp(self):
        self.URL = '/api/v1/content/page/'
        self.client = APIClient()
        page_types = settings.CHOICES_PAGE_TYPES
        self.pages = []
        for type, title in page_types:
            page = Page.objects.create(title=title, slug=type)
            self.pages.append(page)

    def test_page_response(self):
        for page in self.pages:
            slug = page.slug
            response = self.client.get(f'{self.URL}{slug}', data={"slug": slug})
            self.assertEqual(response.status_code, 200)


# class SlugPageTest(SlugPageViewTest):
#
#     def test_get_page_by_slug(self):
#         slug = self.some_page.slug
#         response = self.client.get(f'{self.URL}{slug}', data={"slug": "hhggqq"})
#         self.assertEqual(response.status_code, 200)
