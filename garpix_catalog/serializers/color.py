from ..models import Color
from rest_framework import serializers


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ('id', 'title', 'color')
