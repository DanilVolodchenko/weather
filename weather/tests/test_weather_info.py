import pytest
from unittest.mock import Mock

from weather_info import (get_current_weather_info,
                          get_gps_coordinates,
                          Coordinates)


@pytest.fixture(scope='module')
def address():
    return "Новосибирск"


def test_get_gps_coordinates(address):
    """Test get_gps_coordinates function to
    return correct response."""
    coordinates = get_gps_coordinates(address)
    assert isinstance(coordinates, Coordinates), "Invalid return type"
    assert coordinates.latitude == 54.96781445, "Incorrect latitude"
    assert coordinates.longitude == 82.95159894278376, "Incorrect longitude"


def test_get_gps_coordinates_exception():
    """Check get_gps_coordinates function
    raise exception AttributeError."""
    not_exists_address = 'does_not_exists_city'
    with pytest.raises(AttributeError):
        get_gps_coordinates(not_exists_address)


def test_get_weather_in_json():
    """Test response of the get_current_weather_info function with data."""
    get_weather_in_json = Mock()
    get_weather_in_json.return_value = {
        'current': {'last_updated_epoch': 1689309000,
                    'last_updated': '2023-07-14 11:30',
                    'temp_c': 28.0,
                    'temp_f': 82.4,
                    'is_day': 1,
                    'condition': {
                        'text': 'Солнечно',
                        'icon': ('//cdn.weatherapi.com'
                                 '/weather/64x64/day/113.png'),
                        'code': 1000
                    },
                    'wind_mph': 16.1,
                    'wind_kph': 25.9,
                    'wind_degree': 170
                    }
    }

    response = (
        'Температура: 28.0 °C\n'
        'Погода: Солнечно\n'
        'Скорость ветра: 25.9 км/ч\n'
    )
    result = get_current_weather_info(get_weather_in_json())

    assert isinstance(result, str), 'Returns type must be str'
    assert result == response, ('Incorrect result, '
                                f'result should be a {response}')


def test_get_weather_in_json_exception():
    """Check get_current_weather_info function
    raise exception AttributeError."""
    get_weather_in_json = Mock()
    get_weather_in_json.return_value = {
        'current': {'last_updated_epoch': 1689309000,
                    'last_updated': '2023-07-14 11:30',
                    'temp_c': 28.0,
                    'temp_f': 82.4,
                    'is_day': 1}
    }
    with pytest.raises(AttributeError):
        get_current_weather_info(get_weather_in_json())
