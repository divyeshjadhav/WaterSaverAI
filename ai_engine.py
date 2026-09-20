"""
AI ENGINE - Connects to Ollama
This file is in the utils/ folder, so imports are simple
"""

import requests
import sys
import os

# Add parent directory to path so we can import from utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_templates import build_messages
from fallback_responses import fallback_response

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "mistral"   # Change to "llama3.2" if you prefer


class AIEngine:
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.chat_url = f"{OLLAMA_URL}/api/chat"
        self.tags_url = f"{OLLAMA_URL}/api/tags"

    def is_ollama_running(self):
        """Check if Ollama is accessible"""
        try:
            return requests.get(self.tags_url, timeout=2).status_code == 200
        except:
            return False

    def is_model_available(self):
        """Check if model is downloaded"""
        try:
            data = requests.get(self.tags_url, timeout=2).json()
            names = [m.get("name", "") for m in data.get("models", [])]
            return any(n.split(":")[0] == self.model.split(":")[0] for n in names)
        except:
            return False

    def generate_response(self, user_input, user_profile, chat_history, stats):
        """
        Generate response from Ollama or fallback
        
        Returns:
            (answer_text, system_prompt, source)
        """
        messages, system_text, intent = build_messages(
            user_input, user_profile, chat_history, stats
        )

        if not self.is_ollama_running():
            return fallback_response(intent, user_profile, stats), system_text, "fallback"

        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 400,
                },
            }
            r = requests.post(self.chat_url, json=payload, timeout=180)
            r.raise_for_status()
            answer = r.json()["message"]["content"].strip()
            if not answer:
                raise ValueError("Empty response")
            return answer, system_text, "ollama"

        except Exception as e:
            print(f"[AIEngine] Error: {e}")
            note = f"\n\n_(⚠️ Using quick answer: {str(e)[:50]})_"
            return fallback_response(intent, user_profile, stats) + note, system_text, "fallback"