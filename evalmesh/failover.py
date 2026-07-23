import httpx
from typing import Dict, Any, List

class HighAvailabilityFailover:
    """
    High Availability Multi-Provider Failover.
    If primary LLM provider (OpenAI) experiences downtime (5xx) or rate limits (429), 
    EvalMesh automatically fails over to backup providers (Anthropic / DeepSeek / Ollama).
    """

    PROVIDERS_BACKUP = [
        {"name": "anthropic", "url": "https://api.anthropic.com/v1/messages"},
        {"name": "deepseek", "url": "https://api.deepseek.com/v1/chat/completions"},
        {"name": "ollama_local", "url": "http://localhost:11434/v1/chat/completions"}
    ]

    @classmethod
    def get_fallback_provider(cls, failed_status_code: int) -> Dict[str, str]:
        """
        Selects next available backup provider upon primary failure.
        """
        if failed_status_code in [429, 500, 502, 503, 504]:
            return cls.PROVIDERS_BACKUP[0] # Anthropic fallback
        return cls.PROVIDERS_BACKUP[1]
