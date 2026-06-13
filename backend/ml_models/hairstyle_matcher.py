from __future__ import annotations

from typing import Any

from .recommendation_engine import build_recommendations


def match_hairstyles(recommendations: dict[str, Any]) -> list[str]:
    return list(recommendations.get("hairstyles", []))


def recommend_hairstyles_for_profile(
    *,
    face_shape: str,
    skin_tone: str = "Warm neutral",
    contrast_level: str = "Medium",
    favorite_style: str = "Smart casual",
    profession: str = "Student",
    occasion: str = "Everyday",
    wellness_focus: str = "Energy",
) -> list[str]:
    recommendations = build_recommendations(
        face_shape=face_shape,
        skin_tone=skin_tone,
        contrast_level=contrast_level,
        favorite_style=favorite_style,
        profession=profession,
        occasion=occasion,
        wellness_focus=wellness_focus,
    )
    return match_hairstyles(recommendations)


def score_hairstyle_match(style_name: str, face_shape: str, contrast_level: str) -> dict[str, Any]:
    score = 72
    text = style_name.lower()
    if face_shape.lower() in text:
        score += 8
    if contrast_level == "High" and any(word in text for word in ["textured", "quiff", "crop"]):
        score += 7
    if contrast_level == "Low" and any(word in text for word in ["soft", "layered", "waves"]):
        score += 7
    return {"hairstyle": style_name, "score": min(score, 98)}
