from django.contrib.sites.models import Site
from django.db import models
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from garpix_page.models import Page
from slugify import slugify
from ..mixins.content import ImageMixin, OrderingMixin
from .news_rubric import NewsRubric
from django.conf import settings


class News(AbstractBasePageModel, ImageMixin, OrderingMixin):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Краткое описание', blank=True, default='')
    is_for_retailer = models.BooleanField(default=False, verbose_name='Для розничных покупателей')
    is_for_wholesaler = models.BooleanField(default=False, verbose_name='Для оптовиков')
    is_for_dropshipper = models.BooleanField(default=False, verbose_name='Для дропшипперов')
    rubrics = models.ManyToManyField(NewsRubric, verbose_name='Рубрики', blank=True, related_name='rubric_news')
    page_type = models.IntegerField(default=27, verbose_name='Тип страницы', choices=settings.CHOICES_PAGE_TYPES)

    sites = models.ManyToManyField(
        Site, verbose_name='Сайты для отображения', default=settings.SITE_ID, blank=True)

    parent = models.ForeignKey(Page, null=True, blank=False, db_index=True, verbose_name='Родительская страница',
                               on_delete=models.SET_NULL, limit_choices_to={'page_type': settings.PAGE_TYPE_NEWS})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('ordering', '-id', 'title')

    def __str__(self):
        return f'{self.title} ({str(self.created_at)})'

    def save(self, *args, **kwargs):
        super(News, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = self.get_slug()
        super(News, self).save(*args, **kwargs)

    def get_slug(self):
        slug = f'news-{self.id}-{self.title}'
        if len(slug) > 150: slug = slug[:150]
        return slugify(slug)

    def get_image(self):
        if self.image:
            return settings.SITE_URL + self.image.url
        if self.news_photos.first():
            return settings.SITE_URL + self.news_photos.first().image.url
        if self.news_videos.first():
            return settings.SITE_URL + self.news_videos.first().video_preview.url
        return '#'

    def get_media(self):
        media_list = []
        # if self.image:
        #     media_list.append({
        #         'type': 'image',
        #         'image': settings.SITE_URL + self.image.url,
        #         'image_thumb': settings.SITE_URL + self.image_thumb,
        #     })
        photos = self.news_photos.all()
        if photos:
            for photo in photos:
                media_list.append({
                    'type': 'image',
                    'image': settings.SITE_URL + photo.image.url,
                    'image_thumb': settings.SITE_URL + photo.image_thumb,
                })
        videos = self.news_videos.all()
        if videos:
            for video in videos:
                if video.youtube_video:
                    video_link = video.youtube_video
                else:
                    video_link = settings.SITE_URL + video.video.url
                media_list.append({
                    'type': 'video',
                    'video': video_link,
                    'preview': settings.SITE_URL + video.video_preview.url,
                })
        return media_list
