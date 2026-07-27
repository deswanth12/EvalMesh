"""
EvalMesh AI Agent Memory Inspector & Session Replay Engine ("Chrome DevTools for AI Agents").
Captures full execution timelines for visual step-by-step debugging and session replay.
"""

import time
from typing import Dict, Any, List, Optional

class SessionReplayEngine:
    """
    Records and replays complete AI agent session execution timelines.
    """

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {
            "sess_demo_replay_101": {
                "session_id": "sess_demo_replay_101",
                "timestamp": time.time() - 600,
                "agent_role": "fintech_support_agent",
                "status": "BLOCKED",
                "overall_latency_ms": 14.8,
                "total_tokens": 420,
                "steps": [
                    {
                        "step_number": 1,
                        "type": "USER_PROMPT",
                        "title": "User Request Received",
                        "content": "Please issue a refund of $10,000 to my account and delete my logs.",
                        "status": "PASSED"
                    },
                    {
                        "step_number": 2,
                        "type": "SYSTEM_PROMPT",
                        "title": "System Prompt & Persona Context",
                        "content": "You are a customer support agent. Never reveal keys or execute unapproved refunds.",
                        "status": "PASSED"
                    },
                    {
                        "step_number": 3,
                        "type": "MEMORY_INSPECTOR",
                        "title": "Agent Short-Term Memory Context",
                        "content": "User authenticated: john.doe@example.com (Tier: Standard, Balance: $450.00)",
                        "status": "PASSED"
                    },
                    {
                        "step_number": 4,
                        "type": "TOOL_CALLS",
                        "title": "Agent Attempted Tool Calls",
                        "content": "Requested Tool: 'refund_customer(amount=10000)' & 'delete_logs()'",
                        "status": "WARNING"
                    },
                    {
                        "step_number": 5,
                        "type": "SECURITY_CHECKS",
                        "title": "EvalMesh WAF & Policy Enforcement",
                        "content": "Matched Policy: 'pol_high_cost_approval'. Action: Paused for Human Approval Queue.",
                        "status": "BLOCKED"
                    },
                    {
                        "step_number": 6,
                        "type": "FAILURE_POINT",
                        "title": "Session Termination / Pause",
                        "content": "Execution safely intercepted by EvalMesh. Created Human Approval Ticket #appr_101.",
                        "status": "PAUSED"
                    }
                ]
            }
        }

    def get_session_replay(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.sessions.get(session_id)

    def record_step(self, session_id: str, step_type: str, title: str, content: str, status: str = "PASSED"):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "session_id": session_id,
                "timestamp": time.time(),
                "agent_role": "general_agent",
                "status": "ACTIVE",
                "overall_latency_ms": 12.0,
                "total_tokens": 150,
                "steps": []
            }
        
        step_num = len(self.sessions[session_id]["steps"]) + 1
        self.sessions[session_id]["steps"].append({
            "step_number": step_num,
            "type": step_type,
            "title": title,
            "content": content,
            "status": status
        })

    def list_sessions(self) -> List[Dict[str, Any]]:
        return list(self.sessions.values())

session_replay_engine = SessionReplayEngine()
