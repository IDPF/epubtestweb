from django.forms import ModelForm
from django import forms
from models import *
from django.forms.models import inlineformset_factory

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def is_valid(self):
        return len(self.username) > 0 and len(self.password) > 0

class ReadingSystemChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        l = "{0} {1}".format(obj.name, obj.version)
        if len(obj.operating_system) > 0:
            l += " ({0})".format(obj.operating_system)
        if len(obj.locale) > 0:
            l += " ({0})".format(obj.locale)
        return l

class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluation_type', 'reading_system']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(EvaluationForm, self).__init__(*args, **kwargs)
        self.fields['reading_system'] = ReadingSystemChoiceField(queryset=ReadingSystem.objects.all())


class ReadingSystemForm(ModelForm):
    class Meta:
        model = ReadingSystem

    def __init__(self, *args, **kw):
        super(ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'name',
            'version',
            'locale',
            'operating_system',
            'sdk_version',
        ]




ResultFormSet = inlineformset_factory(Evaluation, Result, extra=0, can_delete=False, fields = ['result'])

