from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from ..models import Category
from ..serializers import ProductListSerializer
from ..mixins.serializers import FullImagePathMixin


class CatalogSerializer(FullImagePathMixin, serializers.ModelSerializer):
    children = RecursiveField(required=False, many=True)
    product_set = ProductListSerializer(required=False, many=True)

    class Meta:
        model = Category
        fields = ['parent', 'page_type', 'title', 'is_active',
                  'slug', 'created_at', 'updated_at',
                  'seo_title', 'seo_keywords', 'seo_description',
                  'seo_author', 'seo_og_type', 'seo_image', 'content',
                  'image', 'image_thumb', 'ordering',
                  'objects', 'on_site', ]
