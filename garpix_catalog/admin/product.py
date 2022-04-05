from django import forms
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.urls import resolve, path, re_path
from garpix_page.models import Page
from ..models import Product, ProductImage, ProductVideo, ProductSku, Size, Color
from content.models import Review
from garpix_multiupload import admin as multiupload_admin
from django.shortcuts import get_object_or_404


class ProductFileWidget(forms.ClearableFileInput):
    template_name = "product_clearable_file_input.html"


class ProductAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = ProductFileWidget()


class ProductSkuInlineAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductSkuInlineAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = ProductFileWidget()


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    # fields = ('image', 'image_thumb', 'ordering',)
    extra = 0


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    fields = ('video', 'youtube_video', 'video_preview', 'description', 'ordering')
    extra = 0


class ProductSkuInline(admin.TabularInline):
    model = ProductSku
    form = ProductSkuInlineAdminForm
    show_change_link = True
    template = 'admin/product_sku_inline.html'
    extra = 0

    def get_product(self, request):
        try:
            product_id = resolve(request.path_info).kwargs['object_id']
            product = Product.objects_all.filter(id=product_id).first()
            return product
        except Exception as e:
            print(str(e))
            return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'size':
            from ..models import Size
            product = self.get_product(request)
            if product:
                if product.is_one_size:
                    kwargs['queryset'] = Size.objects.filter(size=0)
                else:
                    kwargs['queryset'] = Size.objects.exclude(size=0)
            else:
                kwargs['queryset'] = Size.objects.none()
        return super(ProductSkuInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        if obj.is_in_stock:
            return ['size', 'color', 'image', 'in_stock_count']
        else:
            return ['size', 'color', 'image']


class ReviewsInline(admin.TabularInline):
    model = Review
    fields = ['profile', 'content', 'is_approved']
    extra = 0


@admin.register(Product)
class ProductAdmin(multiupload_admin.MultiUploadAdmin):

    form = ProductAdminForm
    multiupload_template = "admin/multiupload/upload.html"
    change_form_template = 'admin/clone_product.html'
    change_list_template = ''
    multiupload_maxfilesize = 3 * 2 ** 20  # 3 Mb
    multiupload_acceptedformats = ("image/jpeg", "image/pjpeg", "image/png",
                                   "video/mp4", "video/avi", "video/mov",)

    list_display = ['title', 'brand', 'category', 'purchase_price', 'is_in_stock', 'is_one_size', 'in_archive', 'vendor_code'] #'active'
    inlines = (ProductImageInline, ProductVideoInline, ProductSkuInline, ReviewsInline)

    readonly_fields = (
        'slug', 'stock',
        'retailer_price_auto', 'dropshipper_price_auto', 'wholesaller_price_auto',
        'retailer_total_price_auto', 'dropshipper_total_price_auto', 'wholesaller_total_price_auto',
        'brand', 'category', 'image_thumb',
    )
    search_fields = ['title', 'brand__title', 'category__title', 'purchase_price', 'vendor_code']
    list_filter = ['is_in_stock', 'is_new', 'is_closeout', 'is_bestseller', 'in_archive']

    def process_uploaded_file(self, uploaded, object, request):
        file = request.FILES['files[]']
        if 'video' in file.content_type:
            f = ProductVideo.objects.create(product=object, video=uploaded)
            return {
                'url': f.video.url,
                'thumbnail_url': f.video_preview.url,
                'id': f.id,
                'name': request.POST['title'] if request.POST['title'] else uploaded.name
            }
        elif 'image' in file.content_type:
            f = ProductImage.objects.create(product=object, image=uploaded)

            return {
                'url': f.image.url,
                'thumbnail_url': f.image_thumb,
                'id': f.id,
                'name': request.POST['title'] if request.POST['title'] else uploaded.name
            }

    def delete_file(self, pk, request):
        obj = get_object_or_404(ProductImage, pk=pk)
        return obj.delete()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return [
                (None, {'fields': (
                    'brand_category', 'title', 'purchase_price', 'image'
                )}),
                ('ВАЖНО!!!', {'fields': (
                    'is_in_stock',
                )}),
                ('СКУ', {'fields': (
                    'sizes', 'colors'
                )}),
            ]
        return [
            (None, {'fields': (
                'in_archive',
                'vendor_code',
                'brand_category',
                'title', 'slug', 'ordering', 'is_active',
                'image', 'image_thumb',
                ('purchase_price',),
                ('retailer_price', 'dropshipper_price', 'wholesaller_price',),
                ('retailer_price_auto', 'dropshipper_price_auto', 'wholesaller_price_auto',),
                ('retailer_total_price_auto', 'dropshipper_total_price_auto', 'wholesaller_total_price_auto',),
                ('weight', 'stock'),
                'is_new', 'is_closeout', 'is_bestseller',
                'content', 'extra', 'short_content', 'product_rc', 'page_type', 'parent')}),
            ('SEO', {'fields': ('seo_title', 'seo_keywords', 'seo_description', 'seo_author',
                                'seo_og_type', 'seo_image',), 'classes': ('tabed',)})]

    def get_inlines(self, request, obj):
        if not obj:
            return []
        else:
            return ProductImageInline, ProductVideoInline, ProductSkuInline, ReviewsInline

    def get_queryset(self, request):
        qs = self.model.objects_all.all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.parent = Page.objects.filter(page_type=settings.PAGE_TYPE_CATALOG).first()
            super(ProductAdmin, self).save_model(request, obj, form, change)
            sizes = request.POST.getlist('sizes', [])
            colors = request.POST.getlist('colors', [])
            sizes_qs = Size.objects.filter(id__in=sizes)
            is_one_size = sizes_qs.filter(size=0).exists()
            if is_one_size:
                sizes_qs = sizes_qs.filter(size=0)
                obj.is_one_size = True
            else:
                sizes_qs = sizes_qs.exclude(size=0)
                obj.is_one_size = False
            colors_qs = Color.objects.filter(id__in=colors)
            for size in sizes_qs:
                for color in colors_qs:
                    ProductSku.objects.create(product=obj, size=size, color=color)
        super(ProductAdmin, self).save_model(request, obj, form, change)

    def get_urls(self, *args, **kwargs):
        my_urls = [
            path('<path:pk>/change/clone_product/', self.clone_product, name='clone_product'),
        ]
        return my_urls + super(ProductAdmin, self).get_urls(*args, **kwargs)

    def clone_product(self, request, pk):
        is_in_stock = request.GET.get('is_in_stock', False)
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        origin_instance = self.get_object(request, pk)
        new_instance = self.get_object(request, pk)
        new_instance.pk = None
        new_instance.title = origin_instance.title + ' (clone)'
        if is_in_stock:
            new_instance.is_in_stock = True
        new_instance.save()
        for image in origin_instance.product_images.all():
            new_image = image
            new_image.pk = None
            new_image.product = new_instance
            new_image.save()
        for video in origin_instance.product_videos.all():
            new_video = video
            new_video.pk = None
            new_video.product = new_instance
            new_video.save()
        origin_skus = origin_instance.product_skus.all()
        for sku in origin_skus:
            origin_sku = sku
            values = origin_skus.filter(id=sku.id).values().first()
            values.pop('id')
            values.update({'product_id': new_instance.pk})
            new_sku = ProductSku.objects.create(**values)
            for image in origin_sku.product_sku_images.all():
                new_image = image
                new_image.pk = None
                new_image.product_sku = new_sku
                new_image.save()
            for video in origin_sku.product_sku_videos.all():
                new_video = video
                new_video.pk = None
                new_video.product_sku = new_sku
                new_video.save()

        self.message_user(request, "товар успешно скопирован...", level=messages.DEFAULT_LEVELS['SUCCESS'])
        return HttpResponseRedirect('../')
