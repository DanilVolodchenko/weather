from dotenv import dotenv_values
from exceptions import MessageDoesNotSend
from telegram.chat import Chat
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler, Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from weather_info import weather_info

config = dotenv_values('.env')

TELEGRAM_TOKEN: str = config.get('TELEGRAM_TOKEN')


def get_message(update: Update, context: CallbackContext) -> None:
    """Returns message and photo from API."""
    chat = update.effective_chat
    message = weather_info(update.message.text).info
    photo = weather_info(update.message.text).photo
    return send_message(chat, message, photo, context)


def send_message(chat: Chat,
                 message: str,
                 photo: str,
                 context: CallbackContext) -> None:
    """Sends info about weather in telegram."""
    try:
        context.bot.send_message(chat_id=chat.id, text=message)
        context.bot.send_photo(chat_id=chat.id, photo=photo)
    except BadRequest:
        raise BadRequest('Can not send message!')
    except Exception as error:
        raise MessageDoesNotSend(f'Error with message {error}')


def connect_telegram_bot() -> None:
    """Gets information from telegram."""
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_message))
    updater.start_polling(poll_interval=5.0)
    updater.idle()
