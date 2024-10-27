from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserCreationForm,
)

UserModel = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    class Meta:
        model = UserModel
        fields = ['username', 'password']

    error_messages = {
        'invalid_login':
            'Please enter a correct username/email and password. Note that both '
            'fields may be case-sensitive.',
        'inactive': 'This account is inactive.',
    }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('This email already exists')
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and UserModel.objects.filter(
            email=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError('This email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and UserModel.objects.filter(
            username=username
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError('This username already exists')
        return username


class UserPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address doesn't exist")
        return email

    def get_user(self):
        email = self.cleaned_data.get('email')
        try:
            user = UserModel._default_manager.get(email=email)
            return user
        except UserModel.DoesNotExist:
            return None
