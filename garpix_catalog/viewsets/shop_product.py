from django.conf import settings
from django.db.models import F, Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from user.permissions import IsOwnerOrReject
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from ..models import Product, ShopProduct
from ..serializers import (
    CabinetProductMainListSerializer,
    CabinetCreateProductSerializer,
    CabinetProductMyListSerializer,
    CabinetUpdateProductSerializer,
)
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import django_filters
from utils.pagination import CustomPagination


class ShopProductFilter(django_filters.FilterSet):
    is_bestseller = django_filters.BooleanFilter(field_name='is_bestseller')
    is_new = django_filters.BooleanFilter(field_name='is_new')
    is_closeout = django_filters.BooleanFilter(field_name='is_closeout')
    sizes = django_filters.BaseInFilter(field_name='product_skus__size', lookup_expr='in')
    colors = django_filters.BaseInFilter(field_name='product_skus__color', lookup_expr='in')
    brands = django_filters.BaseInFilter(field_name='brand', lookup_expr='in')
    sertificate = django_filters.BooleanFilter(field_name='product__brand__sertificate')

    is_in_stock = django_filters.BooleanFilter(method='is_in_stock_filter')
    is_not_range = django_filters.BooleanFilter(method='is_not_range_filter')
    is_in_collection = django_filters.BooleanFilter(method='is_in_collection_filter')
    category = django_filters.Filter(method='category_filter')
    product = django_filters.Filter(field_name='title', lookup_expr='icontains')
    categories = django_filters.BaseInFilter(method='categories_filter', lookup_expr='in')

    class Meta:
        model = Product
        fields = (
            'is_in_stock', 'is_bestseller', 'is_new', 'is_closeout',
            'is_not_range', 'is_in_collection', 'category',
            'sizes', 'colors', 'categories', 'brands', 'sertificate',
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


class ShopProductPagination(CustomPagination):
    pass


class ShopProductViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Product.objects.all().distinct().annotate(redeemed=Count(
        'product_skus__product_ordered_skus', filter=Q(
            product_skus__product_ordered_skus__status=settings.ORDER_ITEM_STATUS_REDEEMED)))
    permission_classes = [IsOwnerOrReject, IsAuthenticated]
    filterset_class = ShopProductFilter
    pagination_class = ShopProductPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['price', 'created_at', 'redeemed']

    def get_serializer_class(self):
        if self.action == 'create':
            return CabinetCreateProductSerializer
        if self.action == 'my_catalog':
            return CabinetProductMyListSerializer
        if self.action in ['update', 'partial_update']:
            return CabinetUpdateProductSerializer
        return CabinetProductMainListSerializer

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'delete']:
            return ShopProduct.objects.all()
        return self.queryset

    @action(methods=['get', ], detail=False)
    def main_catalog(self, request, *args, **kwargs):
        shop_id = request.user.profile.profile_shop.id
        products = ShopProduct.get_products_not_in_shop_qs(shop_id).annotate(
            price=F('dropshipper_total_price_auto')).annotate(
            redeemed=Count('product_skus__product_ordered_skus', filter=Q(
                product_skus__product_ordered_skus__status=settings.ORDER_ITEM_STATUS_REDEEMED)))
        queryset = self.filter_queryset(products)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get', ], detail=False)
    def my_catalog(self, request, *args, **kwargs):
        shop_id = request.user.profile.profile_shop.id
        products = ShopProduct.get_products_in_shop_qs(shop_id).order_by('-id').annotate(
            price=F('dropshipper_total_price_auto')).annotate(
            redeemed=Count('product_skus__product_ordered_skus', filter=Q(
                product_skus__product_ordered_skus__status=settings.ORDER_ITEM_STATUS_REDEEMED)))
        queryset = self.filter_queryset(products)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        shop = request.user.profile.profile_shop
        if not shop or not data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for data_item in data:
            ShopProduct.create(shop=shop, data=data_item)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['DELETE', ], detail=False)
    def delete(self, request, *args, **kwargs):
        product_ids = request.data.get('product_id', [])
        if not product_ids:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for pk in product_ids:
            instance = self.get_queryset().filter(id=pk).first()
            if instance:
                instance.delete()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = kwargs.get('pk', None)
        instance = self.get_queryset().filter(id=pk).first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
