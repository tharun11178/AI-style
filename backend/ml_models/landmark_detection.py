from __future__ import annotations

import hashlib
import math
from typing import Any

from .face_detection import detect_face_region


LANDMARK_TEMPLATE = {
    "forehead": (0.50, 0.08),
    "left_temple": (0.18, 0.24),
    "right_temple": (0.82, 0.24),
    "left_eye": (0.35, 0.34),
    "right_eye": (0.65, 0.34),
    "left_cheekbone": (0.25, 0.50),
    "right_cheekbone": (0.75, 0.50),
    "nose_tip": (0.50, 0.52),
    "left_jaw": (0.31, 0.76),
    "right_jaw": (0.69, 0.76),
    "mouth_center": (0.50, 0.69),
    "chin": (0.50, 0.93),
}


def _jitter(seed: str, index: int, span: float) -> float:
    value = int(seed[index : index + 2], 16)
    return ((value % 15) - 7) / 1000 * span


def _by_name(landmarks: list[dict[str, float]]) -> dict[str, dict[str, float]]:
    return {point["name"]: point for point in landmarks}


def _distance(first: dict[str, float], second: dict[str, float]) -> float:
    return math.dist((first["x"], first["y"]), (second["x"], second["y"]))


def extract_landmarks(
    image_bytes: bytes,
    face_region: dict[str, Any] | None = None,
) -> list[dict[str, float]]:
    region = face_region or detect_face_region(image_bytes)
    digest = hashlib.sha256(image_bytes[-8192:]).hexdigest()
    x = float(region["x"])
    y = float(region["y"])
    width = float(region["width"])
    height = float(region["height"])

    landmarks: list[dict[str, float]] = []
    for index, (name, (relative_x, relative_y)) in enumerate(LANDMARK_TEMPLATE.items()):
        point_x = x + (relative_x * width) + _jitter(digest, index * 2, width)
        point_y = y + (relative_y * height) + _jitter(digest, index * 2 + 1, height)
        landmarks.append({"name": name, "x": round(point_x, 2), "y": round(point_y, 2)})
    return landmarks


def measure_landmark_ratios(landmarks: list[dict[str, float]]) -> dict[str, float]:
    points = _by_name(landmarks)
    cheek_width = _distance(points["left_cheekbone"], points["right_cheekbone"])
    jaw_width = _distance(points["left_jaw"], points["right_jaw"])
    temple_width = _distance(points["left_temple"], points["right_temple"])
    face_length = _distance(points["forehead"], points["chin"])
    eye_line = _distance(points["left_eye"], points["right_eye"])

    base_width = max(cheek_width, 1.0)
    left_eye_to_nose = _distance(points["left_eye"], points["nose_tip"])
    right_eye_to_nose = _distance(points["right_eye"], points["nose_tip"])
    jaw_balance = abs(
        _distance(points["left_jaw"], points["chin"])
        - _distance(points["right_jaw"], points["chin"])
    )

    return {
        "face_length_ratio": round(face_length / base_width, 3),
        "jaw_to_cheek_ratio": round(jaw_width / base_width, 3),
        "temple_to_cheek_ratio": round(temple_width / base_width, 3),
        "eye_to_cheek_ratio": round(eye_line / base_width, 3),
        "eye_balance_delta": round(abs(left_eye_to_nose - right_eye_to_nose) / base_width, 3),
        "jaw_balance_delta": round(jaw_balance / base_width, 3),
    }
