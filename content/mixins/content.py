from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.functional import cached_property
from garpix_utils.file_field import get_file_path
from PIL import Image
import ffmpeg
import sys
from django.core.files import File
from django.conf import settings
from garpix_utils.youtube import get_youtube_id, get_youtube_thumbnail, get_cleaned_yt_info
import requests
import os


class ImageMixin(models.Model):
    image = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True,
                             verbose_name='Изображение')
    image_thumb = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        super(ImageMixin, self).save()

        if self.image:
            image_path = str(self.image.path)
            image_url = str(self.image.url)
            im = Image.open(image_path).convert('RGB')

            extension = image_path.rsplit('.', 1)[1]
            filename = image_path.rsplit('/', 1)[1].rsplit('.', 1)[0]
            fullpath = image_path.rsplit('/', 1)[0]
            url = image_url.rsplit('/', 1)[0]

            if extension not in ['jpg', 'jpeg', 'gif', 'png']:
                sys.exit()

            from ..models import Banner, Announce, MainPage, News, NewsPhoto, ReviewPhoto
            if type(self) == Banner:
                size = (450, 680)
            elif type(self) == Announce:
                size = (1920, 60)
            elif type(self) == MainPage:
                size = (1000, 750)
            elif type(self) == News:
                size = (400, 300)
            elif type(self) == NewsPhoto:
                if im.size[0] > im.size[1]:
                    size = (300, 225)
                else:
                    size = (225, 300)
            elif type(self) == ReviewPhoto:
                size = (75, 100)
            else:
                size = (300, 400)

            im.thumbnail(size, Image.ANTIALIAS)

            thumbname = filename + "_" + str(size[0]) + "x" + str(size[1]) + ".jpg"
            im.save(fullpath + '/' + thumbname)
            self.image_thumb = url + '/' + thumbname

            super(ImageMixin, self).save()

    class Meta:
        abstract = True


class VideoMixin(models.Model):
    video = models.FileField(max_length=255, upload_to=get_file_path,
                             default='', blank=True, null=True, verbose_name='Видео')
    youtube_video = models.CharField(max_length=1024, default='', blank=True, null=True,
                                     verbose_name='Ссылка на видео (YouTube)')
    video_preview = models.FileField(max_length=255, upload_to=get_file_path,
                                     default='', blank=True, null=True, verbose_name='Видео превью')

    def save(self, *args, **kwargs):
        super(VideoMixin, self).save()
        if not self.video_preview:
            if self.youtube_video:
                file_link = self.get_youtube_video_preview()
                r = requests.get(file_link, allow_redirects=True)
                file_name = f'{settings.MEDIA_ROOT}/tmp.jpg'
                open(file_name, 'wb').write(r.content)
                f = open(file_name, 'rb')
                djangofile = File(f)
                self.video_preview.save(file_name, djangofile)
                f.close()
                try:
                    os.remove(file_name)
                except:
                    print(f'No file {file_name} ')
            elif self.video:
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
            print(e.stderr.decode(), file=sys.stderr)
            sys.exit(1)

    def get_youtube_video_id(self):
        return get_youtube_id(self.youtube_video)

    def get_youtube_video_info(self):
        return get_cleaned_yt_info(self.youtube_video)

    def get_youtube_video_preview(self):
        return get_youtube_thumbnail(self.get_youtube_video_id())

    class Meta:
        abstract = True


class OrderingMixin(models.Model):
    ordering = models.IntegerField(default=0, verbose_name='Порядок', db_index=True)

    class Meta:
        abstract = True


class TitleMixin(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class TitleSlugMixin(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='ЧПУ', blank=True, default='', unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @cached_property
    def absolute_url(self):
        return self.slug if self.slug == '/' else f'{self.slug}'


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        abstract = True


class SEOMixin(models.Model):
    seo_title = models.CharField(max_length=250, verbose_name='SEO заголовок страницы (title)', blank=True, default='')
    seo_keywords = models.CharField(max_length=250, verbose_name='SEO ключевые слова (keywords)', blank=True,
                                    default='')
    seo_description = models.CharField(max_length=250, verbose_name='SEO описание (description)', blank=True,
                                       default='')
    seo_author = models.CharField(max_length=250, verbose_name='SEO автор (author)', blank=True, default='')
    seo_og_type = models.CharField(max_length=250, verbose_name='SEO og:type', blank=True, default="website")

    class Meta:
        abstract = True


class ActiveMixin(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Включено')

    class Meta:
        abstract = True


class ContentMixin(models.Model):
    content = RichTextUploadingField(verbose_name='Содержимое', blank=True, default='')

    class Meta:
        abstract = True


class ContentAsTextMixin(models.Model):
    content = models.TextField(verbose_name='Содержимое', blank=True, default='')

    class Meta:
        abstract = True


class PubDateMixin(models.Model):
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    class Meta:
        abstract = True
