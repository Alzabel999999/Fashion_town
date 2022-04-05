from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import CommonFeedback
from ..serializers import CommonFeedbackSerializer


class CommonFeedbackViewSet(CreateModelMixin, GenericViewSet):

    queryset = CommonFeedback.objects.all()
    serializer_class = CommonFeedbackSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
