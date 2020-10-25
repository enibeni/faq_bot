import os
import logging
import logging.config
import telegram


class TelegramLogsHandler(logging.Handler):
    # dictLogConfig = {
    #     "version": 1,
    #     "handlers": {
    #         "fileHandler": {
    #             "class": "logging.FileHandler",
    #             "formatter": "myFormatter",
    #             "filename": "config2.log"
    #         }
    #     },
    #     "loggers": {
    #         "exampleApp": {
    #             "handlers": ["fileHandler"],
    #             "level": "INFO",
    #         }
    #     },
    #     "formatters": {
    #         "myFormatter": {
    #             "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    #         }
    #     }
    # }

    # logging.config.dictConfig(dictLogConfig)

    def emit(self, record):
        log_entry = self.format(record)

        bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN_LOGGER'))
        bot.send_message(chat_id=os.getenv('CHAT_ID'), text=log_entry)
