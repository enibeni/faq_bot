import os
from dotenv import load_dotenv
import dialogflow_v2 as dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from logs_handler import TelegramLogsHandler


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Здравствуйте")


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

    return response.query_result.fulfillment_text


def start_answer_handler(bot, update):
    tg_logger.info('Телеграм бот запущен')
    project_id = os.getenv('PROJECT_ID')
    session_id = update.message.chat_id
    texts = [update.message.text]
    try:
        response_text = detect_intent_texts(project_id, session_id, texts, "ru-RU")
        bot.send_message(chat_id=update.message.chat_id, text=response_text)
    except Exception as e:
        tg_logger.error('Бот упал с ошибкой:')
        tg_logger.exception(e)


if __name__ == '__main__':
    load_dotenv()
    tg_logger = logging.getLogger("telegram-bot")
    tg_logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler()
    tg_logger.addHandler(handler)

    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    answer_handler = MessageHandler(Filters.text, start_answer_handler)
    dispatcher.add_handler(answer_handler)
    updater.start_polling()
