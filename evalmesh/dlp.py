import re
from typing import Dict, List, Tuple

class PIIDLPScanner:
    """
    Data Loss Prevention (DLP) & PII Redaction Engine.
    Scans prompt payloads before forwarding to third-party LLMs.
    """
    
    PATTERNS: Dict[str, str] = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
        "PHONE": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    }

    def __init__(self, enabled_rules: List[str] = None):
        if enabled_rules:
            self.active_patterns = {k: v for k, v in self.PATTERNS.items() if k in enabled_rules}
        else:
            self.active_patterns = self.PATTERNS

    def sanitize(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Redacts PII tokens from input text and returns sanitized text along with redacted metadata logs.
        """
        if not text or not isinstance(text, str):
            return text, []
            
        redactions = []
        sanitized_text = text
        
        for pii_type, pattern in self.active_patterns.items():
            matches = re.finditer(pattern, sanitized_text)
            for match in matches:
                matched_val = match.group(0)
                placeholder = f"[REDACTED_{pii_type}]"
                sanitized_text = sanitized_text.replace(matched_val, placeholder)
                redactions.append({
                    "type": pii_type,
                    "original_length": len(matched_val),
                    "placeholder": placeholder
                })
                
        return sanitized_text, redactions
