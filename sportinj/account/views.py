from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView, UpdateView, View
from resources.utils import ExtraContextMixin

from account import forms


class UserLoginView(LoginView):
    form_class = forms.UserLoginForm
    template_name = 'account/login.html'
    extra_context = {'title': 'Authorization'}


class UserRegistrationView(CreateView):
    form_class = forms.UserRegistrationForm
    template_name = 'account/register.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('account:user_confirm_register')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.request = self.request
        user.save()
        return HttpResponseRedirect(self.success_url)


class UserProfileUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = forms.UserProfileForm
    template_name = 'account/profile.html'
    extra_context = {'title': "Profile"}
    success_message = 'Profile was changed successfully'

    def get_success_url(self):
        return reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = forms.UserPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    title = "Password change"


class UserConfirmRegisterView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_confirm_register.html'
    title_page = 'Confirm register'


class UserConfirmRegisterActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(get_user_model(), pk=uid)
        except (TypeError, ValueError, get_user_model().DoesNotExist):
            user = None

        if (
                user is not None and
                default_token_generator.check_token(user, token) and
                not user.is_active
            ):
            user.is_active = True
            user.save()
            return redirect('account:user_confirm_register_success')
        elif user is not None and user.is_active:
            return redirect('account:user_already_confirm_register')
        else:
            return redirect('account:user_confirm_register_fail')


class UserConfirmRegisterSuccessView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_confirm_register_success.html'
    title_page = 'Successful registration'


class UserConfirmRegisterFailView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_confirm_register_fail.html'
    title_page = 'Failed registration'


class UserAlreadyConfirmRegisterView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_already_confirm_register.html'
    title_page = 'Confirm registration'
