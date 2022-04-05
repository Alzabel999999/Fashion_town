from rest_framework import serializers
from ..models import Requisites


class RequisitesSerializer(serializers.ModelSerializer):

    requisites = serializers.SerializerMethodField()

    def get_requisites(self, obj):
        requisites = [f"<p>{requisites_str}</p>" for requisites_str in obj.requisites.split('\r\n')]
        return ''.join(requisites)

    class Meta:
        model = Requisites
        fields = ['id', 'requisites']
