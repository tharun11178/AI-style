from __future__ import annotations

import sqlite3
from typing import Any

from fastapi import APIRouter, Depends, File, Form, UploadFile

from ..database import get_db
from ..services.auth_service import require_user
from ..services.face_service import analyze_face_upload
from ..services.history_service import delete_history_item, get_history


router = APIRouter(tags=["analysis"])


@router.post("/api/analyze-face")
async def analyze_face(
    image: UploadFile = File(...),
    favorite_style: str = Form("Smart casual"),
    profession: str = Form("Student"),
    occasion: str = Form("Everyday"),
    wellness_focus: str = Form("Energy"),
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any]:
    return await analyze_face_upload(
        image=image,
        favorite_style=favorite_style,
        profession=profession,
        occasion=occasion,
        wellness_focus=wellness_focus,
        user=user,
        db=db,
    )


@router.get("/api/history")
def history(
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> list[dict[str, Any]]:
    return get_history(db, user)


@router.delete("/api/history/{analysis_id}")
def remove_history_item(
    analysis_id: int,
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, str]:
    return delete_history_item(db, user, analysis_id)
