from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


class RestorePasswordTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/user/restore_password/'
        self.user = get_user_model().objects.create_user(
            email='test@gg1.com',
            password='testpass111111',
            username='test',
            phone='89969185053',
            first_name='van',
            last_name='darkholme'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_restore_password(self):
        response = self.client.post(f'{self.URL}', data={
            "username": "test",
            "email": "test@gg1.com",
            "phone": "89969185053",
            "first_name": "van",
            "last_name": "darkholme"
        })
        self.assertEqual(response.status_code, 200)
