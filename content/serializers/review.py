from rest_framework import serializers
from ..models import Review, ReviewPhoto, ReviewVideo
from ..mixins.serializers import FullImagePathMixin


class ReviewPhotoSerializer(FullImagePathMixin, serializers.ModelSerializer):
    class Meta:
        model = ReviewPhoto
        fields = ['review', 'image', 'image_thumb']


class ReviewVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField(read_only=True)
    video_preview = serializers.SerializerMethodField(read_only=True)

    def get_video(self, obj):
        return obj.get_video()

    def get_video_preview(self, obj):
        return obj.get_video_preview()

    class Meta:
        model = ReviewVideo
        fields = ['review', 'video', 'video_preview']


class ReviewCabinetSerializer(serializers.ModelSerializer):

    review_type = serializers.SerializerMethodField(read_only=True)
    review_photos = serializers.SerializerMethodField(read_only=True)
    review_videos = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    def get_review_type(self, obj):
        if obj.product:
            return {'type': 'Отзыв о товаре', 'product': obj.product.title}
        else:
            return {'type': 'Отзыв о сервисе', 'product': None}

    def get_review_photos(self, obj):
        return ReviewPhotoSerializer(obj.review_photos.all(), many=True).data

    def get_review_videos(self, obj):
        return ReviewVideoSerializer(obj.review_videos.all(), many=True).data

    def get_status(self, obj):
        # todo добавить статус "отклонено"
        return 'Опубликовано' if obj.is_approved else 'На модерации'

    class Meta:
        model = Review
        fields = [
            'id', 'review_type', 'review_photos', 'review_videos', 'created_at', 'likes_count',
            'status', 'content', 'stars'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    review_photos = serializers.SerializerMethodField(read_only=True)
    review_videos = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    user_rating = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True, source='get_likes_count')
    is_current_user_liked = serializers.SerializerMethodField(read_only=True)
    current_user_like_id = serializers.SerializerMethodField(read_only=True)
    product_url = serializers.SerializerMethodField(read_only=True)
    review_rating = serializers.SerializerMethodField(read_only=True)

    def get_review_photos(self, obj):
        return ReviewPhotoSerializer(obj.review_photos.all(), many=True).data

    def get_review_videos(self, obj):
        return ReviewVideoSerializer(obj.review_videos.all(), many=True).data

    def get_user(self, obj):
        return obj.get_hidden_username()

    def get_user_rating(self, obj):
        from user.models import Profile
        if obj.profile:
            rating = Profile.objects.filter(id=obj.profile.id).first().rating
            # todo текстовое представление рейтинга
            rating_title = 'Королева шоппинга'
            return {'rating': rating, 'rating_title': rating_title}
        return 0

    def get_is_current_user_liked(self, obj):
        user = get_user(self)
        return obj.get_is_current_user_liked(user)

    def get_current_user_like_id(self, obj):
        user = get_user(self)
        return obj.get_current_user_like_id(user)

    def get_product_url(self, obj):
        return obj.product.slug if obj.product else ''

    def get_review_rating(self, obj):
        if obj and hasattr(obj, 'review_rating'):
            return obj.review_rating

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_rating', 'stars',
            'content',
            'likes_count', 'review_rating', 'is_current_user_liked', 'current_user_like_id',
            'product', 'product_url',
            'review_photos', 'review_videos',
            'created_at', 'updated_at',
        ]


class UpdateReviewSerializer(serializers.ModelSerializer):

    def validate(self, validated_data):
        return super(UpdateReviewSerializer, self).validated_data

    def update(self, instance, validated_data):
        review = Review.objects.update(
            content=validated_data['content'],
        )
        return review

    class Meta:
        model = Review
        fields = ['content', 'product', 'stars', 'profile']


def get_user(data):
    try:
        if 'user' in data.context.keys():
            return data.context['user']
        return data.context['request'].user
    except Exception:
        return None
