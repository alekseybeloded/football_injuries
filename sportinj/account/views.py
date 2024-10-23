from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, TemplateView, UpdateView, View
from resources.utils import ExtraContextMixin

from account import forms
from account.tasks import send_email

UserModel = get_user_model()


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
        user.save()

        token = default_token_generator.make_token(user)

        cache.set(
            f'account_{user.pk}_verification_token',
            token,
            timeout=3600 * 24,
        )

        send_email.delay_on_commit(
            self.request.scheme,
            self.request.get_host(),
            user.email,
            'confirmation_account',
        )

        return HttpResponseRedirect(self.success_url)


class UserProfileUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = forms.UserProfileForm
    template_name = 'account/profile.html'
    extra_context = {'title': "Profile"}
    success_message = 'Profile was changed successfully'

    def get_success_url(self):
        return reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    title = "Password change"


class UserPasswordResetView(PasswordResetView):
    form_class = forms.UserPasswordResetForm
    template_name = 'account/password_reset_form.html'
    email_template_name = 'account/password_reset_email.html'
    success_url = reverse_lazy('account:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        token = default_token_generator.make_token(UserModel.objects.get(email=email))

        cache.set(
            f'reset_password_token_for_{email}',
            token,
            timeout=3600 * 24,
        )

        send_email.delay_on_commit(
            self.request.scheme,
            self.request.get_host(),
            email,
            'reset_password',
        )

        return HttpResponseRedirect(self.success_url)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(UserModel, pk=uid)
        except (TypeError, ValueError, UserModel.DoesNotExist):
            user = None

        if (
            user is not None and
            cache.get(f'reset_password_token_for_{user.email}')
        ):
            cache.delete(f'reset_password_token_for_{user.email}')
            return super().get(request, uidb64, token)
        else:
            return redirect('account:password_reset_fail')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs


@method_decorator(cache_page(timeout=None), name='get')
class UserPasswordResetFailView(ExtraContextMixin, TemplateView):
    template_name = 'account/password_reset_fail.html'
    title_page = 'Faild reset password'


@method_decorator(cache_page(timeout=None), name='get')
class UserConfirmRegisterView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_confirm_register.html'
    title_page = 'Confirm register'


class UserConfirmRegisterActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(UserModel, pk=uid)
        except (TypeError, ValueError, UserModel.DoesNotExist):
            user = None

        if (
            user is not None and
            cache.get(f'account_{user.pk}_verification_token') and
            not user.is_active
        ):
            user.is_active = True
            user.save()
            return redirect('account:user_confirm_register_success')
        elif user is not None and user.is_active:
            return redirect('account:user_already_confirm_register')
        elif not cache.get(f'account_{user.pk}_verification_token'):
            UserModel.objects.filter(pk=uid).delete()
            return redirect('account:user_confirm_register_link_expired')
        else:
            return redirect('account:user_confirm_register_fail')


@method_decorator(cache_page(timeout=None), name='get')
class UserConfirmRegisterSuccessView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_confirm_register_success.html'
    title_page = 'Successful registration'


@method_decorator(cache_page(timeout=None), name='get')
class UserConfirmRegisterFailView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_confirm_register_fail.html'
    title_page = 'Failed registration'


@method_decorator(cache_page(timeout=None), name='get')
class UserAlreadyConfirmRegisterView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_already_confirm_register.html'
    title_page = 'Confirm registration'


@method_decorator(cache_page(timeout=None), name='get')
class UserConfirmRegisterLinkExpiredView(ExtraContextMixin, TemplateView):
    template_name = 'account/user_confirm_register_link_expired.html'
    title_page = 'Link expired'
