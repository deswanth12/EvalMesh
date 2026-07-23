import time
from typing import Dict

class CostAndLoopCircuitBreaker:
    """
    Prevents runaway token bills and infinite agent loops.
    """

    def __init__(self, max_messages_per_session: int = 25, max_estimated_tokens: int = 16000):
        self.max_messages = max_messages_per_session
        self.max_tokens = max_estimated_tokens
        # Session state storage (In-memory, replaceable with Redis)
        self.session_tracker: Dict[str, Dict[str, Any]] = {}

    def validate_session(self, session_id: str, messages: list) -> tuple[bool, str]:
        """
        Validates message length, depth, and estimated token count.
        """
        num_messages = len(messages)
        if num_messages > self.max_messages:
            return False, f"Agent Loop Guard: Message count ({num_messages}) exceeded limit ({self.max_messages})."

        # Rough token estimator (1 word ~ 1.33 tokens)
        total_words = sum(len(str(m.get("content", "")).split()) for m in messages if isinstance(m, dict))
        estimated_tokens = int(total_words * 1.33)

        if estimated_tokens > self.max_tokens:
            return False, f"Token Budget Exceeded: Estimated tokens ({estimated_tokens}) exceeded session limit ({self.max_tokens})."

        return True, ""
