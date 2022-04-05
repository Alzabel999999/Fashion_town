from rest_framework import serializers
from ..models import Producer
from ..mixins.serializers import FullImagePathMixin


class ProducerSerializer(FullImagePathMixin, serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ['is_active', 'image', 'image_thumb',
                  'ordering', 'created_at', 'updated_at', 'title', ]
