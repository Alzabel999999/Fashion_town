from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest
from django.conf import settings
from ..models.banner import Banner


class BannerViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/content/banner/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.some_banner = self.create_banner(ordering=2, is_active=True, content="some some some",
                                              url="https://git-scm.com/", target_blank=True, css_class="",
                                              banner_type=settings.BANNER_TYPE_MAIN_NEAR_SLIDER)

        self.fixtures = {'ordering': 2,
                         'title': 'fff',
                         'title_ru': 'some some some',
                         'is_active': True,
                         'content': 'fff',
                         'content_ru': 'ffff',
                         'url': 'fff',
                         'target_blank': True,
                         'css_class': 'Truffe',
                         'banner_type': settings.BANNER_TYPE_MAIN_NEAR_SLIDER}


class BannerTest(BannerViewTest):

    def test_get_banner(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_banner(self):
        response = self.client.post(f'{self.URL}', self.fixtures)
        self.assertEqual(response.status_code, 201)

    def test_put_banner(self):
        _id = self.some_banner.id
        response = self.client.put(f'{self.URL}{_id}/', self.fixtures, format='json', )
        self.assertEqual(response.status_code, 200)

    def test_patch_banner(self):
        _id = self.some_banner.id
        response = self.client.patch(f'{self.URL}{_id}/', self.fixtures, format='json', )
        self.assertEqual(response.status_code, 200)

    def test_delete_banner(self):
        _id = self.some_banner.id
        response = self.client.delete(f'{self.URL}{_id}/', self.fixtures, format='json', follow=True, )
        self.assertEquals(response.status_code, 204)

    def test_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    def test_access(self):
        self.user = get_user_model().objects.create_user(
            email='test@gg12.com',
            password='testpass12',
            username='test12')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 403)

    def test_banner(self):
        obj = Banner.objects.create(title='Test Banner')
        self.assertEqual(str(obj), obj.title)
