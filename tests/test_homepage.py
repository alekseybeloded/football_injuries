from django.urls import reverse
import pytest
from resources.models import Team


@pytest.mark.django_db
def test__homepage__renders_correct_template(client):
    team_1 = Team.objects.create(name='Team 1')
    team_2 = Team.objects.create(name='Team 2')

    response = client.get(reverse('home'))
    teams = response.context['teams']

    assert response.status_code == 200
    assert 'resources/index.html' in [template.name for template in response.templates]
    assert len(teams) == 2
    assert list(response.context['teams']) == [team_1, team_2]
    assert response.context['title'] == 'Homepage - Football injuries'


@pytest.mark.django_db
def test__homepage__pagination(client):
    for i in range(11):
        Team.objects.create(name=f'Team {i}')

    response_page_1 = client.get(reverse('home'))
    response_page_2 = client.get(reverse('home') + '?page=2')
    teams_page_1 = response_page_1.context['teams']
    teams_page_2 = response_page_2.context['teams']

    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200
    assert len(teams_page_1) == 10
    assert len(teams_page_2) == 1
