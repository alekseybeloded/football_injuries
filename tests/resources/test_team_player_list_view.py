import pytest
from django.urls import reverse
from resources.models import Player


@pytest.mark.django_db
def test__team_player_list_view__renders_correct_template(admin_client, team):
    player_1 = Player.objects.create(name='Player 1', team=team)
    player_2 = Player.objects.create(name='Player 2', team=team)

    response = admin_client.get(reverse('team-players', kwargs={'team_slug': team.slug}))

    assert response.status_code == 200
    assert 'resources/player.html' in [template.name for template in response.templates]
    assert response.context['team'] == team
    assert list(response.context['players']) == [player_1, player_2]
    assert response.context['title'] == f'{team} players'


@pytest.mark.django_db
def test__team_player_list_view__with_no_players(admin_client, team):
    response = admin_client.get(reverse('team-players', kwargs={'team_slug': team.slug}))

    assert response.status_code == 200
    assert list(response.context['players']) == []


@pytest.mark.django_db
def test__team_player_list_view__with_invalid_team_slug(admin_client):
    response = admin_client.get(reverse('team-players', kwargs={'team_slug': 'non-existent-team'}))

    assert response.status_code == 404


@pytest.mark.django_db
def test__team_player_list_view__redirects_for_anonymous_user(client, team):
    response = client.get(reverse('team-players', kwargs={'team_slug': team.slug}))

    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test__team_player_list_view__pagination(admin_client, team):
    for i in range(15):
        Player.objects.create(name=f'Player {i}', team=team)

    response_page_1 = admin_client.get(
        reverse(
            'team-players',
            kwargs={'team_slug': team.slug},
        )
    )
    response_page_2 = admin_client.get(
        reverse(
            'team-players',
            kwargs={'team_slug': team.slug}
        ) + '?page=2'
    )

    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200
    assert len(response_page_1.context['players']) == 10
    assert len(response_page_2.context['players']) == 5

