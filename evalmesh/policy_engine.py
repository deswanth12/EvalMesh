"""
EvalMesh Declarative Policy Engine.
Allows organizations to define custom dynamic security & governance policies.
"""

from typing import Dict, Any, List, Optional

class DeclarativePolicyEngine:
    """
    Evaluates dynamic, rule-based policies against incoming LLM requests and agent tool calls.
    """

    def __init__(self):
        self.policies = [
            {
                "id": "pol_intern_restriction",
                "name": "Restrict Intern Role Tools",
                "condition": lambda ctx: ctx.get("role") == "intern" and "delete_database" in ctx.get("requested_tools", []),
                "action": "BLOCK",
                "reason": "Intern role is prohibited from executing 'delete_database' tool."
            },
            {
                "id": "pol_high_cost_approval",
                "name": "Require Human Approval for High-Cost Actions",
                "condition": lambda ctx: ctx.get("estimated_cost_usd", 0.0) > 0.50 or ctx.get("action_type") == "refund_large_amount",
                "action": "REQUIRE_HUMAN_APPROVAL",
                "reason": "Request cost exceeds $0.50 threshold or involves high-value financial refund."
            },
            {
                "id": "pol_pci_redact",
                "name": "Enforce Mandatory PCI Card Redaction",
                "condition": lambda ctx: "credit_card" in ctx.get("detected_pii", []),
                "action": "REDACT_PCI",
                "reason": "PCI-DSS compliance: Credit card detected in request payload."
            }
        ]

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates context against registered policies.
        Returns evaluation outcome dictionary.
        """
        triggered_policies = []
        final_action = "ALLOW"
        reason = "All security policies satisfied."

        for pol in self.policies:
            try:
                if pol["condition"](context):
                    triggered_policies.append(pol)
                    if pol["action"] == "BLOCK":
                        final_action = "BLOCK"
                        reason = pol["reason"]
                        break
                    elif pol["action"] == "REQUIRE_HUMAN_APPROVAL":
                        final_action = "REQUIRE_HUMAN_APPROVAL"
                        reason = pol["reason"]
                    elif pol["action"] == "REDACT_PCI" and final_action != "BLOCK":
                        final_action = "REDACT_PCI"
                        reason = pol["reason"]
            except Exception:
                continue

        return {
            "action": final_action,
            "reason": reason,
            "triggered_policies": [p["id"] for p in triggered_policies]
        }

    def list_policies(self) -> List[Dict[str, Any]]:
        return [
            {"id": p["id"], "name": p["name"], "action": p["action"], "reason": p["reason"]}
            for p in self.policies
        ]

policy_engine = DeclarativePolicyEngine()
