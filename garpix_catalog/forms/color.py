from django.forms import ModelForm
from django.forms.widgets import TextInput
from ..models import Color


class ColorAdminForm(ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
