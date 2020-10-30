import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from logs_handler import TelegramLogsHandler
from dialogflow_helper import fetch_dialogflow_answer


logger = logging.getLogger(__file__)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Здравствуйте, чем можем помочь?")


def error_callback(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def start_answer_handler(bot, update):
    project_id = os.getenv("GOOGLE_APPLICATION_PROJECT_ID")
    session_id = update.message.chat_id
    text = update.message.text
    response_text, _ = fetch_dialogflow_answer(project_id, session_id, text, "ru-RU")
    bot.send_message(chat_id=update.message.chat_id, text=response_text)


if __name__ == "__main__":
    load_dotenv()
    logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler()
    logger.addHandler(handler)

    logger.info("Телеграм бот запущен")
    updater = Updater(token=os.getenv("TG_TOKEN_ANSWER_BOT"))
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    answer_handler = MessageHandler(Filters.text, start_answer_handler)
    dispatcher.add_handler(answer_handler)

    dispatcher.add_error_handler(error_callback)
    updater.start_polling()

