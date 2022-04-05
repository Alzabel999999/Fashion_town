from django.db import models
from shop.models import Shop
from . import LivePhotoAlbum, LivePhotoImage, LivePhotoVideo
from ..mixins.content import OrderingMixin


class ShopLivePhoto(OrderingMixin):

    is_selected = models.BooleanField(verbose_name='Выбрано', default=True)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='shop_albums',
                             on_delete=models.CASCADE, default=None)
    title = models.CharField(verbose_name='Название', blank=True, null=True, default=None, max_length=256)
    album = models.ForeignKey(LivePhotoAlbum, verbose_name='Альбом', related_name='photo_album_shop_albums',
                              on_delete=models.CASCADE)
    photos = models.ManyToManyField(LivePhotoImage, verbose_name='Фото', related_name='live_photo_photo_shop_albums',
                                    blank=True)
    videos = models.ManyToManyField(LivePhotoVideo, verbose_name='Видео', related_name='live_photo_video_shop_albums',
                                    blank=True)

    class Meta:
        verbose_name = 'Альбом живых фото магазина'
        verbose_name_plural = 'Альбомы живых фото магазинов'
        ordering = ('ordering', '-id')
        unique_together = ['shop', 'album']

    def __str__(self):
        title = self.title if self.title not in [None, ''] else self.album.title
        return f'{title} - {self.shop.title}'

    def check_album_selected(self):
        return self.photos.filter(album=self.album).exists() or self.videos.filter(album=self.album).exists()

    def check_media_selected(self, media):
        return media in self.photos.all() or media in self.videos.all()

    @classmethod
    def get_album(cls, album, shop):
        return cls.objects.filter(shop=shop, album=album).first()

    @classmethod
    def get_or_create(cls, origin_album, shop):
        album = cls.objects.filter(album=origin_album, shop=shop).first()
        if not album:
            album = cls.objects.create(album=origin_album, shop=shop, title=origin_album.title)
        return album

