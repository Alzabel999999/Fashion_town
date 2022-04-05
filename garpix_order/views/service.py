from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from user.permissions import IsBuyerProfileOrReject
from ..models import Service
from ..serializers import ServiceSerializer


class ServiceViewSet(ListModelMixin, GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsBuyerProfileOrReject, ]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        role = user.profile.role
        status = user.status
        if status == 0 or role in [0, 1]:
            return self.queryset.filter(for_retail=True)
        elif role == 2:
            return self.queryset.filter(for_drop=True)
        elif role == 3:
            return self.queryset.filter(for_opt=True)
        else:
            return self.queryset.none()
