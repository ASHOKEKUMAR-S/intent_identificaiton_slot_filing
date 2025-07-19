# services/intent_classifier.py

import json
from services.llm_client import LLMClient

class IntentClassifier:
    def __init__(self, llm_client: LLMClient, prompt_path: str):
        self.llm_client = llm_client
        self.prompt_path = prompt_path

    def classify(self, user_input: str) -> dict:
        try:
            response = self.llm_client.complete_prompt(
                prompt_path=self.prompt_path,
                variables={"user_input": user_input}
            )
            parsed = json.loads(response)
            return parsed
        except json.JSONDecodeError:
            raise ValueError(f"Could not parse response as JSON:\n{response}")
        except Exception as e:
            raise RuntimeError(f"Intent classification failed: {str(e)}")
