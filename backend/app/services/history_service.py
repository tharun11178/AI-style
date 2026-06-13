from __future__ import annotations

import json
import sqlite3
from typing import Any

from fastapi import HTTPException

from ..schemas.recommendation_schema import FeedbackRequest
from ..utils.response_handler import now_iso


def get_history(db: sqlite3.Connection, user: dict[str, Any]) -> list[dict[str, Any]]:
    rows = db.execute(
        """
        SELECT *
        FROM analyses
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 30
        """,
        (user["id"],),
    ).fetchall()
    return [
        {
            "id": row["id"],
            "face_shape": row["face_shape"],
            "skin_tone": row["skin_tone"],
            "symmetry_score": row["symmetry_score"],
            "jawline_score": row["jawline_score"],
            "contrast_level": row["contrast_level"],
            "recommendations": json.loads(row["recommendations_json"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def delete_history_item(db: sqlite3.Connection, user: dict[str, Any], analysis_id: int) -> dict[str, str]:
    db.execute("DELETE FROM analyses WHERE id = ? AND user_id = ?", (analysis_id, user["id"]))
    db.commit()
    return {"status": "deleted"}


def save_feedback(db: sqlite3.Connection, user_id: int, payload: FeedbackRequest) -> dict[str, str]:
    comments = payload.comments.strip()
    if len(comments) < 3:
        raise HTTPException(status_code=400, detail="Feedback comment is too short")

    db.execute(
        "INSERT INTO feedback (user_id, rating, comments, created_at) VALUES (?, ?, ?, ?)",
        (user_id, payload.rating, comments, now_iso()),
    )
    db.commit()
    return {"status": "received"}
