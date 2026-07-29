import uuid
import time
from typing import Dict, Any, Tuple, Optional
from backend.auth.hashing import hasher
from backend.auth.jwt import jwt_handler

class AuthService:
    """
    User Authentication & Session Management Service.
    Handles Registration, Login, Token Refresh, Password Reset, and OAuth Stubs.
    """
    def __init__(self):
        # In-Memory Storage (backed by PostgreSQL in production)
        self._users: Dict[str, Dict[str, Any]] = {
            "admin@evalmesh.io": {
                "id": "usr_superadmin_101",
                "name": "Deswanth",
                "email": "admin@evalmesh.io",
                "password_hash": hasher.hash_password("evalmesh2026!"),
                "email_verified": True,
                "role": "Super Admin",
                "organization_id": "org_evalmesh_labs"
            }
        }
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._failed_attempts: Dict[str, int] = {}
        self._lockout_until: Dict[str, float] = {}

    def register_user(self, name: str, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        clean_email = email.strip().lower()
        if clean_email in self._users:
            return False, "Email already registered.", None
        
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        user = {
            "id": user_id,
            "name": name,
            "email": clean_email,
            "password_hash": hasher.hash_password(password),
            "email_verified": False,
            "role": "developer",
            "organization_id": "org_evalmesh_labs"
        }
        self._users[clean_email] = user
        return True, "User registered successfully.", user

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        clean_email = email.strip().lower()
        now = time.time()

        # Check Account Lockout
        if clean_email in self._lockout_until:
            if now < self._lockout_until[clean_email]:
                remaining = int(self._lockout_until[clean_email] - now)
                return False, f"Account locked due to 5 consecutive failed attempts. Try again in {remaining} seconds.", None
            else:
                # Lockout expired
                del self._lockout_until[clean_email]
                self._failed_attempts[clean_email] = 0

        user = self._users.get(clean_email)
        if not user or not hasher.verify_password(password, user["password_hash"]):
            # Track failed attempt
            fails = self._failed_attempts.get(clean_email, 0) + 1
            self._failed_attempts[clean_email] = fails
            if fails >= 5:
                self._lockout_until[clean_email] = now + 900  # Lockout for 15 minutes (900s)
                return False, "Account locked due to 5 consecutive failed attempts. Try again in 15 minutes.", None
            return False, "Invalid email or password.", None

        # Reset failed attempts on successful login
        self._failed_attempts[clean_email] = 0
        self._lockout_until.pop(clean_email, None)

        access_token = jwt_handler.create_access_token(user["id"], user["email"], user["role"])
        refresh_token = jwt_handler.create_refresh_token(user["id"])
        
        self._sessions[user["id"]] = {
            "refresh_token": refresh_token,
            "created_at": now
        }


        return True, "Authentication successful.", {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "organization": "EvalMesh Labs"
            }
        }

    def refresh_session(self, refresh_token: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        is_valid, payload = jwt_handler.verify_token(refresh_token)
        if not is_valid:
            return False, "Invalid or expired refresh token.", None
        
        user_id = payload.get("sub")
        user = next((u for u in self._users.values() if u["id"] == user_id), None)
        if not user:
            return False, "User not found.", None

        new_access_token = jwt_handler.create_access_token(user["id"], user["email"], user["role"])
        return True, "Token refreshed successfully.", {
            "access_token": new_access_token,
            "token_type": "Bearer"
        }

auth_service = AuthService()
