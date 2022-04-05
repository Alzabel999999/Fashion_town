from rest_framework import serializers
from ..models import Banner
from ..mixins.serializers import FullImagePathMixin


class BannerSerializer(FullImagePathMixin, serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['id', 'url', 'target_blank', 'css_class', 'banner_type', 'footnote',
                  'is_active', 'content', 'image', 'image_thumb',
                  'ordering', 'created_at', 'updated_at', 'title', 'objects']
