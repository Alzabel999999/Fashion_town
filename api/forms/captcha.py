from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from snowpenguin.django.recaptcha3.widgets import ReCaptchaHiddenInput


class CaptchaForm(forms.Form):
    recaptcha = ReCaptchaField(widget=ReCaptchaHiddenInput())
