from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest


class MenuItemViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/content/menu_item/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_menu_item = self.create_menu_item(title="", page=None, is_active=True, url='', target_blank=True,
                                                    css_class='', edition_style='', is_only_for_authenticated=False)

        self.fixtures = {'ordering': 2,
                         'title': 'fff',
                         'title_ru': 'some some some',
                         'is_active': True,
                         'content': 'fff',
                         'content_ru': 'ffff',
                         'url': 'fff',
                         'target_blank': True,
                         'css_class': 'Truffe',
                         }


class MenuItemTest(MenuItemViewTest):

    def test_get_menu_item(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_menu_item(self):
        response = self.client.post(f'{self.URL}', self.fixtures)
        self.assertEqual(response.status_code, 201)

    def test_put_menu_item(self):
        _id = self.some_menu_item.id
        response = self.client.put(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_menu_item(self):
        _id = self.some_menu_item.id
        response = self.client.patch(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_menu_item(self):
        _id = self.some_menu_item.id
        response = self.client.delete(f'{self.URL}{_id}/', self.fixtures, format='json', follow=True)
        self.assertEquals(response.status_code, 204)

    def test_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    def test_access(self):
        self.user = get_user_model().objects.create_user(
            email='test@g3g1.com',
            password='testpfass1',
            username='testf1',
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 403)
