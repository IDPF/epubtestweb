from django.forms import ModelForm
from django import forms
from testsuite_app.models import *
from django.forms.models import inlineformset_factory
from django.db.models.fields import BLANK_CHOICE_DASH

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
        fields = ('name', 'version', 'operating_system', 'operating_system_version', 'notes')

class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = ('result', 'notes', 'publish_notes')

        # clear the 'result' label: it's visually distracting
        labels = {
            'result': '',
        }

        # use a custom text area
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 40, 'rows': 3, 'title': 'Notes'}),
        }

class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ('is_archived', 'notes', 'short_summary', 'long_summary')
        labels = {
            'is_archived': 'Archived',
            'notes': 'Notes',
            'short_summary': 'Short summary',
            'long_summary': 'Long summary'
        }
        # use a custom text area
        widgets = {
            'short_summary': forms.Textarea(attrs={'cols': 100, 'rows': 3, 'title': 'Short summary'}),
            'long_summary': forms.Textarea(attrs={'cols': 100, 'rows': 20, 'title': 'Long summary'})
        }

class ATMetadataForm(ModelForm):
    class Meta:
        model = ATMetadata
        fields = ('assistive_technology', 'input_type', 'supports_braille', 'supports_screenreader')
        labels = {
            'input_type': 'Input type',
            'supports_screenreader': 'Testing includes screenreader output',
            'supports_braille': 'Testing includes Braille output',
        }
        widgets = {
            'input_type': forms.RadioSelect,
        }

ResultFormSet = inlineformset_factory(Evaluation, Result, extra=0, can_delete=False, form = ResultForm)
