import pytest
from unittest.mock import Mock, patch
from weather_info import get_weather_data


def response_mock(url, params):
    print(url)
    print(params)
    response_mock = Mock()
    response_mock.status_code.return_value = 200
    response_mock.json.return_value = {'Weather': 'Shiny'}

    return response_mock


@patch('weather_info.requests')
def test_get_weather_in_json(request_mock):
    request_mock.get.side_effect = response_mock
    request_mock.RequestException.return_value = None

    assert get_weather_data(Mock(latitude=34, longitude=23)) == {'Weather': 'Shiny'}
    # assert get_weather_in_json(Mock())
