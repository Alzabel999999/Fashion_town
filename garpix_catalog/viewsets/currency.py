from rest_framework.viewsets import GenericViewSet, ViewSet
from garpix_catalog.models import Currency
from ..serializers.currency import CurrencySerializer
from rest_framework.decorators import action

class CurrencyViewSet(GenericViewSet, ViewSet):
    currency = Currency.objects.all()
    serializer_class = CurrencySerializer
    #@action(detail=False, methods=['get'])
    def current(self, request):

        serializer = CurrencySerializer(currency)
        return Response(serializer.data)
