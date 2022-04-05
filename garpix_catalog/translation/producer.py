from modeltranslation.translator import TranslationOptions, register
from ..models import Producer


@register(Producer)
class ProducerTranslationOptions(TranslationOptions):
    fields = ('title',)
