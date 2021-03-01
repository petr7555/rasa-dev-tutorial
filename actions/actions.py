from typing import Text, List, Optional
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker


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
