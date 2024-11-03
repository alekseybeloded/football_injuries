from resources.utils import parse_players_from_team_data


def test__parse_players_from_team_data__has_team_data(teams_data, players_data):
    teams_data = teams_data()

    result = parse_players_from_team_data(teams_data)

    assert result == players_data


def test__parse_players_from_team_data__team_data_is_empty(teams_data):
    teams_data = teams_data(html='<html><body></body></html>')

    assert parse_players_from_team_data(teams_data) == []

