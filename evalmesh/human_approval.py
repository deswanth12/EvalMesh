"""
EvalMesh Human Approval Workflows Engine.
Pauses high-risk or high-cost agent actions and requests manual human approval.
"""

import time
from typing import Dict, Any, List, Optional

class HumanApprovalManager:
    """
    Manages pending human approval queues for high-stakes enterprise AI operations.
    """

    def __init__(self):
        self.pending_requests: Dict[str, Dict[str, Any]] = {
            "appr_101": {
                "id": "appr_101",
                "session_id": "sess_fin_881",
                "action": "Refund Customer $10,000.00 USD",
                "agent_role": "billing_support_agent",
                "reason": "Financial threshold exceeded ($10,000 > $500 max limit)",
                "status": "PENDING",
                "created_at": time.time() - 300,
                "resolved_at": None,
                "resolved_by": None
            },
            "appr_102": {
                "id": "appr_102",
                "session_id": "sess_hr_994",
                "action": "Execute SQL TRUNCATE TABLE employee_payroll",
                "agent_role": "hr_payroll_bot",
                "reason": "Destructive DDL SQL statement requested",
                "status": "PENDING",
                "created_at": time.time() - 120,
                "resolved_at": None,
                "resolved_by": None
            }
        }

    def request_approval(self, session_id: str, action: str, agent_role: str, reason: str) -> Dict[str, Any]:
        req_id = f"appr_{int(time.time()*1000)}"
        item = {
            "id": req_id,
            "session_id": session_id,
            "action": action,
            "agent_role": agent_role,
            "reason": reason,
            "status": "PENDING",
            "created_at": time.time(),
            "resolved_at": None,
            "resolved_by": None
        }
        self.pending_requests[req_id] = item
        return item

    def resolve_approval(self, req_id: str, decision: str, admin_email: str) -> Optional[Dict[str, Any]]:
        """Resolves request as APPROVED or REJECTED."""
        if req_id in self.pending_requests:
            item = self.pending_requests[req_id]
            item["status"] = decision.upper() # APPROVED or REJECTED
            item["resolved_at"] = time.time()
            item["resolved_by"] = admin_email
            return item
        return None

    def list_pending(self) -> List[Dict[str, Any]]:
        return [v for v in self.pending_requests.values() if v["status"] == "PENDING"]

    def list_all(self) -> List[Dict[str, Any]]:
        return list(self.pending_requests.values())

human_approval_engine = HumanApprovalManager()
