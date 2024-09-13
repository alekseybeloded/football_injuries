import pytest
from resources.models import Team


@pytest.mark.django_db
def test_team_slug_is_generated_on_save():
    team = Team(name='Test team')

    team.save()

    assert team.slug == 'test-team'
    assert Team.objects.get(name='Test team').slug == 'test-team'
