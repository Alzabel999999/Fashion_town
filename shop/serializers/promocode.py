from rest_framework import serializers
from ..models import Promocode


class PromocodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promocode
        fields = ['id', 'is_active', 'title', 'discount', 'usage_count']

        extra_kwargs = {
            'usage_count': {'read_only': True},
        }
