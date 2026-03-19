"""OpenAI model client."""

from openai import OpenAI

from bench.models.base import ModelClient, SYSTEM_PROMPT


class OpenAIClient(ModelClient):

    def _get_api_key(self) -> str:
        return self._env_key("OPENAI_API_KEY")

    def generate(self, prompt: str, system: str = SYSTEM_PROMPT) -> str:
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=self.DEFAULT_TEMPERATURE,
            max_tokens=self.DEFAULT_MAX_TOKENS,
        )
        return response.choices[0].message.content or ""
