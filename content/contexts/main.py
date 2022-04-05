from django.db.models import Sum

from ..serializers import BannerSerializer, MainPageSerializer, NewsListSerializer, ReviewSerializer, PageSerializer
from ..models import Banner, MainPage, News, Review
from app.settings import BANNER_TYPE_MAIN_FIRST_PAGE, BANNER_TYPE_MAIN_FOR_PARTNER, BANNER_TYPE_MAIN_ABOUT
from .common import common_context
from garpix_catalog.models import Product, LivePhotoAlbum, Category
from garpix_catalog.serializers import ProductListSerializer, LivePhotoAlbumListSerializer


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs.get('user', None)
    currency = request.headers.get('currency', 'PLN')

    banners = BannerSerializer(Banner.objects.filter(banner_type=BANNER_TYPE_MAIN_FIRST_PAGE), many=True).data
    partner_banners = BannerSerializer(Banner.objects.filter(banner_type=BANNER_TYPE_MAIN_FOR_PARTNER), many=True).data
    about_banner = BannerSerializer(Banner.objects.filter(banner_type=BANNER_TYPE_MAIN_ABOUT).first(), many=False).data

    products = Product.objects.filter(is_in_stock=True, product_skus__in_stock_count__gt=0).distinct()
    in_stock_category = Category.objects.filter(
            category_products__is_in_stock=True, category_products__product_skus__in_stock_count__gt=0).distinct().first()
    if in_stock_category:
        products = products.filter(category=in_stock_category)
    serialized_products = ProductListSerializer(products[:12], many=True,
                                                context={'user': user, 'currency': currency}).data

    user_role = user.profile.role if user else 0
    if user_role == 3:
        news = News.objects.filter(is_for_wholesaler=True)
    elif user_role == 2:
        news = News.objects.filter(is_for_dropshipper=True)
    else:
        news = News.objects.filter(is_for_retailer=True)
    serialized_news = NewsListSerializer(news[:4], many=True).data

    serialized_live_photos = LivePhotoAlbumListSerializer(LivePhotoAlbum.objects.all()[:6], many=True).data

    serialized_service_reviews = ReviewSerializer(
        Review.approved_objects.filter(product__isnull=True)[:3], many=True, context={'user': user}).data
    serialized_product_reviews = ReviewSerializer(
        Review.approved_objects.filter(product__isnull=False)[:3], many=True, context={'user': user}).data

    context = {
        'page_info': PageSerializer(page).data,
        'main_page': MainPageSerializer(MainPage.get_solo()).data,
        'banners': banners,
        'partner_banners': partner_banners,
        'about_banner': about_banner,
        'products': serialized_products,
        'news': serialized_news,
        'live_photos': serialized_live_photos,
        'reviews': {'service_reviews': serialized_service_reviews, 'product_reviews': serialized_product_reviews},
    }
    context.update(common_context(user, page))

    return context
