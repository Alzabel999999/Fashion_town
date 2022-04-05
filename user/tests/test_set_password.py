from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


class PasswordSetTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/user/restore_password/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass111111',
            username='test',
            phone='89969185053',
            first_name='van',
            last_name='darkholme',
            password_reset_key='sdtfygubhijr6ftg7uyhinujtguyh'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_set_password(self):
        response = self.client.post(f'{self.URL}', data={
            "username": "test",
            "email": "test@gg.com",
            "phone": "89969185053",
            "first_name": "van",
            "last_name": "darkholme",
            "reset_key": 'sdtfygubhijr6ftg7uyhinujtguyh',
            "password": 'testpass111111',
            "new_password": 'testpass1111112',
        })
        self.assertEqual(response.status_code, 200)
