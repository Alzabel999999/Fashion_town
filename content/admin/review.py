from django.contrib import admin
from ..models.likes import Likes
from ..models.review import Review
from ..models.review_photo import ReviewPhoto
from ..models.review_video import ReviewVideo


class ReviewPhotoInline(admin.TabularInline):
    model = ReviewPhoto
    extra = 0


class ReviewVideoInline(admin.TabularInline):
    model = ReviewVideo
    extra = 0


class ReviewLikesInline(admin.TabularInline):
    model = Likes
    fields = ['profile', 'is_active', ]
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'profile', 'product', 'stars', 'is_approved', 'real_likes_count', 'fake_likes_count',
        'likes_count', 'is_with_media'
    ]
    list_editable = ['is_approved', 'fake_likes_count']
    inlines = (ReviewPhotoInline, ReviewVideoInline, ReviewLikesInline)
    fields = [
        'is_approved', 'profile', 'product', 'stars', 'content', 'real_likes_count', 'fake_likes_count', 'likes_count']
    raw_id_fields = ['product', ]
    readonly_fields = ['likes_count', ]

    # def likes_count(self, obj):
    #     return obj.likes_count
    #
    # likes_count.__name__ = 'Кол-во лайков'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.annotate(likes_count=Count("review_likes"))
        return queryset
