from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest
from ..models import Category, ProductImage


class ProductViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/catalog/product/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_product = self.create_product()
        self.some_product_image = ProductImage.objects.create(product=self.some_product)
        self.some_category = Category.objects.create(title='qwerty')

        self.fixtures = {
            "productimage_set": [
                {"product": self.some_product_image.id}
            ],
            "title": "Это поле обязательно.",
            "price": 22
        }


class ProductTest(ProductViewTest):

    def test_get_product(self):
        response = self.client.get(f'{self.URL}', format='json')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_product(self):
        response = self.client.post(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 201)

    def test_put_product(self):
        _id = self.some_product.id
        response = self.client.put(f'{self.URL}{_id}/',
                                   data={"title": "bbbb", "productimage_set": [
                                       {"product": self.some_product_image.id}
                                   ], "price": 666}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_product(self):
        _id = self.some_product.id
        response = self.client.patch(f'{self.URL}{_id}/', data={'title': 'bbbb'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        _id = self.some_product.id
        response = self.client.delete(f'{self.URL}{_id}/', self.fixtures, format='json', follow=True)
        self.assertEquals(response.status_code, 204)

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
        _id = self.some_product.id
        response = self.client.delete(f'{self.URL}{_id}/', format='json', follow=True)
        self.assertEquals(response.status_code, 403)
