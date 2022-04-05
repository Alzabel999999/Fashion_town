from rest_framework import serializers
from garpix_catalog.models import Brand


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'title']
