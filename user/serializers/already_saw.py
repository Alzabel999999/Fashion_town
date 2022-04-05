from rest_framework import serializers
from ..models import AlreadySaw
from garpix_catalog.serializers import ProductListSerializer


class AlreadySawSerializer(serializers.ModelSerializer):

    product = ProductListSerializer()

    class Meta:
        model = AlreadySaw
        fields = ['id', 'profile', 'product', ]


class AlreadySawCreateSerializer(serializers.ModelSerializer):

    def validate_empty_values(self, data):
        data = data.copy()
        user = self.context['request'].user
        profile = user.profile
        data['profile'] = profile.id
        return super(AlreadySawCreateSerializer, self).validate_empty_values(data)

    def validate(self, data):
        return super(AlreadySawCreateSerializer, self).validate(data)

    def create(self, validated_data):
        profile = self.validated_data['profile']
        product = self.validated_data['product']
        already_saw = AlreadySaw.objects.filter(profile=profile, product=product).first()
        if already_saw:
            return already_saw
        already_saw = AlreadySaw.objects.create(profile=profile, product=product)
        return already_saw

    class Meta:
        model = AlreadySaw
        fields = ['product', 'profile']
