from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from ..models.payment_method import PaymentMethod


class PaymentMethodViewTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/order/payment_method/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.some_payment = PaymentMethod.objects.create(title='ff', is_active=True, content="some some some",
                                                         type='cash')

        self.fixtures = {
            "image_thumb": "",
            "ordering": 0,
            "title": "gg",
            "created_at": "2020-04-27T11:46:25.949780",
            "updated_at": "2020-04-27T11:46:25.949805",
            "is_active": True,
            "content": "",
            "type": "online"
        }


class PaymentMethodTest(PaymentMethodViewTest):

    def test_get_payment_method(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_payment_method(self):
        response = self.client.post(f'{self.URL}', self.fixtures)
        self.assertEqual(response.status_code, 201)

    def test_put_payment_method(self):
        _id = self.some_payment.id
        response = self.client.put(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_payment_method(self):
        _id = self.some_payment.id
        response = self.client.patch(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_payment_method(self):
        _id = self.some_payment.id
        response = self.client.delete(f'{self.URL}{_id}/', self.fixtures, format='json', follow=True)
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
        _id = self.some_payment.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 403)
