import time
import json
import base64
import hmac
import hashlib
from typing import Dict, Any, Tuple

import os

SECRET_KEY = os.getenv("EVALMESH_JWT_SECRET_KEY", "evalmesh_jwt_secret_key_production_2026_fallback")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("EVALMESH_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("EVALMESH_REFRESH_TOKEN_EXPIRE_DAYS", "7"))


class JWTHandler:
    """
    HMAC-SHA256 JWT Token Handler.
    Generates and verifies access and refresh tokens.
    """
    @staticmethod
    def create_access_token(user_id: str, email: str, role: str) -> str:
        payload = {
            "sub": user_id,
            "email": email,
            "role": role,
            "type": "access",
            "exp": time.time() + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        }
        return JWTHandler._encode(payload)

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": time.time() + (REFRESH_TOKEN_EXPIRE_DAYS * 86400)
        }
        return JWTHandler._encode(payload)

    @staticmethod
    def verify_token(token: str) -> Tuple[bool, Dict[str, Any]]:
        try:
            payload = JWTHandler._decode(token)
            if payload.get("exp", 0) < time.time():
                return False, {"error": "Token expired"}
            return True, payload
        except Exception as e:
            return False, {"error": str(e)}

    @staticmethod
    def _encode(payload: Dict[str, Any]) -> str:
        header = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode('utf-8')).decode('utf-8').rstrip('=')
        body = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').rstrip('=')
        sig = hmac.new(SECRET_KEY.encode('utf-8'), f"{header}.{body}".encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(sig).decode('utf-8').rstrip('=')
        return f"{header}.{body}.{signature}"

    @staticmethod
    def _decode(token: str) -> Dict[str, Any]:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT format")
        header, body, signature = parts
        # Re-compute expected signature and verify with constant-time comparison
        expected_sig = hmac.new(
            SECRET_KEY.encode('utf-8'),
            f"{header}.{body}".encode('utf-8'),
            hashlib.sha256
        ).digest()
        expected_signature = base64.b64encode(expected_sig).decode('utf-8').rstrip('=')
        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError("Invalid JWT signature")
        padding = "=" * (4 - len(body) % 4)
        body_bytes = base64.b64decode(body + padding)
        return json.loads(body_bytes.decode('utf-8'))


jwt_handler = JWTHandler()
