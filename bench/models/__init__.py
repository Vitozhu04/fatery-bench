"""Model adapters for FateryBench."""

from bench.models.base import ModelClient
from bench.models.google import GeminiClient
from bench.models.openai_client import OpenAIClient
from bench.models.deepseek import DeepSeekClient

MODEL_REGISTRY: dict[str, type[ModelClient]] = {
    "gemini-3-flash-preview": GeminiClient,
    "gemini-3-pro-preview": GeminiClient,
    "gemini-3.1-pro-preview": GeminiClient,
    "gemini-3.1-flash-lite-preview": GeminiClient,
    "gpt-5.4": OpenAIClient,
    "gpt-5.3-chat-latest": OpenAIClient,
    "deepseek-reasoner": DeepSeekClient,
    "deepseek-chat": DeepSeekClient,
}

# Fatery = gemini-3-flash-preview + fatery-enhanced prompt
FATERY_MODEL = "gemini-3-flash-preview"


def create_client(model_name: str) -> ModelClient:
    """Create a model client by name."""
    for key, cls in MODEL_REGISTRY.items():
        if key in model_name or model_name in key:
            return cls(model_name=model_name)
    raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_REGISTRY.keys())}")
