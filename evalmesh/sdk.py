import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

class EvalMeshClient:
    """
    Python Client SDK for EvalMesh.
    Allows developers to route OpenAI API calls through EvalMesh with custom metadata.
    """

    def __init__(self, proxy_url: str = "http://localhost:8000", api_key: str = "mock_key"):
        self.base_url = proxy_url.rstrip("/")
        self.proxy_url = self.base_url
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

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req) as resp:
                res_body = resp.read().decode("utf-8")
                return json.loads(res_body)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            try:
                return json.loads(err_body)
            except Exception:
                raise Exception(f"EvalMesh API Error [{e.code}]: {err_body}")
