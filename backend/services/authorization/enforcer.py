from typing import List, Dict, Any, Optional

ROLE_SCOPES_MAP: Dict[str, List[str]] = {
    "Super Admin": [
        "chat:read", "chat:write", "evaluate:run", "dataset:write",
        "apikey:create", "apikey:delete", "deploy:execute", "deploy:rollback",
        "organization:invite", "billing:manage", "admin:all"
    ],
    "Admin": [
        "chat:read", "chat:write", "evaluate:run", "dataset:write",
        "apikey:create", "deploy:execute", "organization:invite"
    ],
    "Evaluator": [
        "chat:read", "evaluate:run", "dataset:write"
    ],
    "Developer": [
        "chat:read", "chat:write", "evaluate:run"
    ],
    "Viewer": [
        "chat:read"
    ]
}

from fastapi import HTTPException, Header, Depends

class ScopeAuthorizationEnforcer:
    """
    Scope-Based Authorization Enforcer.
    Evaluates required scopes (e.g. 'deploy:execute', 'chat:write') against user roles or token scopes.
    """
    @staticmethod
    def check_permission(role_or_scopes: Any, required_scope: str) -> bool:
        if isinstance(role_or_scopes, str):
            granted_scopes = ROLE_SCOPES_MAP.get(role_or_scopes, ["chat:read"])
        elif isinstance(role_or_scopes, list):
            granted_scopes = role_or_scopes
        else:
            granted_scopes = ["chat:read"]

        if "admin:all" in granted_scopes:
            return True
        return required_scope in granted_scopes

authz_enforcer = ScopeAuthorizationEnforcer()

def require_scope(required_scope: str):
    """
    Reusable FastAPI Dependency for Scope-Based Authorization.
    Enforces required permission scope automatically before route execution.
    """
    async def scope_checker(x_user_role: Optional[str] = Header("developer")):
        if not authz_enforcer.check_permission(x_user_role, required_scope):
            raise HTTPException(status_code=403, detail=f"Access Denied: Missing required scope '{required_scope}'")
        return True
    return scope_checker

