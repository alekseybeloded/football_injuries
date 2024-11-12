import pytest
from resources.models import Injury
from django.urls import reverse


@pytest.mark.django_db
def test__player_injury_list_view__renders_correct_template(admin_client, player):
    injury_1 = Injury.objects.create(name='Injury 1', player=player)
    injury_2 = Injury.objects.create(name='Injury 2', player=player)

    response = admin_client.get(
        reverse(
            'player-injuries',
            kwargs={
                'player_slug': player.slug,
            }
        )
    )

    assert response.status_code == 200
    assert 'resources/injury.html' in [template.name for template in response.templates]
    assert list(response.context['injuries']) == [
        {'name': 'Injury 1' },
        {'name': 'Injury 2'},
    ]
    assert response.context['title'] == f'{player.name}"s injuries'


@pytest.mark.django_db
def test__player_injury_list_view__with_no_injuries(admin_client, player):
    response = admin_client.get(
        reverse(
            'player-injuries',
            kwargs={
                'player_slug': player.slug
            }
        )
    )

    assert response.status_code == 200
    assert list(response.context['injuries']) == []
