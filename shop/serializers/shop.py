from rest_framework import serializers
from ..models import Shop
from user.models import Profile


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ShopCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    domain = serializers.CharField()

    class Meta:
        model = Shop
        fields = '__all__'
        extra_kwargs = {
            'profile': {'write_only': True, 'required': True},
            'domain': {'write_only': True, 'required': True},
            'title': {'write_only': True, 'required': True},
            'first_name': {'write_only': True, 'required': True},
            'middle_name': {'write_only': True, 'required': True},
            'last_name': {'write_only': True, 'required': True},
            'comment': {'write_only': True, 'required': True}
        }


class ShopUpdateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Shop
        fields = '__all__'
        extra_kwargs = {
            'profile': {'read_only': True},
            'site': {'read_only': True},
            'first_name': {'read_only': True},
            'middle_name': {'read_only': True},
            'last_name': {'read_only': True},
            'comment': {'read_only': True},
            'is_active': {'read_only': True},
        }
