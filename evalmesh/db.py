import sqlite3
import os
import json
import time
from typing import Dict, Any, List

class EvalMeshDatabase:
    """
    Persistent SQLite Database Engine for EvalMesh.
    Stores telemetry, blocked injections, PII redactions, and prompt performance.
    """

    def __init__(self, db_path: str = "evalmesh.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    session_id TEXT,
                    agent_role TEXT,
                    prompt_version TEXT,
                    model TEXT,
                    latency_ms REAL,
                    status_code INTEGER,
                    blocked_reason TEXT,
                    redactions_count INTEGER,
                    raw_payload TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_type TEXT, -- PII or INJECTION
                    pattern_name TEXT,
                    pattern_regex TEXT,
                    is_active INTEGER DEFAULT 1
                )
            """)
            conn.commit()

    def log_request(
        self,
        session_id: str,
        agent_role: str,
        prompt_version: str,
        model: str,
        latency_ms: float,
        status_code: int,
        blocked_reason: str = None,
        redactions_count: int = 0,
        payload_meta: dict = None
    ):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO telemetry_logs 
                (timestamp, session_id, agent_role, prompt_version, model, latency_ms, status_code, blocked_reason, redactions_count, raw_payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                time.time(),
                session_id,
                agent_role,
                prompt_version,
                model,
                latency_ms,
                status_code,
                blocked_reason,
                redactions_count,
                json.dumps(payload_meta or {})
            ))
            conn.commit()

    def get_summary_analytics() -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM telemetry_logs")
            total_reqs = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE status_code = 403")
            total_blocked = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(redactions_count) FROM telemetry_logs")
            total_redactions = cursor.fetchone()[0] or 0

            cursor.execute("SELECT AVG(latency_ms) FROM telemetry_logs WHERE status_code = 200")
            avg_latency = cursor.fetchone()[0] or 0.0

            return {
                "total_requests": total_reqs,
                "total_blocked_injections": total_blocked,
                "total_pii_redacted": total_redactions,
                "avg_latency_ms": round(avg_latency, 2),
                "estimated_savings_usd": round(total_blocked * 12.50, 2) # Est $12.50 per prevented breach/loop
            }

    def get_recent_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, timestamp, session_id, agent_role, prompt_version, model, latency_ms, status_code, blocked_reason, redactions_count 
                FROM telemetry_logs 
                ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
