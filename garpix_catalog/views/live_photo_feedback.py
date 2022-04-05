from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.live_photo_feedback import LivePhotoFeedback, LivePhotoVideo, LivePhotoImage


@api_view(['POST', ])
def feedback(request, *args, **kwargs):
    name = request.data.get('name', None)
    message = request.data.get('message', None)
    media_photo_id = request.data.get('media_photo', None)
    media_video_id = request.data.get('media_video', None)
    if not name or not (media_photo_id or media_video_id):
        return Response({'status': False}, status=400)
    media_photo = LivePhotoImage.objects.filter(id=media_photo_id).first() if media_photo_id else None
    media_video = LivePhotoVideo.objects.filter(id=media_video_id).first() if media_video_id else None
    fb = LivePhotoFeedback.objects.create(name=name, message=message, media_photo=media_photo, media_video=media_video)
    return Response({'status': True}, status=200)
