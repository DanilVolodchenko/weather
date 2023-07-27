import pytest
from requests import Timeout, RequestException
from unittest.mock import Mock, patch

from weather_info import (get_current_weather_info,
                          get_weather_data,
                          get_gps_coordinates,
                          get_astro_info,
                          get_photo_about_weather,
                          weather_info,
                          Weather,
                          Coordinates)


class TestGetGpsCoordinates:
    @staticmethod
    @pytest.fixture(scope='module')
    def correct_address():
        return "Novosibirsk"

    @staticmethod
    @pytest.fixture(scope='module')
    def does_not_exist_address():
        return 'Does not exist data'

    @pytest.mark.parametrize("address, expected_coordinates", [
        ("Moscow", Coordinates(40.7128, -74.0060)),
        ("Novosibirsk", Coordinates(51.5074, -0.1278)),
    ])
    def test_get_gps_coordinates(self, address, expected_coordinates):
        """Test get_gps_coordinates function to
        return correct response."""
        mock_location = Mock(latitude=expected_coordinates.latitude,
                             longitude=expected_coordinates.longitude)

        mock_geolocator = Mock()
        mock_geolocator.geocode.return_value = mock_location

        with patch('weather_info.Nominatim') as mock_nominatim:
            mock_nominatim.return_value = mock_geolocator
            result = get_gps_coordinates(address)

        assert result == expected_coordinates, \
            f'Incorrect result, expected result is: {expected_coordinates}'

    def test_get_gps_coordinates_exception(self, does_not_exist_address):
        """Check get_gps_coordinates function
        raise exception AttributeError."""

        with pytest.raises(AttributeError):
            get_gps_coordinates(does_not_exist_address)


class TestGetWeatherInJson:

    @patch('weather_info.requests')
    def test_get_weather_in_json_exception(self, requests_mock):
        """Raises TimeOut and RequestException exceptions."""
        requests_mock.get.side_effect = [Timeout, RequestException]

        with pytest.raises(Timeout):
            get_weather_data(Mock())

        with pytest.raises(RequestException):
            get_weather_data(Mock())


class TestGetCurrentWeatherInfo:
    expected_data = ('Температура: 28.0 °C\n'
                     'Погода: Солнечно\n'
                     'Скорость ветра: 25.9 км/ч\n')
    correct_data = {
        'current': {'temp_c': 28.0,
                    'condition': {
                        'text': 'Солнечно',
                    },
                    'wind_kph': 25.9
                    }
    }
    key_exception_data = {
        'cur': {'temp_c': 28.0,
                'condition': {
                    'text': 'Солнечно',
                },
                'wind_kph': 25.9
                }
    }

    def test_get_current_weather_info(self):
        """Test response of the get_current_weather_info function with data."""
        result = get_current_weather_info(self.correct_data)

        assert isinstance(result, str), 'Returns type must be str'
        assert self.expected_data == result, \
            f'Incorrect result, result should be a {self.expected_data}'

    def test_get_current_weather_info_exception(self):
        """Check get_current_weather_info function
        raise exception AttributeError."""
        with pytest.raises(KeyError):
            get_current_weather_info(self.key_exception_data), \
                'Do not raise KeyError exception'


class TestGetAstroInfo:
    correct_data = {
        'forecast': {'forecastday': [
            {'astro': {
                'sunrise': '05:09 AM',
                'sunset': '09:59 PM', }}
        ]
        }
    }
    expected_response = (
        '\n'
        'Восход солнца: 05:09\n'
        'Закат солнца: 21:59\n'
    )

    key_exception_data = {
        'fore': {'forecastday': [
            {'astro': {
                'sunrise': '05:09 AM',
                'sunset': '09:59 PM'}}
        ]
        }
    }

    type_exception_data = {
        'forecast': {'forecastday': [
            {'astro': {
                'sun': '05:09 AM',
                'sunset': '09:59 PM'}}
        ]
        }
    }

    def test_get_astro_info(self):
        """Test response of the get_astro_info function with data."""

        result = get_astro_info(self.correct_data)
        assert result == self.expected_response

    def test_get_astro_info_exceptions(self):
        """Check get_current_weather_info function to
           raise KeyError and TypeError exceptions."""
        with pytest.raises(KeyError):
            get_astro_info(self.key_exception_data)

        with pytest.raises(TypeError):
            get_astro_info(self.type_exception_data)


