from django.conf import settings
from django.db.models import F, Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from garpix_catalog.permissions import IsAdminOrReadOnly
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from ..models import Product, ShopProduct, Category, ShopCategoryMarkup
from ..serializers import CabinetCategoryMarkupListSerializer, CabinetCategoryMarkupUpdateSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import django_filters


class ShopCategoryMarkupViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Category.objects_with_products.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = {
        'title': ['icontains', ],
    }
    ordering_fields = ('title',)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CabinetCategoryMarkupUpdateSerializer
        return CabinetCategoryMarkupListSerializer

    def get_queryset(self):
        # if self.action in ['update', 'partial_update']:
        #     return ShopCategoryMarkup.objects.all()
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = kwargs.get('pk', None)
        shop = request.user.profile.profile_shop
        category = self.get_object()
        instance = category.category_markups.filter(shop=shop, category__id=pk).first()
        if not instance:
            instance = ShopCategoryMarkup.objects.create(shop=shop, category=category)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

