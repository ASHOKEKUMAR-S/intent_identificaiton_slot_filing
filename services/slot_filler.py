# services/slot_filler.py

import json
from services.llm_client import LLMClient

class SlotFiller:
    def __init__(self, llm_client: LLMClient, config_path: str, prompt_path: str):
        self.llm_client = llm_client
        self.prompt_path = prompt_path
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, "r") as f:
            return json.load(f)

    def fill_slots(self, domain: str, action: str, slots: dict, max_turns: int = 3) -> dict:
        key = f"{domain}.{action}"
        if key not in self.config:
            raise ValueError(f"Unknown domain+action: {key}")

        required_slots = set(self.config[key]["required_slots"])
        optional_slots = set(self.config[key]["optional_slots"])
        all_required = required_slots.union(optional_slots)

        turns = 0
        while turns < max_turns:
            missing = list(required_slots - slots.keys())
            if not missing:
                break

            prompt_vars = {
                "domain": domain,
                "action": action,
                "filled_slots": slots,
                "missing_slots": missing
            }

            followup_question = self.llm_client.complete_prompt(self.prompt_path, prompt_vars)
            print(f"\n🤖 GPT: {followup_question}")
            user_reply = input("🧑 You: ")

            # Re-run classification to extract new slot values
            from services.intent_classifier import IntentClassifier
            classifier = IntentClassifier(self.llm_client, self.prompt_path.replace("slot_filling", "intent_classification"))
            update = classifier.classify(user_reply)

            if update.get("slots"):
                slots.update(update["slots"])
            turns += 1

        return slots
