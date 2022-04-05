from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from ..models import Review
from ..serializers import ReviewSerializer, UpdateReviewSerializer, ReviewCabinetSerializer
from utils.pagination import CustomPagination


class ReviewPagination(CustomPagination):
    pass


class ReviewViewSet(ModelViewSet):
    queryset = Review.approved_objects.annotate(review_rating=Sum('profile__profile_reviews__likes_count'))
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = {
        'profile__user__username': ['iexact', ],
        'product': ['isnull', 'exact'],
        'is_with_media': ['exact', ]
    }
    ordering_fields = ['created_at', 'likes_count', 'review_rating']
    pagination_class = ReviewPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly,]
        return super(ReviewViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            # return CreateReviewSerializer
            return ReviewSerializer
        if self.action == 'update':
            return UpdateReviewSerializer
        if self.action == 'cabinet_reviews_list':
            return ReviewCabinetSerializer
        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        files = request.FILES.getlist('files', [])
        review = Review.create_review(user=user, data=data, files=files)
        serializer = self.get_serializer_class()
        serializer = serializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET', ], detail=False)
    def cabinet_reviews_list(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_authenticated:
            queryset = Review.objects.filter(profile__user=user)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 403}, status=403)
