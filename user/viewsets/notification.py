from rest_framework import viewsets, permissions
from ..models import Notification
from ..serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    filter_fields = {
        # 'profile': ['exact', ],
        # 'product': ['exact', ],
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Notification.objects.filter(profile=user.profile).order_by('id')
        return Notification.objects.none()

    def get_serializer_class(self):
        return NotificationSerializer

    @action(methods=['GET', ], detail=False)
    def get_notifications(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
            notifications = Notification.objects.filter(profile=profile)
            #return Response({'ok': str('ok')})
            return Response(NotificationSerializer(notifications, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})

    @action(methods=['POST', ], detail=False)
    def readed_notifications(self, request, *args, **kwargs):
        try:
            ids = request.data.get('ids')
            #ids = request.POST.getlist('ids', [])
            #return Response({'error1': ids})
            for id in ids:
                notification = Notification.objects.get(id=id)
                notification.is_read = True
                notification.save()
            #return Response({'status': str('success')})
            profile = request.user.profile
            notifications = Notification.objects.filter(profile=profile)
            return Response(NotificationSerializer(notifications, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})

    @action(methods=['DELETE', ], detail=False)
    def delete_notifications(self, request, *args, **kwargs):
        try:
            ids = request.data.get('ids')
            #ids = request.POST.getlist('ids', [])
            #return Response({'error1': ids})
            for id in ids:
                notification = Notification.objects.get(id=id)
                notification.delete()
            profile = request.user.profile
            notifications = Notification.objects.filter(profile=profile)
            return Response(NotificationSerializer(notifications, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})
