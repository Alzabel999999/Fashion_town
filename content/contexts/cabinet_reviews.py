from ..serializers import PageSerializer
from .cabinet_common import cabinet_common_context


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    # todo убрать заглушки описания статуса и баллов

    context = {
        'page_info': PageSerializer(page).data,
        'status_description': 'Участник уровня «Королева шоппинга». Скидка для данного статуса составляет 4%. Вам не хватает 100 балла (-ов), чтобы получить свой следующий уровень. Скидка станет доступна через 20 дней (какое-то время модерации отзывов).',
        'score': 900,
    }
    context.update(cabinet_common_context(user, page, currency))

    return context
