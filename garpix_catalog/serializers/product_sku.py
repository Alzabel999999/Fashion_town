from rest_framework import serializers
from ..models import ProductSku, ProductSkuImage
from ..mixins.serializers import FullImagePathMixin
from django.conf import settings


class ProductSkuImageSerializer(FullImagePathMixin, serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductSkuImage
        fields = ['id', 'product_sku', 'description', 'image', 'image_thumb', 'ordering', ]

    def get_image(self, obj):
        return settings.SITE_URL + obj.image


class ProductSkuSerializer(serializers.ModelSerializer):
    productskuimage_set = ProductSkuImageSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductSku
        fields = [
            'id', 'product', 'size', 'color', 'weight', 'price',
            'in_stock_count', 'orders_count',
            'is_in_stock',  #'is_new', 'is_closeout','is_bestseller',
            'content', 'image', 'image_thumb',
            'created_at', 'updated_at', 'ordering',
            'seo_title', 'seo_keywords', 'seo_description',
            'seo_author', 'seo_og_type', 'seo_image',
            'objects', 'on_site', 'productskuimage_set'
        ]

    def get_image(self, obj):
        try:
            return settings.SITE_URL + obj.image.url
        except:
            return '-'
