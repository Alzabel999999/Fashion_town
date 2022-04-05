from django.conf import settings
from rest_framework import serializers
from garpix_page.models import Page, ComponentChildren, Component


class PageComponentChildrenSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return settings.SITE_URL + obj.image.url
        else:
            return '#'

    class Meta:
        model = ComponentChildren
        fields = ['id', 'title', 'title_ru', 'content', 'content_ru', 'image', 'sort']


class PageComponentSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_children(self, obj):
        return PageComponentChildrenSerializer(obj.componentchildren_set.all(), many=True).data

    def get_image(self, obj):
        if obj.image:
            return settings.SITE_URL + obj.image.url
        else:
            return '#'

    class Meta:
        model = Component
        fields = ['id', 'title', 'title_ru', 'content', 'content_ru', 'image', 'sort', 'children']


class PageSerializer(serializers.ModelSerializer):

    components = serializers.SerializerMethodField()

    def get_components(self, obj):
        try:
            return PageComponentSerializer(obj.get_components(), many=True).data
        except Exception:
            return []

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'title_ru', 'slug', 'created_at', 'updated_at',
            'seo_title', 'seo_title_ru', 'seo_keywords', 'seo_keywords_ru',
            'seo_description', 'seo_description_ru', 'seo_author', 'seo_author_ru',
            'seo_og_type', 'seo_image',
            'objects', 'content', 'content_ru',
            'parent', 'page_type', 'login_required',
            'components',
        ]
