import sys

from loguru import logger

from send_message_to_telegram import connect_telegram_bot
from tokens_access import check_tokens


@logger.catch
def main():
    logger.add(
        sys.stdout,
        level='DEBUG',
        colorize=True,
        format='<green>{time}</green> <bold>{level}</bold> {message} {name}'
    )

    if check_tokens():
        try:
            connect_telegram_bot()
        except Exception as error:
            message = f'Error in program: {error}'
            logger.error(message)
            logger.exception(error)
    else:
        logger.error('Not access to tokens!')


if __name__ == '__main__':
    main()
