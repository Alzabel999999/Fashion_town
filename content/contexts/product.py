from decimal import Decimal
from django.db.models import Sum
from .common import common_context
from ..models import Review
from ..serializers import PageSerializer
from garpix_catalog.models import Product, Color, Size, Currency
from garpix_catalog.serializers import ProductSerializer, ProductListSerializer


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    if user and user.is_authenticated and user.profile:
        from user.models import AlreadySaw
        AlreadySaw.add_or_update(product=page, profile=user.profile)
    currency = request.headers.get('currency', 'PLN')
    currency_obj = Currency.objects.filter(title=currency, ratio__gt=0).first()
    currency_ratio = currency_obj.ratio if currency_obj else Decimal('1.0000')

    all_product_reviews = Review.approved_objects.filter(product=page)
    reviews_count = all_product_reviews.count()
    reviews_statistic = get_reviews_statistic(all_product_reviews)
    in_category = ProductListSerializer(Product.objects.filter(category=page.category)[:30], many=True,
                                        context={'user': user, 'currency': currency}).data
    recommended = ProductListSerializer(Product.get_products_in_collection()[:30], many=True,
                                        context={'user': user, 'currency': currency}).data

    context = {
        'page_info': PageSerializer(page).data,
        'reviews_count': reviews_count,
        'reviews_statistic': reviews_statistic,
        'recommended': recommended,
        'in_category': in_category,
    }
    if user and user.is_authenticated and user.profile and user.profile.role in [2, 3]:
        context['recommended_price'] = (page.retailer_total_price_auto / currency_ratio).__ceil__()
    if user and user.is_authenticated and user.profile and user.profile.role == 3 and\
            page.get_condition().rc_type in [1, 2]:
        context['adding_type'] = 'pack'
    else:
        context['adding_type'] = 'item'
    context.update(common_context(user, page))

    return context


def get_reviews_statistic(reviews):
    if reviews.count() > 0:
        reviews_count = reviews.count()
        max_stars_count = reviews_count * 5
        stars_count = reviews.aggregate(stars_count=Sum('stars'))['stars_count']

        return {
            'all_count': reviews_count,
            'all_count_percent': stars_count / max_stars_count * 5,
            '1_stars_count': reviews.filter(stars=1).count(),
            '1_stars_percent': reviews.filter(stars=1).count() / reviews.count() * 100,
            '2_stars_count': reviews.filter(stars=2).count(),
            '2_stars_percent': reviews.filter(stars=2).count() / reviews.count() * 100,
            '3_stars_count': reviews.filter(stars=3).count(),
            '3_stars_percent': reviews.filter(stars=3).count() / reviews.count() * 100,
            '4_stars_count': reviews.filter(stars=4).count(),
            '4_stars_percent': reviews.filter(stars=4).count() / reviews.count() * 100,
            '5_stars_count': reviews.filter(stars=5).count(),
            '5_stars_percent': reviews.filter(stars=5).count() / reviews.count() * 100,
        }
    else:
        return {
            'all_count': reviews.count(),
            'all_count_percent': 0,
            '1_stars_count': 0,
            '1_stars_percent': 0,
            '2_stars_count': 0,
            '2_stars_percent': 0,
            '3_stars_count': 0,
            '3_stars_percent': 0,
            '4_stars_count': 0,
            '4_stars_percent': 0,
            '5_stars_count': 0,
            '5_stars_percent': 0,
        }
