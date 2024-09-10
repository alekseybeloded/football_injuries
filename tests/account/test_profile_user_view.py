from django.urls import reverse
import pytest


@pytest.mark.django_db
def test__profile_user__renders_correct_template(admin_client):
    response = admin_client.get(reverse('account:profile'))

    assert response.status_code == 200
    assert 'account/profile.html' in [template.name for template in response.templates]
    assert response.context['title'] == 'Profile'


@pytest.mark.django_db
def test__profile_user__successful_update_profile(client, django_user_model):
    user = django_user_model.objects.create_user(username='test_username', email='testemail@mail.ru', password='test_password')
    login_successful = client.login(username='test_username', password='test_password')

    assert login_successful


    data = {
        'first_name': 'test first name',
        'last_name': 'test last name',
    }

    response_get = client.get(reverse('account:profile'))
    response_post = client.post(reverse('account:profile'), data)
    user.refresh_from_db()

    assert response_get.status_code == 200
    assert response_post.status_code == 302
    assert user.first_name == 'test first name'
    assert user.last_name == 'test last name'


@pytest.mark.django_db
def test__profile_user__user_not_authorized(client):
    response = client.get(reverse('account:profile'))

    assert response.status_code == 302
