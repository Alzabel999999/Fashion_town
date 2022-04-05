from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsOwnerProfileOrReject
from ..models import DeliveryAddress
from ..serializers import DeliveryAddressSerializer
from utils.pagination import CustomPagination


class DeliveryAddressPagination(CustomPagination):
    pass


class DeliveryAddressViewSet(ModelViewSet):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfileOrReject]
    filter_backends = (DjangoFilterBackend, )
    pagination_class = DeliveryAddressPagination
    filter_fields = {
    }

    def get_queryset(self):
        _qs = self.queryset
        if self.request.user.is_authenticated:
            user = self.request.user
            qs = _qs.filter(profile=user.profile)
            return qs
        else:
            return _qs.none()

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return DeliveryAddressCreateSerializer
    #     return DeliveryAddressSerializer


class AddressSearch(APIView):

    def get(self, request):
        user = request.user
        if user and user.is_authenticated and hasattr(user, 'profile'):
            if request.method == 'GET':
                q = request.GET.get('q', '')
                q = ' '.join(q.split())
                addresses = user.profile.profile_addresses.filter(
                    Q(post_code__icontains=q) | Q(country__title__icontains=q) | Q(city__icontains=q)
                    | Q(street__icontains=q) | Q(house__icontains=q) | Q(flat__icontains=q) | Q(first_name__icontains=q)
                    | Q(middle_name__icontains=q) | Q(last_name__icontains=q) | Q(phone__icontains=q)
                ).distinct()
                return Response(DeliveryAddressSerializer(addresses, many=True).data)
            return Response(status=400)
        return Response(status=403)
