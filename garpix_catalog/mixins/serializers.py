from django.conf import settings
from rest_framework import serializers
from .content import ImageMixin


class FullImagePathMixin(serializers.Serializer):
    image = serializers.SerializerMethodField()
    image_thumb = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return settings.SITE_URL + obj.image.url

    def get_image_thumb(self, obj):
        if obj.image_thumb:
            return settings.SITE_URL + obj.image_thumb


class ImageSerializer(serializers.Serializer):

    class Meta:
        model = ImageMixin
        fields = 'image'
