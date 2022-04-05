from rest_framework import serializers
from ..models import LivePhotoAlbum, LivePhotoImage, LivePhotoVideo
from ..mixins.serializers import FullImagePathMixin
from django.conf import settings


class LivePhotoImageSerializer(FullImagePathMixin, serializers.ModelSerializer):
    class Meta:
        model = LivePhotoImage
        fields = ['id', 'description', 'album', 'image', 'image_thumb', 'ordering', ]


class LivePhotoVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField(read_only=True)
    video_preview = serializers.SerializerMethodField(read_only=True)

    def get_video(self, obj):
        return obj.get_video()

    def get_video_preview(self, obj):
        return obj.get_video_preview()

    class Meta:
        model = LivePhotoVideo
        fields = ['id', 'description', 'album', 'video', 'video_preview', 'ordering', ]


class LivePhotoAlbumSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField(read_only=True)
    livephotoimage_set = serializers.SerializerMethodField()
    livephotovideo_set = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    image_thumb = serializers.SerializerMethodField()

    def get_brand(self, obj):
        return {
            'id': obj.brand.id if obj.brand else None,
            'title': obj.brand.title if obj.brand else None,
        }

    def get_livephotoimage_set(self, obj):
        return LivePhotoImageSerializer(obj.live_photo_photos.all(), many=True).data

    def get_livephotovideo_set(self, obj):
        return LivePhotoVideoSerializer(obj.live_photo_videos.all(), many=True).data

    def get_image(self, obj):
        return settings.SITE_URL + obj.image.url

    def get_image_thumb(self, obj):
        return settings.SITE_URL + obj.image_thumb

    class Meta:
        model = LivePhotoAlbum
        fields = [
            'id', 'title', 'brand', 'slug',
            'content', 'image', 'image_thumb',
            'livephotoimage_set', 'livephotovideo_set',
            'created_at', 'updated_at', 'ordering',
            'seo_title', 'seo_keywords', 'seo_description', 'seo_author',
            'seo_og_type', 'seo_image',
            'objects', 'on_site',
        ]


class LivePhotoAlbumListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    brand = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    def get_image(self, obj):
        if obj.get_image():
            return settings.SITE_URL + obj.get_image().url
        return '#'

    def get_brand(self, obj):
        return obj.brand.title if obj.brand else ''

    def get_url(self, obj):
        return obj.slug

    class Meta:
        model = LivePhotoAlbum
        fields = ['id', 'title', 'brand', 'image', 'created_at', 'url', ]
