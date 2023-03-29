import sys
from typing import NamedTuple, TypeAlias

import requests
import telegram
from dotenv import dotenv_values
from geopy.geocoders import Nominatim
from loguru import logger
from telegram.error import BadRequest

from exceptions import MessageDoesNotSend

config = dotenv_values('.env')

API_KEY: str = config.get('API_KEY')
TELEGRAM_TOKEN: str = config.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID: str = config.get('TELEGRAM_CHAT_ID')

URL_NAME: str = f'https://api.weatherapi.com/v1/current.json'

Json: TypeAlias = dict
Bot: TypeAlias = telegram.bot.Bot


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def check_tokens():
    """Returns True if all tokens allow,
    False otherwise."""
    return all([API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def get_gps_coordinates(place: str) -> Coordinates:
    """Requests coordinates certain place
    and returns latitude and longitude."""
    geolocator = Nominatim(user_agent='Coordinates')
    location = geolocator.geocode(place)
    try:
        coordinates = Coordinates(location.latitude, location.longitude)
    except AttributeError:
        raise AttributeError('Error with location')
    else:
        return coordinates


def get_weather(coordinates: Coordinates) -> Json:
    """Gets coordinates and returns json
    response with data of weather."""
    data = {
        'key': API_KEY,
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
        raise requests.RequestException(f'Request status is {weather.status_code}')


def get_temperature_and_weather_description(data: Json) -> str:
    """Gets data in json format and
    returns weather description."""
    try:
        temperature = data.get('temp_c')
        text = data.get('condition').get('text')
        wind_speed = data['wind_kph']
    except KeyError:
        raise KeyError('Keys "temp_c" or "text" are absent')
    response = (
        f'Temperature: {temperature} degree Celsius\n'
        f'Description: {text}\n'
        f'Wind speed: {wind_speed} km/h'
    )
    return response


def get_photo_about_weather(data: Json) -> str:
    """Gets data in json format
    and returns icon's url."""
    try:
        condition = data['condition']
        icon = condition['icon']
    except KeyError:
        raise KeyError('Key condition or icon are absent')
    else:
        return 'https:' + icon


def send_message(bot: Bot, message: str, photo: str) -> None:
    """Sends info about weather in telegram."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        bot.send_photo(TELEGRAM_CHAT_ID, photo=photo)
    except BadRequest:
        raise BadRequest('Can not send message!')
    except Exception as error:
        raise MessageDoesNotSend(f'Error with message {error}')


@logger.catch
def main():
    place = str(input('Введите город: '))

    logger.add(
        sys.stdout,
        level='DEBUG',
        colorize=True,
        format='<green>{time}</green> <bold>{level}</bold> {message} {name}'
    )

    if not check_tokens():
        logger.critical('Tokens is absent')
        raise TypeError()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    try:
        location = get_gps_coordinates(place)
        weather = get_weather(location)
        message = get_temperature_and_weather_description(weather)
        photo = get_photo_about_weather(weather)

        send_message(bot, message, photo)
    except Exception as error:
        message = f'Error in program: {error}'
        logger.error(message)
        logger.exception(error)
        bot.send_message(TELEGRAM_CHAT_ID, message)


if __name__ == '__main__':
    main()
