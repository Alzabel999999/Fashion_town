from modeltranslation.translator import TranslationOptions, register
from ..models import Feature


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
