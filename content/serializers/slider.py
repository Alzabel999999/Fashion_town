from rest_framework import serializers
from ..models import Slider, SliderImage
from ..mixins.serializers import FullImagePathMixin


class SliderImageSerializer(FullImagePathMixin, serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = ['slider', 'url', 'image', 'image_thumb', 'title', 'content', 'ordering', ]


class SliderSerializer(serializers.ModelSerializer):
    sliderimage_set = SliderImageSerializer(many=True, read_only=True)

    class Meta:
        model = Slider
        fields = ['title', 'slider_type', 'sliderimage_set']
