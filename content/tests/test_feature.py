from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest


class FeatureViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/content/feature/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_feature = self.create_feature(is_active=True, content="some some some")

        self.fixtures = {
            "ordering": 0,
            "title": "string",
            "title_ru": "string",
            "is_active": True,
            "content": "string",
            "content_ru": "string"
        }


class FeatureTest(FeatureViewTest):

    def test_get_feature(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_feature(self):
        response = self.client.post(f'{self.URL}', self.fixtures)
        self.assertEqual(response.status_code, 201)

    def test_put_feature(self):
        _id = self.some_feature.id
        response = self.client.put(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_feature(self):
        _id = self.some_feature.id
        response = self.client.patch(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_feature(self):
        _id = self.some_feature.id
        response = self.client.delete(f'{self.URL}{_id}/', self.fixtures, format='json', follow=True)
        self.assertEquals(response.status_code, 204)

    def test_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    def test_access(self):
        self.user = get_user_model().objects.create_user(
            email='test@gg1.com',
            password='testpass51',
            username='test51',
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 403)
