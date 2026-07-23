import re
from typing import Dict, List, Tuple

class CustomRulesEngine:
    """
    Dynamic Rules Engine for custom enterprise DLP patterns and security signatures.
    Allows developers to define custom project secrets or confidential terms.
    """

    def __init__(self):
        self.custom_pii_rules: Dict[str, str] = {
            "SECRET_KEY": r"(?i)api[_-]?key\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?",
            "INTERNAL_PROJECT": r"\bPROJECT_[A-Z0-9_]{3,}\b"
        }

    def add_pii_rule(self, name: str, regex_pattern: str):
        self.custom_pii_rules[name] = regex_pattern

    def scan_custom_rules(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        if not text or not isinstance(text, str):
            return text, []

        matches_found = []
        sanitized = text

        for name, pattern in self.custom_pii_rules.items():
            matches = re.finditer(pattern, sanitized)
            for match in matches:
                val = match.group(0)
                placeholder = f"[REDACTED_{name}]"
                sanitized = sanitized.replace(val, placeholder)
                matches_found.append({
                    "rule": name,
                    "placeholder": placeholder
                })

        return sanitized, matches_found
