from rest_framework import serializers
from ..models import Collection, CollectionItem
from django.conf import settings


class CollectionItemSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        try:
            image = settings.SITE_URL + obj.sku.image.url
        except:
            image = ''
        return {
            'id': obj.sku.size.id,
            'title': obj.sku.size.get_size_name(),
            'color': obj.sku.color.color,
            'color_name': obj.sku.color.title,
            'color_id': obj.sku.color.id,
            'image': image
        }

    class Meta:
        model = CollectionItem
        fields = ['size', 'redeemed']


class CollectionItemsRowSerializer(serializers.ModelSerializer):

    row = serializers.SerializerMethodField()

    def get_row(self, obj):
        return []

    class Meta:
        model = CollectionItem
        fields = ['row', ]


class CollectionSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()
    is_grid = serializers.SerializerMethodField()
    is_status = serializers.SerializerMethodField()

    def get_items(self, obj):
        """if obj.product.get_condition().rc_type == 1:
            result = []
            for items_row in obj.get_items_rows():
                result.append(CollectionItemSerializer(items_row, many=True).data)
            return result"""
        return CollectionItemSerializer(obj.collection_items.all(), many=True).data

    def get_is_grid(self, obj):
        if obj.product.get_condition().rc_type == 1:
            return True
        return False

    def get_is_status(self, obj):
        if obj.status == 0:
            return 'IN_COLLECTION'
        else:
            return 'COLLECTED'

    class Meta:
        model = Collection
        fields = ['id', 'is_grid', 'is_status', 'product', 'items']
