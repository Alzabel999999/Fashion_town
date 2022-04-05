from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


class RestorePasswordSetPasswordTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/user/restore_password_set_password/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass111111',
            username='test',
            phone='89969185053',
            first_name='van',
            last_name='darkholme',
            password_reset_key='password_reset_key'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        print(self.user.password_reset_key, 'spassword_reset_key')

    def test_restore_password_set_password(self):
        response = self.client.post(f'{self.URL}', data={
            "username": "test",
            "email": "test@gg.com",
            "phone": "89969185053",
            "first_name": "van",
            "last_name": "darkholme",
            "reset_key": self.user.password_reset_key,
            "password": "testpass111111"
        })

        self.assertEqual(response.status_code, 200)
