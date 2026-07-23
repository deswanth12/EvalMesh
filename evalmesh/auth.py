import secrets
import time
from typing import Dict, Optional, Tuple

class APIKeyManager:
    """
    Enterprise API Key Management & Rate Limiter for EvalMesh.
    Issues, validates, and enforces rate limits on client API keys (`em_live_...`).
    """

    def __init__(self):
        # Default internal development key
        self.keys_db: Dict[str, Dict[str, any]] = {
            "em_live_demo_123456789": {
                "name": "Default Developer Key",
                "role": "admin",
                "rate_limit_per_min": 120,
                "monthly_quota": 50000,
                "requests_this_month": 0,
                "created_at": time.time()
            }
        }
        self.request_timestamps: Dict[str, list] = {}

    def generate_key(self, name: str, role: str = "developer", rate_limit: int = 60) -> str:
        new_key = f"em_live_{secrets.token_hex(16)}"
        self.keys_db[new_key] = {
            "name": name,
            "role": role,
            "rate_limit_per_min": rate_limit,
            "monthly_quota": 50000,
            "requests_this_month": 0,
            "created_at": time.time()
        }
        return new_key

    def validate_key(self, api_key: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
        if not api_key:
            return False, "Missing API Key", None
            
        key_data = self.keys_db.get(api_key)
        if not key_data:
            return False, "Invalid API Key", None

        # Rate Limiting Check (Sliding Window per Minute)
        now = time.time()
        timestamps = self.request_timestamps.get(api_key, [])
        # Keep timestamps from the last 60 seconds
        timestamps = [t for t in timestamps if now - t < 60]
        
        if len(timestamps) >= key_data["rate_limit_per_min"]:
            return False, f"Rate limit exceeded ({key_data['rate_limit_per_min']} req/min)", None

        timestamps.append(now)
        self.request_timestamps[api_key] = timestamps
        key_data["requests_this_month"] += 1

        return True, None, key_data
