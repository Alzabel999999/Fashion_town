from rest_framework import serializers
from ..models import ShopRequisites


class ShopRequisitesSerializer(serializers.ModelSerializer):

    requisites = serializers.SerializerMethodField()

    def get_requisites(self, obj):
        if '\r\n' in obj.requisites:
            requisites = [f"<p>{requisites_str}</p>" for requisites_str in obj.requisites.split('\r\n')]
        else:
            requisites = [f"<p>{requisites_str}</p>" for requisites_str in obj.requisites.split('\n')]
        return ''.join(requisites)

    class Meta:
        model = ShopRequisites
        fields = ['id', 'requisites']

    def validate(self, attrs):
        requisites = self.context['request'].data.get('requisites', '')
        attrs.update({'requisites': requisites})
        shop = self.context['request'].user.profile.profile_shop
        attrs.update({'shop': shop})
        return attrs
