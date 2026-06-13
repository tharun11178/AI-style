from __future__ import annotations

import hashlib
from typing import Any


SKIN_TONES = ["Warm neutral", "Cool neutral", "Golden", "Olive", "Deep warm", "Soft cool"]
CONTRAST_LEVELS = ["Low", "Medium", "High"]


def _pick(values: list[str], digest: str, offset: int) -> str:
    number = int(digest[offset : offset + 8], 16)
    return values[number % len(values)]


def _sample_bytes(image_bytes: bytes, sample_size: int = 4096) -> bytes:
    if len(image_bytes) <= sample_size:
        return image_bytes
    step = max(1, len(image_bytes) // sample_size)
    return image_bytes[::step][:sample_size]


def analyze_color_bytes(
    image_bytes: bytes,
    digest: str | None = None,
    available_skin_tones: list[str] | None = None,
    available_contrast_levels: list[str] | None = None,
) -> dict[str, Any]:
    sample = _sample_bytes(image_bytes)
    digest = digest or hashlib.sha256(sample).hexdigest()
    skin_tones = available_skin_tones or SKIN_TONES
    contrast_levels = available_contrast_levels or CONTRAST_LEVELS

    if not sample:
        return {
            "skin_tone": skin_tones[0],
            "contrast_level": contrast_levels[1],
            "warmth_score": 50,
            "brightness_score": 50,
            "color_confidence": 0.65,
        }

    average = sum(sample) / len(sample)
    variance = sum((byte - average) ** 2 for byte in sample) / len(sample)
    contrast_signal = min(100, int(variance ** 0.5))
    warm_signal = (sum(sample[::3]) - sum(sample[1::3])) if len(sample) > 3 else int(average)

    if warm_signal > len(sample) * 5:
        skin_tone = "Golden" if "Golden" in skin_tones else _pick(skin_tones, digest, 8)
    elif warm_signal < -len(sample) * 5:
        skin_tone = "Cool neutral" if "Cool neutral" in skin_tones else _pick(skin_tones, digest, 8)
    elif average < 92 and "Deep warm" in skin_tones:
        skin_tone = "Deep warm"
    elif 92 <= average <= 128 and "Olive" in skin_tones:
        skin_tone = "Olive"
    else:
        skin_tone = _pick(skin_tones, digest, 8)

    if contrast_signal >= 70 and "High" in contrast_levels:
        contrast_level = "High"
    elif contrast_signal <= 34 and "Low" in contrast_levels:
        contrast_level = "Low"
    else:
        contrast_level = "Medium" if "Medium" in contrast_levels else _pick(contrast_levels, digest, 16)

    return {
        "skin_tone": skin_tone,
        "contrast_level": contrast_level,
        "warmth_score": max(0, min(100, 50 + int(warm_signal / max(len(sample), 1)))),
        "brightness_score": max(0, min(100, int(average / 255 * 100))),
        "contrast_score": contrast_signal,
        "color_confidence": round(0.7 + (int(digest[18:20], 16) % 20) / 100, 2),
    }


def extract_palette(recommendations: dict[str, Any]) -> dict[str, Any]:
    return dict(recommendations.get("palette", {}))
