from decimal import Decimal

from rest_framework import serializers
from ..models import Service
from garpix_catalog.models import Currency


class ServiceSerializer(serializers.ModelSerializer):

    cost = serializers.SerializerMethodField()

    def get_cost(self, obj):
        return get_price_with_currency(self, obj.cost)

    class Meta:
        model = Service
        fields = ('id', 'title', 'description', 'cost')


def get_price_with_currency(data, price):
    try:
        if 'request' in data.context.keys():
            currency_title = data.context['request'].headers.get('currency', 'PLN')
        else:
            currency_title = data.context['currency']
        currency = Currency.objects.get(title=currency_title).ratio
    except:
        currency = Decimal('1.0000')
    price = price / currency
    return price.__round__(2)
