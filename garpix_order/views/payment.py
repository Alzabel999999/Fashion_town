import requests
from django.conf import settings
from django.db.models import Q, Count
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from ..models import Payment
from ..serializers import PaymentSerializer, PaymentCreateSerializer, PaymentUpdateSerializer
from utils.pagination import CustomPagination
from user.permissions import IsBuyerProfileOrReject


class PaymentPagination(CustomPagination):
    pass


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PaymentPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        if self.action == 'update':
            return PaymentUpdateSerializer
        return PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        _qs = self.queryset
        if user.is_authenticated:
            return _qs.filter(Q(profile__user=user) | Q(order__profile__user=user) | Q(delivery__order__profile__user=user))
        return _qs.none()

    def create(self, request, *args, **kwargs):
        # if 'order_id' not in request.data.keys() and 'delivery_id' not in request.data.keys():
        #     return Response({'status': False}, status=400)
        return super(PaymentViewSet, self).create(request, *args, **kwargs)

    @action(methods=['post', ], detail=False, permission_classes=[IsBuyerProfileOrReject, ])
    def get_payu_link(self, request, *args, **kwargs):
        from ..models import Order
        user = request.user
        if user.profile.role != 1:
            return Response({'error': 'wrong user role'}, status=403)
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        customer_ip = request.META.get('REMOTE_ADDR')
        order_id = request.data.get('order_id', None)
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({'error': 'not order'}, status=400)
        token_url = f'https://secure.payu.com/pl/standard/user/oauth/authorize' \
                    f'?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
        token = requests.post(token_url).json()
        return Response({"id":client_id, "secret": client_secret, "token": token})
        link_url = 'https://secure.payu.com/api/v2_1/orders'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token["access_token"]}'
        }
        data = {
            "customerIp": customer_ip,
            "merchantPosId": client_id,
            "extOrderId": order.order_number,
            "description": "fashion town pl",
            "currencyCode": "PLN",
            "totalAmount": order.total_cost,
            "buyer": {
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
            },
        }
        order_item_groups = order.order_items.all().order_by('product__id').distinct('product')
        products = []
        for item in order_item_groups:
            product = {
                "name": f'{item.product.product.title} {item.product.color.__str__()} {item.product.size.__str__()}',
                "unitPrice": item.total_price,
                "quantity": order.order_items.filter(product=item.product).count(),
            }
            products.append(product)
        if hasattr(order, 'order_delivery'):
            product = {
                "name": 'Delivery',
                "unitPrice": order.order_delivery.cost,
                "quantity": 1,
            }
            products.append(product)
        for item in order.services.all():
            product = {
                "name": item.title,
                "unitPrice": item.cost,
                "quantity": 1,
            }
            products.append(product)
        data.update({"products": products})
        response = requests.post(link_url, headers=headers, data=data).json()
        return Response(response)
