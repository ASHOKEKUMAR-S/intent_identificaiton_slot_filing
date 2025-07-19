import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from dotenv import load_dotenv
import os
from services.llm_client import LLMClient
from services.intent_classifier import IntentClassifier

# Load .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Instantiate GPT client and classifier
llm = LLMClient(api_key=api_key)
classifier = IntentClassifier(llm_client=llm, prompt_path="prompts/intent_classification.txt")

# Test a sample user input
user_input = "Show all alerts for app Apollo last week"
result = classifier.classify(user_input)

print("Parsed Intent:\n", result)
print("Token Usage:\n", llm.token_tracker.get_total_usage())
