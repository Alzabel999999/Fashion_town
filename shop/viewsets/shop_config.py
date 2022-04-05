from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsOwnerOrReject
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import ShopConfig
from ..serializers import ShopConfigSerializer


class ShopConfigViewSet(GenericViewSet):
    queryset = ShopConfig.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReject]

    def get_serializer_class(self):
        return ShopConfigSerializer
    
    @action(methods=['GET', ], detail=False)
    def shop_config(self, request, *args, **kwargs):
        instance = request.user.profile.profile_shop.shop_config
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['PUT', ], detail=False)
    def update_shop_config(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user.profile.profile_shop.shop_config
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        instance.update_double(serializer.validated_data)
        return Response(self.get_serializer(instance).data)
