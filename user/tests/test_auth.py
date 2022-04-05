from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


class AuthTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/auth/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass1',
            username='test1',
            is_staff=True,
            is_superuser=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_crate_token(self):
        response = self.client.post(f'{self.URL}', data={"username": "test1", "password": "testpass1"})
        self.assertEqual(response.status_code, 200,)
        # 200 если токен создан
        # 201 если токен не создан
