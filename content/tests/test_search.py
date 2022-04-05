from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest


class SearchViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/content/search/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class SearchTest(SearchViewTest):

    def test_get_search(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))
