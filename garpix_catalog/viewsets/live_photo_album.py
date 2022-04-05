from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from garpix_catalog.permissions import IsAdminOrReadOnly
from ..models import LivePhotoAlbum
from ..serializers.live_photo import LivePhotoAlbumSerializer
from utils.pagination import CustomPagination


class LivePhotoAlbumPagination(CustomPagination):
    pass


class LivePhotoAlbumViewSet(ModelViewSet):
    queryset = LivePhotoAlbum.objects.all()
    serializer_class = LivePhotoAlbumSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = LivePhotoAlbumPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = {
        'brand': ['exact', ],
        'created_at': ['lte', 'gte']
    }
    ordering_fields = ['created_at', ]

    def get_queryset(self):
        return self.queryset.exclude(image='').exclude(brand=None).exclude(
            live_photo_photos=None, live_photo_videos=None).distinct()
