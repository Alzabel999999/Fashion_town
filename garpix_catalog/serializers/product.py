from decimal import Decimal
from django.db.models import Sum
from rest_framework import serializers
from ..models import Product, ProductImage, ProductVideo, ProductSku, ProductSkuImage, ProductSkuVideo, Color, Currency
from ..mixins.serializers import FullImagePathMixin
from django.conf import settings
from garpix_order.models import Collection
from garpix_order.serializers import CollectionSerializer
from ..serializers.product_sku import ProductSkuSerializer


class ProductImageSerializer(FullImagePathMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'description', 'image', 'image_thumb', 'ordering', ]


class ProductVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField(read_only=True)
    video_preview = serializers.SerializerMethodField(read_only=True)

    def get_video(self, obj):
        return obj.get_video()

    def get_video_preview(self, obj):
        return obj.get_video_preview()

    class Meta:
        model = ProductVideo
        fields = ['id', 'product', 'description', 'video', 'video_preview', 'ordering']


class ProductImageSkuSerializer(FullImagePathMixin, serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return obj.product_sku.product.id

    class Meta:
        model = ProductSkuImage
        fields = ['id', 'product', 'description', 'image', 'image_thumb', 'ordering', ]


class ProductVideoSkuSerializer(FullImagePathMixin, serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField(read_only=True)
    video_preview = serializers.SerializerMethodField(read_only=True)

    def get_product(self, obj):
        return obj.product_sku.product.id

    def get_video(self, obj):
        return obj.get_video()

    def get_video_preview(self, obj):
        return obj.get_video_preview()

    class Meta:
        model = ProductSkuVideo
        fields = ['id', 'product', 'description', 'video', 'video_preview', 'ordering', ]


class ProductSerializer(serializers.ModelSerializer):

    product_rc = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    in_cart_count = serializers.SerializerMethodField()
    in_stock_count = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    collections = serializers.SerializerMethodField()
    is_collection = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    def get_article(self, obj):
        try:
            return obj.vendor_code
        except:
            return ''

    def get_media(self, obj):
        filters = get_filters(self)
        return obj.get_media(size=filters['size'], color=filters['color'])

    def get_colors(self, obj):
        filters = get_filters(self)
        return obj.get_colors(size=filters['size'], color=filters['color'])

    def get_sizes(self, obj):
        filters = get_filters(self)
        return obj.get_sizes(size=filters['size'], color=filters['color'])

    def get_in_cart_count(self, obj):
        filters = get_filters(self)
        return obj.get_in_cart_count(size=filters['size'], color=filters['color'], user=get_user(self))

    def get_in_stock_count(self, obj):
        if obj.is_in_stock:
            filters = get_filters(self)
            return obj.get_in_stock_count(size=filters['size'], color=filters['color'])
        return 0

    def get_product_rc(self, obj):
        return obj.get_condition().__str__()

    def get_is_collection(self, obj):
        try:
            if obj.product_rc.rc_type == 1:
                return True
            else:
                return False
        except:
            return False

    def get_prices(self, obj):
        user = get_user(self)
        currency = get_currency(self)
        prices = get_prices(obj, user=user, currency=currency)
        more_3_item_price = round(prices['price'] * 0.95,2) if prices['price'] else None
        more_5_item_price = round(prices['price'] * 0.90,2) if prices['price'] else None
        prices.update({'more_3_item_price': more_3_item_price, 'more_5_item_price': more_5_item_price})
        return prices

    def get_is_in_stock(self, obj):
        return True if obj.product_skus.filter(is_in_stock=True).count() > 0 else False

    def get_is_liked(self, obj):
        user = get_user(self)
        return obj.get_is_liked(user)

    def get_category(self, obj):
        return obj.category.title

    def get_brand(self, obj):
        return obj.brand.title

    def get_review(self, obj):
        reviews = obj.product_reviews.filter(is_approved=True)
        if reviews:
            reviews_count = reviews.count()
            stars_count = reviews.aggregate(stars_count=Sum('stars'))['stars_count']
            max_stars_count = reviews_count * 5
            return {
                'all_count': reviews_count,
                'stars_count': stars_count,
                'max_stars_count': max_stars_count,
                'all_count_percent': stars_count / max_stars_count * 5,
            }
        return {
            'all_count': 0,
            'all_count_percent': 0,
        }

    def get_collections(self, obj):
        user = get_user(self)
        if hasattr(user, 'profile'):
            if user.profile.role == 2:
                filters = get_filters(self)
                #collections = Collection.get_collections(product=obj, color=filters['color'])

                if filters['color']:
                    collections = Collection.get_collections(product=obj, color=filters['color'])
                else:
                    collections  = Collection.objects.filter(product=obj)
                return CollectionSerializer(collections, many=True).data
        return []

    def get_product_sku(self, obj):
        products_sku = obj.product_skus.all()
        return ProductSkuSerializer(products_sku, many=True).data




    class Meta:
        model = Product
        fields = [
            'id', 'title', 'category', 'brand',
            'page_type', 'slug',
            'media', 'colors', 'sizes', 'collections',
            'is_new', 'is_bestseller', 'is_closeout', 'is_in_stock', 'is_liked',
            'in_cart_count', 'in_stock_count',
            'prices', 'product_rc', 'is_collection', 'product_sku',
            'content', 'extra', 'short_content',
            'created_at', 'updated_at', 'ordering', 'review',
            'seo_title', 'seo_keywords', 'seo_description',
            'seo_author', 'seo_og_type', 'seo_image',
            'objects', 'on_site', 'article'
        ]


class ProductListSerializer(serializers.ModelSerializer):

    is_in_stock = serializers.SerializerMethodField(read_only=True)
    colors = serializers.SerializerMethodField(read_only=True)
    sizes = serializers.SerializerMethodField(read_only=True)
    prices = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    brand = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    product_rc = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    article = serializers.SerializerMethodField(read_only=True)

    def get_is_in_stock(self, obj):
        return True if obj.is_in_stock and obj.product_skus.all().aggregate(
            in_stock=Sum('in_stock_count'))['in_stock'] > 0 else False

    def get_colors(self, obj):
        colors = Color.objects.filter(color_skus__in=obj.product_skus.all()).distinct()
        return [{
            'title': color.title, 'color': color.color,
            'image': str(ProductSku.objects.filter(color=color, product=obj).first().get_image())
        } for color in colors]

    def get_sizes(self, obj):
        return obj.get_sizes()

    def get_prices(self, obj):
        user = get_user(self)
        currency = get_currency(self)
        return get_prices(obj, user=user, currency=currency)

    def get_images(self, obj):
        images = obj.get_all_images_list()[:4]
        return [settings.SITE_URL + image for image in images]

    def get_brand(self, obj):
        return obj.brand.title if obj.brand else ''

    def get_is_liked(self, obj):
        user = get_user(self)
        return obj.get_is_liked(user)

    def get_product_rc(self, obj):
        return obj.get_condition().__str__()

    def get_url(self, obj):
        return obj.slug

    def get_article(self, obj):
        try:
            return obj.vendor_code
        except:
            return ''

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'url', 'brand', 'is_liked', 'stock',
            'is_new', 'is_bestseller', 'is_closeout', 'is_in_stock',
            'colors', 'sizes', 'prices', 'images', 'product_rc', 'article'
        ]


def get_user(data):
    if 'user' in data.context.keys():
        return data.context['user']
    return data.context['request'].user


def get_currency(data):
    if 'currency' in data.context.keys():
        currency_title = data.context['currency']
    elif 'request' in data.context.keys():
        try:
            currency_title = data.context['request'].headers.get('currency', 'PLN')
        except Exception:
            currency_title = 'PLN'
    else:
        currency_title = 'PLN'
    if currency_title not in ['PLN', None]:
        currency = Currency.objects.filter(title=currency_title).first()
        return currency.ratio
    return 1.00


def get_prices(obj, user=None, currency=None):
    prices = obj.get_prices(user, currency)
    prices['price'] = round(float(prices['price']),2) if prices['price'] else None
    prices['old_price'] = round(float(prices['old_price']),2) if prices['old_price'] else None
    return prices


def get_filters(data):
    try:
        size = data.context['request'].GET.get('size', None)
    except:
        size = None
    try:
        color = data.context['request'].GET.get('color', None)
    except:
        color = None
    return {'size': size, 'color': color}


def get_skus_by_filters(filters):
    return
