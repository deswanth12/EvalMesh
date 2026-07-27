import sqlite3
import os
import json
import time
import hashlib
from typing import Dict, Any, List, Optional

def hash_password(password: str) -> str:
    """Hashes password securely with SHA-256 and salt."""
    return hashlib.sha256(f"evalmesh_salt_{password}".encode('utf-8')).hexdigest()

class EvalMeshDatabase:
    """
    Persistent Multi-Tenant SQLite Database Engine for EvalMesh.
    Supports Organizations, Users, RBAC, Projects, Evaluations, Subscriptions, Audit Logs & Telemetry.
    """

    def __init__(self, db_path: str = "evalmesh.db"):
        self.db_path = db_path
        self._init_db()
        self._seed_default_data()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Telemetry Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    session_id TEXT,
                    organization_id TEXT DEFAULT 'org_acme_01',
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
            try:
                cursor.execute("ALTER TABLE telemetry_logs ADD COLUMN organization_id TEXT DEFAULT 'org_acme_01'")
            except sqlite3.OperationalError:
                pass


            # Custom WAF & DLP Rules
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_type TEXT,
                    pattern_name TEXT,
                    pattern_regex TEXT,
                    is_active INTEGER DEFAULT 1
                )
            """)

            # Organizations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS organizations (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    logo TEXT,
                    plan TEXT DEFAULT 'Enterprise',
                    status TEXT DEFAULT 'Active', -- Active, Suspended, Archived
                    storage_limit_mb INTEGER DEFAULT 50000,
                    created_at REAL
                )
            """)

            # Users Table (RBAC Roles: Super Admin, Admin, Evaluator, Viewer)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL, -- Super Admin, Admin, Evaluator, Viewer
                    organization_id TEXT,
                    status TEXT DEFAULT 'Active', -- Active, Suspended
                    created_at REAL,
                    updated_at REAL,
                    FOREIGN KEY (organization_id) REFERENCES organizations(id)
                )
            """)

            # Projects Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    organization_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    owner_id TEXT NOT NULL,
                    status TEXT DEFAULT 'Active',
                    created_at REAL,
                    FOREIGN KEY (organization_id) REFERENCES organizations(id)
                )
            """)

            # Evaluations Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    organization_id TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    score REAL,
                    status TEXT DEFAULT 'Passed', -- Passed, Failed, Running
                    model_name TEXT,
                    created_at REAL,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            """)

            # Subscriptions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id TEXT PRIMARY KEY,
                    organization_id TEXT NOT NULL,
                    plan_name TEXT NOT NULL,
                    price_usd REAL NOT NULL,
                    billing_cycle TEXT DEFAULT 'Monthly',
                    status TEXT DEFAULT 'Active',
                    created_at REAL
                )
            """)

            # Audit Logs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    organization_id TEXT,
                    actor_email TEXT NOT NULL,
                    action TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    ip_address TEXT DEFAULT '127.0.0.1',
                    timestamp REAL
                )
            """)

            conn.commit()

    def _seed_default_data(self):
        """Seeds default multi-tenant organizations, users, projects, and evals."""
        now = time.time()
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Seed Organizations
            cursor.execute("SELECT COUNT(*) as count FROM organizations")
            if cursor.fetchone()["count"] == 0:
                cursor.execute("""
                    INSERT INTO organizations (id, name, logo, plan, status, storage_limit_mb, created_at)
                    VALUES 
                    ('org_acme_01', 'Acme Corp', '🏢', 'Enterprise', 'Active', 50000, ?),
                    ('org_stark_02', 'Stark Industries', '⚡', 'Team', 'Active', 20000, ?),
                    ('org_cyber_03', 'Cyberdyne Systems', '🤖', 'Pro', 'Suspended', 10000, ?)
                """, (now, now, now))

            # Seed Users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            if cursor.fetchone()["count"] == 0:
                pw_super = hash_password("SuperAdmin123!")
                pw_admin = hash_password("Admin123!")
                pw_eval = hash_password("Evaluator123!")
                pw_viewer = hash_password("Viewer123!")
                pw_stark = hash_password("Stark123!")

                cursor.execute("""
                    INSERT INTO users (id, name, email, password_hash, role, organization_id, status, created_at, updated_at)
                    VALUES 
                    ('u_super_01', 'Deshu (Super Admin)', 'deshu@evalmesh.ai', ?, 'Super Admin', NULL, 'Active', ?, ?),
                    ('u_admin_01', 'John (Acme Admin)', 'john@acme.com', ?, 'Admin', 'org_acme_01', 'Active', ?, ?),
                    ('u_eval_01', 'Sarah (Acme Evaluator)', 'eval@acme.com', ?, 'Evaluator', 'org_acme_01', 'Active', ?, ?),
                    ('u_viewer_01', 'Alice (Acme Viewer)', 'alice@acme.com', ?, 'Viewer', 'org_acme_01', 'Active', ?, ?),
                    ('u_stark_01', 'Tony Stark', 'admin@stark.com', ?, 'Admin', 'org_stark_02', 'Active', ?, ?)
                """, (pw_super, now, now, pw_admin, now, now, pw_eval, now, now, pw_viewer, now, now, pw_stark, now, now))

            # Seed Projects
            cursor.execute("SELECT COUNT(*) as count FROM projects")
            if cursor.fetchone()["count"] == 0:
                cursor.execute("""
                    INSERT INTO projects (id, organization_id, name, description, owner_id, status, created_at)
                    VALUES
                    ('proj_acme_customer_support', 'org_acme_01', 'Customer Support Bot Guardrails', 'WAF & DLP rules for live chat agent', 'u_admin_01', 'Active', ?),
                    ('proj_acme_fintech_eval', 'org_acme_01', 'Fintech Model Drift Evaluation', 'Continuous schema validation for financial LLM', 'u_eval_01', 'Active', ?),
                    ('proj_stark_jarvis_sec', 'org_stark_02', 'JARVIS Security Mesh', 'Defense network AI guardrails', 'u_stark_01', 'Active', ?)
                """, (now, now, now))

            # Seed Evals
            cursor.execute("SELECT COUNT(*) as count FROM evaluations")
            if cursor.fetchone()["count"] == 0:
                cursor.execute("""
                    INSERT INTO evaluations (id, project_id, organization_id, created_by, score, status, model_name, created_at)
                    VALUES
                    ('eval_101', 'proj_acme_customer_support', 'org_acme_01', 'u_eval_01', 98.4, 'Passed', 'gpt-4o', ?),
                    ('eval_102', 'proj_acme_fintech_eval', 'org_acme_01', 'u_eval_01', 94.2, 'Passed', 'claude-3-5-sonnet', ?),
                    ('eval_103', 'proj_stark_jarvis_sec', 'org_stark_02', 'u_stark_01', 99.9, 'Passed', 'gpt-4o-mini', ?)
                """, (now, now, now))

            conn.commit()

    # --- USER AUTH & PROFILES ---
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_all_users(self, organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if organization_id:
                cursor.execute("SELECT id, name, email, role, organization_id, status, created_at FROM users WHERE organization_id = ?", (organization_id,))
            else:
                cursor.execute("SELECT id, name, email, role, organization_id, status, created_at FROM users")
            return [dict(row) for row in cursor.fetchall()]

    def create_user(self, name: str, email: str, password: str, role: str, organization_id: Optional[str]) -> Dict[str, Any]:
        now = time.time()
        user_id = f"u_{int(now*1000)}"
        hashed_pw = hash_password(password)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (id, name, email, password_hash, role, organization_id, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 'Active', ?, ?)
            """, (user_id, name, email, hashed_pw, role, organization_id, now, now))
            conn.commit()
        return {"id": user_id, "name": name, "email": email, "role": role, "organization_id": organization_id}

    def update_user_role(self, user_id: str, role: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET role = ?, updated_at = ? WHERE id = ?", (role, time.time(), user_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, user_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    # --- ORGANIZATIONS ---
    def list_organizations(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, COUNT(u.id) as user_count 
                FROM organizations o 
                LEFT JOIN users u ON o.id = u.organization_id 
                GROUP BY o.id
            """)
            return [dict(row) for row in cursor.fetchall()]

    def get_organization(self, org_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM organizations WHERE id = ?", (org_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create_organization(self, name: str, plan: str = "Enterprise") -> Dict[str, Any]:
        now = time.time()
        org_id = f"org_{name.lower().replace(' ', '_')}_{int(now%10000)}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO organizations (id, name, logo, plan, status, storage_limit_mb, created_at)
                VALUES (?, ?, '🏢', ?, 'Active', 50000, ?)
            """, (org_id, name, plan, now))
            conn.commit()
        return {"id": org_id, "name": name, "plan": plan, "status": "Active"}

    def update_org_status(self, org_id: str, status: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE organizations SET status = ? WHERE id = ?", (status, org_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_organization(self, org_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE organization_id = ?", (org_id,))
            cursor.execute("DELETE FROM projects WHERE organization_id = ?", (org_id,))
            cursor.execute("DELETE FROM evaluations WHERE organization_id = ?", (org_id,))
            cursor.execute("DELETE FROM organizations WHERE id = ?", (org_id,))
            conn.commit()
            return True

    # --- PROJECTS ---
    def list_projects(self, organization_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE organization_id = ? ORDER BY id DESC", (organization_id,))
            return [dict(row) for row in cursor.fetchall()]

    def create_project(self, organization_id: str, name: str, description: str, owner_id: str) -> Dict[str, Any]:
        now = time.time()
        proj_id = f"proj_{int(now*1000)}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (id, organization_id, name, description, owner_id, status, created_at)
                VALUES (?, ?, ?, ?, ?, 'Active', ?)
            """, (proj_id, organization_id, name, description, owner_id, now))
            conn.commit()
        return {"id": proj_id, "organization_id": organization_id, "name": name, "description": description}

    # --- EVALUATIONS ---
    def list_evaluations(self, organization_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM evaluations WHERE organization_id = ? ORDER BY id DESC", (organization_id,))
            return [dict(row) for row in cursor.fetchall()]

    def create_evaluation(self, project_id: str, organization_id: str, created_by: str, score: float, status: str, model_name: str) -> Dict[str, Any]:
        now = time.time()
        eval_id = f"eval_{int(now*1000)}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO evaluations (id, project_id, organization_id, created_by, score, status, model_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (eval_id, project_id, organization_id, created_by, score, status, model_name, now))
            conn.commit()
        return {"id": eval_id, "project_id": project_id, "score": score, "status": status}

    # --- AUDIT LOGS ---
    def log_audit(self, organization_id: Optional[str], actor_email: str, action: str, resource: str, ip_address: str = "127.0.0.1"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_logs (organization_id, actor_email, action, resource, ip_address, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (organization_id, actor_email, action, resource, ip_address, time.time()))
            conn.commit()

    def get_audit_logs(self, organization_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if organization_id:
                cursor.execute("SELECT * FROM audit_logs WHERE organization_id = ? ORDER BY id DESC LIMIT ?", (organization_id, limit))
            else:
                cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    # --- TELEMETRY ---
    def log_request(self, session_id: str, agent_role: str, prompt_version: str, model: str, latency_ms: float, status_code: int, blocked_reason: str = None, redactions_count: int = 0, payload_meta: dict = None, organization_id: str = "org_acme_01"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO telemetry_logs 
                (timestamp, session_id, organization_id, agent_role, prompt_version, model, latency_ms, status_code, blocked_reason, redactions_count, raw_payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (time.time(), session_id, organization_id, agent_role, prompt_version, model, latency_ms, status_code, blocked_reason, redactions_count, json.dumps(payload_meta or {})))
            conn.commit()

    def get_summary_analytics(self, organization_id: Optional[str] = None) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if organization_id:
                cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE organization_id = ?", (organization_id,))
                total_reqs = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE organization_id = ? AND status_code = 403", (organization_id,))
                total_blocked = cursor.fetchone()[0]
                cursor.execute("SELECT SUM(redactions_count) FROM telemetry_logs WHERE organization_id = ?", (organization_id,))
                total_redactions = cursor.fetchone()[0] or 0
                cursor.execute("SELECT AVG(latency_ms) FROM telemetry_logs WHERE organization_id = ? AND status_code = 200", (organization_id,))
                avg_latency = cursor.fetchone()[0] or 0.0
            else:
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
                "estimated_savings_usd": round(total_blocked * 12.50, 2)
            }

    def get_recent_logs(self, limit: int = 20, organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if organization_id:
                cursor.execute("""
                    SELECT id, timestamp, session_id, organization_id, agent_role, prompt_version, model, latency_ms, status_code, blocked_reason, redactions_count 
                    FROM telemetry_logs WHERE organization_id = ?
                    ORDER BY id DESC LIMIT ?
                """, (organization_id, limit))
            else:
                cursor.execute("""
                    SELECT id, timestamp, session_id, organization_id, agent_role, prompt_version, model, latency_ms, status_code, blocked_reason, redactions_count 
                    FROM telemetry_logs 
                    ORDER BY id DESC LIMIT ?
                """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
