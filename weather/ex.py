import requests
from dotenv import dotenv_values

config = dotenv_values('.env')

API_KEY: str = config.get('API_KEY')

URL_NAME: str = 'https://api.weatherapi.com/v1/forecast.json'

data = {
    'key': API_KEY,
    'lang': 'ru',
    'q': f"Novosibirsk",
}
weather = requests.get(
    URL_NAME,
    params=data,
).json()

print(weather['forecast']['forecastday'][0]['astro'])
