from __future__ import annotations

from pydantic import BaseModel

from .user_schema import UserOut


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str
    user: UserOut
