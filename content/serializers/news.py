from ..models import News, NewsRubric
from rest_framework import serializers



class NewsRubricSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsRubric
        fields = ['id', 'title']


class NewsSerializer(serializers.ModelSerializer):

    rubrics = serializers.SerializerMethodField(read_only=True)
    media = serializers.SerializerMethodField()

    def get_rubrics(self, obj):
        return NewsRubricSerializer(obj.rubrics, many=True).data

    def get_media(self, obj):
        return obj.get_media()

    class Meta:
        model = News
        fields = [
            'id', 'slug', 'title',
            'rubrics', 'description', 'content',
            'is_for_retailer', 'is_for_wholesaler', 'is_for_dropshipper',
            'image', 'image_thumb', 'media',
            'created_at', 'updated_at',
            'seo_title', 'seo_keywords', 'seo_description',
            'seo_author', 'seo_og_type', 'seo_image',
            'objects', 'on_site'
        ]


class NewsListSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    rubrics = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        return obj.slug

    def get_image(self, obj):
        return obj.get_image()

    def get_rubrics(self, obj):
        return NewsRubricSerializer(obj.rubrics, many=True).data

    class Meta:
        model = News
        fields = ['id', 'title', 'url', 'created_at', 'image', 'rubrics']
