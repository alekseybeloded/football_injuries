from django.urls import reverse
import pytest


@pytest.mark.django_db
def test__login_user__valid_username_and_password(client, user):
    response = client.post(
        reverse('account:login'),
        {
            'username': user.username,
            'password': user.raw_password
        }
    )

    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, password, expected_status_code',
    [
        pytest.param(
            'invalid_username',
            'valid_password',
            200,
            id='invalid username and valid password',
        ),
        pytest.param(
            'valid_username',
            'invalid_password',
            200,
            id='valid username and invalid password',
        ),
    ],
)
def test__login_user__invalid_username_or_password(
    client,
    user,
    username, password,
    expected_status_code,
):
    response = client.post(reverse('account:login'), {'username': username, 'password': password})

    assert response.status_code == expected_status_code
    assert "Please enter a correct username/email and password. Note that both fields may be case-sensitive." in str(response.content)


@pytest.mark.django_db
def test__login_user__renders_correct_template(client):
    response = client.get(reverse('account:login'))

    assert response.status_code == 200
    assert 'account/login.html' in [template.name for template in response.templates]
    assert response.context['title'] == 'Authorization'
