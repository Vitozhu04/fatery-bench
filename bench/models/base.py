"""Base model client interface."""

import os
from abc import ABC, abstractmethod


SYSTEM_PROMPT = (
    "你是一位精通中国传统命理学的专家，包括八字命理、紫微斗数等。"
    "请根据给定的信息进行分析和回答。"
)


class ModelClient(ABC):
    """Abstract base class for LLM model clients."""

    DEFAULT_TEMPERATURE = 0.0
    DEFAULT_MAX_TOKENS = 4096

    def __init__(self, model_name: str, api_key: str | None = None):
        self.model_name = model_name
        self.api_key = api_key or self._get_api_key()

    @abstractmethod
    def _get_api_key(self) -> str:
        """Get API key from environment."""

    @abstractmethod
    def generate(self, prompt: str, system: str = SYSTEM_PROMPT) -> str:
        """Generate a response. Returns the text content."""

    def _env_key(self, *names: str) -> str:
        for name in names:
            if val := os.getenv(name):
                return val
        raise ValueError(
            f"API key not found. Set one of: {', '.join(names)}"
        )
