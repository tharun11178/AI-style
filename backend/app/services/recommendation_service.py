from __future__ import annotations

import json
import sqlite3
from typing import Any

from ml_models.recommendation_engine import build_recommendations


def latest_recommendations(db: sqlite3.Connection, user: dict[str, Any]) -> dict[str, Any]:
    row = db.execute(
        """
        SELECT recommendations_json
        FROM analyses
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],),
    ).fetchone()
    if row:
        return json.loads(row["recommendations_json"])

    return build_recommendations(
        face_shape="Oval",
        skin_tone="Warm neutral",
        contrast_level="Medium",
        favorite_style=user.get("favorite_style") or "Smart casual",
        profession=user.get("profession") or "Student",
        occasion=user.get("occasion_preference") or "Everyday",
        wellness_focus=user.get("wellness_focus") or "Energy",
    )


def hairstyle_recommendations(db: sqlite3.Connection, user: dict[str, Any]) -> dict[str, Any]:
    recommendations = latest_recommendations(db, user)
    return {
        "hairstyles": recommendations["hairstyles"],
        "beard": recommendations["beard"],
        "source": "latest_analysis",
    }


def outfit_recommendations(db: sqlite3.Connection, user: dict[str, Any]) -> dict[str, Any]:
    recommendations = latest_recommendations(db, user)
    return {
        "outfits": recommendations["outfits"],
        "accessories": recommendations["accessories"],
    }


def color_recommendations(db: sqlite3.Connection, user: dict[str, Any]) -> dict[str, Any]:
    recommendations = latest_recommendations(db, user)
    return {"palette": recommendations["palette"]}
