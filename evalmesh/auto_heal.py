import json
from typing import Dict, Any, Tuple, Optional

class AutoHealingRetryEngine:
    """
    Autonomous Self-Correction Engine.
    Intercepts failed or malformed LLM responses (e.g. invalid JSON, missing schema keys)
    and constructs micro-retry prompts to heal outputs transparently before returning to client.
    """

    @classmethod
    def validate_and_heal_json(cls, response_content: str, required_keys: Optional[list] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Validates whether response is valid JSON and contains required schema keys.
        If invalid, returns healing instruction prompt for micro-retry.
        """
        if not response_content or not isinstance(response_content, str):
            return False, "Response payload is empty.", None

        try:
            parsed = json.loads(response_content)
        except Exception as e:
            healing_prompt = (
                f"SYSTEM CORRECTION: Your previous output was not valid JSON. Error: {str(e)}. "
                "Please output ONLY valid JSON format with proper quotes and commas."
            )
            return False, healing_prompt, None

        if required_keys:
            missing_keys = [k for k in required_keys if k not in parsed]
            if missing_keys:
                healing_prompt = (
                    f"SYSTEM CORRECTION: Your JSON output is missing required fields: {missing_keys}. "
                    f"Please return the full JSON object including keys: {required_keys}."
                )
                return False, healing_prompt, parsed

        return True, "Valid JSON Payload", parsed
