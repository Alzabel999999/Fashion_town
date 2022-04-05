from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import ShopRequisites
from ..serializers import ShopRequisitesSerializer
from user.permissions import IsOwnerOrReject
from rest_framework.permissions import IsAuthenticated


class ShopRequisitesViewSet(GenericViewSet):
    queryset = ShopRequisites.objects.all()
    serializer_class = ShopRequisitesSerializer
    permission_classes = [IsOwnerOrReject, IsAuthenticated]

    @action(methods=['GET', ], detail=False)
    def shop_requisites(self, request, *args, **kwargs):
        requisites = get_requisites(request)
        if requisites:
            serializer = self.serializer_class(requisites, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'requisites': '', 'id': None})

    @action(methods=['POST', ], detail=False)
    def update_shop_requisites(self, request, *args, **kwargs):
        requisites = get_requisites(request)
        data = request.data.copy()
        if requisites:
            serializer = self.get_serializer(requisites, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(requisites, '_prefetched_objects_cache', None):
                requisites._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_200_OK)
        shop = request.user.profile.profile_shop
        data.update({'shop': shop})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_requisites(request):
    shop = request.user.profile.profile_shop
    if hasattr(shop, 'shop_requisites'):
        return shop.shop_requisites
    return None
