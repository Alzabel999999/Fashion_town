from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from garpix_utils.file_field import get_file_path


class RoleConfiguration(models.Model):

    class ROLE:
        RETAIL = 1
        DROPSHIPPER = 2
        WHOLESALE = 3
        TYPES = (
            (RETAIL, 'Розничный покупатель'),
            (DROPSHIPPER, 'Дропшиппер'),
            (WHOLESALE, 'Оптовый покупатель'),
        )

    role = models.IntegerField(
        verbose_name='Роль пользователя', default=ROLE.RETAIL, choices=ROLE.TYPES, unique=True)
    delivery_condition = RichTextUploadingField(blank=True, verbose_name='Доставка', default='')
    payment_info = RichTextUploadingField(blank=True, verbose_name='Оплата', default='')
    public_offer = models.FileField(verbose_name='Публичная оферта', upload_to=get_file_path,
                                    blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Настройки роли'
        verbose_name_plural = 'Настройки ролей'
        ordering = ['role',]

    def __str__(self):
        return f'Настройки роли "{self.get_role_display()}"'
