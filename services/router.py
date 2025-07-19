# services/router.py

from services.intent_classifier import IntentClassifier
from services.slot_filler import SlotFiller
from services.llm_client import LLMClient

class Router:
    def __init__(self, llm_client: LLMClient, config_path: str, intent_prompt_path: str, slot_prompt_path: str):
        self.intent_classifier = IntentClassifier(llm_client, intent_prompt_path)
        self.slot_filler = SlotFiller(llm_client, config_path, slot_prompt_path)
        self.llm_client = llm_client

    def run(self):
        print("💬 Start chatting! Type 'exit' to quit.\n")
        while True:
            user_input = input("🧑 You: ")
            if user_input.lower() in ("exit", "quit"):
                break

            try:
                # Step 1: Classify intent
                parsed = self.intent_classifier.classify(user_input)
                domain = parsed.get("domain")
                action = parsed.get("action")
                slots = parsed.get("slots", {})

                print(f"🔍 Detected domain: {domain}, action: {action}")
                print(f"🧩 Initial slots: {slots}")

                # Step 2: Fill missing slots
                complete_slots = self.slot_filler.fill_slots(domain, action, slots)
                print(f"\n✅ All slots filled: {complete_slots}")

                # Step 3: Final response (mock)
                print(f"\n🚀 [Mock] Executing `{domain}.{action}` with slots:")
                for k, v in complete_slots.items():
                    print(f"   - {k}: {v}")

                # Step 4: Token usage summary
                usage = self.llm_client.token_tracker.get_total_usage()
                print(f"\n📊 Token usage so far: {usage}")

            except Exception as e:
                print(f"❌ Error: {str(e)}")
