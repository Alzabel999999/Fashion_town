from django.db import models
from .review import Review
from ..mixins.content import ImageMixin, OrderingMixin


class ReviewPhoto(ImageMixin, OrderingMixin):
    review = models.ForeignKey(Review, verbose_name='Отзыв',
                               related_name='review_photos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('ordering', '-id')

    def save(self, *args, **kwargs):
        super(ReviewPhoto, self).save()
        self.review.save()

    def delete(self, using=None, keep_parents=False):
        super(ReviewPhoto, self).delete()
        self.review.save()
