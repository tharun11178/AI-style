from __future__ import annotations

import json
import sqlite3
from typing import Any

from fastapi import Form, UploadFile

from ..utils.file_handler import save_upload_bytes
from ..utils.image_utils import read_valid_image
from ..utils.response_handler import now_iso
from ml_models.face_shape_classifier import analyze_image_bytes
from ml_models.recommendation_engine import build_recommendations


async def analyze_face_upload(
    *,
    image: UploadFile,
    favorite_style: str = Form("Smart casual"),
    profession: str = Form("Student"),
    occasion: str = Form("Everyday"),
    wellness_focus: str = Form("Energy"),
    user: dict[str, Any],
    db: sqlite3.Connection,
) -> dict[str, Any]:
    contents = await read_valid_image(image)
    analysis_result = analyze_image_bytes(contents, user["email"])
    image_name = save_upload_bytes(contents, image.filename)

    recommendations = build_recommendations(
        face_shape=analysis_result["face_shape"],
        skin_tone=analysis_result["skin_tone"],
        contrast_level=analysis_result["contrast_level"],
        favorite_style=favorite_style,
        profession=profession,
        occasion=occasion,
        wellness_focus=wellness_focus,
    )

    db.execute(
        """
        UPDATE users
        SET favorite_style = ?, profession = ?, occasion_preference = ?, wellness_focus = ?
        WHERE id = ?
        """,
        (favorite_style, profession, occasion, wellness_focus, user["id"]),
    )
    cursor = db.execute(
        """
        INSERT INTO analyses (
            user_id, image_name, face_shape, skin_tone, symmetry_score,
            jawline_score, contrast_level, recommendations_json, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user["id"],
            image_name,
            analysis_result["face_shape"],
            analysis_result["skin_tone"],
            analysis_result["symmetry_score"],
            analysis_result["jawline_score"],
            analysis_result["contrast_level"],
            json.dumps(recommendations),
            now_iso(),
        ),
    )
    db.execute(
        """
        INSERT INTO recommendation_history (user_id, analysis_id, recommendations_json, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (user["id"], cursor.lastrowid, json.dumps(recommendations), now_iso()),
    )
    db.commit()

    analysis = {
        "id": cursor.lastrowid,
        "face_shape": analysis_result["face_shape"],
        "skin_tone": analysis_result["skin_tone"],
        "symmetry_score": analysis_result["symmetry_score"],
        "jawline_score": analysis_result["jawline_score"],
        "contrast_level": analysis_result["contrast_level"],
        "face_region": analysis_result.get("face_region"),
        "landmark_count": analysis_result.get("landmark_count"),
        "landmark_metrics": analysis_result.get("landmark_metrics"),
        "color_metrics": analysis_result.get("color_metrics"),
        "model_source": analysis_result.get("model_source"),
        "created_at": now_iso(),
    }
    return {"analysis": analysis, "recommendations": recommendations}
