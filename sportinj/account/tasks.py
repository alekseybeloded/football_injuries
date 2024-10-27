from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from sportinj import settings

User = get_user_model()


@shared_task
def send_email(scheme, host, email, type):
    user = User.objects.get(email=email)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    protocol = scheme
    domain = host

    if type == 'confirmation_account':
        email_title = 'Confirm registration'
        email_body = render_to_string(
            'account/user_confirm_register_email.html',
            {
                'site_name': domain,
                'protocol': protocol,
                'domain': domain,
                'uid': uid,
                'token': cache.get(f'account_{user.pk}_verification_token')
            }
        )
    elif type == 'reset_password':
        email_title = 'Reset password'
        email_body = render_to_string(
            'account/password_reset_email.html',
            {
                'site_name': domain,
                'protocol': protocol,
                'domain': domain,
                'uid': uid,
                'token': cache.get(f'reset_password_token_for_{email}')
            }
        )
    else:
        raise ValueError('Incorrect type')

    send_mail(
        email_title,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
