from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from garpix_catalog.permissions import IsAdminOrReadOnly
from ..models import News
from ..serializers import NewsSerializer, NewsListSerializer
from utils.pagination import CustomPagination


class NewsPagination(CustomPagination):
    pass


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = NewsPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = {
        'is_for_retailer': ['exact', ],
        'is_for_wholesaler': ['exact', ],
        'is_for_dropshipper': ['exact', ],
        'rubrics': ['exact', ],
    }
    ordering_fields = ['updated_at', ]

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.profile.role == 2:
                return self.queryset.filter(is_for_dropshipper=True)
            if user.profile.role == 3:
                return self.queryset.filter(is_for_wholesaler=True)
        return self.queryset.filter(is_for_retailer=True)
