import pytest
from django.urls import reverse


@pytest.mark.django_db
def test__contact_page_view__renders_correct_template(client):
    response = client.get(reverse('contacts'))

    assert response.status_code == 200
    assert 'resources/contacts.html' in [template.name for template in response.templates]
    assert response.context['title'] == 'Contacts'
