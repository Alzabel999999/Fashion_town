from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from ..models import Category, Product
from ..mixins.serializers import FullImagePathMixin


class CategorySerializer(FullImagePathMixin, serializers.ModelSerializer):
    children = RecursiveField(required=False, many=True)

    class Meta:
        model = Category
        fields = [
            'id', 'title', 'page_type', 'slug', 'parent', 'children',
            'content', 'image', 'image_thumb', 'ordering',
            'created_at', 'updated_at',
            'seo_title', 'seo_keywords', 'seo_description',
            'seo_author', 'seo_og_type', 'seo_image',
            'objects', 'on_site',
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    children = RecursiveField(required=False, many=True)
    count = serializers.SerializerMethodField()
    filter = serializers.SerializerMethodField()

    def get_count(self, obj):
        count = 0
        if obj.children.count() > 0:
            for child in obj.children.all():
                count += get_coursive_count(child)
        count += Product.objects.filter(category=obj).count()
        return count

    def get_filter(self, obj):
        return f'?category={obj.id}'

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'children', 'count', 'filter']


class CategoryRawListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        count = 0
        if obj.children.count() > 0:
            for child in obj.children.all():
                count += get_coursive_count(child)
        count += Product.objects.filter(category=obj).count()
        return count

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'count', ]


def get_coursive_count(category):
    count = 0
    if category.children.count() > 0:
        for child in category.children.all():
            count += get_coursive_count(child)
    count += Product.objects.filter(category=category).count()
    return count
