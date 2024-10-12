from django.urls import reverse
import pytest


@pytest.mark.django_db
def test__user_password_change_view__renders_correct_template(admin_client):
    response = admin_client.get(reverse('account:password_change'))

    assert response.status_code == 200
    assert 'account/password_change_form.html' in [template.name for template in response.templates]
    assert response.context['title'] == 'Password change'


def test__user_password_change_view__successful_update_password(client, user):
    user = user()
    client.login(username=user.username, password=user.raw_password)

    response_get = client.get(reverse('account:password_change'))

    data = {
        'old_password': user.raw_password,
        'new_password1': 'new_valid_password',
        'new_password2': 'new_valid_password',
    }

    response_post = client.post(reverse('account:password_change'), data)
    user.refresh_from_db()

    assert response_get.status_code == 200
    assert response_post.status_code == 302
    assert user.check_password('new_valid_password')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'old_password, new_password1, new_password2, expected_status_code',
    [
        pytest.param(
            'invalid_old_password',
            'new_valid_password',
            'new_valid_password',
            200,
            id='invalid old password',
        ),
        pytest.param(
            'valid_password',
            'new_invalid_password',
            'new_valid_password',
            200,
            id='invalid new password 1',
        ),
        pytest.param(
            'valid_password',
            'new_valid_password',
            'new_invalid_password',
            200,
            id='invalid new password 2',
        ),
    ],
)
def test__user_password_change_view__invalid_data(
    client,
    user,
    old_password,
    new_password1,
    new_password2,
    expected_status_code,
):
    user = user()
    data = {
        'old_password': old_password,
        'new_password1': new_password1,
        'new_password2': new_password2,
    }
    client.login(username=user.username, password=user.raw_password)

    response = client.post(reverse('account:password_change'), data)

    assert response.status_code == expected_status_code
    assert user.check_password('valid_password')
