from rest_framework import viewsets, permissions, pagination, status
from rest_framework.response import Response
from ..models import WishListItem
from ..serializers import WishListSerializer, WishListCreateSerializer


class WishListPagination(pagination.PageNumberPagination):

    def get_page_size(self, request):
        page_size = request.GET.get('page_size', 30)
        return page_size


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishListItem.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = WishListPagination
    filter_fields = {
        'profile': ['exact', ],
        'product': ['exact', ],
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return WishListItem.objects.filter(profile=user.profile).order_by('id')
        return WishListItem.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return WishListCreateSerializer
        return WishListSerializer

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_authenticated:
            instance = WishListItem.objects.filter(profile=user.profile, product=kwargs['pk']).first()
            if instance:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()
