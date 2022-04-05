from django.db import models
from solo.models import SingletonModel
from ckeditor_uploader.fields import RichTextUploadingField
from garpix_utils.file_field import get_file_path


class AnyPages(SingletonModel):
    auth_reg_image = models.FileField(
        max_length=255, upload_to=get_file_path, default='', blank=True,
        verbose_name='Изображение на странице авторизации/регистрации')
    auth_reg_text = RichTextUploadingField(
        verbose_name='Текст на странице авторизации/регистрации', blank=True, default='')

    def __str__(self):
        return 'Другие страницы'

    class Meta:
        verbose_name = 'Другие страницы'
