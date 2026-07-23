from typing import List, Dict, Any, Optional

class PromptInjectionFirewall:
    """
    WAF for AI Agents: Blocks jailbreak attempts, system prompt overrides, 
    and malicious injection patterns.
    """
    
    INJECTION_SIGNATURES = [
        "ignore previous instructions",
        "ignore all prior prompts",
        "system prompt override",
        "you are now dan",
        "do anything now",
        "bypass safety filter",
        "reveal your system prompt",
        "repeat the text above",
        "jailbreak active"
    ]

    @classmethod
    def check_injection(cls, text: str) -> Optional[str]:
        if not text or not isinstance(text, str):
            return None
            
        lowered = text.lower()
        for signature in cls.INJECTION_SIGNATURES:
            if signature in lowered:
                return signature
        return None


class ToolRBACEnforcer:
    """
    Role-Based Access Control for AI Agent Tool Execution.
    Ensures agents cannot invoke functions outside their explicit permissions.
    """
    
    DEFAULT_PERMISSIONS = {
        "support_agent": ["search_faq", "create_ticket", "fetch_order_status"],
        "developer_agent": ["read_repo", "run_unit_tests", "create_pull_request"],
        "admin_agent": ["*"] # Full access
    }

    def __init__(self, custom_permissions: Optional[Dict[str, List[str]]] = None):
        self.permissions = custom_permissions or self.DEFAULT_PERMISSIONS

    def authorize_tools(self, role: str, requested_tools: List[Dict[str, Any]]) -> List[str]:
        """
        Validates tool definitions against role policy.
        Returns a list of unauthorized tool names if any violation occurs.
        """
        allowed = self.permissions.get(role, [])
        if "*" in allowed:
            return [] # Admin has full access
            
        violations = []
        for tool in requested_tools:
            tool_name = tool.get("function", {}).get("name") or tool.get("name")
            if tool_name and tool_name not in allowed:
                violations.append(tool_name)
                
        return violations
