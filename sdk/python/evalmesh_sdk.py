import httpx
from typing import List, Dict, Any, Optional

class EvalMeshClient:
    """
    Official Standalone EvalMesh Python Client SDK.
    Provides sub-15ms proxy routing, WAF firewall protection, and live telemetry tracking.
    """
    def __init__(self, proxy_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.proxy_url = proxy_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def get_health(self) -> Dict[str, Any]:
        with httpx.Client() as client:
            res = client.get(f"{self.proxy_url}/health", headers=self.headers)
            return res.json()

    def get_reliability_score(self) -> Dict[str, Any]:
        with httpx.Client() as client:
            res = client.get(f"{self.proxy_url}/api/reliability", headers=self.headers)
            return res.json()

    def create_chat_completion(self, messages: List[Dict[str, str]], agent_role: str = "support_agent", model: str = "gpt-4o") -> Dict[str, Any]:
        headers = {**self.headers, "x-evalmesh-agent-role": agent_role}
        payload = {"model": model, "messages": messages}
        with httpx.Client() as client:
            res = client.post(f"{self.proxy_url}/v1/chat/completions", json=payload, headers=headers)
            return res.json()
