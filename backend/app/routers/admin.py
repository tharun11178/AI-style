from __future__ import annotations

import sqlite3
from typing import Any

from fastapi import APIRouter, Depends

from ..database import get_db
from ..services.auth_service import require_admin
from ..utils.response_handler import now_iso
from ml_models.recommendation_engine import collect_ml_assets


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users")
def admin_users(
    admin: dict[str, Any] = Depends(require_admin),
    db: sqlite3.Connection = Depends(get_db),
) -> list[dict[str, Any]]:
    rows = db.execute(
        """
        SELECT
            users.id,
            users.name,
            users.email,
            users.role,
            users.favorite_style,
            users.profession,
            users.created_at,
            COUNT(analyses.id) AS analysis_count
        FROM users
        LEFT JOIN analyses ON analyses.user_id = users.id
        GROUP BY users.id
        ORDER BY users.created_at DESC
        """
    ).fetchall()
    db.execute(
        "INSERT INTO admin_logs (admin_id, action, details, created_at) VALUES (?, ?, ?, ?)",
        (admin["id"], "view_users", "Admin viewed user list", now_iso()),
    )
    db.commit()
    return [dict(row) for row in rows]


@router.get("/analytics")
def analytics(
    _: dict[str, Any] = Depends(require_admin),
    db: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any]:
    total_users = db.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
    total_analyses = db.execute("SELECT COUNT(*) AS count FROM analyses").fetchone()["count"]
    feedback_count = db.execute("SELECT COUNT(*) AS count FROM feedback").fetchone()["count"]
    shapes = db.execute(
        """
        SELECT face_shape, COUNT(*) AS count
        FROM analyses
        GROUP BY face_shape
        ORDER BY count DESC
        """
    ).fetchall()
    latest = db.execute(
        """
        SELECT analyses.id, users.name, analyses.face_shape, analyses.created_at
        FROM analyses
        JOIN users ON users.id = analyses.user_id
        ORDER BY analyses.id DESC
        LIMIT 8
        """
    ).fetchall()
    return {
        "total_users": total_users,
        "total_analyses": total_analyses,
        "feedback_count": feedback_count,
        "shape_distribution": [dict(row) for row in shapes],
        "latest_activity": [dict(row) for row in latest],
    }


@router.get("/ml-assets")
def ml_assets(_: dict[str, Any] = Depends(require_admin)) -> dict[str, Any]:
    return collect_ml_assets()
