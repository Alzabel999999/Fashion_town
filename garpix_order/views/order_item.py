from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.permissions import IsOwnerProfileOrReject
from rest_framework.viewsets import GenericViewSet
from ..serializers import (
    OrderBrandSerializer,
    OrderItemSerializer,
    UnformedOrderItemSerializer,
)
from ..models import Order, OrderItem
from django.conf import settings


class OrderItemViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):

    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerProfileOrReject, ]
    filter_fields = {
        'status': ['exact', ]
    }

    def get_serializer_class(self):
        user = self.request.user
        if user.profile.role == 3:
            return OrderBrandSerializer
        else:
            if self.action in ['update', 'partial_update']:
                return UnformedOrderItemSerializer
            return OrderItemSerializer

    def get_queryset(self):
        _qs = self.queryset
        user = self.request.user
        order_id = self.request.GET.get('order_id', None)
        order = Order.objects.filter(id=order_id).first()
        if user.profile.role == 3:
            #qs = order.get_brands()
            order_items = OrderItem.objects.filter(order=order)
            qs = []
            for item in order_items:
                if item.cart_item:
                    brand = item.cart_item.product.product.brand
                elif item.cart_items_pack:
                    brand = item.cart_items_pack.product.brand
                else:
                    brand = None
                if brand not in qs:
                    qs.append(brand)
        else:
            if self.action in ['update', 'partial_update']:
                order = Order.objects.filter(profile=user.profile, status=settings.ORDER_STATUS_UNFORMED).first()
            qs = order.order_items.all()
        return qs

    def list(self, request, *args, **kwargs):
        user = self.request.user
        currency = request.headers.get('currency', 'PLN')
        if not user.is_authenticated:
            return Response({'status': False}, status=403)
        order_id = request.GET.get('order_id', None)
        if not order_id:
            return Response({'status': False}, status=400)
        order = Order.objects.filter(id=order_id).first()
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        serializer_data = serializer(queryset, many=True, context={'order': order, 'currency': currency}).data
        return Response(serializer_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.update_item(request)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
