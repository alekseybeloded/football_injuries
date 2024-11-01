import pytest
from django.contrib.auth import get_user_model
from account.authentication import EmailAuthBackend
from resources.models import Team, Player, Injury
from unittest.mock import Mock
from bs4 import BeautifulSoup


@pytest.fixture
def user(db):
    def create_user(
        username='valid_username',
        email='valid@mail.com',
        password='valid_password',
        first_name='first_name',
        last_name='last_name',
        is_active=True,
    ):
        user = get_user_model()
        user = user.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
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


@pytest.fixture
def mock_response():
    mock_response = Mock()
    mock_response.status = 200
    mock_response.content = '''
        <html>
            <h3 class="transfers-club-header__team-name u-hide-mob">Team 1</h3>
            <h3 class="transfers-club-header__team-name u-hide-mob">Team 2</h3>
            <table>
                <tr><td>Player 1</td><td>Injury 1</td></tr>
                <tr><td>Player 2</td><td>Injury 2</td></tr>
            </table>
            <table>
                <tr><td>Player 3</td><td>Injury 3</td></tr>
                <tr><td>Player 4</td><td>Injury 4</td></tr>
            </table>
        </html>
    '''
    return mock_response


@pytest.fixture
def teams_data():
    def create_team_table(
        html='''
            <table>
                <tr><td>Header 1</td><td>Header 2</td></tr>
                <tr><td>Player 1</td><td>Injury 1</td><td><a href="https://example.com/details1">Details</a></td></tr>
                <tr><td>Player 2</td><td>Injury 2</td><td><a href="https://example.com/details2">Details</a></td></tr>
            </table>
        '''
    ):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find('table')
    return create_team_table


@pytest.fixture
def teams_names():
    return ['Team 1', 'Team 2']


@pytest.fixture
def players_data():
    return [
        ['Player 1', 'Injury 1'],
        ['Player 2', 'Injury 2'],
    ]

