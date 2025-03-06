import os
from typing import List, Optional

from langchain_core.language_models import LLM
from together import Together


class TogetherLLM(LLM):
    model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"
    api_key: Optional[str] = os.getenv("TOGETHER_AI_API_KEY")

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Send a prompt to TogetherAI and return the response."""
        client = Together(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        return "together_ai"