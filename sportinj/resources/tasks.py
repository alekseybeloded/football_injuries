from bs4 import BeautifulSoup
from celery import shared_task
from curl_cffi import requests

from resources.models import Injury, Player, Team


def fetch_teams_and_names():
    response = requests.get(
            "https://www.asdasdaf.ru",
            impersonate="chrome",
        )

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


def parse_players_from_team_table(team_table):
    players_data = []
    for tr in team_table.find_all('tr')[1:]:
        player_info = [td.get_text(strip=True) for td in tr.find_all('td')[:-1]]
        players_data.append(player_info)
    return players_data


def update_players_for_team(players_data, team):
    existing_players = []
    for player_data in players_data:
        player_name = player_data[0]

        player, _ = Player.objects.get_or_create(name=player_name, team=team)
        existing_players.append(player)

        update_injuries_for_player(player, player_data)

    Player.objects.filter(team=team).exclude(pk__in=[p.pk for p in existing_players]).delete()


def update_injuries_for_player(player, player_data):
    injury_name = player_data[1]

    if injury_name == '-':
        injury_name = 'Unkown injury'
    elif not injury_name.lower().endswith("injury"):
        injury_name = f'{injury_name} injury'

    injury, _ = Injury.objects.get_or_create(name=injury_name, player=player)

    player.injuries.exclude(pk=injury.pk).delete()


@shared_task
def update_teams_and_players():
    teams_data, teams_names = fetch_teams_and_names()

    teams = update_teams(teams_names)

    for team, team_data in zip(teams, teams_data):
        players_data = parse_players_from_team_table(team_data)
        update_players_for_team(players_data, team)
