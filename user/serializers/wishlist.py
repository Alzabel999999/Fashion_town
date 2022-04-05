from rest_framework import serializers
from ..models import WishListItem
from garpix_catalog.serializers import ProductListSerializer


class WishListSerializer(serializers.ModelSerializer):

    product = ProductListSerializer()

    class Meta:
        model = WishListItem
        fields = ['id', 'profile', 'product', ]


class WishListCreateSerializer(serializers.ModelSerializer):

    def validate_empty_values(self, data):
        data = data.copy()
        user = self.context['request'].user
        profile = user.profile
        data['profile'] = profile.id
        return super(WishListCreateSerializer, self).validate_empty_values(data)

    def validate(self, data):
        return super(WishListCreateSerializer, self).validate(data)

    def create(self, validated_data):
        profile = self.validated_data['profile']
        product = self.validated_data['product']
        wishlist_item = WishListItem.objects.filter(profile=profile, product=product).first()
        if wishlist_item:
            return wishlist_item
        wishlist_item = WishListItem.objects.create(profile=profile, product=product)
        return wishlist_item

    class Meta:
        model = WishListItem
        fields = ['product', 'profile']
