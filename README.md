# Intent Identification & Slot Filling (Colab-Based)

This project implements a modular, LLM-powered system in Google Colab that detects user intent, performs slot filling over a multi-turn conversation, and returns user-friendly natural language responses.

## 🚀 Features

- Intent classification using GPT-4.1
- Slot filling with up to 3 user turns
- Token usage tracking
- Secure API key handling via getpass
- Modular and FastAPI / LangChain ready
- External configuration via JSON and prompt templates

## 🧱 Project Structure

```
intent_identificaiton_slot_filing/
├── config/
│   └── intents_config.json
├── prompts/
│   ├── intent_classification.txt
│   └── slot_filling_template.txt
├── services/
│   ├── llm_client.py
│   ├── intent_classifier.py
│   ├── slot_filler.py
│   └── router.py
├── utils/
│   ├── token_tracker.py
│   └── validator.py
└── main_colab_runner.ipynb
```

## 🔌 Compatibility

- ✅ GPT-4.1 via OpenAI API
- ✅ LangChain Tool/Step ready
- ✅ FastAPI Route integration ready
- 🟡 Guardrails, RBAC stubs included

## 🔒 Security

- Uses getpass for secure OpenAI key input (no plaintext storage)
