from rest_framework import serializers
from ..models import Likes


class LikesSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField

    class Meta:
        model = Likes
        fields = ['id', 'profile', 'review', 'is_active', ]


class CreateLikesSerializer(serializers.ModelSerializer):

    def validate_empty_values(self, data):
        data = data.copy()
        user = self.context['request'].user
        profile = user.profile
        data['profile'] = profile.id
        return super(CreateLikesSerializer, self).validate_empty_values(data)

    def get_unique_together_validators(self):
        return []

    def validate(self, data):
        return super(CreateLikesSerializer, self).validate(data)

    def create(self, validated_data):
        profile = self.context['request'].user.profile
        like = Likes.objects.filter(profile=profile, review=validated_data['review']).first()
        if like:
            like.is_active = not like.is_active
            like.save()
            return like
        like = Likes.objects.create(
            profile=profile,
            review=validated_data['review'],
            is_active=True,
        )
        return like

    class Meta:
        model = Likes
        fields = ['id', 'profile', 'review', 'is_active', ]


class UpdateLikesSerializer(serializers.ModelSerializer):

    def validate_empty_values(self, data):
        data = data.copy()
        user = self.context['request'].user
        profile = user.profile
        data['profile'] = profile.id
        return super(UpdateLikesSerializer, self).validate_empty_values(data)

    def get_unique_together_validators(self):
        return []

    def validate(self, data):
        return super(UpdateLikesSerializer, self).validate(data)

    def update(self, instance, validated_data):
        instance.is_active = not instance.is_active
        instance.save()
        return instance

    class Meta:
        model = Likes
        fields = ['id', 'profile', 'review', 'is_active', ]
