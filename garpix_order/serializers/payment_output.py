from decimal import Decimal
from django.conf import settings
from rest_framework import serializers
from ..models import Payment, Requisites, Order, Delivery, PaymentOutput
from ..serializers import RequisitesSerializer
from garpix_catalog.models import Currency


class PaymentOutputCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = PaymentOutput
        fields = (
            'id',
            'user',
            'cost',
            'name',
            'bank',
            'receipt',
            'number',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        user = validated_data.pop('user')
        profile = user.profile if hasattr(user, 'profile') else None
        validated_data.update({'profile': profile})
        validated_data.update({'cost': get_pln_price(self, validated_data['cost'])})
        payment = PaymentOutput.objects.create(**validated_data)
        return payment


def get_pln_price(data, price):
    try:
        if 'request' in data.context.keys():
            currency_title = data.context['request'].headers.get('currency', 'PLN')
        else:
            currency_title = data.context['currency']
        currency = Currency.objects.get(title=currency_title).ratio
    except:
        currency = Decimal('1.0000')
    price = price * currency
    return price.__round__(2)
