import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os
import json


def create_intent(intent_name, answer, questions):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(os.getenv("GOOGLE_APPLICATION_PROJECT_ID"))

    training_phrases = []
    for question in questions:
        training_phrase = {
            "parts": [
                {
                    "text": f"{question}"
                }
            ]
        }
        training_phrases.append(training_phrase)

    intent = {
        "display_name": f"{intent_name}",
        "messages": [
            {
                "text": {
                    "text": [
                        f"{answer}"
                    ]
                }
            }
        ],
        "training_phrases": training_phrases
    }

    client.create_intent(parent, intent)


def train_agent():
    client = dialogflow.AgentsClient()
    parent = client.project_path(os.getenv("GOOGLE_APPLICATION_PROJECT_ID"))
    client.train_agent(parent)


def fetch_dialogflow_answer(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text,
        language_code=language_code
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session,
        query_input=query_input
    )
    response_text = response.query_result.fulfillment_text
    is_fallback = response.query_result.intent.is_fallback
    return response_text, is_fallback


if __name__ == '__main__':
    load_dotenv()
    with open("questions.json", "r") as json_file:
        intent_data = json.load(json_file)
    for intent_name, intent_name_data in intent_data.items():
        answer = intent_name_data["answer"]
        questions = intent_name_data["questions"]
        create_intent(intent_name, answer, questions)
    train_agent()


