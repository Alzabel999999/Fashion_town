from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from ..models import Brand
from ..serializers.brand import BrandListSerializer, BrandSerializer
import django_filters


class BrandFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    sertificate = django_filters.BooleanFilter(method='is_sertificate_filter')
    is_with_photo = django_filters.BooleanFilter(method='is_with_photo_filter')

    class Meta:
        model = Brand
        fields = (
            'title',
            'is_with_photo',
            'sertificate',
        )


    def is_with_photo_filter(self, request, name, value):
        if value:
            return request.exclude(brand_live_photo_albums=None)
        return request

    def is_sertificate_filter(self, request, name, value):
        if value and value is True:
            return request.filter(sertificate=value)
        if name:
            return request.filter(title=value)
        return request


class BrandViewSet(GenericViewSet, ViewSet):
    queryset = Brand.objects_with_products.filter(is_active=True)
    serializer_class = BrandListSerializer
    filter_class = BrandFilter

    filter_fields = {
         'title': ['icontains', ],
     }

    @action(detail=False, methods=['get'])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = BrandListSerializer(queryset, many=True)
        return Response(serializer.data)
