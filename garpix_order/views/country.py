from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from ..models import Country
from ..serializers import CountrySerializer
from garpix_catalog.models import Currency
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class CountryViewSet(GenericViewSet, ViewSet): #GenericViewSet, ViewSet
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    #@action(methods=['GET', ], detail=False)
    def list(self, request, *args, **kwargs):#list
        data = CountrySerializer(self.queryset, many=True).data
        return Response(data)

    @action(methods=['POST', ], detail=False)
    def post(self, request):
        try:
            currency = request.data.get('currency')  # , None
            country = request.data.get('country')  # , None
            if currency == 'PLN':
                kurs = 1
            else:
                kurs = Currency.objects.get(title=currency).ratio
        except Exception as e:
            return Response({'error': str(e)})
        try:
            price = Country.objects.get(title=country)
            price = price.delivery_price
            price_delivery = price / kurs
            res = {'price': round(float(price_delivery),2), 'country': country}
            return Response(res)
        except Exception as e:
            return Response({'error': str(e)})

"""class AddressSearch(APIView):
    def post(self, request):
        return Response({'yes': 'yes'})
        currency = request.data.get('currency')#, None
        country = request.data.get('country')#, None
        kurs = Currency.objects.get(title=currency).ratio
        try:
            price = Country.objects.get(title=country)
            price_delivery = price*kurs
            res = {'price': price, 'country': country}
            return Response(res)
        except:
            return Responce({'error': 'Нет страны'})"""