class TestGetPhotoAboutWeather:
    correct_data = {
        'current': {'temp_c': 28.0,
                    'condition': {
                        'icon': ('//cdn.weatherapi.com'
                                 '/weather/64x64/day/113.png'),
                    },
                    }
    }

    key_exception_data = {
        'cur': {'temp_c': 28.0,
                'condition': {
                    'icon': ('//cdn.weatherapi.com'
                             '/weather/64x64/day/113.png'),
                },
                'wind_kph': 25.9,
                }
    }

    type_exception_data = {
        'current': {'temp_c': 28.0,
                    'cond': {
                        'icon': ('//cdn.weatherapi.com'
                                 '/weather/64x64/day/113.png'),
                    },
                    'wind_kph': 25.9,
                    }
    }

    def test_get_photo_about_weather(self):
        """Test response of the get_photo_about_weather function."""
        response = 'https://cdn.weatherapi.com/weather/64x64/day/113.png'
        result = get_photo_about_weather(self.correct_data)

        assert result == response

    def test_get_photo_about_weather_exception(self):
        """Check get_photo_about_weather function to
           raise KeyError and TypeError exceptions."""
        with pytest.raises(KeyError):
            get_photo_about_weather(self.key_exception_data), \
                'Don not raise KeyError exception'

        with pytest.raises(TypeError):
            get_photo_about_weather(self.type_exception_data), \
                'Do not raise TypeError exception'


class TestWeatherInfo:
    @patch('weather_info.get_photo_about_weather')
    @patch('weather_info.get_astro_info')
    @patch('weather_info.get_current_weather_info')
    @patch('weather_info.get_weather_data')
    @patch('weather_info.get_gps_coordinates')
    def test_weather_info(self,
                          mock_get_gps_coordinates,
                          mock_get_weather_data,
                          mock_get_current_weather_info,
                          mock_get_astro_info,
                          mock_get_photo_about_weather
                          ):
        """Test response of the weather_info function."""
        mock_get_gps_coordinates.return_value = Coordinates(54.96781445,
                                                            82.95159894278376)
        get_weather_data.return_value = {
            'current': {'temp_c': 14.0,
                        'condition': {'text': 'Дымка',
                                      'icon': '//cdn.weatherapi.com/weather/64x64/night/143.png'},
                        'wind_kph': 6.8},
            'forecast': {'forecastday': [
                {'astro': {
                    'sunrise': '05:09 AM',
                    'sunset': '09:59 PM'}}
            ]
            }
        }
        mock_get_current_weather_info.return_value = (
            'Температура: 25.9 °C\n'
            'Погода: Солнечно\n'
            'Скорость ветра: 13.5 км/ч\n'
        )
        mock_get_astro_info.return_value = (
            '\n'
            'Восход солнца: 05:10\n'
            'Закат солнца: 21:58\n'
        )
        mock_get_photo_about_weather.return_value = 'https://example.com/photo.jpg'

        result = weather_info('Новосибирск')

        assert isinstance(result, Weather)
        assert result.photo == 'https://example.com/photo.jpg'
        assert result.info == (
            'Температура: 25.9 °C\n'
            'Погода: Солнечно\n'
            'Скорость ветра: 13.5 км/ч\n'
            '\n'
            'Восход солнца: 05:10\n'
            'Закат солнца: 21:58\n'
        )

    @patch('weather_info.get_gps_coordinates', side_effect=Exception)
    def test_weather_info_exception(self, mock_get_gps_coordinates):
        """Check weather_info function to
                   raise exception."""
        result = weather_info('Does not exist city')

        assert isinstance(result, Weather), ''
        assert result.info == 'Oops, something went wrong!'
        assert result.photo == 'https://encrypted-tbn0.gstatic.com/' \
                               'images?q=tbn:ANd9GcQuIsbz9QvAixpDw1Rjghft9tusNgYw3alFVx6MkzOo&s'
