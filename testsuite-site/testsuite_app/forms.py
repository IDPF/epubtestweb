from django.forms import ModelForm
from django import forms
from models import *
from django.forms.models import inlineformset_factory

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def is_valid(self):
        return len(self.username) > 0 and len(self.password) > 0

class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluation_type']

    def __init__(self, *args, **kwargs):
        #user = kwargs.pop('user','')
        super(EvaluationForm, self).__init__(*args, **kwargs)
        #self.fields['reading_system'] = ReadingSystemChoiceField(queryset=ReadingSystem.objects.all())


class ReadingSystemForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = ReadingSystem
        fields = ('name', 'version', 'operating_system', 'locale', 'sdk_version')


ResultFormSet = inlineformset_factory(Evaluation, Result, extra=0, can_delete=False, fields = ['result', 'notes'])
