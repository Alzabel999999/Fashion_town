from django.conf import settings
from django.contrib import admin
from django.shortcuts import get_object_or_404
from garpix_multiupload.admin import MultiUploadAdmin
from garpix_page.models import Page
from ..models import LivePhotoAlbum, LivePhotoImage, LivePhotoVideo, Brand
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import messages


class LivePhotoImageInline(admin.TabularInline):
    model = LivePhotoImage
    extra = 0


class LivePhotoVideoInline(admin.TabularInline):
    model = LivePhotoVideo
    extra = 0
    fields = ('video', 'youtube_video', 'video_preview', 'description', 'ordering')


@admin.register(LivePhotoAlbum)
class LivePhotoAlbumAdmin(MultiUploadAdmin):
    side_bar_on = True

    multiupload_form = True
    multiupload_template = "admin/multiupload/upload.html"
    change_list_template = "admin/create_live_photo_album.html"
    multiupload_maxfilesize = 3 * 2 ** 20  # 3 Mb
    multiupload_acceptedformats = ("image/jpeg", "image/pjpeg", "image/png",
                                   "video/mp4", "video/avi", "video/mov",)

    list_display = ('title', 'brand', 'created_at',)
    readonly_fields = ('created_at', 'slug',)
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'brand', 'created_at', 'is_active', 'ordering', 'image',
                           'image_thumb', 'content', 'parent',)}),
        ('SEO', {'fields': ('seo_title', 'seo_keywords', 'seo_description', 'seo_author',
                            'seo_og_type', 'seo_image',), 'classes': ('tabed',)})
    )
    inlines = (LivePhotoImageInline, LivePhotoVideoInline)
    search_fields = ['title', 'brand__title']

    # Множественная загрузка фотографий в админке

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('create_live_photo_album/', self.create_live_photo_album),
        ]
        return my_urls + urls

    def changelist_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        all_brands = Brand.objects.all()
        for i, brand in enumerate(all_brands):
            extra_context[f'brand {i}'] = brand
        extra_context = extra_context.values()
        return super(LivePhotoAlbumAdmin, self).changelist_view(
            request, extra_context={'extra_context': extra_context})

    def get_valid_data(self, request):
        brand = request.POST['Brand']
        title = request.POST['album_title']
        uploaded_files = request.FILES.getlist('file')
        if not title:
            self.message_user(request, f"Что то пошло не так. Введите название альбома.",
                              level=messages.DEFAULT_LEVELS['ERROR'])
            return False
        if not brand:
            self.message_user(request, f"Что то пошло не так. Выберите бренд.",
                              level=messages.DEFAULT_LEVELS['ERROR'])
            return False
        if not uploaded_files:
            self.message_user(request, f"Что то пошло не так. Загрузите фотографии.",
                              level=messages.DEFAULT_LEVELS['ERROR'])
            return False
        return True

    def create_live_photo_album(self, request):
        if "_create_live_photo_album" in request.POST:
            if self.get_valid_data(request):
                try:
                    brand = request.POST['Brand']
                    title = request.POST['album_title']
                    brand_instance = Brand.objects.filter(title=brand).first()
                    uploaded_files = request.FILES.getlist('file')
                    album = LivePhotoAlbum.objects.create(
                        title=title,
                        brand=brand_instance,
                    )
                    for file in uploaded_files:
                        LivePhotoImage.objects.create(album=album, image=file)
                except Exception as e:
                    self.message_user(request, f"Что то пошло не так. Проверте содержимое загружаемого файла."
                                               f" "f"Ошибка: {str(e)}", level=messages.DEFAULT_LEVELS['ERROR'])
                return HttpResponseRedirect("../")
            else:
                return HttpResponseRedirect("../")

    def process_uploaded_file(self, uploaded, object, request):
        file = request.FILES['files[]']
        if 'video' in file.content_type:
            f = LivePhotoVideo.objects.create(album=object, video=uploaded)
            return {
                'url': f.video.url,
                'thumbnail_url': f.video_preview.url,
                'id': f.id,
                'name': request.POST['title'] if request.POST['title'] else uploaded.name
            }
        elif 'image' in file.content_type:
            f = LivePhotoImage.objects.create(album=object, image=uploaded)
            return {
                'url': f.image.url,
                'thumbnail_url': f.image_thumb,
                'id': f.id,
                'name': request.POST['title'] if request.POST['title'] else uploaded.name
            }

    def delete_file(self, pk, request):
        obj = get_object_or_404(LivePhotoImage, pk=pk)
        return obj.delete()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.parent = Page.objects.filter(page_type=settings.PAGE_TYPE_LIVE_PHOTOS).first()
        return super(LivePhotoAlbumAdmin, self).save_model(request, obj, form, change)
