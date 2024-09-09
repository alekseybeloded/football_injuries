import pytest
from resources.models import Team, Player, Injury
from django.urls import reverse


@pytest.mark.django_db
def test__get_injuries_for_player__renders_correct_template(admin_client):
    team = Team.objects.create(name='Team')
    player = Player.objects.create(name='Player', team=team)
    injury_1 = Injury.objects.create(name='Injury 1', player=player)
    injury_2 = Injury.objects.create(name='Injury 2', player=player)

    response = admin_client.get(
        reverse(
            'injuries',
            kwargs={
                'team_slug': team.slug,
                'player_slug': player.slug
            }
        )
    )

    assert response.status_code == 200
    assert 'resources/injury.html' in [template.name for template in response.templates]
    assert list(response.context['injuries']) == [injury_1, injury_2]
    assert response.context['title'] == f"{player.name}'s injuries"


@pytest.mark.django_db
def test__get_injuries_for_player__with_no_injuries(admin_client):
    team = Team.objects.create(name='Empty Team', slug='empty-team')
    player = Player.objects.create(name='Player', team=team)

    response = admin_client.get(
        reverse(
            'injuries',
            kwargs={
                'team_slug': team.slug,
                'player_slug': player.slug
            }
        )
    )

    assert response.status_code == 200
    assert list(response.context['injuries']) == []


@pytest.mark.django_db
def test__get_injuries_for_player__with_invalid_slug(admin_client):
    response = admin_client.get(
        reverse(
            'injuries',
            kwargs={
                'team_slug': 'non-existent-team',
                'player_slug': 'non-existent-player'
            }
        )
    )

    assert response.status_code == 404

