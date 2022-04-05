from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from ..models import Promocode
from ..serializers import PromocodeSerializer


class PromocodeViewSet(ModelViewSet):
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        profile = self.request.user.profile
        shop = profile.profile_shop if hasattr(profile, 'profile_shop') else None
        return self.queryset.filter(shop=shop)

    def create(self, request, *args, **kwargs):
        shop = request.user.profile.profile_shop
        data = request.data
        if 'title' not in data.keys() or 'discount' not in data.keys() or not shop:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data.update({'shop': shop})
        try:
            promocode = Promocode.objects.create(
                shop=shop, title=request.data['title'], discount=request.data['discount']
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(promocode)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['DELETE', ], detail=False)
    def delete_all(self, request, *args, **kwargs):
        shop = request.user.profile.profile_shop
        try:
            shop.shop_promocodes.all().delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
