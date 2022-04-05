from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from ..models.cart import Cart


class CardViewTest(APITestCase):
    def setUp(self):
        self.URL = '/api/v1/cart/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_card = Cart.objects.create(is_active=True, session='qwerty', extra='', user=self.user)

        self.fixtures = {
            "cartitem_set": [

            ],
            "is_active": True,
            "session": "string",
            "extra": {}
        }


class CardTest(CardViewTest):

    def test_get_card(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_card(self):
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 201)

    def test_delete_card(self):
        _id = self.some_card.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 204)

    def test_get_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    def test_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    def test_access(self):
        self.user = get_user_model().objects.create_user(
            email='test@gg1.com',
            password='testpass1',
            username='test1',
        )
        self.client.force_authenticate(user=self.user)
        _id = self.some_card.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 403)
