from django.forms import ModelForm
from django import forms
from models import *
from django.forms.models import inlineformset_factory

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def is_valid(self):
        return len(self.username) > 0 and len(self.password) > 0


class ReadingSystemForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = ReadingSystem
        fields = ('name', 'version', 'operating_system', 'locale', 'sdk_version')


ResultFormSet = inlineformset_factory(Evaluation, Result, extra=0, can_delete=False, fields = ['result', 'notes'])
