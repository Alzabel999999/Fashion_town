from django.forms import ModelForm
from django.conf import settings
from backend.garpix_catalog.models.live_photo_feedback import LivePhotoFeedback
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from snowpenguin.django.recaptcha3.widgets import ReCaptchaHiddenInput
import re


class FeedbackForm(ModelForm):
    recaptcha = ReCaptchaField(widget=ReCaptchaHiddenInput())
    # def clean_phone(self):
    #     cleaned_data = self.clean()
    #     print('ASDASDASDASD')
    #     phone = cleaned_data.get('phone')
    #     if not re.match(settings.PHONE_REGEX, phone):
    #         self.add_error('phone', "Введите корректный номер")
    #         #raise ValueError("Введите корректный номер")
    #     return phone

    class Meta:
        model = LivePhotoFeedback
        fields = [
            'name',
            'message',
            'image',
            'recaptcha',
        ]
