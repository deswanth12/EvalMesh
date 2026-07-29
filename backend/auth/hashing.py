import hashlib
import os

class PasswordHasher:
    """
    Secure Password Hashing Utility.
    Uses SHA-256 with per-user salt for hashing and verification.
    """
    @staticmethod
    def hash_password(password: str) -> str:
        salt = os.urandom(16).hex()
        pwd_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return f"{salt}${pwd_hash}"

    @staticmethod
    def verify_password(plain_password: str, stored_hash: str) -> bool:
        try:
            salt, original_hash = stored_hash.split("$")
            calc_hash = hashlib.sha256((plain_password + salt).encode('utf-8')).hexdigest()
            return calc_hash == original_hash
        except Exception:
            return False

hasher = PasswordHasher()
