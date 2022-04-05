from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsOwnerOrReject
from ..models import LivePhotoAlbum, ShopLivePhoto, LivePhotoImage, LivePhotoVideo
from ..serializers import CabinetLivePhotoSerializer


class ShopLivePhotoAlbumViewSet(ListModelMixin, GenericViewSet):
    queryset = LivePhotoAlbum.objects.all()
    serializer_class = CabinetLivePhotoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReject]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = {
        'brand': ['exact', ],
        'created_at': ['lte', 'gte']
    }
    ordering_fields = ['created_at', ]

    def get_queryset(self):
        return self.queryset.exclude(image='').exclude(brand=None).exclude(
            live_photo_photos=None, live_photo_videos=None).distinct()

    @action(methods=['POST', ], detail=False)
    def select_unselect_photos(self, request, *args, **kwargs):
        data = request.data
        shop = request.user.profile.profile_shop
        for item in data:
            if item['type'] == 'album':
                origin_album = LivePhotoAlbum.objects.filter(id=item['id']).first()
                if origin_album:
                    album = ShopLivePhoto.get_or_create(origin_album=origin_album, shop=shop)
                    if 'title' in item.keys():
                        album.title = item['title']
                    if 'is_selected' in item.keys():
                        album.is_selected = item['is_selected']
                    album.save()
            if item['type'] == 'image':
                image = LivePhotoImage.objects.filter(id=item['id']).first()
                if image:
                    origin_album = image.album
                    if origin_album:
                        album = ShopLivePhoto.get_or_create(origin_album=origin_album, shop=shop)
                        if "is_selected" in item.keys():
                            if item['is_selected']:
                                album.photos.add(image)
                            else:
                                album.photos.remove(image)
                        album.save()
            if item['type'] == 'video':
                video = LivePhotoVideo.objects.filter(id=item['id']).first()
                if video:
                    origin_album = video.album
                    if origin_album:
                        album = ShopLivePhoto.get_or_create(origin_album=origin_album, shop=shop)
                        if "is_selected" in item.keys():
                            if item['is_selected']:
                                album.videos.add(video)
                            else:
                                album.videos.remove(video)
                        album.save()
        return Response(status=status.HTTP_200_OK)
