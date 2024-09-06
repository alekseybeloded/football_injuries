import pytest
from django.urls import reverse
from resources.models import Team, Player


@pytest.mark.django_db
def test__get_players_for_team__renders_correct_template(admin_client):
    team = Team.objects.create(name='Team')
    player_1 = Player.objects.create(name='Player 1', team=team)
    player_2 = Player.objects.create(name='Player 2', team=team)

    response = admin_client.get(reverse('players', kwargs={'team_slug': team.slug}))

    assert response.status_code == 200
    assert 'resources/player.html' in [template.name for template in response.templates]
    assert response.context['team'] == team
    assert list(response.context['players']) == [player_1, player_2]
    assert response.context['title'] == f'{team} players'


@pytest.mark.django_db
def test__get_players_for_team__with_no_players(admin_client):
    team = Team.objects.create(name='Empty Team', slug='empty-team')

    response = admin_client.get(reverse('players', kwargs={'team_slug': team.slug}))

    assert response.status_code == 200
    assert list(response.context['players']) == []


@pytest.mark.django_db
def test__get_players_for_team__with_invalid_team_slug(admin_client):
    response = admin_client.get(reverse('players', kwargs={'team_slug': 'non-existent-team'}))

    assert response.status_code == 404


@pytest.mark.django_db
def test__get_players_for_team__redirects_for_anonymous_user(client):
    team = Team.objects.create(name='Private Team', slug='private-team')

    response = client.get(reverse('players', kwargs={'team_slug': team.slug}))

    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test__get_players_for_team__with_correct_url_params(admin_client):
    team_1 = Team.objects.create(name='Team 1', slug='team-1')
    team_2 = Team.objects.create(name='Team 2', slug='team-2')

    player_1 = Player.objects.create(name='Player 1', team=team_1)
    player_2 = Player.objects.create(name='Player 2', team=team_2)

    response = admin_client.get(reverse('players', kwargs={'team_slug': team_1.slug}))

    assert list(response.context['players']) == [player_1]


@pytest.mark.django_db
def test__get_players_for_team__pagination(admin_client):
    team = Team.objects.create(name='Paginated Team', slug='paginated-team')
    for i in range(15):
        Player.objects.create(name=f'Player {i}', team=team)

    response_page_1 = admin_client.get(reverse('players', kwargs={'team_slug': team.slug}))
    response_page_2 = admin_client.get(reverse('players', kwargs={'team_slug': team.slug}) + '?page=2')

    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200
    assert len(response_page_1.context['players']) == 10
    assert len(response_page_2.context['players']) == 5



