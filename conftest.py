import pytest
from django.contrib.auth import get_user_model
from account.authentication import EmailAuthBackend
from resources.models import Team, Player, Injury


@pytest.fixture
def user(db):
    def create_user(is_active=True):
        user = get_user_model()
        user = user.objects.create_user(
            username='valid_username',
            email='valid@mail.com',
            password='valid_password',
            first_name='first_name',
            last_name='last_name',
            is_active=is_active,
        )
        user.raw_password = 'valid_password'
        return user
    return create_user


@pytest.fixture
def team():
    return Team.objects.create(name='Team 1')


@pytest.fixture
def player(team):
    return Player.objects.create(name='Player 1', team=team)


@pytest.fixture
def injury(player):
    return Injury.objects.create(name='Injury 1', player=player)


@pytest.fixture
def email_auth_backend():
    return EmailAuthBackend()
