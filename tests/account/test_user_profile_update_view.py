from django.urls import reverse
import pytest


@pytest.mark.django_db
def test__user_profile_update_view__renders_correct_template(admin_client):
    response = admin_client.get(reverse('account:profile'))

    assert response.status_code == 200
    assert 'account/profile.html' in [template.name for template in response.templates]
    assert response.context['title'] == 'Profile'


@pytest.mark.django_db
def test__user_profile_update_view__successful_update_profile(client, user):
    user = user()
    login_successful = client.login(username=user.username, password=user.raw_password)

    assert login_successful

    data = {
        'username': user.username,
        'email': user.email,
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
    }

    response_get = client.get(reverse('account:profile'))
    response_post = client.post(reverse('account:profile'), data)
    user.refresh_from_db()

    assert response_get.status_code == 200
    assert response_post.status_code == 302
    assert user.first_name == 'new_first_name'
    assert user.last_name == 'new_last_name'


@pytest.mark.django_db
def test__user_profile_update_view__user_not_authorized(client):
    response = client.get(reverse('account:profile'))

    assert response.status_code == 302
