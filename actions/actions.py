from typing import Text, List, Optional, Dict, Any
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, Action
from dotenv import load_dotenv
import os
import requests
import json
import uuid

load_dotenv()


def get_env_var(key):
    env_var = os.getenv(key)
    if env_var is None:
        raise RuntimeError(f"Environment variable {key} was not found.")
    return env_var


airtable_api_key = get_env_var("AIRTABLE_API_KEY")
base_id = get_env_var("BASE_ID")
table_name = get_env_var("TABLE_NAME")


def create_newsletter_record(email, frequency, notifications, can_ask_age, age):
    request_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {airtable_api_key}",
    }

    data = {
        "fields": {
            "Id": str(uuid.uuid4()),
            "Email": email,
            "Frequency": frequency,
            "Notifications?": notifications,
            "Can ask age?": can_ask_age,
            "Age": age,
        }
    }

    print(request_url)
    print(headers)
    print(json.dumps(data))

    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response


class ValidateNewsletterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_newsletter_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        if not tracker.get_slot("can_ask_age"):
            slots_mapped_in_domain.remove("age")

        return slots_mapped_in_domain


class SubmitNewsletterForm(Action):

    def name(self) -> Text:
        return "submit_newsletter_form"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        frequency = tracker.get_slot("frequency")
        notifications = tracker.get_slot("notifications")
        can_ask_age = tracker.get_slot("can_ask_age")
        age = tracker.get_slot("age")

        response = create_newsletter_record(email, frequency, notifications, can_ask_age, age)

        dispatcher.utter_message("Thanks, your answers have been recorded!")

        return []

# class ActionSayStuff(Action):
#     def name(self) -> Text:
#         return "action_say_stuff"
#
#     def run(self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message("Stuff")
#
#         return []
