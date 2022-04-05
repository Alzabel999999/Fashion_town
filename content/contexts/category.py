from ..serializers import PageSerializer
from garpix_catalog.models import Producer, Product, ProductImage, Category, ProductSku, Brand, Color
from garpix_catalog.serializers import BrandSerializer, CategorySerializer, ProductListSerializer
from ..serializers import BrandSerializer, CategorySerializer, ColorSerializer
from .common import common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    categories = CategorySerializer(Category.objects.filter(is_active=True), many=True).data
    brands = BrandSerializer(Brand.objects.filter(is_active=True), many=True).data
    filter_by_brand = brands
    filter_by_color = ColorSerializer(Color.objects.all(), many=True).data
    filter_by_size = [{'id': size[0], 'title': size[1]} for size in ProductSku.SIZE.TYPES]
    products = ProductListSerializer(Product.objects.filter(category__id=page.id)[:30], many=True,
                                     context={'user': user, 'currency': currency}).data

    context = {
        'page_info': PageSerializer(page).data,
        'categories': categories,
        'brands': brands,
        'multy_choise_filters': {
            'by_brand': filter_by_brand,
            'by_color': filter_by_color,
            'by_size': filter_by_size,
        },
        'products': products
    }
    context.update(common_context(user, page))

    return context
