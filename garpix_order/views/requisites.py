from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from ..models.requisites import Requisites
from ..serializers import RequisitesSerializer


class RequisitesViewSet(ViewSet, GenericViewSet):
    queryset = Requisites.objects.all()
    serializer_class = RequisitesSerializer

    @action(detail=False, methods=['get'])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = RequisitesSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', ])
    def get_random_requisites(self, request, *args, **kwargs):
        requisites = Requisites.random_requisites()
        serializer = RequisitesSerializer(requisites, many=False)
        return Response(serializer.data)
