import time
import jwt
from typing import Optional, Dict, Any
from backend.core.config import settings

def create_access_token(data: dict, expires_delta_seconds: Optional[int] = None) -> str:
    to_encode = data.copy()
    now = time.time()
    expire = now + (expires_delta_seconds or (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60))
    to_encode.update({"iat": now, "exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception:
        return None
