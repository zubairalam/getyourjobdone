from django import forms
from apps.accounts.forms import RegistrationForm

class UploadProfilePhotoForm(forms.Form):
    photo = forms.FileField()

