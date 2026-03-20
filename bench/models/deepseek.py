"""DeepSeek model client (OpenAI-compatible API).

Supports both deepseek-chat and deepseek-reasoner (thinking model).
The reasoner model does not support temperature or system messages.
"""

import time

import httpx
from openai import OpenAI

from bench.models.base import ModelClient, SYSTEM_PROMPT

_MAX_RETRIES = 3
_RETRY_DELAY = 5  # seconds


class DeepSeekClient(ModelClient):

    def _get_api_key(self) -> str:
        return self._env_key("DEEPSEEK_API_KEY")

    @property
    def _is_reasoner(self) -> bool:
        return "reasoner" in self.model_name

    def generate(self, prompt: str, system: str = SYSTEM_PROMPT) -> str:
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com",
            timeout=httpx.Timeout(300, connect=30),
        )

        if self._is_reasoner:
            messages = [{"role": "user", "content": f"{system}\n\n{prompt}"}]
            kwargs: dict = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.DEFAULT_MAX_TOKENS,
            }
        else:
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ]
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.DEFAULT_TEMPERATURE,
                "max_tokens": self.DEFAULT_MAX_TOKENS,
            }

        for attempt in range(_MAX_RETRIES):
            try:
                response = client.chat.completions.create(**kwargs)
                return response.choices[0].message.content or ""
            except Exception:
                if attempt == _MAX_RETRIES - 1:
                    raise
                time.sleep(_RETRY_DELAY * (attempt + 1))
