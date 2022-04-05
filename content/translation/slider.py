from modeltranslation.translator import TranslationOptions, register
from ..models import Slider


@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title',)
