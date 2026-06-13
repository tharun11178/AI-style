from __future__ import annotations

import sqlite3
from typing import Any

from fastapi import APIRouter, Depends, Header

from ..database import get_db
from ..schemas.auth_schema import LoginRequest, RegisterRequest
from ..services.auth_service import login_user, logout_token, register_user, require_user


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: sqlite3.Connection = Depends(get_db)) -> dict[str, Any]:
    return register_user(payload, db)


@router.post("/login")
def login(payload: LoginRequest, db: sqlite3.Connection = Depends(get_db)) -> dict[str, Any]:
    return login_user(payload, db)


@router.get("/me")
def me(user: dict[str, Any] = Depends(require_user)) -> dict[str, Any]:
    return user


@router.post("/logout")
def logout(
    authorization: str | None = Header(default=None),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, str]:
    return logout_token(authorization, db)
