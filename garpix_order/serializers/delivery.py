from rest_framework import serializers
from ..models import Delivery


class DeliverySerializer(serializers.ModelSerializer):

    order_number = serializers.SerializerMethodField()

    def get_order_number(self, obj):
        return obj.order.order_number

    class Meta:
        model = Delivery
        fields = ['id', 'order', 'order_number', 'cost', 'status']
