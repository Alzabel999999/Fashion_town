from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Likes
from ..serializers.likes import LikesSerializer, CreateLikesSerializer, UpdateLikesSerializer


class LikesViewSet(ModelViewSet):
    queryset = Likes.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_fields = {'profile__user__username': ['iexact', ]}
    ordering_fields = ['created_at', ]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateLikesSerializer
        if self.action == 'update':
            return UpdateLikesSerializer
        return LikesSerializer
