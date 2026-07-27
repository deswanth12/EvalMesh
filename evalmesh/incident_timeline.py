"""
EvalMesh Incident Timeline Logger Stream.
Captures GitHub-style chronological incident event timelines for operations teams.
"""

import time
from typing import Dict, Any, List

class IncidentTimelineLogger:
    """
    Tracks and formats chronological security and operational events.
    """

    def __init__(self):
        now = time.time()
        self.events: List[Dict[str, Any]] = [
            {"time_offset": "2:15 PM", "timestamp": now - 300, "event": "Prompt Injection Blocked", "tag": "WAF_BLOCK", "severity": "HIGH"},
            {"time_offset": "2:16 PM", "timestamp": now - 240, "event": "Agent Loop Detected (Message Depth 26)", "tag": "LOOP_DETECTED", "severity": "MEDIUM"},
            {"time_offset": "2:17 PM", "timestamp": now - 180, "event": "Cost Circuit Breaker Tripped (Session Halted)", "tag": "CIRCUIT_BREAKER", "severity": "HIGH"},
            {"time_offset": "2:18 PM", "timestamp": now - 120, "event": "System Recovered & Returned 200 OK", "tag": "RECOVERED", "severity": "LOW"}
        ]

    def log_incident(self, event: str, tag: str, severity: str = "MEDIUM"):
        t_str = time.strftime("%I:%M %p")
        self.events.insert(0, {
            "time_offset": t_str,
            "timestamp": time.time(),
            "event": event,
            "tag": tag,
            "severity": severity
        })

    def get_timeline(self) -> List[Dict[str, Any]]:
        return self.events

incident_timeline_logger = IncidentTimelineLogger()
