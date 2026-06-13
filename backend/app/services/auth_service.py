from __future__ import annotations

import sqlite3
from typing import Any

from fastapi import Depends, Header, HTTPException

from ..database import get_db
from ..models.user_model import row_to_user
from ..schemas.auth_schema import LoginRequest, RegisterRequest
from ..utils.jwt_handler import create_session, hash_password, verify_password
from ..utils.response_handler import now_iso


def register_user(payload: RegisterRequest, db: sqlite3.Connection) -> dict[str, Any]:
    name = payload.name.strip()
    email = payload.email.strip().lower()
    password = payload.password

    if len(name) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Enter a valid email address")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    try:
        cursor = db.execute(
            """
            INSERT INTO users (name, email, password_hash, role, created_at)
            VALUES (?, ?, ?, 'user', ?)
            """,
            (name, email, hash_password(password), now_iso()),
        )
        db.commit()
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Email already registered") from exc

    token = create_session(db, cursor.lastrowid)
    user = db.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return {"token": token, "user": row_to_user(user)}


def login_user(payload: LoginRequest, db: sqlite3.Connection) -> dict[str, Any]:
    email = payload.email.strip().lower()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_session(db, user["id"])
    return {"token": token, "user": row_to_user(user)}


def logout_token(authorization: str | None, db: sqlite3.Connection) -> dict[str, str]:
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        db.execute("DELETE FROM sessions WHERE token = ?", (token,))
        db.commit()
    return {"status": "signed_out"}


def require_user(
    authorization: str | None = Header(default=None),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing authentication token")

    token = authorization.split(" ", 1)[1].strip()
    row = db.execute(
        """
        SELECT users.*
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.token = ?
        """,
        (token,),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return row_to_user(row)


def require_admin(user: dict[str, Any] = Depends(require_user)) -> dict[str, Any]:
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
