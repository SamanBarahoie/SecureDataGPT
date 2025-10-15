# app/llm_helper.py
import os
import requests
from app.config  import OPENROUTER_API_KEY, OPENROUTER_API_BASE, OPENROUTER_MODEL


class LLMHelper:
    """
    Wrapper for OpenRouter API for generating natural language summaries or recommendations.
    """

    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_API_BASE
        self.model = OPENROUTER_MODEL

        if not self.api_key:
            raise ValueError("OpenRouter API key not found in config.py.")


    def generate_text(self, prompt: str) -> str:
        """
        Sends a prompt to the OpenRouter API and returns the model's response.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": """Act as a highly knowledgeable data security analyst AI. 
                    Provide concise, practical, and actionable insights with a focus on real-world applicability,
                    prioritizing clarity and precision in responses."""},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[LLM Error]: {str(e)}"

