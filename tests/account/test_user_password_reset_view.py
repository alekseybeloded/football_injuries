import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
def test__user_password_reset_view__form_valid(client, user):
    user = user()
    form_data = {'email': 'valid@mail.com'}

    with (
        patch('account.views.default_token_generator.make_token', return_value='token') as token_mock,
        patch('account.views.send_email.delay_on_commit') as send_email_mock,
        patch('account.views.cache.set') as cache_set_mock,
    ):
        response = client.post(reverse('account:password_reset'), form_data)

        send_email_mock.assert_called_once_with(
            'http',
            'testserver',
            'valid@mail.com',
            'reset_password',
        )
        cache_set_mock.assert_called_once_with(
            f'reset_password_token_for_{form_data["email"]}',
            'token',
            3600 * 24,
        )

    assert response.status_code == 302
    assert response.url == reverse('account:password_reset_done')


@pytest.mark.django_db
def test__user_password_reset_view__form_invalid(client, user):
    user = user()
    form_data = {'email': 'invalid@mail.com'}

    with (
        patch('account.views.default_token_generator.make_token', return_value='token') as token_mock,
        patch('account.views.send_email.delay_on_commit') as send_email_mock,
        patch('account.views.cache.set') as cache_set_mock,
    ):
        response = client.post(reverse('account:password_reset'), form_data)

        send_email_mock.assert_not_called()
        cache_set_mock.assert_not_called()

    assert response.status_code == 200
    assert 'account/password_reset_form.html' in [template.name for template in response.templates]
