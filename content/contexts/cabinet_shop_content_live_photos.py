from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context
from garpix_catalog.models import LivePhotoAlbum, Brand


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    albums_qs = LivePhotoAlbum.objects.all().exclude(live_photo_photos__isnull=True, live_photo_videos__isnull=True)
    brands_qs = Brand.objects.filter(brand_live_photo_albums__in=albums_qs).distinct()
    brands = [{'id': brand.id, 'title': brand.title} for brand in brands_qs]
    context = {
        'page_info': PageSerializer(page).data,
        'brands': brands
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
