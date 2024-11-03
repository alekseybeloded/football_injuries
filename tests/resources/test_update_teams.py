import pytest
from resources.models import Team
from resources.utils import update_teams


@pytest.mark.django_db
def test__update_teams__has_teams_names():
    result = update_teams(['Team 1', 'Team 2'])
    expected_teams = list(Team.objects.filter(name__in=['Team 1', 'Team 2']))

    assert result == expected_teams


@pytest.mark.django_db
def test__update_teams__teams_names_is_empty():
    assert update_teams([]) == []
