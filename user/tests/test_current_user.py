from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


class CurrentUserTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/user/current/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_current_user(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200)
