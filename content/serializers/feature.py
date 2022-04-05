from rest_framework import serializers
from ..models import Feature
from ..mixins.serializers import FullImagePathMixin


class FeatureSerializer(FullImagePathMixin, serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = ['is_active', 'content', 'image', 'image_thumb', 'ordering',
                  'created_at', 'updated_at', 'title', ]
