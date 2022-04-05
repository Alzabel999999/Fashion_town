from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from garpix_catalog.permissions import IsAdminOrReadOnly
from ..models import Banner
from ..serializers import BannerSerializer


class BannerViewSet(ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filter_fields = {
        'banner_type': ['exact', ],
    }
