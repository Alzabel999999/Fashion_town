from django.conf import settings
from rest_framework import serializers
from garpix_catalog.models import Product


class SearchProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_price(self, obj):
        user = self.context['user']
        if user.is_authenticated:
            if user.profile.role == user.profile.ROLE.WHOLESALE:
                return obj.wholesaller_price_auto
            if user.profile.role == user.profile.ROLE.DROPSHIPPER:
                return obj.dropshipper_price_auto
            return obj.retailer_price_auto
        else:
            return obj.retailer_price_auto

    def get_image(self, obj):
        return settings.SITE_URL + obj.image_thumb

    class Meta:
        model = Product
        fields = ['title', 'slug', 'image', 'price']
