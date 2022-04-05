from django.db import models
from user.models import Profile
from ..models import Review


class Likes(models.Model):
    profile = models.ForeignKey(Profile, null=True, verbose_name='Профиль',
                                related_name='profile_likes', on_delete=models.SET_NULL)
    review = models.ForeignKey(Review, verbose_name='Отзыв', related_name='review_likes', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('profile', 'review',)
        
    def save(self, *args, **kwargs):
        super(Likes, self).save(*args, **kwargs)
        self.review.save()
