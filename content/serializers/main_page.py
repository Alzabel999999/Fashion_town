from django.db.models import Count
from rest_framework import serializers
from ..models import MainPage


class FirstScreenSerializer(serializers.ModelSerializer):

    filters = serializers.SerializerMethodField(read_only=True)

    def get_filters(self, obj):
        filters = []
        for category in obj.filters.all():
            if category.category_products.count() > 0:
                filters.append({'url': category.slug, 'title': category.title, 'id': category.id})
        return filters

    class Meta:
        model = MainPage
        fields = ['title', 'overtitle', 'undertitle', 'filters', 'image']


class MainPageSerializer(serializers.ModelSerializer):

    first_screen = serializers.SerializerMethodField()
    in_stock_product_filters = serializers.SerializerMethodField()

    def get_first_screen(self, obj):
        return FirstScreenSerializer(obj).data

    def get_in_stock_product_filters(self, obj):
        from garpix_catalog.models import Category
        filters = []
        categories = Category.objects.filter(
            category_products__is_in_stock=True, category_products__product_skus__in_stock_count__gt=0).distinct()[:5]
        for category in categories:
            if category.category_products.count() > 0:
                filters.append({'title': category.title, 'id': category.id})
        return filters

    class Meta:
        model = MainPage
        fields = ['first_screen', 'in_stock_product_filters']
