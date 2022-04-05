from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models import QuestionCategory
from ..serializers import QuestionCategorySerializer


class QuestionCategoryViewSet(ListModelMixin, GenericViewSet):

    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer
    pagination_class = None
