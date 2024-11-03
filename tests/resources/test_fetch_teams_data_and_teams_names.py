from unittest.mock import patch

from curl_cffi.requests.exceptions import DNSError, ProxyError
from resources.utils import fetch_teams_data_and_teams_names


def test__fetch_teams_and_names__valid_response(mock_response, teams_names):
    with patch('resources.utils.requests.get', return_value=mock_response):
        teams_data, teams_names_result = fetch_teams_data_and_teams_names()

        assert teams_names_result == teams_names
        assert len(teams_data) == 2


def test__fetch_teams_and_names__invalid_url():
    with patch('resources.utils.requests.get', side_effect=DNSError('Failed to resolve host')):
        teams_data, teams_names = fetch_teams_data_and_teams_names()

        assert teams_data is None
        assert teams_names is None


def test__fetch_teams_and_names__invalid_proxy():
    with patch('resources.utils.requests.get', side_effect=ProxyError('Failed to connect to proxy')):
        teams_data, teams_names = fetch_teams_data_and_teams_names()

        assert teams_data is None
        assert teams_names is None






