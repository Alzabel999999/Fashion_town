from rest_framework import serializers
from ..models import DeliveryAddress, Country


class DeliveryAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    country = serializers.SerializerMethodField(read_only=True)

    def get_country(self, obj):
        return obj.country.__str__()

    class Meta:
        model = DeliveryAddress
        fields = [
            'user', 'id', 'profile', 'post_code', 'country', 'city', 'street', 'house', 'flat',
            'first_name', 'middle_name', 'last_name', 'phone',
        ]
        extra_kwargs = {
            'profile': {'read_only': True}
        }

    def create(self, validated_data):
        user = validated_data.pop('user')
        validated_data.update({'profile': user.profile})
        if user.profile.role in [1, 3] and user.profile.profile_addresses.all().count() >= 3:
            raise serializers.ValidationError('Слишком много адресов')
        try:
            country_id = self.context['request'].data['country']
            country = Country.objects.filter(id=country_id).first()
            validated_data.update({'country': country})
        except Exception as e:
            raise serializers.ValidationError('wrong country id')
        return super(DeliveryAddressSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        validated_data.update({'profile': user.profile})
        return super(DeliveryAddressSerializer, self).update(instance, validated_data)
