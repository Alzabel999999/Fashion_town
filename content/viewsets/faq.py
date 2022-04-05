from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models import FAQ, FAQUserQuestion
from ..serializers import FAQSerializer, FAQUserQuestionSerializer


class FAQViewSet(ListModelMixin, GenericViewSet):

    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class FAQUserQuestionViewSet(CreateModelMixin, GenericViewSet):

    queryset = FAQUserQuestion.objects.all()
    serializer_class = FAQUserQuestionSerializer
