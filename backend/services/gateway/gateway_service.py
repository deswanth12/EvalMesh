import time
from typing import Dict, Any, Tuple

class GatewayService:
    """
    Decoupled Gateway Service.
    Handles entry routing, request validation, rate limiting, and reverse proxy forwarding.
    """
    def __init__(self):
        self.gateway_version = "v1.0.0"
        self.status = "HEALTHY"

    def validate_request_payload(self, body: Dict[str, Any]) -> Tuple[bool, str]:
        if not isinstance(body, dict):
            return False, "Payload must be a JSON object"
        if "messages" in body and not isinstance(body["messages"], list):
            return False, "'messages' field must be an array"
        return True, "Payload valid"

gateway_service = GatewayService()
