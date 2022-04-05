from django.contrib.sites.models import Site
from django.db import models
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from garpix_page.models import Page
from slugify import slugify
from . import Brand
from ..mixins.content import OrderingMixin, ImageMixin
from django.conf import settings


class LivePhotoAlbum(OrderingMixin, ImageMixin, AbstractBasePageModel):
    page_type = models.IntegerField(default=25, verbose_name='Тип страницы', choices=settings.CHOICES_PAGE_TYPES)
    brand = models.ForeignKey(Brand, blank=True, null=True, related_name='brand_live_photo_albums',
                              verbose_name='Бренд', on_delete=models.SET_NULL)

    sites = models.ManyToManyField(
        Site, verbose_name='Сайты для отображения', default=settings.SITE_ID, blank=True)

    parent = models.ForeignKey(Page, null=True, blank=True, db_index=True, verbose_name='Родительская страница',
                               on_delete=models.SET_NULL,
                               limit_choices_to={'page_type': settings.PAGE_TYPE_LIVE_PHOTOS})

    class Meta:
        verbose_name = 'Альбом живых фото'
        verbose_name_plural = 'Альбомы живых фото'
        ordering = ['ordering', '-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(LivePhotoAlbum, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = self.get_slug()
        super(LivePhotoAlbum, self).save(*args, **kwargs)

    def get_slug(self):
        slug = f'live-photo-album-{self.id}-{self.title}'
        return slugify(slug)

    def get_image(self):
        if self.image:
            return self.image
        if self.live_photo_photos.exclude(image='').first():
            return self.live_photo_photos.exclude(image='').first().image
        return None
