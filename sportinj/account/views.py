from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from account import forms


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'account/login.html'
    extra_context = {'title': 'Authorization'}


class RegisterUser(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'account/register.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('account:login')


class ProfileUser(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = forms.ProfileUserForm
    template_name = 'account/profile.html'
    extra_context = {'title': "Profile"}
    success_message = 'Profile was changed successfully'

    def get_success_url(self):
        return reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(SuccessMessageMixin, PasswordChangeView):
    form_class = forms.UserPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    title = "Password change"
