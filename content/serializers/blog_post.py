from rest_framework import serializers
from ..models import BlogPost
from ..mixins.serializers import FullImagePathMixin


class BlogPostSerializer(FullImagePathMixin, serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ['tags', 'title', 'is_active', 'slug', 'sites', 'created_at', 'updated_at', 'seo_title',
                  'seo_keywords', 'seo_description', 'seo_author', 'seo_og_type', 'seo_image', 'content',
                  'ordering', 'image', 'image_thumb', ]
