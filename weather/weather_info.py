from typing import NamedTuple, TypeAlias

import requests
from dotenv import dotenv_values
from geopy import Nominatim
from loguru import logger

config = dotenv_values('.env')

API_KEY: str = config.get('API_KEY')

URL_NAME: str = 'https://api.weatherapi.com/v1/current.json'

Json: TypeAlias = dict


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def _get_gps_coordinates(ip_address: str) -> Json:
    """Requests ip_address and
    returns latitude and longitude."""
    geolocator = Nominatim(user_agent='Coordinates')
    location = geolocator.geocode(ip_address)
    try:
        coordinates = Coordinates(location.latitude, location.longitude)
    except AttributeError:
        raise AttributeError('Error with location')
    else:
        return _get_weather(coordinates)


def _get_weather(coordinates: Coordinates) -> Json:
    """Gets coordinates and returns json
    response with data of weather."""
    data = {
        'key': API_KEY,
        'lang': 'ru',
        'q': f"{coordinates.latitude} {coordinates.longitude}",
    }
    weather = requests.get(
        URL_NAME,
        params=data,
    )
    logger.info(weather.json())
    logger.info(weather.url)
    if weather.status_code == requests.codes.ok:
        try:
            response = weather.json()['current']
        except KeyError:
            raise KeyError('Key "forecast" is absent')
        except Exception as error:
            raise Exception(f'{error}')
        else:
            return response
    else:
        raise requests.RequestException(
            f'Request status is {weather.status_code}'
        )


def get_weather_description(context) -> str:
    """Get name of city in str
    and returns weather information."""
    try:
        data = _get_gps_coordinates(context)
        temperature = data.get('temp_c')
        text = data.get('condition').get('text')
        wind_speed = data['wind_kph']
    except KeyError:
        raise KeyError('Keys "temp_c" or "text" are absent')
    response = (
        f'Температура: {temperature} градусов по цельсию\n'
        f'Погода: {text}\n'
        f'Скорость ветра: {wind_speed} км/ч'
    )
    return response


def get_photo_about_weather(context) -> str:
    """Gets city in str
    and returns icon's url."""
    try:
        data = _get_gps_coordinates(context)
        condition = data['condition']
        icon = condition['icon']
    except KeyError:
        raise KeyError('Key condition or icon are absent')
    else:
        return 'https:' + icon
