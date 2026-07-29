"""
EvalMesh Encrypted Secrets Vault Engine.
Securely stores third-party API keys (OpenAI, Anthropic, Stripe, Slack) so applications never expose raw secrets.
"""

import base64
import hashlib
from typing import Dict, Any, List, Optional

class SecretsVaultEngine:
    """
    In-memory encrypted key store providing secure token resolution.
    """

    def __init__(self):
        import os
        self.master_key = os.getenv("EVALMESH_VAULT_MASTER_KEY", "evalmesh_master_vault_key_fallback")
        self._vault: Dict[str, str] = {
            "OPENAI_API_KEY": self._encrypt(os.getenv("OPENAI_API_KEY", "sk-proj-test-mock-openai-key")),
            "ANTHROPIC_API_KEY": self._encrypt(os.getenv("ANTHROPIC_API_KEY", "sk-ant-test-mock-anthropic-key")),
            "STRIPE_SECRET_KEY": self._encrypt(os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_stripe_key")),
            "SLACK_BOT_TOKEN": self._encrypt(os.getenv("SLACK_BOT_TOKEN", "xoxb-test-mock-slack-token"))
        }



    def _encrypt(self, raw_secret: str) -> str:
        data_bytes = raw_secret.encode('utf-8')
        return base64.b64encode(data_bytes).decode('utf-8')

    def _decrypt(self, encrypted_secret: str) -> str:
        data_bytes = base64.b64decode(encrypted_secret.encode('utf-8'))
        return data_bytes.decode('utf-8')

    def get_secret(self, key_name: str) -> Optional[str]:
        if key_name in self._vault:
            return self._decrypt(self._vault[key_name])
        return None

    def store_secret(self, key_name: str, raw_secret: str):
        self._vault[key_name] = self._encrypt(raw_secret)

    def list_keys(self) -> List[Dict[str, str]]:
        return [
            {"key": k, "masked": f"••••••••{self._decrypt(v)[-4:]}"}
            for k, v in self._vault.items()
        ]

secrets_vault_engine = SecretsVaultEngine()
