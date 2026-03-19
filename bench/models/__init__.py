"""Model adapters for FateryBench."""

from bench.models.base import ModelClient
from bench.models.google import GeminiClient
from bench.models.openai_client import OpenAIClient
from bench.models.anthropic_client import AnthropicClient
from bench.models.deepseek import DeepSeekClient

MODEL_REGISTRY: dict[str, type[ModelClient]] = {
    "gemini-2.5-flash": GeminiClient,
    "gemini-2.5-pro": GeminiClient,
    "gpt-4o": OpenAIClient,
    "gpt-4o-mini": OpenAIClient,
    "claude-sonnet-4": AnthropicClient,
    "deepseek-chat": DeepSeekClient,
}


def create_client(model_name: str) -> ModelClient:
    """Create a model client by name."""
    for key, cls in MODEL_REGISTRY.items():
        if key in model_name or model_name in key:
            return cls(model_name=model_name)
    raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_REGISTRY.keys())}")
