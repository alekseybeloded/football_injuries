import pytest
from resources.models import Player
from resources.utils import update_players_for_team


@pytest.mark.django_db
def test__update_players_for_team__length_player_data_is_equal_two_for_each_player(players_data, team):
    update_players_for_team(players_data, team)
    updated_players = Player.objects.filter(team=team)

    assert updated_players.count() == 2
    assert Player.objects.filter(name='Player 1', team=team).exists()
    assert Player.objects.filter(name='Player 2', team=team).exists()


@pytest.mark.django_db
def test__update_players_for_team__length_player_data_is_not_equal_two_for_each_player(team):
    update_players_for_team([['Injury 1'], ['Player 2', 'Injury 2']], team)
    updated_players = Player.objects.filter(team=team)

    assert updated_players.count() == 1
    assert Player.objects.filter(name='Player 2', team=team).exists()
