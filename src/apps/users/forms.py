from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from apps.users.models import User


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        User.objects.filter(username=username).exists()

        raise ValidationError(self.error_messages["duplicate_username"])
