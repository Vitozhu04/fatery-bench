"""OpenAI model client."""

from openai import OpenAI

from bench.models.base import ModelClient, SYSTEM_PROMPT

# Models that don't support temperature=0 or max_completion_tokens
_CHAT_ONLY_MODELS = {"gpt-5.3-chat-latest"}


class OpenAIClient(ModelClient):

    def _get_api_key(self) -> str:
        return self._env_key("OPENAI_API_KEY")

    def generate(self, prompt: str, system: str = SYSTEM_PROMPT) -> str:
        client = OpenAI(api_key=self.api_key)

        kwargs: dict = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }

        if self.model_name in _CHAT_ONLY_MODELS:
            # Chat-only models: no temperature control
            kwargs["max_completion_tokens"] = self.DEFAULT_MAX_TOKENS
        else:
            kwargs["temperature"] = self.DEFAULT_TEMPERATURE
            kwargs["max_completion_tokens"] = self.DEFAULT_MAX_TOKENS

        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""
