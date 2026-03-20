"""DeepSeek model client (OpenAI-compatible API).

Supports both deepseek-chat and deepseek-reasoner (thinking model).
The reasoner model does not support temperature or system messages.
"""

from openai import OpenAI

from bench.models.base import ModelClient, SYSTEM_PROMPT


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
        )

        if self._is_reasoner:
            # Reasoner model: no system message, no temperature
            messages = [{"role": "user", "content": f"{system}\n\n{prompt}"}]
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.DEFAULT_MAX_TOKENS,
            )
        else:
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ]
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.DEFAULT_TEMPERATURE,
                max_tokens=self.DEFAULT_MAX_TOKENS,
            )

        return response.choices[0].message.content or ""
