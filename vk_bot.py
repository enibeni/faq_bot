import os
import random
from dotenv import load_dotenv
import dialogflow_v2 as dialogflow
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import logging
from logs_handler import TelegramLogsHandler


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text
    else:
        return None


def start_vk_listener(event, vk_api):
    project_id = os.getenv("GOOGLE_APPLICATION_PROJECT_ID")
    session_id = event.user_id,
    texts = [event.text]
    try:
        response = detect_intent_texts(project_id, session_id, texts, "ru-RU")
        if response is not None:
            vk_api.messages.send(
                user_id=event.user_id,
                message=response,
                random_id=random.randint(1,1000)
            )
    except Exception as e:
        vk_logger.error("Бот упал с ошибкой:")
        vk_logger.exception(e)


if __name__ == "__main__":
    load_dotenv()
    vk_logger = logging.getLogger("vk-bot")
    vk_logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler()
    vk_logger.addHandler(handler)

    vk_logger.info("ВК бот запущен")
    vk_session = vk_api.VkApi(token=os.getenv('VK_TOKEN_ANSWER_BOT'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            start_vk_listener(event, vk_api)

