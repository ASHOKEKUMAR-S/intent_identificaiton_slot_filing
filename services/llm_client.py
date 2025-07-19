# services/llm_client.py

from openai import OpenAI
from pathlib import Path
import json
from utils.token_tracker import TokenTracker

class LLMClient:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.token_tracker = TokenTracker()

    def _load_prompt(self, prompt_path: str) -> str:
        path = Path(prompt_path)
        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
        return path.read_text()

    def _format_prompt(self, template: str, variables: dict) -> str:
        for key, value in variables.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, indent=2)
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def complete_prompt(self, prompt_path: str, variables: dict) -> str:
        prompt_template = self._load_prompt(prompt_path)
        prompt_text = self._format_prompt(prompt_template, variables)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.2,
        )

        result = response.choices[0].message.content
        usage = response.usage
        self.token_tracker.update_usage(usage.prompt_tokens, usage.completion_tokens)
        return result
