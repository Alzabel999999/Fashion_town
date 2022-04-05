from django.conf import settings
from rest_framework import serializers
from ..models import DeliveryMethod


class DeliveryMethodSerializer(serializers.ModelSerializer):

    need_passport = serializers.SerializerMethodField()

    def get_need_passport(self, obj):
        return settings.DELIVERY_TYPES[obj.type]['need_passport']

    class Meta:
        model = DeliveryMethod
        fields = ['id', 'title', 'type', 'need_passport']
