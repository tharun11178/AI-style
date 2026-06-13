from __future__ import annotations

from typing import Any

from .recommendation_engine import build_recommendations


def match_outfits(recommendations: dict[str, Any]) -> list[str]:
    return list(recommendations.get("outfits", []))


def recommend_outfits_for_profile(
    *,
    face_shape: str,
    skin_tone: str,
    contrast_level: str,
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
    return match_outfits(recommendations)


def score_outfit_match(outfit: str, occasion: str, profession: str) -> dict[str, Any]:
    text = outfit.lower()
    score = 70
    if occasion and occasion.lower() in text:
        score += 10
    if profession and profession.lower() in text:
        score += 8
    if any(word in text for word in ["tailored", "structured", "clean"]):
        score += 7
    return {"outfit": outfit, "score": min(score, 98)}
