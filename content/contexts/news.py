from django.db.models import Count

from ..serializers import PageSerializer
from .common import common_context
from ..models import NewsRubric, News


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    role = user.profile.role if user else 0

    if role == 3:
        news = News.objects.filter(is_for_wholesaler=True)
    elif role == 2:
        news = News.objects.filter(is_for_dropshipper=True)
    else:
        news = News.objects.filter(is_for_retailer=True)

    news_rubrics = NewsRubric.objects.filter(rubric_news__in=news).distinct()
    rubrics = [{'id': rubric.id, 'title': rubric.title} for rubric in news_rubrics]

    user_role = user.profile.role if user else 0

    context = {
        'page_info': PageSerializer(page).data,
        'user_role': user_role,
        'rubrics': rubrics,
    }
    context.update(common_context(user, page))

    return context
