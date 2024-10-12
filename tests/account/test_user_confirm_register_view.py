from django.urls import reverse
import pytest


@pytest.mark.django_db
def test__user_confirm_register_view__renders_correct_template(client):
    response = client.get(reverse('account:user_confirm_register'))

    assert response.status_code == 200
    assert 'account/user_confirm_register.html'
    assert response.context['title'] == 'Confirm register'
