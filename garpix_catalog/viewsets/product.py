from django.conf import settings
from django.db.models import F, Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from garpix_catalog.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ..models import Product, Brand
from ..serializers.product import ProductListSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import django_filters
from utils.pagination import CustomPagination


class ProductFilter(django_filters.FilterSet):
    is_bestseller = django_filters.BooleanFilter(field_name='is_bestseller')
    is_new = django_filters.BooleanFilter(field_name='is_new')
    is_closeout = django_filters.BooleanFilter(field_name='is_closeout')
    sizes = django_filters.BaseInFilter(field_name='product_skus__size', lookup_expr='in')
    colors = django_filters.BaseInFilter(field_name='product_skus__color', lookup_expr='in')
    brands = django_filters.BaseInFilter(field_name='brand', lookup_expr='in')
    sertificate = django_filters.BooleanFilter(field_name='brand__sertificate')
    producer = django_filters.Filter(field_name='brand__producer')
    is_in_stock = django_filters.BooleanFilter(method='is_in_stock_filter')
    is_not_range = django_filters.BooleanFilter(method='is_not_range_filter')
    is_in_collection = django_filters.BooleanFilter(method='is_in_collection_filter')
    category = django_filters.Filter(method='category_filter')
    categories = django_filters.BaseInFilter(method='categories_filter', lookup_expr='in')
    is_polish = django_filters.BooleanFilter(method='is_polish_filter')
    is_import = django_filters.BooleanFilter(method='is_import_filter')

    class Meta:
        model = Product
        fields = (
            'is_in_stock', 'is_bestseller', 'is_new', 'is_closeout',
            'is_not_range', 'is_in_collection', 'category', 'producer',
            'sizes', 'colors', 'categories', 'brands', 'sertificate',
            'is_polish', 'is_import',
        )

    def is_not_range_filter(self, request, name, value):
        if value:
            return request.exclude(product_rc__rc_type=1).exclude(brand__brand_rc__rc_type=1)
        return request

    def is_in_stock_filter(self, request, name, value):
        if value:
            qs = request.filter(is_in_stock=True, stock__gt=0)
            return qs
        return request

    def is_in_collection_filter(self, request, name, value):
        if value:
            return request.filter(product_collections__status=0)
        return request

    def category_filter(self, request, name, value):
        qs = request.filter(Q(category=value) | Q(category__parent=value)).distinct()
        return qs

    def categories_filter(self, request, name, value):
        qs = request.filter(Q(category__in=value) | Q(category__parent__in=value)).distinct()
        return qs

    def is_polish_filter(self, request, name, value):
        #if not value:
        return request.exclude(brand__producer=Brand.PRODUCER.IMPORT)
        #return request

    def is_import_filter(self, request, name, value):
        #if not value:
        return request.exclude(brand__producer=Brand.PRODUCER.POLAND)
        #return request


class ProductListByIdsFilter(django_filters.FilterSet):
    ids = django_filters.BaseInFilter(field_name='id', lookup_expr='in')

    class Meta:
        model = Product
        fields = (
            'ids',
        )


class ProductPagination(CustomPagination):
    pass


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().distinct().annotate(redeemed=Count(
        'product_skus__product_ordered_skus', filter=Q(
            product_skus__product_ordered_skus__status=settings.ORDER_ITEM_STATUS_REDEEMED)))
    queryset = queryset.filter(in_archive=False)
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['price', 'created_at', 'redeemed']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductSerializer
        return ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            if request.user.profile.role == 3:
                price = 'wholesaller_total_price_auto'
            elif request.user.profile.role == 2:
                price = 'dropshipper_total_price_auto'
            else:
                price = 'retailer_total_price_auto'

        else:
            price = 'retailer_total_price_auto'
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.annotate(price=F(price))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET', ], detail=False, serializer_class=ProductListSerializer, filterset_class=ProductListByIdsFilter)
    def list_by_ids(self, request, *args, **kwargs):
        if request.GET.get('ids', None):
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 400}, status=400)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def export_to_shop(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.profile and user.profile.role == 2:
            return Response({}, status=200)
        return Response(status=403)

    @action(methods=['GET', ], detail=False)
    def photos_list(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            if request.user.profile.role == 3:
                price = 'wholesaller_total_price_auto'
            elif request.user.profile.role == 2:
                price = 'dropshipper_total_price_auto'
            else:
                price = 'retailer_total_price_auto'

        else:
            price = 'retailer_total_price_auto'
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.annotate(price=F(price))
        photos = Product.get_photos_by_qs(queryset)
        page = self.paginate_queryset(photos)
        if page is not None:
            return self.get_paginated_response(page)
        return Response({
            'count': len(photos),
            'next': None,
            'previous': None,
            'result': photos
        })

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def download_photos(self, request, *args, **kwargs):
        import zipfile
        import os
        from datetime import datetime
        user = request.user
        profile = user.profile
        selected_photos = request.data['photos']
        photos = []
        for photo in selected_photos:
            photos.append(photo['origin'])
        count = len(photos)
        available_for_download = profile.get_available_for_download()
        if available_for_download >= count:
            profile.set_download_count(count)
            today = datetime.now()
            now = today.strftime('%Y%m%d%H%M%S')
            filename = f"photos_{profile.id}{now}.zip"
            zip_path = settings.MEDIA_ROOT + '/uploads/%s/%s/%s' % (today.year, today.month, filename)
            with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                for file in photos:
                    file = file.replace(settings.SITE_URL, '')
                    file_path = os.path.join(settings.BASE_DIR, '..', 'public') + file
                    zf.write(file_path, os.path.basename(file_path))
            file_url = settings.SITE_URL + zf.filename.split('public')[-1]
            return Response({'url': file_url}, status=200)
        return Response(status=400)
