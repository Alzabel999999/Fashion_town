import os
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from django.conf import settings

from ..models import DeliveryMethod, DeliveryAddress, PaymentMethod
from ..models.order import Order
from garpix_cart_rest.models import Cart


class OrderViewTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/order/order/'
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
        self.some_delivery_adders = DeliveryAddress.objects.create(is_active=True, address='qwerty', profile=self.user.profile)
        self.some_card = Cart.objects.create(is_active=True, session='qwerty', extra='', user=self.user)
        self.some_payment = PaymentMethod.objects.create(title='ff', is_active=True, content="some some some",
                                                         type='cash'
                                                         )
        self.some_oder = Order.objects.create(status='placed', extra={},
                                              cart=self.some_card,
                                              delivery_method=self.some_delivery_method,
                                              delivery_address=self.some_delivery_adders,
                                              payment_method=self.some_payment

                                              )

        self.fixtures = {

            "status": "placed",

            "cart": self.some_card.id,
            "delivery_method": self.some_delivery_method.id,
            "delivery_address": self.some_delivery_adders.id,
            "payment_method": self.some_payment.id
        }


class OrderTest(OrderViewTest):

    def test_get_order(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_order(self):
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 201)

    def test_put_order(self):
        _id = self.some_oder.id
        response = self.client.put(f'{self.URL}{_id}/', data={

            "total": 0,
            "created_at": "2020-04-27T15:46:47.590126",
            "updated_at": "2020-04-27T16:05:56.518344",
            "status": "placed",
            "extra": {},
            "cart": self.some_card.id,
            "delivery_method": self.some_delivery_method.id,
            "delivery_address": self.some_delivery_adders.id,
            "payment_method": self.some_payment.id
        }, format='json', )
        self.assertEqual(response.status_code, 200)

    def test_patch_order(self):
        _id = self.some_oder.id
        response = self.client.patch(f'{self.URL}{_id}/', data={

            "total": 0,
            "created_at": "2020-04-27T15:46:47.590126",
            "updated_at": "2020-04-27T16:05:56.518344",
            "status": "placed",
            "extra": {},
            "cart": self.some_card.id,
            "delivery_method": self.some_delivery_method.id,
            "delivery_address": self.some_delivery_adders.id,
            "payment_method": self.some_payment.id
        }, format='json', )
        self.assertEqual(response.status_code, 200)

    def test_delete_order(self):
        _id = self.some_oder.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True, )
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
        _id = self.some_oder.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True, )
        self.assertEquals(response.status_code, 403)
