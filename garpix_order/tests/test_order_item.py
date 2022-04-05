# import os
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient, APITestCase
# from django.conf import settings
#
# from ..models import DeliveryMethod, DeliveryAddress, PaymentMethod
# from ..models.order import Order
# from garpix_cart_rest.models import Cart
#
#
# class OrderItemViewTest(APITestCase):
#
#     def setUp(self):
#         self.URL = '/api/v1/order/order/'
#         self.user = get_user_model().objects.create_user(
#             email='test@gg.com',
#             password='testpass',
#             username='test',
#             is_superuser=True,
#             is_staff=True,
#             buyer_role=1
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         self.some_delivery_method = DeliveryMethod.objects.create(
#             image_thumb="", ordering=3, title="qwerty",
#             created_at="2020-04-27T11:46:13.970752",
#             updated_at="2020-04-27T11:46:13.970774",
#             is_active=True, content="", type="pickup")
#         self.some_delivery_adders = DeliveryAddress.objects.create(is_active=True, address='qwerty', user=self.user)
#         self.some_card = Cart.objects.create(is_active=True, session='qwerty', extra='', user=self.user)
#         self.some_payment = PaymentMethod.objects.create(title='ff', is_active=True, content="some some some",
#                                                          type='cash'
#                                                          )
#         self.some_oder = Order.objects.create(status='placed', extra={},
#                                               cart=self.some_card,
#                                               delivery_method=self.some_delivery_method,
#                                               delivery_address=self.some_delivery_adders,
#                                               payment_method=self.some_payment
#
#                                               )
#
#         self.fixtures = {
#
#             "status": "placed",
#
#             "cart": self.some_card.id,
#             "delivery_method": self.some_delivery_method.id,
#             "delivery_address": self.some_delivery_adders.id,
#             "payment_method": self.some_payment.id
#         }
#
# class OrderItemTest(OrderItemViewTest):
#
#     def test_post_order_item(self):
#         response = self.client.get(f'{self.URL}')
