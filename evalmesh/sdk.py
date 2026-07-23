from typing import Optional, Dict, Any
import requests

class EvalMeshClient:
    """
    Python Client SDK for EvalMesh.
    Allows developers to route OpenAI API calls through EvalMesh with custom metadata.
    """

    def __init__(self, proxy_url: str = "http://localhost:8000", api_key: str = "mock_key"):
        self.proxy_url = proxy_url.rstrip("/")
        self.api_key = api_key

    def create_chat_completion(
        self,
        messages: list,
        model: str = "gpt-4o",
        agent_role: str = "support_agent",
        prompt_version: str = "v1.0.0",
        tools: Optional[list] = None
    ) -> Dict[str, Any]:
        
        url = f"{self.proxy_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "x-evalmesh-agent-role": agent_role,
            "x-evalmesh-prompt-version": prompt_version
        }
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        if tools:
            payload["tools"] = tools

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"EvalMesh Error ({response.status_code}): {response.text}")
            
        return response.json()
