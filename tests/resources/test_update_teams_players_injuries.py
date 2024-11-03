from unittest.mock import patch

import pytest
from resources.tasks import update_teams_players_injuries


def test__update_teams_and_players__teams_data_and_teams_names_are_none():
    with patch(
        'resources.utils.fetch_teams_data_and_teams_names',
        return_value=(None, None),
    ):
        assert update_teams_players_injuries() is None


@pytest.mark.django_db
def test__update_teams_and_players__successful_update(teams_data, teams_names):
    teams_data = teams_data()
    with (
        patch(
            'resources.utils.fetch_teams_data_and_teams_names',
            return_value=(teams_data, teams_names)
        ),
        patch('resources.utils.update_teams') as update_teams_mock,
    ):

        update_teams_players_injuries()

        update_teams_mock.assert_called_once_with(teams_names)
