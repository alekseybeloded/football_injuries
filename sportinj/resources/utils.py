import logging
import os
from dataclasses import dataclass

from bs4 import BeautifulSoup
from curl_cffi import requests
from curl_cffi.requests.exceptions import DNSError, ProxyError
from dotenv import load_dotenv

from resources.models import Injury, Player, Team

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True, slots=True)
class MenuItem:
    title: str
    url_name: str


menu = [MenuItem(title='Contacts', url_name='contacts')]


class ExtraContextMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        context.update(self.extra_context)
        context.update(kwargs)
        return context


def fetch_teams_data_and_teams_names():
    proxies = {"https": os.getenv('PROXY')}
    try:
        response = requests.get(
            "https://www.premierleague.com/latest-player-injuries",
            impersonate="chrome110", proxies=proxies,
        )
    except DNSError as e:
        logger.error('Failed to fetch correct response due to DNSError: %s', e)
        return None, None
    except ProxyError as e:
        logger.error('Failed to fetch correct response due to ProxyError: %s', e)
        return None, None

    soup = BeautifulSoup(response.content, features='html.parser')

    teams_data = soup.find_all('table')
    teams_names = [
        h3.get_text() for h3 in soup.find_all(
            'h3',
            class_='transfers-club-header__team-name u-hide-mob'
        )
    ]
    return teams_data, teams_names


def update_teams(teams_names):
    existing_teams = []
    for team_name in teams_names:
        team, _ = Team.objects.get_or_create(name=team_name)
        existing_teams.append(team)

    Team.objects.exclude(pk__in=[team.pk for team in existing_teams]).delete()
    return existing_teams


def parse_players_from_team_data(teams_data):
    if teams_data is None:
        return []

    players_data = []
    for tr in teams_data.find_all('tr')[1:]:
        player_info = [td.get_text(strip=True) for td in tr.find_all('td')[:-1]]
        players_data.append(player_info)
    return players_data


def update_players_for_team(players_data, team):
    existing_players = []
    for player_data in players_data:
        if len(player_data) != 2:
            continue
        player_name = player_data[0]

        player, _ = Player.objects.get_or_create(name=player_name, team=team)
        existing_players.append(player)

        update_injuries_for_player(player, player_data)

    Player.objects.filter(team=team).exclude(pk__in=[p.pk for p in existing_players]).delete()


def update_injuries_for_player(player, player_data):
    injury_name = player_data[1] if player_data[1] != '-' else 'Unkown injury'
    injury_name = (
        injury_name
        if injury_name.lower().endswith('injury')
        else f'{injury_name} injury'
    )

    injury, _ = Injury.objects.get_or_create(name=injury_name, player=player)
    player.injuries.exclude(pk=injury.pk).delete()
