from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from .models import User, UserProfile

import uuid

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password. For Admin and Fixtures use currently.
    """
    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput,
                                help_text=_('Enter the same password as above, for verification.'))

    class Meta:
        model = User

    def clean_email(self):
        # Since AbstractUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("This email id is already registered with JopPlus")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin's password hash display field.
    For Admin and Fixtures use currently.
    """
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see  this user\'s password,'
            ' but you can change the password using <a href=\"password/\">this form</a>.'
        )
    )

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']


class LoginForm(forms.Form):
    """
    The User Login Form!
    """
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.user_cache = authenticate(username=email, password=password)
        if self.user_cache is None:
            raise forms.ValidationError('Your email and password did not match. Please try again.')
        elif not self.user_cache.is_active:
            raise forms.ValidationError('The current account is not active. Please contact support.')

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class RegistrationForm(forms.ModelForm):
    """
    The User Registration Form!
    """
    error_messages = {
        'duplicate_email': _('A User with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput,
                                help_text=_('Enter the same password as above, for verification.'))
    first_name = forms.CharField(label=_('First Name'), max_length=100)
    last_name = forms.CharField(label=_('Last Name'), max_length=100)

    class Meta:
        model = User
        fields = ('email', 'terms')

    def clean_email(self):
        # Since AbstractCustomUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            #user = User._default_manager.get(email=email)
            user = get_user_model().objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        # creating a user using CustomUserManager.create_user()
        # user_custom = get_user_model().objects.create_user(user.email, user.first_name, user.last_name, user.password)
        user_custom = get_user_model().objects.create_user(user.email, user.password)
        user_custom.terms = user.terms

        #user.hash = uuid.uuid1()
        if commit:
            user_custom.save()
            # create a user profile object
            UserProfile.objects.create(user=user_custom,first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'])
        return user_custom


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    repeat_new_password = forms.CharField(widget=forms.PasswordInput())

    error_messages = {
        'duplicate_email': _('A User with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    def clean_repeat_new_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('repeat_new_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True, user=None):
        # Save the provided password in hashed format
        if user:
            user.set_password(self.cleaned_data['new_password'])
            if commit:
                user.save()
        return user
