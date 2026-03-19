"""Anthropic Claude model client."""

import anthropic

from bench.models.base import ModelClient, SYSTEM_PROMPT


class AnthropicClient(ModelClient):

    def _get_api_key(self) -> str:
        return self._env_key("ANTHROPIC_API_KEY")

    def generate(self, prompt: str, system: str = SYSTEM_PROMPT) -> str:
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model_name,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.DEFAULT_TEMPERATURE,
            max_tokens=self.DEFAULT_MAX_TOKENS,
        )
        return response.content[0].text
