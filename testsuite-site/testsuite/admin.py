from django.contrib import admin
from testsuite_app.models import UserProfile

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserProfileCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            # Not sure why UserCreationForm doesn't do this in the first place,
            # or at least test to see if _meta.model is there and if not use User...
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta:
        model = UserProfile
        fields = ("username", "password", "email", "first_name", "last_name")

class UserProfileChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile

class UserProfileAdmin(UserAdmin):
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm

admin.site.register(UserProfile, UserProfileAdmin)
