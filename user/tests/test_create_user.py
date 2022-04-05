from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from user.models import User


class CreateAndGetUserTest(APITestCase):

    def setUp(self):
        self.URL = '/api/v1/user/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get__user(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200)

    def test_create__user_valid(self):
        response = self.client.post(f'{self.URL}', data={
            "username": "dimaa",
            "email": "dima@dima.com",
            "phone": "89969185053",
            "password": "top-secret",
            "first_name": "dima",
            "last_name": "qqq"
        })
        self.assertEqual(response.status_code, 201)

    def test_create__user_invalid_email(self):
        response = self.client.post(f'{self.URL}', data={
            "username": "dimaa1",
            "email": "blablainvalid",
            "phone": "89969285053",
            "password": "top-secret",
            "first_name": "dima1",
            "last_name": "qqqq1"
        })
        self.assertEqual(response.status_code, 400)

    def test_create__user_invalid_pass(self):
        response = self.client.post(f'{self.URL}', data={
            "username": "dimaa1",
            "email": "dima@dmitry.com",
            "phone": "89969285053",
            "password": "1",
            "first_name": "dima11",
            "last_name": "qqqq11"
        })
        self.assertEqual(response.status_code, 400)

    def test_create__user_email_is_busy(self):
        response = self.client.post(f'{self.URL}', data={
            "username": "some",
            "email": "test@gg.com",
            "phone": "89969285753",
            "password": "1gg124ynnewfw",
            "first_name": "this1",
            "last_name": "this2"
        })
        self.assertEqual(response.status_code, 400)

    def test_put_user(self):
        _id = self.user.id
        response = self.client.put(f'{self.URL}{_id}/')
        self.assertEqual(response.status_code, 200)

    def test_patch_user(self):
        _id = self.user.id
        response = self.client.patch(f'{self.URL}{_id}/', data={
            "username": "string",
            "phone": "string",
            "first_name": "string",
            "last_name": "string",
            "email_to": "qq@qq.com"
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        _id = self.user.id
        response = self.client.delete(f'{self.URL}{_id}/')
        self.assertEqual(response.status_code, 204)

    def test_get_permissions(self):
        self.client.force_authenticate(user=None)
        _id = self.user.id
        response = self.client.patch(f'{self.URL}{_id}/', data={
            "username": "dimaa",
            "email": "dima@dima.com",
            "phone": "89969185053",
            "password": "top-secret",
            "first_name": "dima",
            "last_name": "qqq"
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_access(self):
        # может ли один юзер удалить другого юзера
        self.other_user = get_user_model().objects.create_user(
            email='qwe@gg.com',
            password='tgwegesgwegegss11111',
            username='otheruser',
        )
        self.user = get_user_model().objects.create_user(
            email='test@gg1.com',
            password='testpass11111',
            username='test113в3а',
        )
        self.client.force_authenticate(user=self.user)
        _id = self.other_user.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 403)

    # def test_get_other_user(self):
    #     self.other_user = get_user_model().objects.create_user(
    #         email='qw2f323e@gg.com',
    #         password='tgwe3ff32gesgwegegss11111',
    #         username='othe3ff32ruser',
    #
    #     )
    #     self.user = get_user_model().objects.create_user(
    #         email='tesf3f32t@gg1.com',
    #         password='f32f32fff32f232f3g',
    #         username='32g23g23d',
    #
    #     )
    #     self.client.force_authenticate(user=self.user)
    #     _id = self.other_user.id
    #     response = self.client.get(f'{self.URL}{_id}/', format='json', follow=True, )
    #     self.assertEquals(response.status_code, 403)
