from django.conf import settings
from rest_framework import serializers
from config.models import RoleConfiguration


class RoleConfigurationSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    public_offer = serializers.SerializerMethodField()

    def get_role(self, obj):
        return {'number': obj.role, 'name': obj.get_role_display()}

    def get_public_offer(self, obj):
        return settings.SITE_URL + obj.public_offer.url if obj.public_offer else '#'

    class Meta:
        model = RoleConfiguration
        fields = ['role', 'delivery_condition', 'payment_info', 'public_offer']
