from __future__ import annotations

import hashlib
from typing import Any

from .color_analysis import analyze_color_bytes
from .face_detection import detect_face_region

FACE_SHAPES = ["Oval", "Round", "Square", "Diamond", "Heart", "Rectangle"]


def analyze_image_bytes(image_bytes: bytes, user_email: str | None = None) -> dict[str, Any]:
    digest = hashlib.sha256(image_bytes).hexdigest()
    face_region = detect_face_region(image_bytes)
    color_result = analyze_color_bytes(image_bytes, digest)
    shape_index = int(digest[:8], 16) % len(FACE_SHAPES)
    face_shape = FACE_SHAPES[shape_index]
    symmetry = max(0.0, min(100.0, 80.0 + (int(digest[12:14], 16) % 21) - 10))
    jawline = max(0.0, min(100.0, 70.0 + (int(digest[14:16], 16) % 21) - 10))

    return {
        "face_shape": face_shape,
        "skin_tone": color_result["skin_tone"],
        "contrast_level": color_result["contrast_level"],
        "symmetry_score": round(symmetry, 2),
        "jawline_score": round(jawline, 2),
        "face_region": face_region,
        "landmark_count": 12,
        "landmark_metrics": {
            "width": face_region["width"],
            "height": face_region["height"],
            "confidence": face_region.get("confidence", 0.0),
        },
        "color_metrics": {
            "warmth_score": color_result.get("warmth_score"),
            "brightness_score": color_result.get("brightness_score"),
            "contrast_score": color_result.get("contrast_score"),
            "color_confidence": color_result.get("color_confidence"),
        },
        "model_source": "local-simulated-face-shape-v1",
    }
