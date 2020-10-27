import os
import logging.config
import telegram


class TelegramLogsHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)

        bot = telegram.Bot(token=os.getenv("TG_TOKEN_LOGGER_BOT"))
        bot.send_message(chat_id=os.getenv("TG_CHAT_ID"), text=log_entry)
