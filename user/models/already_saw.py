from django.db import models
from .profile import Profile
from garpix_catalog.models import Product


class AlreadySaw(models.Model):

    profile = models.ForeignKey(Profile, verbose_name='Пользователь', related_name='user_already_saw',
                                on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Подукт', related_name='product_already_saw',
                                on_delete=models.CASCADE)
    max_for_user = 30

    class Meta:
        verbose_name = 'Уже смотрели'
        verbose_name_plural = 'Уже смотрели'
        unique_together = ('profile', 'product')
        ordering = ['-id', ]

    def __str__(self):
        return f'{self.profile} - {self.product}'

    @classmethod
    def add_or_update(cls, profile, product):
        instance = cls.objects.filter(profile=profile, product=product).first()
        if instance:
            instance.delete()
        count = cls.objects.filter(profile=profile).count()
        if count >= cls.max_for_user:
            extra_instances = cls.objects.filter(profile=profile)[cls.max_for_user-1:count]
            [i.delete() for i in extra_instances]
        cls.objects.create(profile=profile, product=product)
