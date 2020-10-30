import os
import random
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import logging
from logs_handler import TelegramLogsHandler
from dialogflow_helper import fetch_dialogflow_answer

logger = logging.getLogger(__file__)


def start_vk_listener(event, vk_api):
    project_id = os.getenv("GOOGLE_APPLICATION_PROJECT_ID")
    session_id = event.user_id,
    text = event.text
    try:
        response_text, is_fallback = fetch_dialogflow_answer(project_id, session_id, text, "ru-RU")
        if is_fallback:
            logger.info("Бот не нашел что сказать.")
            return
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_text,
            random_id=random.randint(1,1000)
        )
    except Exception as e:
        logger.error("Бот упал с ошибкой:")
        logger.exception(e)


if __name__ == "__main__":
    load_dotenv()
    logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler()
    logger.addHandler(handler)

    logger.info("ВК бот запущен")
    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN_ANSWER_BOT"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            start_vk_listener(event, vk_api)

