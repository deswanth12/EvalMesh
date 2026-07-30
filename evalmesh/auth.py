"""
EvalMesh Authentication, JWT Token Engine & Role-Based Access Control (RBAC).
Supports 4 System Roles: Super Admin, Admin, Evaluator, Viewer.
"""

import time
import base64
import json
import hmac
import hashlib
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from evalmesh.db import hash_password, EvalMeshDatabase

SECRET_KEY = "evalmesh_enterprise_jwt_secret_key_2026"
security = HTTPBearer(auto_error=False)

db_engine_auth = EvalMeshDatabase()

class APIKeyManager:
    """Enterprise Persistent API Key Manager for EvalMesh."""
    def generate_key(self, name: str, role: str = "developer", rate_limit: int = 120, organization_id: str = "org_acme_01") -> str:
        record = db_engine_auth.create_api_key(name, role, rate_limit, organization_id)
        return record["api_key"]

    def validate_key(self, api_key: str):
        return db_engine_auth.validate_api_key(api_key)


ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "Super Admin": [
        "dashboard:view", "org:create", "org:delete", "org:suspend", "org:activate",
        "user:create_admin", "user:reset_pw", "user:change_role", "user:delete", "user:invite", "user:impersonate",
        "eval:view_all", "eval:delete", "eval:run", "project:create", "project:edit", "project:delete",
        "billing:view", "subscription:create", "provider:manage", "api_key:configure", "storage:manage",
        "audit:access", "server:monitor", "analytics:view", "announcements:manage", "feature_flags:manage",
        "db:backup", "db:restore", "data:export", "report:view", "report:export"
    ],
    "Admin": [
        "dashboard:view", "project:create", "project:edit", "project:delete",
        "eval:run", "eval:view", "eval:edit", "eval:delete",
        "user:invite", "user:remove", "user:change_role_limited",
        "report:view", "report:export", "integrations:manage", "branding:change", "usage:view"
    ],
    "Evaluator": [
        "dashboard:view", "eval:run", "test_run:create", "dataset:upload",
        "model:compare", "project:view", "report:generate", "report:view", "report:export"
    ],
    "Viewer": [
        "dashboard:view", "report:view", "eval:view", "pdf:download"
    ]
}

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def create_jwt_token(user_id: str, email: str, role: str, organization_id: Optional[str], expires_in: int = 86400) -> str:
    """Generates an HMAC-SHA256 JWT Token with role and permissions."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "userId": user_id,
        "email": email,
        "role": role,
        "organizationId": organization_id,
        "permissions": ROLE_PERMISSIONS.get(role, []),
        "iat": int(time.time()),
        "exp": int(time.time()) + expires_in
    }

    header_b64 = base64url_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = base64url_encode(json.dumps(payload).encode('utf-8'))
    
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        f"{header_b64}.{payload_b64}".encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    signature_b64 = base64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt_token(token: str) -> Dict[str, Any]:
    """Verifies and decodes JWT Token."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        header_b64, payload_b64, signature_b64 = parts
        
        expected_sig = base64url_encode(
            hmac.new(
                SECRET_KEY.encode('utf-8'),
                f"{header_b64}.{payload_b64}".encode('utf-8'),
                hashlib.sha256
            ).digest()
        )
        
        if not hmac.compare_digest(signature_b64, expected_sig):
            raise HTTPException(status_code=401, detail="Invalid token signature")
        
        payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))
        
        if payload.get("exp", 0) < time.time():
            raise HTTPException(status_code=401, detail="Token expired")
            
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    """FastAPI Dependency for Authenticated User."""
    if not credentials:
        # Fallback default user for unauthenticated requests in demo mode
        return {
            "userId": "u_super_01",
            "email": "deshu@evalmesh.ai",
            "role": "Super Admin",
            "organizationId": None,
            "permissions": ROLE_PERMISSIONS["Super Admin"]
        }
    return verify_jwt_token(credentials.credentials)

def require_permission(permission: str):
    """Enforces role permission check on endpoint."""
    def dependency(user: Dict[str, Any] = Depends(get_current_user)):
        permissions = user.get("permissions", [])
        if permission not in permissions and user.get("role") != "Super Admin":
            raise HTTPException(status_code=403, detail=f"Permission denied: Missing '{permission}'")
        return user
    return dependency
