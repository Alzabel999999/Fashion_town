from django.db import models
from ..mixins.content import OrderingMixin
from garpix_catalog.models import Product
from user.models import Profile


class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedManager, self).get_queryset().filter(is_approved=True)


class Review(OrderingMixin):

    class STARS:
        ONE_STAR = 1
        TWO_STARS = 2
        THREE_STARS = 3
        FOUR_STARS = 4
        FIVE_STARS = 5
        TYPES = (
            (ONE_STAR, '1'),
            (TWO_STARS, '2'),
            (THREE_STARS, '3'),
            (FOUR_STARS, '4'),
            (FIVE_STARS, '5'),
        )

    profile = models.ForeignKey(Profile, verbose_name='Профиль', related_name='profile_reviews',
                                on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name='Товар',
                                related_name='product_reviews', on_delete=models.SET_NULL)
    stars = models.IntegerField(verbose_name='Кол-во звезд', default=STARS.FIVE_STARS, choices=STARS.TYPES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_approved = models.BooleanField(verbose_name='Показать', default=False)
    content = models.TextField(verbose_name='Содержимое', blank=True, default='')
    real_likes_count = models.PositiveIntegerField(verbose_name='Количество лайков (реальное)', default=0)
    fake_likes_count = models.PositiveIntegerField(verbose_name='Количество лайков', default=0)
    likes_count = models.PositiveIntegerField(verbose_name='Количество лайков (будет показано)', default=0)
    is_with_media = models.BooleanField(verbose_name='Наличие медиа', default=False)

    objects = models.Manager()
    approved_objects = ApprovedManager()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('ordering', '-id')

    def save(self, *args, **kwargs):
        self.real_likes_count = self.review_likes.filter(is_active=True).count()
        if self.fake_likes_count and self.fake_likes_count > self.real_likes_count:
            self.likes_count = self.fake_likes_count
        else:
            self.likes_count = self.real_likes_count
        self.is_with_media = True if self.review_photos.all() or self.review_videos.all() else False
        super(Review, self).save(*args, **kwargs)

    def get_hidden_username(self):
        if not self.profile:
            return 'deleted'
        hidden_username = self.profile.user.username[0] + ''.join(
            ['*' for i in list(self.profile.user.username)[1:-1]]) + self.profile.user.username[-1]
        return f'{hidden_username}'

    @property
    def get_likes_count(self):
        # likes_count = self.review_likes.filter(is_active=True).count()
        likes_count = self.fake_likes_count if self.fake_likes_count > self.real_likes_count else self.real_likes_count
        return f'{likes_count}'

    def get_is_current_user_liked(self, user):
        from . import Likes
        is_liked = False
        if user and user.is_authenticated:
            if Likes.objects.filter(profile=user.profile, review=self, is_active=True).first():
                is_liked = True
        return is_liked

    def get_current_user_like_id(self, user):
        from . import Likes
        like_id = None
        if user and user.is_authenticated:
            like = Likes.objects.filter(profile=user.profile, review=self).first()
            like_id = like.id if like else None
        return like_id

    @classmethod
    def create_review(cls, user, data, files=None):
        from ..models import ReviewPhoto, ReviewVideo
        profile = user.profile
        content = data.get('content', '')
        product_id = data.get('product', None)
        product = Product.objects.filter(id=product_id).first() if product_id else None
        stars = data.get('stars', 5)
        if int(stars) < 1: stars = 1
        new_review = Review.objects.create(
            profile=profile,
            content=content,
            product=product,
            stars=stars,
        )
        for file in files:
            if 'image' in file.content_type and file.size < 3000000:
                ReviewPhoto.objects.create(review=new_review, image=file)
            if 'video' in file.content_type and file.size < 5000000:
                ReviewVideo.objects.create(review=new_review, video=file)
        return new_review
