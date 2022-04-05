from decimal import Decimal
from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q
from django.utils.safestring import mark_safe
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from garpix_page.models import Page
from slugify import slugify
from ..mixins.content import OrderingMixin, ImageMixin


def validate_zero(value):
    if value == 0:
        raise ValidationError('0')


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().exclude(
            Q(product_skus__isnull=True) |
            Q(product_skus__size=None) |
            Q(product_skus__color=None)
        )


class Product(OrderingMixin, ImageMixin, AbstractBasePageModel):
    vendor_code = models.CharField(max_length=255, verbose_name='Артикул', blank=True, default='')
    is_in_stock = models.BooleanField(default=False, verbose_name='Товар в наличии')
    is_one_size = models.BooleanField(default=False, verbose_name='Товар без размера')

    sizes = models.ManyToManyField('Size', verbose_name='Размеры')
    colors = models.ManyToManyField('Color', verbose_name='Цвета')

    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False, validators=[validate_zero, ],
        verbose_name='Закупочная цена', default='0.00')

    wholesaller_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена для оптовика')
    wholesaller_price_auto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена для оптовика (авто)')
    wholesaller_total_price_auto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Итоговая цена для оптовика (авто)')

    dropshipper_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена для дроппшипера')
    dropshipper_price_auto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена для дроппшипера (авто)')
    dropshipper_total_price_auto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Итоговая цена для дроппшипера (авто)')

    retailer_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Розничная цена')
    retailer_price_auto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Розничная цена (авто)')
    retailer_total_price_auto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Итоговая розничная цена (авто)')

    stock = models.PositiveIntegerField(blank=True, default=0, verbose_name='Кол-во на складе')
    weight = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'),
                                 verbose_name='Вес единицы товара, кг', blank=True, null=True)
    category = models.ForeignKey('Category', blank=True, null=True, related_name='category_products',
                                 verbose_name='Категория', on_delete=models.SET_NULL)
    brand = models.ForeignKey('Brand', blank=True, null=True, related_name='brand_products',
                              verbose_name='Бренд', on_delete=models.SET_NULL)
    brand_category = models.ForeignKey('BrandCategory', related_name='brand_category_products', blank=False, null=True,
                                       verbose_name='Бренд / Категория', on_delete=models.SET_NULL)
    extra = RichTextUploadingField(blank=True, verbose_name='Дополнительные данные', default='')
    page_type = models.IntegerField(default=4, verbose_name='Тип страницы', choices=settings.CHOICES_PAGE_TYPES)
    short_content = models.TextField(verbose_name='Содержимое для анонса', blank=True, default='')
    product_rc = models.ForeignKey('RedemptionCondition', related_name='rc_products', verbose_name='Условие выкупа',
                                   on_delete=models.CASCADE, default=1)#, blank=True, null=True, default=None

    sites = models.ManyToManyField(
        Site, verbose_name='Сайты для отображения', default=settings.SITE_ID, blank=True)

    parent = models.ForeignKey(Page, null=True, blank=False, db_index=True, verbose_name='Родительская страница',
                               on_delete=models.SET_NULL, limit_choices_to={'page_type': settings.PAGE_TYPE_CATALOG})

    is_new = models.BooleanField(default=True, verbose_name='Новинка')
    is_closeout = models.BooleanField(default=False, verbose_name='Распродажа')
    is_bestseller = models.BooleanField(default=False, verbose_name='Хит продаж')
    in_archive = models.BooleanField(default=False, verbose_name='В архиве')
    #is_collection = models.BooleanField(default=False, verbose_name='Размерный ряд')

    objects = ProductManager()
    objects_all = models.Manager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('ordering', '-id')

    def __str__(self):
        return self.title

    @mark_safe
    def active(self):
        if self in Product.objects.all():
            return '<img src="/static/admin/img/icon-yes.svg" alt="True">'
        return '<img src="/static/admin/img/icon-no.svg" alt="False">'
    active.short_description = 'Активен'

    def save(self, *args, **kwargs):
        # brand / category
        self.brand = self.brand_category.brand
        self.category = self.brand_category.category
        #self.vendor_code = 'A' + str(self.id)
        # auto prices
        purchase_price = self.purchase_price
        self.retailer_price_auto = purchase_price + self.brand_category.markup_for_retailer
        self.retailer_total_price_auto = self.retailer_price if self.retailer_price else self.retailer_price_auto
        self.dropshipper_price_auto = purchase_price + self.brand_category.markup_for_dropshipper
        self.dropshipper_total_price_auto = self.dropshipper_price if self.dropshipper_price else self.dropshipper_price_auto
        if self.brand_category.markup_for_wholesaller_type == self.brand_category.MURKUP_TYPE.PLN:
            self.wholesaller_price_auto = purchase_price + self.brand_category.markup_for_wholesaller
        else:
            self.wholesaller_price_auto = purchase_price + purchase_price * self.brand_category.markup_for_wholesaller / 100
        self.wholesaller_total_price_auto = self.wholesaller_price if self.wholesaller_price else self.wholesaller_price_auto
        # create slug
        super(Product, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = self.get_slug()
        super(Product, self).save(*args, **kwargs)
        # calculate in stock
        if self.is_in_stock and self.product_skus.all():
            self.stock = self.product_skus.aggregate(models.Sum('in_stock_count'))['in_stock_count__sum']
        super(Product, self).save(*args, **kwargs)
        from garpix_cart_rest.models import CartItem
        for item in self.product_skus.values('sku_cart_items'):
            cart_item = CartItem.objects.filter(id=item['sku_cart_items']).first()
            if cart_item: cart_item.save()
        for item in self.product_cart_packs.all():
            item.save()

    def get_slug(self):
        slug = f'product-{self.id}-{self.title}'
        return slugify(slug)

    def get_condition(self):
        if self.product_rc:
            return self.product_rc
        else:
            return self.brand.get_condition()

    def get_in_pack_count(self, color):
        from . import Pack, SizeRangePack
        condition = self.get_condition()
        if type(condition) == Pack:
            return condition.number
        elif type(condition) == SizeRangePack:
            sizes_count = self.product_skus.filter(color=color).count()
            return condition.number * sizes_count
        return 0

    def get_existing_products_count(self):
        return self.product_skus.aggregate(models.Sum('in_stock_count'))['in_stock_count__sum']

    def delete(self, using=None, keep_parents=False):
        from content.models import ReviewPhoto
        from . import ProductImage, ProductSkuImage
        reviews = self.product_reviews.all()
        photos = ProductImage.objects.filter(product=self)
        photo_product_skus = ProductSkuImage.objects.filter(product_sku__product=self)
        for review in reviews:
            for photo in photos:
                rp = ReviewPhoto(image=photo.image, image_thumb=photo.image_thumb,
                                 review=review)
                rp.save()
            for photo in photo_product_skus:
                rp = ReviewPhoto(image=photo.image, image_thumb=photo.image_thumb,
                                 review=review)
                rp.save()
        super(Product, self).delete()

    def get_image(self):
        return settings.SITE_URL + self.image_thumb

    def get_full_image(self):
        return settings.SITE_URL + self.image.url

    def get_all_images_list(self):
        images_list = []
        if self.image_thumb:
            images_list.append(self.image_thumb)
        images_list.extend(image.image_thumb for image in self.product_images.all())
        # for sku in self.product_skus.all():
        #     if sku.image:
        #         images_list.append(sku.image)
        #     images_list.extend(image.image for image in sku.product_sku_images.all())
        return images_list

    def get_skus_ids_by_condition(self, color=None, size=None):
        from . import SizeRangePack, Pack
        condition = self.get_condition()
        if type(condition) == Pack:
            sku = self.product_skus.filter(color=color, size=size).first()
            if sku:
                return [sku.id, ]
        if type(condition) == SizeRangePack:
            skus = self.product_skus.filter(color=color)
            if skus:
                return [sku.id for sku in skus]
        return []

    def get_skus_by_condition(self, color=None, size=None):
        from . import SizeRangePack, Pack
        condition = self.get_condition()
        if type(condition) == Pack:
            sku = self.product_skus.filter(color=color, size=size).first()
            if sku:
                return [sku, ]
        if type(condition) == SizeRangePack:
            skus = self.product_skus.filter(color=color)
            if skus:
                return [sku for sku in skus]
        return []

    def get_prices(self, user, currency=1.00):
        currency = Decimal(currency)

        if user and user.is_authenticated and user.status == 3:
            if user.profile.role == user.profile.ROLE.WHOLESALE:
                if self.wholesaller_price:
                    return {
                        'price': self.wholesaller_price / currency,
                        'old_price': self.wholesaller_price_auto / currency if self.wholesaller_price < self.wholesaller_price_auto else None
                    }
                return {'price': self.wholesaller_price_auto / currency, 'old_price': None}
            if user.profile.role == user.profile.ROLE.DROPSHIPPER:
                if self.dropshipper_price:
                    return {
                        'price': self.dropshipper_price / currency,
                        'old_price': self.dropshipper_price_auto / currency if self.dropshipper_price < self.dropshipper_price_auto else None
                    }
                return {'price': self.dropshipper_price_auto / currency, 'old_price': None}
            if self.retailer_price:
                return {
                    'price': self.retailer_price / currency,
                    'old_price': self.retailer_price_auto / currency if self.retailer_price < self.retailer_price_auto else None
                    }
        """else:
            return {
                'price': self.retailer_price / currency,
                'old_price': self.retailer_price_auto / currency if self.retailer_price < self.retailer_price_auto else None
            }"""
        return {'price': self.retailer_price_auto / currency, 'old_price': None}

    @classmethod
    def get_products_in_collection(cls):
        products = cls.objects.prefetch_related('product_collections').filter(
            product_collections__isnull=False, product_collections__status=0).distinct()
        return products

    def get_media(self, size=None, color=None):
        from garpix_catalog.models import Color
        skus = self.product_skus.all()
        if color:
            color = Color.objects.filter(id=color).first()
        else:
            color = skus.first().color
        skus = skus.filter(color=color)
        media = list()
        media.append(self.get_image_paths())
        media.extend(image.get_image_paths() for image in self.product_images.all())
        for sku in skus:
            if sku.get_image_paths():
                media.append(sku.get_image_paths())
            media.extend(image.get_image_paths() for image in sku.product_sku_images.all())
        media.extend(video.get_video_paths() for video in self.product_videos.all())
        for sku in skus:
            media.extend(video.get_video_paths() for video in sku.product_sku_videos.all())
        return media

    def get_sizes(self, size=None, color=None):
        from ..models import Size
        if color:
            pass
        else:
            color = self.product_skus.first().color.id
        sizes = Size.objects.filter(size_skus__in=self.get_skus_by_filter(color=color)).distinct()
        if size:
            sku = self.product_skus.filter(size=size, color=color).first()
            if sku:
                size_id = sku.size.id
            else:
                size_id = sizes.first().id
        else:
            size_id = sizes.first().id
        return [
            {
                'id': s.id,
                'title': s.get_size_name(),
                'selected': True if s.id == size_id else False,
            } for s in sizes
        ]

    def get_colors(self, size=None, color=None):
        from ..models import Color
        all_colors = Color.objects.filter(color_skus__in=self.product_skus.all()).distinct()
        if color:
            color_id = int(color)
        else:
            color_id = self.product_skus.first().color.id
        return [
            {
                'id': c.id,
                'title': c.title,
                'color': c.color,
                'selected': True if c.id == color_id else False,
            } for c in all_colors
        ]

    def get_skus_by_filter(self, size=None, color=None):
        skus = self.product_skus.all()
        if size:
            skus = skus.filter(size=size)
        if color:
            skus = skus.filter(color=color)
        return skus

    def get_in_cart_count(self, size=None, color=None, user=None):
        from ..models import Size, Color
        if color:
            color_id = int(color)
        else:
            color_id = self.product_skus.first().color.id
        color = Color.objects.filter(id=color_id).first()
        sizes = Size.objects.filter(size_skus__in=self.get_skus_by_filter(color=color)).distinct()
        if size:
            sku = self.product_skus.filter(size=size, color__id=color_id).first()
            if sku:
                size_id = sku.size.id
            else:
                size_id = sizes.first().id
        else:
            size_id = sizes.first().id
        size = Size.objects.filter(id=size_id).first()

        if not user or not user.is_authenticated:
            return 0
        cart = user.get_cart()
        if cart:
            skus = self.get_skus_by_filter(size=size, color=color)
            items_in_cart_count = cart.cart_items.filter(
                product__in=skus, pack=None, status=0).aggregate(in_cart_count=models.Sum('qty'))['in_cart_count']
            packs_in_cart = cart.cart_packs.filter(product=self, size=size, status=0)
            if packs_in_cart and color:
                packs_in_cart = packs_in_cart.filter(color=color)
            packs_in_cart_count = packs_in_cart.aggregate(in_cart_count=models.Sum('qty'))['in_cart_count']
            if not items_in_cart_count:
                items_in_cart_count = 0
            if not packs_in_cart_count:
                packs_in_cart_count = 0
            return items_in_cart_count + packs_in_cart_count
        return 0

    def get_in_stock_count(self, size=None, color=None):
        from ..models import Size
        if color:
            color_id = color
        else:
            color_id = self.product_skus.first().color.id
        sizes = Size.objects.filter(size_skus__in=self.get_skus_by_filter(color=color)).distinct()
        if size:
            sku = self.product_skus.filter(size__id=size, color__id=color_id).first()
            if sku:
                size_id = sku.size.id
            else:
                size_id = sizes.first().id
        else:
            size_id = sizes.first().id
        sku = self.product_skus.filter(size__id=size_id, color__id=color_id).first()
        if sku:
            return sku.in_stock_count
        return 0

    def get_is_liked(self, user):
        if hasattr(user, 'profile'):
            liked_product = user.profile.user_wishlist_items.filter(product__id=self.id)
            return liked_product.exists()
        return False

    @classmethod
    def get_photos_by_qs(cls, qs):

        def get_photo_item(photo):
            return {
                'origin': settings.SITE_URL + photo.image.url,
                'thumb': settings.SITE_URL + photo.image_thumb,
            }

        all_photos = []
        for product in qs:
            if product.image:
                all_photos.append(get_photo_item(product))
            for product_image in product.product_images.all():
                if product_image.image:
                    all_photos.append(get_photo_item(product_image))
            for sku in product.product_skus.all():
                if sku.image:
                    all_photos.append(get_photo_item(sku))
                for product_sku_image in sku.product_sku_images.all():
                    if product_sku_image.image:
                        all_photos.append(get_photo_item(product_sku_image))
        return all_photos
