import logging

from celery import shared_task

from resources import utils

logger = logging.getLogger(__name__)


@shared_task
def update_teams_players_injuries():
    teams_data, teams_names = utils.fetch_teams_data_and_teams_names()

    if not teams_data or not teams_names:
        logger.warning('update_teams_and_players aborted')
        return None

    teams = utils.update_teams(teams_names)

    for team, team_data in zip(teams, teams_data):
        players_data = utils.parse_players_from_team_data(team_data)
        utils.update_players_for_team(players_data, team)

    logger.info('updating teams and players was completed successfully')
