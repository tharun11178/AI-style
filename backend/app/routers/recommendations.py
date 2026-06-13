from __future__ import annotations

import sqlite3
from typing import Any

from fastapi import APIRouter, Depends

from ..database import get_db
from ..schemas.recommendation_schema import FeedbackRequest
from ..services.auth_service import require_user
from ..services.history_service import save_feedback
from ..services.recommendation_service import color_recommendations, hairstyle_recommendations, outfit_recommendations


router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/recommend/hairstyle")
def recommend_hairstyle(
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any]:
    return hairstyle_recommendations(db, user)


@router.get("/recommend/outfits")
def recommend_outfits(
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any]:
    return outfit_recommendations(db, user)


@router.get("/recommend/colors")
def recommend_colors(
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any]:
    return color_recommendations(db, user)


@router.post("/feedback")
def add_feedback_short_path(
    payload: FeedbackRequest,
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, str]:
    return save_feedback(db, user["id"], payload)


@router.post("/feedback/add")
def add_feedback(
    payload: FeedbackRequest,
    user: dict[str, Any] = Depends(require_user),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, str]:
    return save_feedback(db, user["id"], payload)
