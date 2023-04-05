from dotenv import dotenv_values
from telegram.error import BadRequest
from telegram.ext import Filters, Updater, MessageHandler

from exceptions import MessageDoesNotSend
from weather_info import (get_weather_description,
                          get_photo_about_weather)

config = dotenv_values('.env')

TELEGRAM_TOKEN: str = config.get('TELEGRAM_TOKEN')


def get_message(update, context) -> None:
    """Returns message and photo from API."""
    chat = update.effective_chat
    message = get_weather_description(update.message.text)
    photo = get_photo_about_weather(update.message.text)
    return send_message(chat, message, photo, context)


def send_message(chat, message, photo, context) -> None:
    """Sends info about weather in telegram."""
    try:
        context.bot.send_message(chat_id=chat.id, text=message)
        context.bot.send_photo(chat_id=chat.id, photo=photo)
    except BadRequest:
        raise BadRequest('Can not send message!')
    except Exception as error:
        raise MessageDoesNotSend(f'Error with message {error}')


def connect_telegram_bot():
    """Gets information from telegram."""
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_message))
    updater.start_polling(poll_interval=20.0)
    updater.idle()
