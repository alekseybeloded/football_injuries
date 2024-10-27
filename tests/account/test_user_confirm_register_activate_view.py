from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@pytest.mark.django_db
def test__user_confirm_register_activate_view__success_case(client, user):
    user = user(is_active=False)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    with patch(
        'account.views.cache.get',
        return_value='token',
    ) as cache_get_mock:

        response = client.get(
            reverse(
                'account:user_confirm_register_activate',
                args=[uid, 'token'],
            )
)
        cache_get_mock.assert_called_once_with(f'account_{user.pk}_verification_token')

    user.refresh_from_db()

    assert response.status_code == 302
    assert user.is_active
    assert response.url == reverse('account:user_confirm_register_success')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__invalid_uid(client, user):
    user = user(is_active=False)
    invalid_uid = 'invalid_uid'
    with patch(
        'account.views.cache.get',
        return_value=default_token_generator.make_token(user),
    ) as cache_get_mock:

        response = client.get(
            reverse(
                'account:user_confirm_register_activate',
                args=[invalid_uid, 'token'],
            )
        )

        cache_get_mock.assert_not_called()

    user.refresh_from_db()

    assert response.status_code == 302
    assert not user.is_active
    assert response.url == reverse('account:user_confirm_register_fail')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__invalid_token(client, user):
    user = user(is_active=False)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    with patch(
        'account.views.cache.get',
        return_value='invalid_token',
    ) as cache_get_mock:

        response = client.get(
            reverse(
                'account:user_confirm_register_activate',
                args=[uid, 'token'],
            )
        )

        assert cache_get_mock.call_count == 2

    user.refresh_from_db()

    assert response.status_code == 302
    assert not user.is_active
    assert response.url == reverse('account:user_confirm_register_fail')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__token_expired(client, user):
    user = user(is_active=False)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    with patch(
        'account.views.cache.get',
        return_value=None,
    ) as cache_get_mock:

        response = client.get(
            reverse(
                'account:user_confirm_register_activate',
                args=[uid, 'token'],
            )
        )

        assert cache_get_mock.call_count == 2

    assert not get_user_model().objects.filter(pk=user.pk).exists()
    assert response.status_code == 302
    assert response.url == reverse('account:user_confirm_register_link_expired')


@pytest.mark.django_db
def test__user_confirm_register_activate_view__user_already_active(client, user):
    user = user(is_active=True)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    with patch(
        'account.views.cache.get',
        return_value=None,
    ) as cache_get_mock:

        response = client.get(
            reverse(
                'account:user_confirm_register_activate',
                args=[uid, 'token'],
            )
        )

        cache_get_mock.assert_called_once_with(f'account_{user.pk}_verification_token')

    user.refresh_from_db()

    assert response.status_code == 302
    assert user.is_active
    assert response.url == reverse('account:user_already_confirm_register')
