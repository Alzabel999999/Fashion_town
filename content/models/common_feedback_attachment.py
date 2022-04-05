from django.db import models
from garpix_utils.file_field import get_file_path
from .common_feedback import CommonFeedback


class CommonFeedbackAttachment(models.Model):

    common_feedback = models.ForeignKey(CommonFeedback, verbose_name='Обратная связь', on_delete=models.SET_NULL,
                                        related_name='common_feedback_attachments', blank=True, null=True, default=None)
    attachment = models.FileField(verbose_name='Вложение', upload_to=get_file_path,
                                  blank=False, null=False, default=None)

    class Meta:
        verbose_name = 'Вложенный файл'
        verbose_name_plural = 'Вложенные файлы'
        ordering = ('-id', )
