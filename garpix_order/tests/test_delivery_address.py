from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from ..models.delivery_address import DeliveryAddress


class DeliveryAddersViewTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/order/delivery_address/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_delivery_adders = DeliveryAddress.objects.create(is_active=True, address='qwerty', profile=self.user.profile)

        self.fixtures = {
            "is_active": True,
            "address": "string"
        }


class DeliveryAddersTest(DeliveryAddersViewTest):

    def test_get_delivery_adders(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_delivery_adders(self):
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 201)

    def test_put_delivery_adders(self):
        _id = self.some_delivery_adders.id
        response = self.client.put(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_delivery_adders(self):
        _id = self.some_delivery_adders.id
        response = self.client.patch(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_delivery_adders(self):
        _id = self.some_delivery_adders.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 204)

    def test_get_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    # def test_access(self):
    #     self.user = get_user_model().objects.create_user(
    #         email='test@gg1.com',
    #         password='testpass1',
    #         username='test1',
    #
    #     )
    #     self.client.force_authenticate(user=self.user)
    #     _id = self.some_delivery_adders.id
    #     response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True, )
    #     self.assertEquals(response.status_code, 403)
