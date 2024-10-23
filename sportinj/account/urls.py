from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile'),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path(
        'password-change/done/',
        PasswordChangeDoneView.as_view(
            template_name='account/password_change_done.html'
        ),
        name='password_change_done',
    ),
    path(
        'password-reset/',
        views.UserPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'password-reset/done',
        PasswordResetDoneView.as_view(
            template_name='account/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='account/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path(
        'password-reset/fail/',
        views.UserPasswordResetFailView.as_view(),
        name='password_reset_fail',
    ),
    path(
        'confirm-register/',
        views.UserConfirmRegisterView.as_view(),
        name='user_confirm_register',
    ),
    path(
        'activate/<uidb64>/<token>/',
        views.UserConfirmRegisterActivateView.as_view(),
        name='user_confirm_register_activate',
    ),
    path(
        'confirm-register/success/',
        views.UserConfirmRegisterSuccessView.as_view(),
        name='user_confirm_register_success',
    ),
    path(
        'confirm-register/fail/',
        views.UserConfirmRegisterFailView.as_view(),
        name='user_confirm_register_fail',
    ),
    path(
        'already-confirm-register/',
        views.UserAlreadyConfirmRegisterView.as_view(),
        name='user_already_confirm_register',
    ),
    path(
        'confirm-register/link-expired/',
        views.UserConfirmRegisterLinkExpiredView.as_view(),
        name='user_confirm_register_link_expired',
    )
]
