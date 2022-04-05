from rest_framework import viewsets, permissions, pagination
from ..models import AlreadySaw
from ..serializers import AlreadySawSerializer, AlreadySawCreateSerializer


class AlreadySawPagination(pagination.PageNumberPagination):

    def get_page_size(self, request):
        page_size = request.GET.get('page_size', 30)
        return page_size


class AlreadySawViewSet(viewsets.ModelViewSet):
    queryset = AlreadySaw.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = AlreadySawPagination
    filter_fields = {
        'profile': ['exact', ],
        'product': ['exact', ],
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return AlreadySaw.objects.filter(profile=user.profile).order_by('id')
        return AlreadySaw.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return AlreadySawCreateSerializer
        return AlreadySawSerializer
