from decimal import Decimal
from django.conf import settings
from rest_framework import serializers
from ..models import Payment, Requisites, Order, Delivery
from ..serializers import RequisitesSerializer
from garpix_catalog.models import Currency


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    requisites = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField()
    receipt = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    def get_cost(self, obj):
        return get_price_with_currency(self, obj.cost)

    def get_requisites(self, obj):
        return RequisitesSerializer(obj.requisites, many=False).data

    def get_description(self, obj):
        return obj.__str__()

    def get_receipt(self, obj):
        return settings.SITE_URL + obj.receipt.url if obj.receipt else '#'

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Payment
        fields = (
            'id',
            'description',
            'user',
            'requisites',
            'cost',
            'name',
            'comment',
            'receipt',
            'created_at',
            'updated_at',
            'status',
            'order',
            'delivery',
        )


class PaymentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # cost = serializers.SerializerMethodField()
    #
    # def get_cost(self, obj):
    #     return get_price_with_currency(self, obj.cost)

    class Meta:
        model = Payment
        fields = (
            'id',
            'user',
            'requisites',
            'cost',
            'name',
            'comment',
            'receipt',
            'created_at',
            'updated_at',
            'status',
            'order',
            'delivery',
        )
        extra_kwargs = {
            'requisites_id': {'required': True, 'write_only': True},
            'requisites': {'read_only': True},
            'cost': {'required': True},
            'name': {'required': True},
        }

    def validate(self, attrs):
        data = self.context['request'].data
        requisites_id = data.get('requisites_id', None)
        order_id = data.get('order_id', None)
        delivery_id = data.get('delivery_id', None)
        attrs.update({'requisites': Requisites.objects.filter(id=requisites_id).first()})
        if order_id:
            attrs.update({'order': Order.objects.filter(id=order_id).first()})
        if delivery_id:
            attrs.update({'delivery': Delivery.objects.filter(id=delivery_id).first()})
        return attrs

    def create(self, validated_data):
        user = validated_data.pop('user')
        profile = user.profile if hasattr(user, 'profile') else None
        validated_data.update({'profile': profile})
        validated_data.update({'cost': get_pln_price(self, validated_data['cost'])})
        payment = Payment.objects.create(**validated_data)
        return payment


class PaymentUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cost = serializers.SerializerMethodField()

    def get_cost(self, obj):
        return get_price_with_currency(self, obj.cost)

    class Meta:
        model = Payment
        fields = (
            'id',
            'user',
            'requisites',
            'cost',
            'name',
            'comment',
            'receipt',
            'created_at',
            'updated_at',
            'status',
            'order',
            'delivery',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'requisites': {'read_only': True},
            'cost': {'read_only': True},
            'name': {'read_only': True},
            'comment': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'status': {'read_only': True},
            'order': {'read_only': True},
            'delivery': {'read_only': True},
        }

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        return super(PaymentUpdateSerializer, self).update(instance, validated_data)


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
