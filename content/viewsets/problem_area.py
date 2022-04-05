from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models import ProblemArea
from ..serializers import ProblemAreaSerializer


class ProblemAreaViewSet(ListModelMixin, GenericViewSet):

    queryset = ProblemArea.objects.all()
    serializer_class = ProblemAreaSerializer
    pagination_class = None
