from .models.country import Country
from django.db import models
from garpix_utils.file_field import get_file_path
from PIL import Image
import ffmpeg
import sys


class AddressMixin(models.Model):
    post_code = models.CharField(max_length=10, verbose_name='Индекс', blank=False, null=False, default='')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна', default=None)
    city = models.CharField(max_length=128, verbose_name='Город', blank=False, null=False, default='')
    street = models.CharField(max_length=256, verbose_name='Улица', blank=True, null=True, default='')
    house = models.CharField(max_length=64, verbose_name='Дом', blank=False, null=False, default='')
    flat = models.CharField(max_length=64, verbose_name='Квартира', blank=True, null=True, default='')

    class Meta:
        abstract = True


class ReceiverMixin(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Имя', blank=False, null=False, default='')
    middle_name = models.CharField(max_length=64, verbose_name='Отчество', blank=False, null=False, default='')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия', blank=False, null=False, default='')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=False, null=False, default='')

    class Meta:
        abstract = True


class PassportMixin(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Имя', blank=True, null=True, default='')
    middle_name = models.CharField(max_length=64, verbose_name='Отчество', blank=True, null=True, default='')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия', blank=True, null=True, default='')
    passport_number = models.CharField(max_length=16, verbose_name='Номер', blank=True, null=True, default='')
    passport_issued = models.CharField(max_length=255, verbose_name='Кем выдан', blank=True, null=True, default='')
    passport_issue_date = models.DateField(verbose_name='Дата выдачи', blank=True, null=True, default=None)
    comment_passport = models.TextField(verbose_name='Комментарий ПД', blank=True, null=True, default='')
    wait_call = models.BooleanField(verbose_name='Дождаться звонка', default=False)

    class Meta:
        abstract = True


class VideoMixin(models.Model):
    video = models.FileField(max_length=255, upload_to=get_file_path,
                             default='', blank=True, null=True, verbose_name='Видео')
    video_preview = models.FileField(max_length=255, upload_to=get_file_path,
                                     default='', blank=True, null=True, verbose_name='Видео превью')

    def save(self, *args, **kwargs):
        super(VideoMixin, self).save()
        if not self.video_preview:
            if self.video:
                video_path = str(self.video.path)
                preview_path = video_path.rsplit('.', 1)[0] + '.png'
                video_url = str(self.video.name)
                preview_url = video_url.rsplit('.', 1)[0] + '.png'
                preview = Image.new("RGB", (400, 300))
                preview.save(preview_path, 'PNG')
                self.get_preview(in_filename=video_path, out_filename=preview_path, time=0.1, width=400)
                self.video_preview = preview_url
            else:
                pass
            super(VideoMixin, self).save()

    def get_preview(self, in_filename, out_filename, time, width):
        try:
            (
                ffmpeg
                    .input(in_filename, ss=time)
                    .filter('scale', width, -1)
                    .output(out_filename, vframes=1)
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            sys.exit(1)

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    image = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True,
                             verbose_name='Изображение')
    image_thumb = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        super(ImageMixin, self).save()

        if self.image:
            from .models import CorrespondenceImage
            image_path = str(self.image.path)
            image_url = str(self.image.url)
            im = Image.open(image_path).convert('RGB')

            extension = image_path.rsplit('.', 1)[1]
            filename = image_path.rsplit('/', 1)[1].rsplit('.', 1)[0]
            fullpath = image_path.rsplit('/', 1)[0]
            url = image_url.rsplit('/', 1)[0]

            if extension not in ['jpg', 'jpeg', 'gif', 'png']:
                sys.exit()

            if type(self) == CorrespondenceImage:
                if im.size[0] > im.size[1]:
                    size = (200, 150)
                else:
                    size = (150, 200)
            else:
                size = (300, 400)

            im.thumbnail(size, Image.ANTIALIAS)

            thumbname = filename + "_" + str(size[0]) + "x" + str(size[1]) + ".jpg"
            im.save(fullpath + '/' + thumbname)
            self.image_thumb = url + '/' + thumbname

            super(ImageMixin, self).save()

    class Meta:
        abstract = True
