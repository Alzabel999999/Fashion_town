from django.contrib.sites.models import Site
from django.db import models
from garpix_utils.file_field import get_file_path
from user.models import Profile


class Shop(models.Model):
    profile = models.OneToOneField(Profile, verbose_name='Профиль', blank=False, null=True,
                                   on_delete=models.SET_NULL, related_name='profile_shop')
    site = models.OneToOneField(Site, verbose_name='Сайт', blank=False, null=True,
                                on_delete=models.SET_NULL, related_name='site_shop')
    logo = models.FileField(upload_to=get_file_path, default='', blank=False, verbose_name='Логотип')
    title = models.CharField(verbose_name='Название', max_length=256, default='')
    first_name = models.CharField(verbose_name='Имя', max_length=64, default='')
    middle_name = models.CharField(verbose_name='Отчество', max_length=64, default='')
    last_name = models.CharField(verbose_name='Фамилия', max_length=64, default='')
    comment = models.TextField(verbose_name='Комментарий', default='')
    is_active = models.BooleanField(verbose_name='Включено', default=False)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.title

    @classmethod
    def get_shop_by_request(cls, request):
        domain = request.META.get('REMOTE_ADDR', None)
        if domain:
            shop = cls.objects.filter(site__domain=domain).first()
            if shop:
                return shop
        return None

    def get_buyers(self):
        from user.models import User
        shop_id = f'_shop_{self.id}'
        users = User.objects.filter(is_shop_buyer=True, username__iendswith=shop_id)
        return users

    def save(self, *args, **kwargs):
        super(Shop, self).save(*args, **kwargs)
        if not hasattr(self, 'shop_config'):
            from ..models import ShopConfig
            ShopConfig.objects.create(shop=self, contacts_title=self.title)
