from rest_framework import serializers
from ..models import Product, Currency, ShopProduct, Category, ShopCategoryMarkup
from django.conf import settings
from shop.models import Shop


class CabinetCategoryMarkupListSerializer(serializers.ModelSerializer):

    category_id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    category_markup_id = serializers.SerializerMethodField()
    markup = serializers.SerializerMethodField()

    def get_category_id(self, obj):
        return obj.id

    def get_title(self, obj):
        return obj.title

    def get_category_markup_id(self, obj):
        markup = get_category_markup(obj, self)
        if markup:
            return markup.id
        return None

    def get_markup(self, obj):
        markup = get_category_markup(obj, self)
        if markup:
            return markup.markup
        return None

    class Meta:
        model = Category
        fields = ['category_id', 'title', 'category_markup_id', 'markup']


class CabinetCategoryMarkupCreateSerializer(serializers.ModelSerializer):

    category_id = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    category_markup_id = serializers.SerializerMethodField(read_only=True)

    def get_category_id(self, obj):
        return obj.category.id

    def get_title(self, obj):
        return obj.category.title

    def get_category_markup_id(self, obj):
        return obj.id

    class Meta:
        model = ShopCategoryMarkup
        fields = ['category_id', 'title', 'category_markup_id', 'markup']


class CabinetCategoryMarkupUpdateSerializer(serializers.ModelSerializer):

    category_id = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    category_markup_id = serializers.SerializerMethodField(read_only=True)

    def get_category_id(self, obj):
        return obj.category.id

    def get_title(self, obj):
        return obj.category.title

    def get_category_markup_id(self, obj):
        return obj.id

    class Meta:
        model = ShopCategoryMarkup
        fields = ['category_id', 'title', 'category_markup_id', 'markup']


def get_category_markup(category, data):
    shop = data.context['request'].user.profile.profile_shop
    markup = category.category_markups.filter(shop=shop).first()
    return markup
