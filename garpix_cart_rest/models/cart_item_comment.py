from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class CartItemComment(models.Model):

    comment = RichTextUploadingField(verbose_name='Комментарий', blank=True, default='')

    class Meta:
        verbose_name = 'Комментарий к позиции заказа'
        verbose_name_plural = 'Комментарии к позициям заказов'

    @classmethod
    def create_comment(cls, comment=None, files=None):
        from ..models import CartItemCommentPhoto, CartItemCommentVideo
        new_comment = cls.objects.create(comment=comment)
        for file in files:
            if 'image' in file.content_type and file.size < 3000000:
                CartItemCommentPhoto.objects.create(comment=new_comment, image=file)
            if 'video' in file.content_type and file.size < 5000000:
                CartItemCommentVideo.objects.create(comment=new_comment, video=file)
        return new_comment

    def update_comment(self, comment=None, files=None):
        from ..models import CartItemCommentPhoto, CartItemCommentVideo
        self.comment = comment
        self.save()
        for file in files:
            if 'image' in file.content_type and file.size < 3000000:
                CartItemCommentPhoto.objects.create(comment=self, image=file)
            if 'video' in file.content_type and file.size < 5000000:
                CartItemCommentVideo.objects.create(comment=self, video=file)
        return self
