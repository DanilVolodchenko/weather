from unittest.mock import Mock, patch

import pytest

from send_message_to_telegram import get_message, send_message


@patch('send_message_to_telegram.weather_info')
def test_get_message(mock_weather_info):
    """Test get_message function returns with
    expected args."""
    mock_weather_info.return_value = Mock(
        info='Текст сообщения',
        photo='https://example.com/photo.jpg'
    )

    mock_send_message = Mock()

    with patch('send_message_to_telegram.send_message', mock_send_message):
        update = Mock()
        context = Mock()
        get_message(update, context)

    mock_send_message.assert_called_once_with(update.effective_chat,
                                              'Текст сообщения',
                                              'https://example.com/photo.jpg',
                                              context)


def test_send_message():
    chat = Mock()
    chat.id = 12345
    text = 'Все успешно отправилось'
    photo = 'https://example.com/'
    context = Mock()
    context.bot.send_message.side_effect = Exception('Test Exception')
    context.bot.send_photo.return_value = None

    with pytest.raises(Exception):
        send_message(chat, text, photo, context)

    context.bot.send_message.assert_called_once_with(
        chat_id=chat.id,
        text=text
    ), 'send_message takes two args'
    context.bot.send_photo.assert_not_called(), 'send_photo should not be called'
