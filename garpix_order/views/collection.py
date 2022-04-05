from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from ..serializers import CollectionSerializer
from ..models import Collection
from rest_framework.response import Response
from user.permissions import IsDropShipperOrReject


class CollectionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet, ViewSet):
    queryset = Collection.objects.filter(status=0)
    permission_classes = [IsAuthenticated, IsDropShipperOrReject]
    serializer_class = CollectionSerializer

    def list(self, request, *args, **kwargs):
        product_id = request.data.get('product', None)
        #return Response({'product_id': product_id}, status=status.HTTP_200_OK)
        if not product_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        collections = self.queryset.filter(product__id=product_id)
        serializer = self.get_serializer_class()
        data = serializer(collections, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        collection = self.get_object()
        serializer = self.get_serializer_class()
        data = serializer(collection).data
        return Response(data, status=status.HTTP_200_OK)


    @action(methods=['POST', ], detail=False)
    def get_collections(self, request, *args, **kwargs):
        product_id = request.data.get('product', None)
        if not product_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        collections = self.queryset.filter(product__id=product_id)
        serializer = self.get_serializer_class()
        data = serializer(collections, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def create_fake_empty_collection(self, request, *args, **kwargs):
        product_data = request.data
        collection = Collection.create_fake_empty_collection(product_data)
        serializer = self.get_serializer_class()
        data = serializer(collection).data
        # закоментить, если вдруг надо будет сохранять пустой сбор
        #collection.delete()
        return Response(data, status=status.HTTP_200_OK)
