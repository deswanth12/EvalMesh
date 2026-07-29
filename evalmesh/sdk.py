import json
import urllib.request
import urllib.error
import functools
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

class EvalMeshAgentGuardrail:
    """
    1-Line Guardrail Integration Wrapper for Agent Frameworks (LangGraph, CrewAI, AutoGen, LlamaIndex).
    Intercepts agent tool executions, validates RBAC policy, checks for prompt injection WAF, and enforces circuit breakers.
    """
    def __init__(self, client: Optional[EvalMeshClient] = None, agent_role: str = "support_agent"):
        self.client = client or EvalMeshClient()
        self.agent_role = agent_role
        self.step_counter = 0

    def evaluate_step(self, prompt: str, tool_name: Optional[str] = None) -> Dict[str, Any]:
        self.step_counter += 1
        if self.step_counter > 25:
            return {
                "allowed": False,
                "reason": "Runaway agent loop circuit breaker tripped (depth > 25)",
                "status_code": 429
            }
        
        lower_prompt = prompt.lower()
        if "ignore previous instructions" in lower_prompt or "system override" in lower_prompt:
            return {
                "allowed": False,
                "reason": "Blocked by Prompt Injection WAF Firewall",
                "status_code": 403
            }

        if tool_name and tool_name in ["delete_database", "drop_table", "purge_all"]:
            return {
                "allowed": False,
                "reason": f"Tool '{tool_name}' blocked by Tool RBAC policy for role '{self.agent_role}'",
                "status_code": 403
            }

        return {"allowed": True, "step": self.step_counter, "status_code": 200}

def guardrail(agent_role: str = "support_agent", max_depth: int = 25):
    """
    Decorator for python functions / agent nodes to enforce EvalMesh security guardrails.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            prompt = kwargs.get("prompt", args[0] if args else "")
            tool_name = kwargs.get("tool_name", None)
            
            inspector = EvalMeshAgentGuardrail(agent_role=agent_role)
            eval_res = inspector.evaluate_step(str(prompt), tool_name)
            
            if not eval_res["allowed"]:
                raise PermissionError(f"[EvalMesh Guardrail Blocked] {eval_res['reason']}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

