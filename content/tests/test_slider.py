from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest

from ..models import SliderImage


class SliderViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/content/slider/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.some_slider = self.create_slider(title='111')
        self.some_slider_img = SliderImage.objects.create(title='ff', content='fffff', ordering=1, url='qqq',
                                                          slider=self.some_slider)
        self.fixtures = {
            "sliderimage_set": [
                {
                    "title": "fff",
                    "slider": self.some_slider.id
                }
            ],
            "title": "string",
            "title_ru": "string",
            "slider_type": "main_page"
        }


class SliderTest(SliderViewTest):

    def test_get_slider(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_slider(self):
        response = self.client.post(f'{self.URL}', self.fixtures)
        self.assertEqual(response.status_code, 201)

    def test_put_slider(self):
        _id = self.some_slider.id
        response = self.client.put(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_slider(self):
        _id = self.some_slider.id
        response = self.client.patch(f'{self.URL}{_id}/', self.fixtures, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_slider(self):
        _id = self.some_slider.id
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
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 403)
