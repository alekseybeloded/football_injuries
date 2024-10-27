from unittest.mock import patch

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test__user_registration_view__success_registration(client):
    form_data = {
        'username': 'valid_username',
        'email': 'valid@mail.com',
        'password1': 'valid_password',
        'password2': 'valid_password',
    }
    with patch('account.views.cache.set') as cache_set_mock:

        response = client.post(reverse('account:register'), form_data)

        cache_set_mock.assert_called_once()
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, email, password1, password2, expected_status_code',
    [
        pytest.param(
            'invalid username',
            'valid@mail.com',
            'valid_password',
            'valid_password',
            200,
            id='invalid username',
        ),
        pytest.param(
            'valid_username',
            'invalid email',
            'valid_password',
            'valid_password',
            200,
            id='invalid email',
        ),
        pytest.param(
            'valid_username',
            'valid@mail.com',
            'invalid password',
            'valid_password',
            200,
            id='invalid password 1',
        ),
        pytest.param(
            'valid_username',
            'valid@mail.com',
            'valid_password',
            'invalid password',
            200,
            id='invalid password 2'
        )
    ],
)
def test__user_registration_view__invalid_data(
    client,
    username,
    email,
    password1,
    password2,
    expected_status_code
):
    form_data = {
        'username': username,
        'email': email,
        'password1': password1,
        'password2': password2,
    }

    response = client.post(reverse('account:register'), form_data)

    assert response.status_code == expected_status_code


@pytest.mark.django_db
def test__user_registration_view__renders_correct_template(client):
    response = client.get(reverse('account:register'))

    assert response.status_code == 200
    assert 'account/register.html' in [template.name for template in response.templates]
    assert response.context['title'] == 'Registration'
