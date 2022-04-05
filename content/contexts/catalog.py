from ..serializers import PageSerializer
from garpix_catalog.models import Producer, Product, ProductImage, Category, ProductSku, Brand, Color, Size
from ..serializers import BrandSerializer, ColorSerializer
from garpix_catalog.serializers import (
    BrandSerializer,
    ColorSerializer,
    ProductListSerializer,
    CategoryListSerializer,
    CategoryRawListSerializer,
)
from .common import common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    all_categories = CategoryRawListSerializer(Category.objects_with_products.filter(is_active=True), many=True).data
    parent_categories = CategoryListSerializer(
        Category.objects_with_products.filter(is_active=True, parent=None), many=True).data
    brands = BrandSerializer(Brand.objects_with_products.filter(is_active=True), many=True).data
    filter_by_brand = brands
    filter_by_type = all_categories
    filter_by_color = ColorSerializer(Color.objects.all(), many=True).data
    filter_by_size = [{'id': size.id, 'title': size.get_size_name()} for size in Size.objects.all()]
    products = ProductListSerializer(Product.objects.all()[:30], many=True,
                                     context={'user': user, 'currency': currency}).data

    context = {
        'page_info': PageSerializer(page).data,
        'categories': parent_categories,
        'brands': brands,
        'multy_choise_filters': {
            'by_brand': filter_by_brand,
            'by_type': filter_by_type,
            'by_color': filter_by_color,
            'by_size': filter_by_size,
        },
        'products': products,
    }
    context.update(common_context(user, page))

    return context
