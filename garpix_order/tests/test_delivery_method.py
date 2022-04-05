from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from ..models.delivery_method import DeliveryMethod


class DeliveryMethodViewTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/order/delivery_method/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_delivery_method = DeliveryMethod.objects.create(
            image_thumb="", ordering=3, title="qwerty",
            created_at="2020-04-27T11:46:13.970752",
            updated_at="2020-04-27T11:46:13.970774",
            is_active=True, content="", type="pickup")

        self.fixtures = {
            "image_thumb": "string",
            "ordering": 0,
            "title": "string",
            "is_active": True,
            "content": "string",
            "type": "courier"
        }


class DeliveryMethodTest(DeliveryMethodViewTest):

    def test_get_delivery_method(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_delivery_method(self):
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 201)

    def test_put_delivery_method(self):
        _id = self.some_delivery_method.id
        response = self.client.put(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_delivery_method(self):
        _id = self.some_delivery_method.id
        response = self.client.patch(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_delivery_method(self):
        _id = self.some_delivery_method.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 204)

    def test_get_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    def test_access(self):
        self.user = get_user_model().objects.create_user(
            email='test@gg1.com',
            password='testpass1',
            username='test1',
        )
        self.client.force_authenticate(user=self.user)
        _id = self.some_delivery_method.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 403)
