from rest_framework import serializers
from ..models import Announce


class AnnounceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announce
        fields = ['id', 'url', 'target_blank', 'background', 'content']
