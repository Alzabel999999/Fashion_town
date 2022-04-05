from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.permissions import IsOwnerProfileOrReject
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from ..serializers import OrderSerializer, OrderCorrespondenceSerializer
from ..models import Order, OrderItem, CorrespondenceItem


class CorrespondenceItemViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = CorrespondenceItem.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerProfileOrReject, ]

    def get_serializer_class(self):
        return OrderCorrespondenceSerializer

    def list(self, request, *args, **kwargs):
        order = request.GET.get('order_id', None)
        if order:
            qs = self.queryset.filter(order__id=order)
            return Response(OrderCorrespondenceSerializer(qs, many=True, context={'request': request}).data, status=200)
        return Response({'status': False}, status=400)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        files = self.request.FILES.getlist('files', [])
        user = self.request.user
        item_status = CorrespondenceItem.create(user=user, data=data, files=files)
        if item_status:
            return Response({'status': True}, status=200)
        return Response({'status': False}, status=400)
