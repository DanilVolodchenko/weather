from typing import NamedTuple, TypeAlias

import requests
from dotenv import dotenv_values
from geopy import Nominatim
from loguru import logger

config = dotenv_values('.env')

API_KEY: str = config.get('API_KEY')

URL_NAME: str = 'https://api.weatherapi.com/v1/forecast.json'

Json: TypeAlias = dict


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class Weather(NamedTuple):
    info: str
    photo: str


def get_gps_coordinates(address: str) -> Coordinates:
    """Requests ip_address and
    returns latitude and longitude."""
    geolocator = Nominatim(user_agent='Coordinates')
    try:
        location = geolocator.geocode(address)
    except AttributeError:
        raise AttributeError('Error with location')
    else:
        return Coordinates(location.latitude, location.longitude)


def get_weather_in_json(coordinates: Coordinates) -> Json:
    """Gets data in json and returns
     data of weather in json."""
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
            response = weather.json()
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


def get_current_weather_info(data: Json) -> str:
    """Get name of city in str
    and returns weather information."""
    try:
        current_weather = data['current']
        temperature = current_weather.get('temp_c')
        text = current_weather.get('condition').get('text')
        wind_speed = current_weather.get('wind_kph')
    except KeyError:
        raise KeyError('Keys "temp_c" or "text" are absent')
    response = (
        f'Температура: {temperature}\n'
        f'Погода: {text}\n'
        f'Скорость ветра: {wind_speed} км/ч\n'
    )
    return response


def get_astro_info(data: Json) -> str:
    """Get name of city in str
    and returns weather information."""
    try:
        astro = data['forecast']['forecastday'][0]['astro']
        logger.info(astro)
        sunrise = astro.get('sunrise')
        sunset = astro.get('sunset')
        moonrise = astro.get('moonrise')
        moonset = astro.get('moonset')
    except KeyError:
        raise KeyError('Keys "sunrise", "sunset" etc are absent')
    response = (
        '\n'
        f'Восход солнца: {sunrise[:-3]}\n'
        f'Закат солнца: {int(sunset[:2]) + 12}{sunset[2:-3]}\n'
        '\n'
        f'Восход луны: {int(moonrise[:2]) + 12}{moonrise[2:-3]}\n'
        f'Закат луны: {moonset[:-3]}\n'
    )
    return response


def get_photo_about_weather(data: Json) -> str:
    """Gets city in str
    and returns icon's url."""
    try:
        condition = data['current'].get('condition')
        icon = condition['icon']
    except KeyError:
        raise KeyError('Key condition or icon are absent')
    else:
        return 'https:' + icon


def weather_info(context: str) -> Weather:
    coordinates = get_gps_coordinates(context)
    data = get_weather_in_json(coordinates)

    temp = get_current_weather_info(data)
    astro = get_astro_info(data)
    photo = get_photo_about_weather(data)
    info = temp + astro
    return Weather(info, photo)
