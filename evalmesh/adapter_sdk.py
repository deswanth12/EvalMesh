"""
EvalMesh Custom Model Adapter SDK.
Provides a standard Base Adapter class so enterprise developers can connect any custom/self-hosted LLM to EvalMesh.
"""

from typing import Dict, Any, Optional

class CustomModelAdapter:
    """
    Base Adapter interface for plugging custom enterprise AI models into EvalMesh.
    """

    def __init__(self, model_name: str = "MyCompanyModel", endpoint_url: Optional[str] = None):
        self.model_name = model_name
        self.endpoint_url = endpoint_url or "http://localhost:11434" # e.g. Ollama or local vLLM

    def invoke(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Custom invocation method to be overridden by company implementation.
        """
        return {
            "model": self.model_name,
            "completion": f"[Custom Model Output from {self.model_name}]: Received '{prompt[:30]}...'",
            "latency_ms": 42.0,
            "tokens_used": len(prompt.split()) + 15
        }

class CustomModelAdapterRegistry:
    """
    Registry for managing custom company model adapters.
    """
    def __init__(self):
        self.adapters = {
            "MyCompanyModel": CustomModelAdapter(model_name="MyCompanyModel")
        }

    def register_adapter(self, name: str, endpoint: str):
        self.adapters[name] = CustomModelAdapter(model_name=name, endpoint_url=endpoint)

    def list_adapters(self) -> list:
        return [
            {"model_name": k, "endpoint_url": v.endpoint_url}
            for k, v in self.adapters.items()
        ]

custom_adapter_registry = CustomModelAdapterRegistry()
