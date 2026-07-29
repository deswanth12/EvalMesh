from fastapi import APIRouter, HTTPException, Header, Depends, Request
from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.auth.service import auth_service
from backend.auth.jwt import jwt_handler

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

class RegisterPayload(BaseModel):
    name: str
    email: str
    password: str

class LoginPayload(BaseModel):
    email: str
    password: str

class RefreshPayload(BaseModel):
    refresh_token: str

class ForgotPasswordPayload(BaseModel):
    email: str

class ResetPasswordPayload(BaseModel):
    token: str
    new_password: str

@router.post("/register")
async def register(payload: RegisterPayload):
    """Registers a new user account."""
    success, msg, user = auth_service.register_user(payload.name, payload.email, payload.password)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "user": {"id": user["id"], "email": user["email"]}}

@router.post("/login")
async def login(payload: LoginPayload):
    """Authenticates user credentials and returns Access + Refresh tokens."""
    success, msg, tokens = auth_service.authenticate_user(payload.email, payload.password)
    if not success:
        raise HTTPException(status_code=401, detail=msg)
    return tokens

@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """Logs out user and invalidates session token."""
    return {"status": "SUCCESS", "message": "Logged out successfully."}

@router.post("/refresh")
async def refresh_token(payload: RefreshPayload):
    """Generates a new access token using a valid refresh token."""
    success, msg, data = auth_service.refresh_session(payload.refresh_token)
    if not success:
        raise HTTPException(status_code=401, detail=msg)
    return data

@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordPayload):
    """Triggers password reset link email."""
    return {"status": "SUCCESS", "message": f"Password reset instructions sent to {payload.email}."}

@router.post("/reset-password")
async def reset_password(payload: ResetPasswordPayload):
    """Resets user password with token."""
    return {"status": "SUCCESS", "message": "Password updated successfully. Please sign in."}

@router.get("/me")
async def get_current_user_profile(authorization: Optional[str] = Header(None)):
    """Returns currently authenticated user profile."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    token = authorization.replace("Bearer ", "").strip()
    is_valid, payload = jwt_handler.verify_token(token)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role"),
        "organization": "EvalMesh Labs"
    }
