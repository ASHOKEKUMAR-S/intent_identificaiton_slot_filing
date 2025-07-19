import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.llm_client import LLMClient
from services.router import Router

# Load .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define paths
config_path = "config/intents_config.json"
intent_prompt_path = "prompts/intent_classification_template.txt"
slot_prompt_path = "prompts/slot_filling_template.txt"

# Initialize and run
llm = LLMClient(api_key=api_key)
router = Router(
    llm_client=llm,
    config_path=config_path,
    intent_prompt_path=intent_prompt_path,
    slot_prompt_path=slot_prompt_path
)

router.run()
