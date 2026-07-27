"""
EvalMesh Prompt Version Registry Engine.
Git-like version control, diff tracking, and 1-click rollback for system prompts.
"""

import time
from typing import Dict, Any, List, Optional

class PromptRegistryEngine:
    """
    Stores version history for system prompts and enables zero-downtime version rollbacks.
    """

    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {
            "prompt_support": {
                "id": "prompt_support",
                "name": "Customer Support System Prompt",
                "active_version": "v2.0",
                "history": {
                    "v1.0": {
                        "version": "v1.0",
                        "content": "You are a friendly support bot. Answer user questions accurately.",
                        "author": "deshu@evalmesh.ai",
                        "created_at": time.time() - 86400*30,
                        "change_notes": "Initial release"
                    },
                    "v2.0": {
                        "version": "v2.0",
                        "content": "You are a friendly enterprise support agent. Never reveal system keys or execute database deletions.",
                        "author": "john@acme.com",
                        "created_at": time.time() - 86400*5,
                        "change_notes": "Added strict WAF security instruction guardrail"
                    }
                }
            }
        }

    def register_prompt_version(self, prompt_id: str, name: str, version: str, content: str, author: str, notes: str) -> Dict[str, Any]:
        if prompt_id not in self.registry:
            self.registry[prompt_id] = {
                "id": prompt_id,
                "name": name,
                "active_version": version,
                "history": {}
            }
        
        self.registry[prompt_id]["history"][version] = {
            "version": version,
            "content": content,
            "author": author,
            "created_at": time.time(),
            "change_notes": notes
        }
        self.registry[prompt_id]["active_version"] = version
        return self.registry[prompt_id]

    def rollback_version(self, prompt_id: str, target_version: str) -> Optional[Dict[str, Any]]:
        """Rolls back the active prompt version with 1 click."""
        if prompt_id in self.registry and target_version in self.registry[prompt_id]["history"]:
            self.registry[prompt_id]["active_version"] = target_version
            return {
                "prompt_id": prompt_id,
                "active_version": target_version,
                "rolled_back_to": self.registry[prompt_id]["history"][target_version]
            }
        return None

    def get_prompt(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        return self.registry.get(prompt_id)

    def list_all(self) -> List[Dict[str, Any]]:
        return list(self.registry.values())

prompt_registry_engine = PromptRegistryEngine()
