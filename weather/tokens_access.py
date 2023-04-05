from dotenv import dotenv_values

config = dotenv_values('.env')

API_KEY: str = config.get('API_KEY')
TELEGRAM_TOKEN: str = config.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID: str = config.get('TELEGRAM_CHAT_ID')


def check_tokens():
    """Returns True if all tokens allow,
    False otherwise."""
    return all([API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])
