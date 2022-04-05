from django.db import models
from django.core.exceptions import ValidationError
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
    image = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=False,
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
                raise ValidationError('Некорректный формат файла!')

            size = (300, 400)

            im.thumbnail(size, Image.ANTIALIAS)

            thumbname = filename + "_" + str(size[0]) + "x" + str(size[1]) + ".jpg"
            im.save(fullpath + '/' + thumbname)
            self.image_thumb = url + '/' + thumbname

            super(ImageMixin, self).save()
        else:
            self.image_thumb = ''
            super(ImageMixin, self).save()

    class Meta:
        abstract = True

    def get_image_paths(self):
        if self.image and self.image_thumb:
            return {
                'type': 'image',
                'image': settings.SITE_URL + self.image.url,
                'image_thumb': settings.SITE_URL + self.image_thumb
            }


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
            else:
                video_path = str(self.video.path)
                preview_path = video_path.rsplit('.', 1)[0] + '.png'
                video_url = str(self.video.name)
                preview_url = video_url.rsplit('.', 1)[0] + '.png'
                preview = Image.new("RGB", (400, 300))
                preview.save(preview_path, 'PNG')
                self.get_preview(in_filename=video_path, out_filename=preview_path, time=0.1, width=400)
                self.video_preview = preview_url
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

    def get_video_paths(self):
        if self.youtube_video and self.video_preview:
            return {
                'type': 'youtube_video',
                'video': self.youtube_video,
                'preview': settings.SITE_URL + self.video_preview.url
            }
        if self.video and self.video_preview:
            return {
                'type': 'video',
                'video': settings.SITE_URL + self.video.url,
                'preview': settings.SITE_URL + self.video_preview.url
            }


class OrderingMixin(models.Model):
    ordering = models.IntegerField(default=0, verbose_name='Порядок', db_index=True)

    class Meta:
        abstract = True
