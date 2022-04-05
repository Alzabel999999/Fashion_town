from django.contrib import admin
from django.shortcuts import get_object_or_404
from ..models import ProductSku, ProductSkuImage, ProductSkuVideo
from garpix_multiupload.admin import MultiUploadAdmin


class ProductSkuImageInline(admin.TabularInline):
    model = ProductSkuImage
    # fields = ('image', 'image_thumb', 'ordering',)
    extra = 0


class ProductSkuVideoInline(admin.TabularInline):
    model = ProductSkuVideo
    fields = ('video', 'youtube_video', 'video_preview', 'description', 'ordering')
    extra = 0


@admin.register(ProductSku)
class ProductSkuAdmin(MultiUploadAdmin):

    side_bar_on = True

    multiupload_template = "admin/multiupload/upload.html"
    change_list_template = ''
    multiupload_maxfilesize = 3 * 2 ** 20  # 3 Mb
    multiupload_acceptedformats = ("image/jpeg", "image/pjpeg", "image/png",
                                   "video/mp4", "video/avi", "video/mov",)

    list_display = ('product', 'size', 'color', 'in_stock_count')
    readonly_fields = ('image_thumb', 'is_in_stock',)
    fieldsets = (
        (None, {'fields': (
            'is_active', 'product',
            ('size', 'color'), 'price', 'weight',
            'image', 'image_thumb',
            'content',
            ('in_stock_count', 'is_in_stock'),
            'ordering', )}),
        ('SEO', {'fields': ('seo_title', 'seo_keywords', 'seo_description', 'seo_author',
                            'seo_og_type', 'seo_image',), 'classes': ('tabed',)})
    )
    inlines = (ProductSkuImageInline, ProductSkuVideoInline)
    change_list_template = ""
    search_fields = ['product__title', ]
    list_filter = ['color', 'size']

    def process_uploaded_file(self, uploaded, object, request):
        file = request.FILES['files[]']
        if 'video' in file.content_type:
            f = ProductSkuVideo.objects.create(product_sku=object, video=uploaded)
            return {
                'url': f.video.url,
                'thumbnail_url': f.video_preview.url,
                'id': f.id,
                'name': request.POST['title'] if request.POST['title'] else uploaded.name
            }
        elif 'image' in file.content_type:
            f = ProductSkuImage.objects.create(product_sku=object, image=uploaded)
            return {
                'url': f.image.url,
                'thumbnail_url': f.image_thumb,
                'id': f.id,
                'name': request.POST['title'] if request.POST['title'] else uploaded.name
            }

    def delete_file(self, pk, request):
        obj = get_object_or_404(ProductSkuImage, pk=pk)
        return obj.delete()
