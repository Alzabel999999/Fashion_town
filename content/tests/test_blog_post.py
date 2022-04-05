from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .base import BaseViewTest
from django.conf import settings
from ..models import Tag


class BlogPostViewTest(BaseViewTest):
    def setUp(self):
        self.URL = '/api/v1/content/blog_post/'
        self.user = get_user_model().objects.create_user(
            email='test@gg.com',
            password='testpass',
            username='test',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.some_blog_post = self.create_blog_post(
            title="ffff")
        self.some_teg = Tag.objects.create(title='blablabla')
        self.fixtures = {
            'title': 'fff',
            'title_ru': 'some some some',
            'is_active': True,
            'slug': 'fff',
            'seo_title': 'ffff',
            'seo_keywords': 'fff',
            'seo_description': True,
            'seo_author': 'Truffe',
            'seo_og_type': 'ewghvsds',
            'content': 'ewgeehvsds',
            "sites": [
                f'{settings.SITE_ID}'
            ],
            "tags": [
                f'{self.some_teg.id}'
            ]
        }


class PostBlogTest(BlogPostViewTest):

    def test_get_blog_post(self):
        response = self.client.get(f'{self.URL}')
        self.assertEqual(response.status_code, 200, msg=response.data.get('error'))

    def test_create_blog_post(self):
        response = self.client.post(f'{self.URL}', self.fixtures)
        self.assertEqual(response.status_code, 201)

    def test_put_blog_post(self):
        _id = self.some_blog_post.id
        response = self.client.put(f'{self.URL}{_id}/', data={'title': 'ggggggggg'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_blog_post(self):
        _id = self.some_blog_post.id
        response = self.client.patch(f'{self.URL}{_id}/', data={'title': 'ggggggggg'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_blog_post(self):
        _id = self.some_blog_post.id
        response = self.client.delete(f'{self.URL}{_id}/', self.fixtures, format='json', follow=True)
        self.assertEquals(response.status_code, 204)

    def test_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 401)

    def test_access(self):
        self.user = get_user_model().objects.create_user(
            email='test@gg13.com',
            password='testpass13',
            username='test31',
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.URL}', self.fixtures, format='json')
        self.assertEqual(response.status_code, 403)
