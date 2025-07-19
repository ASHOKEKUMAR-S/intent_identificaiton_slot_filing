# services/router.py

from services.intent_classifier import IntentClassifier
from services.slot_filler import SlotFiller
from services.llm_client import LLMClient

context_slots = {}

class Router:
    def __init__(self, llm_client: LLMClient, config_path: str, intent_prompt_path: str, slot_prompt_path: str):
        self.intent_classifier = IntentClassifier(llm_client, intent_prompt_path)
        self.slot_filler = SlotFiller(llm_client, config_path, slot_prompt_path)
        self.llm_client = llm_client
        self.previous_domain = None
        self.previous_action = None

    def run(self):
        print("💬 Start chatting! Type 'exit' to quit.\n")
        while True:
            user_input = input("🧑 You: ")
            if user_input.lower() in ("exit", "quit"):
                usage = self.llm_client.token_tracker.get_total_usage()
                print(f"\n📊 Final token usage: {usage}")
                break

            try:
                # Step 1: Classify intent
                parsed = self.intent_classifier.classify(user_input)
                domain = parsed.get("domain")
                action = parsed.get("action")
                new_slots = parsed.get("slots", {})

                print(f"🔍 Detected domain: {domain}, action: {action}")
                print(f"🧩 Initial slots: {new_slots}")

                # Reset context_slots if intent/domain/action changes
                if domain != self.previous_domain or action != self.previous_action:
                    context_slots.clear()
                    self.previous_domain = domain
                    self.previous_action = action

                # Merge new slots with context slots (new values override old ones)
                context_slots.update(new_slots)

                # Step 2: Fill missing slots based on merged context
                complete_slots = self.slot_filler.fill_slots(domain, action, context_slots)
                
                # Update context with completed slots
                context_slots.update(complete_slots)

                print(f"\n✅ All slots filled: {context_slots}")

                # Step 3: Final response (mock)
                print(f"\n🚀 [Mock] Executing `{domain}.{action}` with slots:")
                for k, v in context_slots.items():
                    print(f"   - {k}: {v}")

                # Step 4: Token usage summary
                usage = self.llm_client.token_tracker.get_total_usage()
                print(f"\n📊 Token usage so far: {usage}")

            except Exception as e:
                print(f"❌ Error: {str(e)}")
