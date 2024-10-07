from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from sportinj import settings


@receiver(post_save, sender=User)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        protocol = 'https' if settings.USE_HTTPS else 'http'
        domain = settings.DOMAIN

        email_title = 'Confirm registration'
        email_body = render_to_string(
            'account/user_confirm_register_email.html',
            {
                'site_name': domain,
                'protocol': protocol,
                'domain': domain,
                'uid': uid,
                'token': token,
            }
        )

        send_mail(
            email_title,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
