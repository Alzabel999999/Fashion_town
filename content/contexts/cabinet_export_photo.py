from ..serializers import PageSerializer
from garpix_catalog.models import Producer, Product, ProductImage, Category, ProductSku, Brand, Color, Size
from garpix_catalog.serializers import BrandSerializer, CategorySerializer, ProductListSerializer
from ..serializers import BrandSerializer, CategorySerializer, ColorSerializer
from .common import common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']

    categories = CategorySerializer(Category.objects.filter(is_active=True), many=True).data
    brands = BrandSerializer(Brand.objects.filter(is_active=True), many=True).data
    filter_by_brand = brands
    filter_by_color = ColorSerializer(Color.objects.all(), many=True).data
    filter_by_size = [{'id': size.id, 'title': size.get_size_name()} for size in Size.objects.all()]

    context = {
        'page_info': PageSerializer(page).data,
        'categories': categories,
        'brands': brands,
        'multy_choise_filters': {
            'by_brand': filter_by_brand,
            'by_color': filter_by_color,
            'by_size': filter_by_size,
        },
    }
    context.update(common_context(user, page))

    return context
