from django.db import models
from garpix_utils.file_field import get_file_path
from user.models import Profile
from django.conf import settings
from django.dispatch import receiver



class PaymentOutput(models.Model):
    cost = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2,
                           blank=False, null=False, default=0.00)
    name = models.CharField(max_length=100, verbose_name='Имя отправителя', null=False, blank=False, default='')
    number = models.IntegerField(verbose_name='Номер счета', default=0)
    bank = models.CharField(max_length=100, verbose_name='БИК', null=False, blank=False, default='')
    receipt = models.FileField(verbose_name='Заявка', upload_to=get_file_path, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    profile = models.ForeignKey(Profile, verbose_name='Профиль пользователя', related_name='profile_payment_outputs',
                                null=True, blank=True, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f'Заявка №{self.id}'

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'
        ordering = ['-id', ]
