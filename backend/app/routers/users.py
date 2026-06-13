from __future__ import annotations

import sqlite3
from typing import Any

from fastapi import APIRouter, Depends

from ..database import get_db
from ..models.user_model import row_to_user
from ..schemas.user_schema import ProfileUpdate
from ..services.auth_service import require_user


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/profile")
def get_profile(user: dict[str, Any] = Depends(require_user)) -> dict[str, Any]:
    return user


@router.put("/profile")
def update_profile(
    payload: ProfileUpdate,
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any]:
    fields = {
        "name": (payload.name or user["name"]).strip() or user["name"],
        "favorite_style": (payload.favorite_style or user["favorite_style"] or "Smart casual").strip(),
        "profession": (payload.profession or user["profession"] or "Student").strip(),
        "occasion_preference": (payload.occasion_preference or user["occasion_preference"] or "Everyday").strip(),
        "wellness_focus": (payload.wellness_focus or user["wellness_focus"] or "Energy").strip(),
    }
    db.execute(
        """
        UPDATE users
        SET name = ?, favorite_style = ?, profession = ?, occasion_preference = ?, wellness_focus = ?
        WHERE id = ?
        """,
        (
            fields["name"],
            fields["favorite_style"],
            fields["profession"],
            fields["occasion_preference"],
            fields["wellness_focus"],
            user["id"],
        ),
    )
    db.commit()
    updated = db.execute("SELECT * FROM users WHERE id = ?", (user["id"],)).fetchone()
    return row_to_user(updated)
