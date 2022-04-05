import requests
from django.conf import settings
from django.db.models import Q, Count
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from ..models import Payment, PaymentOutput
from ..serializers import PaymentSerializer, PaymentOutputCreateSerializer, PaymentUpdateSerializer
from utils.pagination import CustomPagination
from user.permissions import IsBuyerProfileOrReject


class PaymentOutputPagination(CustomPagination):
    pass

class PaymentOutputViewSet(viewsets.ModelViewSet):
    queryset = PaymentOutput.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PaymentOutputPagination


    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentOutputCreateSerializer

    def create(self, request, *args, **kwargs):
        # if 'order_id' not in request.data.keys() and 'delivery_id' not in request.data.keys():
        #     return Response({'status': False}, status=400)
        try:
            payment_output = super(PaymentOutputViewSet, self).create(request, *args, **kwargs)
            return payment_output
        except Exception as e:
            return Response({'erroe': str(e)}, status=200)
