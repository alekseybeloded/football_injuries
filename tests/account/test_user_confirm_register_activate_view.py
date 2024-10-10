from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


from django.urls import reverse
import pytest


@pytest.mark.django_db
def test__user_confirm_register_activate_view__success_case(client, user):
    user = user(is_active=False)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = client.get(reverse('account:user_confirm_register_activate', args=[uid, token]))

    user.refresh_from_db()

    assert response.status_code == 302
    assert user.is_active
    assert response.url == reverse('account:user_confirm_register_success')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__invalid_uid(client, user):
    user = user(is_active=False)
    invalid_uid = 'invalid_uid'
    token = default_token_generator.make_token(user)

    response = client.get(reverse('account:user_confirm_register_activate', args=[invalid_uid, token]))

    user.refresh_from_db()

    assert response.status_code == 302
    assert not user.is_active
    assert response.url == reverse('account:user_confirm_register_fail')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__invalid_token(client, user):
    user = user(is_active=False)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    invalid_token = 'invalid_token'

    response = client.get(reverse('account:user_confirm_register_activate', args=[uid, invalid_token]))

    user.refresh_from_db()

    assert response.status_code == 302
    assert not user.is_active
    assert response.url == reverse('account:user_confirm_register_fail')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__user_already_active(client, user):
    user = user(is_active=True)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = client.get(reverse('account:user_confirm_register_activate', args=[uid, token]))

    user.refresh_from_db()

    assert response.status_code == 302
    assert user.is_active
    assert response.url == reverse('account:user_already_confirm_register')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__user_already_active(client, user):
    user = user(is_active=True)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = client.get(reverse('account:user_confirm_register_activate', args=[uid, token]))

    user.refresh_from_db()

    assert response.status_code == 302
    assert user.is_active
    assert response.url == reverse('account:user_already_confirm_register')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__user_not_found(client, user):
    user = user(is_active=False)
    user.save()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    user.delete()

    response = client.get(reverse('account:user_confirm_register_activate', args=[uid, token]))

    assert response.status_code == 302
    assert response.url == reverse('account:user_confirm_register_fail')
