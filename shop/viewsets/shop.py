from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from user.permissions import IsDropShipperOrReject
from ..models import Shop
from ..serializers import ShopSerializer, ShopCreateSerializer, ShopUpdateSerializer
from user.models import Profile


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated, IsDropShipperOrReject, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return ShopCreateSerializer
        if self.action in ['update', 'partial_update']:
            return ShopUpdateSerializer
        return ShopSerializer

    def create(self, request, *args, **kwargs):
        # todo отправить заявку админу
        profile = request.user.profile.id
        data = request.data.copy()
        data.update({'profile': profile})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            profile = Profile.objects.filter(id=data.get('profile')).first()
            if profile.role == 2:
                site = Site.objects.create(domain=data.get('domain'), name=data.get('title'))
                Shop.objects.create(
                    profile=profile,
                    site=site,
                    title=data.get('title'),
                    first_name=data.get('first_name'),
                    middle_name=data.get('middle_name'),
                    last_name=data.get('last_name'),
                    comment=data.get('comment'),
                )
        except Exception as e:
            print(str(e))
            return Response({'status': False}, status=400)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # todo отправить заявку админу на удаление
        return Response()
