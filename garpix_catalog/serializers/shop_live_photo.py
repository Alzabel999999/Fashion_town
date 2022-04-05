from django.conf import settings
from rest_framework import serializers
from ..models import LivePhotoAlbum, LivePhotoImage, LivePhotoVideo, ShopLivePhoto


class CabinetLivePhotoImageSerializer(serializers.ModelSerializer):

    is_selected = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_is_selected(self, obj):
        album = self.context['album']
        return album.check_media_selected(obj) if album else False

    def get_image(self, obj):
        return settings.SITE_URL + obj.image_thumb

    def get_type(self, obj):
        return 'image'

    class Meta:
        model = LivePhotoImage
        fields = ['id', 'is_selected', 'image', 'type']


class CabinetLivePhotoVideoSerializer(serializers.ModelSerializer):

    is_selected = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_is_selected(self, obj):
        album = self.context['album']
        return album.check_media_selected(obj) if album else False

    def get_image(self, obj):
        return settings.SITE_URL + obj.video_preview.url

    def get_type(self, obj):
        return 'video'

    class Meta:
        model = LivePhotoVideo
        fields = ['id', 'is_selected', 'image', 'type']


class CabinetLivePhotoSerializer(serializers.ModelSerializer):

    is_selected = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_is_selected(self, obj):
        album = ShopLivePhoto.get_album(album=obj, shop=get_shop(data=self))
        return album.is_selected if album else False

    def get_title(self, obj):
        album = ShopLivePhoto.get_album(album=obj, shop=get_shop(data=self))
        return {
            'origin_title': obj.title,
            'my_title': album.title if album else ''
        }

    def get_brand(self, obj):
        return {
            'id': obj.brand.id,
            'title': obj.brand.title
        }

    def get_items(self, obj):
        album = ShopLivePhoto.get_album(album=obj, shop=get_shop(data=self))
        images = CabinetLivePhotoImageSerializer(obj.live_photo_photos.all(), many=True, context={'album': album}).data
        videos = CabinetLivePhotoVideoSerializer(obj.live_photo_videos.all(), many=True, context={'album': album}).data
        return images + videos

    class Meta:
        model = LivePhotoAlbum
        fields = ['id', 'is_selected', 'title', 'brand', 'items']


def get_shop(data):
    shop = data.context['request'].user.profile.profile_shop
    if shop:
        return shop
    return None
