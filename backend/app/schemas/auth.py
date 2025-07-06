"""
Authentication schemas for API serialization.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """Password change request schema."""
    current_password: str
    new_password: str