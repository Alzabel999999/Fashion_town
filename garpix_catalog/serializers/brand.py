from rest_framework import serializers
from ..models import Brand


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'title', 'description', 'image', 'brand_rc', ]


class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'title']