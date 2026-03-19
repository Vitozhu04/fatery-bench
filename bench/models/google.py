"""Google Gemini model client."""

from google import genai
from google.genai import types

from bench.models.base import ModelClient, SYSTEM_PROMPT


class GeminiClient(ModelClient):

    def _get_api_key(self) -> str:
        return self._env_key("GOOGLE_API_KEY", "GEMINI_API_KEY")

    def generate(self, prompt: str, system: str = SYSTEM_PROMPT) -> str:
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=self.DEFAULT_TEMPERATURE,
                max_output_tokens=self.DEFAULT_MAX_TOKENS,
            ),
        )
        return response.text or ""
