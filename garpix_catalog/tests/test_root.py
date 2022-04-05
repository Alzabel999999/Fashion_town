from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest


class RootViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/catalog/root'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class RootTest(RootViewTest):

    def test_get_root(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200)
