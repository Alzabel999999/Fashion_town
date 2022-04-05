from rest_framework import serializers
from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """messages = serializers.SerializerMethodField()

    def get_messages(self, obj):
        return {
            'id': obj.id,
            'profile': obj.profile,
            'message': obj.message,
            'created_at': obj.created_at,
            'is_read': obj.is_read,
        }"""


    class Meta:
        model = Notification
        fields = ['id', 'profile', 'message', 'created_at', 'is_read']#, 'created_at', 'is_read'

class NotificationListSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()


    def get_items(self, obj):
        return NotificationSerializer(obj.all(), many=True).data

    class Meta:
        model = Notification
        fields = ['items']
