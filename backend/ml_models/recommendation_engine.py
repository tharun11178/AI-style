from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ML_ROOT = Path(__file__).resolve().parent
DATASET_DIR = ML_ROOT / "datasets"
TRAINED_MODEL_DIR = ML_ROOT / "trained_models"
STYLE_RULES_PATH = TRAINED_MODEL_DIR / "style_rules.json"

DEFAULT_STYLE_BY_FACE = {
    "Oval": {
        "hair": ["Textured crop", "Layered side part", "Soft waves"],
        "beard": "Most beard styles work; keep the sides neat for balance.",
        "glasses": ["Square frames", "Geometric frames", "Soft aviators"],
    },
    "Round": {
        "hair": ["High-volume quiff", "Taper fade with height", "Layered crown"],
        "beard": "Add length at the chin and keep cheek volume controlled.",
        "glasses": ["Angular rectangle frames", "Wayfarer frames", "Browline frames"],
    },
    "Square": {
        "hair": ["Loose fringe", "Medium textured layers", "Side swept style"],
        "beard": "Round the beard edges slightly to soften a strong jawline.",
        "glasses": ["Round frames", "Oval frames", "Thin metal frames"],
    },
    "Diamond": {
        "hair": ["Side fringe", "Layered medium cut", "Volume around the temples"],
        "beard": "Keep chin length modest and add softness near the jaw.",
        "glasses": ["Oval frames", "Cat-eye frames", "Rimless frames"],
    },
    "Heart": {
        "hair": ["Curtain fringe", "Medium layers", "Side part with soft volume"],
        "beard": "A short boxed beard can add balance around the chin.",
        "glasses": ["Bottom-heavy frames", "Rounded rectangle frames", "Light wire frames"],
    },
    "Rectangle": {
        "hair": ["Classic side part", "Textured fringe", "Medium length with side volume"],
        "beard": "Avoid extra chin length; keep fullness on the sides.",
        "glasses": ["Tall rectangle frames", "Round frames", "Aviators"],
    },
}

DEFAULT_PALETTES = {
    "Warm neutral": {
        "name": "Warm Clarity",
        "colors": ["#1f6f68", "#f2b880", "#d95d39", "#f7f3e8", "#262626"],
    },
    "Cool neutral": {
        "name": "Cool Balance",
        "colors": ["#355070", "#6d597a", "#b56576", "#e9ecef", "#1b1f24"],
    },
    "Golden": {
        "name": "Golden Everyday",
        "colors": ["#2d6a4f", "#f2cc8f", "#e07a5f", "#3d405b", "#faf3dd"],
    },
    "Olive": {
        "name": "Olive Contrast",
        "colors": ["#283618", "#606c38", "#dda15e", "#fefae0", "#bc6c25"],
    },
    "Deep warm": {
        "name": "Deep Warm",
        "colors": ["#12355b", "#d1495b", "#edae49", "#00798c", "#f4f1de"],
    },
    "Soft cool": {
        "name": "Soft Cool",
        "colors": ["#4a5759", "#b0c4b1", "#dedbd2", "#edafb8", "#2f3e46"],
    },
}


def _load_style_rules() -> dict[str, Any]:
    if STYLE_RULES_PATH.exists():
        with STYLE_RULES_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return {
            "version": data.get("version", "local-rules-v1"),
            "style_by_face": data.get("style_by_face", DEFAULT_STYLE_BY_FACE),
            "palettes": data.get("palettes", DEFAULT_PALETTES),
            "accessories": data.get(
                "accessories",
                ["Minimal watch", "Clean belt hardware", "One texture accent such as linen or suede"],
            ),
        }

    return {
        "version": "local-rules-v1",
        "style_by_face": DEFAULT_STYLE_BY_FACE,
        "palettes": DEFAULT_PALETTES,
        "accessories": ["Minimal watch", "Clean belt hardware", "One texture accent such as linen or suede"],
    }


def _file_inventory(directory: Path) -> list[dict[str, Any]]:
    if not directory.exists():
        return []

    files: list[dict[str, Any]] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.name == ".gitkeep":
            continue
        stat = path.stat()
        files.append(
            {
                "name": path.name,
                "relative_path": str(path.relative_to(ML_ROOT)).replace("\\", "/"),
                "size_bytes": stat.st_size,
                "extension": path.suffix.lower() or "none",
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            }
        )
    return files


def collect_ml_assets() -> dict[str, Any]:
    rules = _load_style_rules()
    return {
        "ml_root": str(ML_ROOT),
        "datasets": _file_inventory(DATASET_DIR),
        "trained_models": _file_inventory(TRAINED_MODEL_DIR),
        "registered_face_shapes": sorted(rules["style_by_face"].keys()),
        "registered_palettes": sorted(rules["palettes"].keys()),
        "rules_version": rules["version"],
    }


def build_recommendations(
    *,
    face_shape: str,
    skin_tone: str,
    contrast_level: str,
    favorite_style: str,
    profession: str,
    occasion: str,
    wellness_focus: str,
) -> dict[str, Any]:
    rules = _load_style_rules()
    style_by_face = rules["style_by_face"]
    palettes = rules["palettes"]
    style = style_by_face.get(face_shape, style_by_face["Oval"])
    palette = palettes.get(skin_tone, palettes["Warm neutral"])
    style_text = favorite_style.strip() or "Smart casual"
    profession_text = profession.strip() or "Student"
    occasion_text = occasion.strip() or "Everyday"

    outfits = [
        f"{style_text} base layer with a structured overshirt for {occasion_text.lower()} use",
        f"Clean monochrome outfit with one palette accent for {profession_text.lower()} settings",
        "Comfort sneakers or loafers, depending on how formal the day needs to feel",
    ]

    if "formal" in occasion_text.lower() or "office" in profession_text.lower():
        outfits.append("Tailored blazer, crisp shirt, and muted trousers from the recommended palette")
    elif "athletic" in style_text.lower() or "fitness" in wellness_focus.lower():
        outfits.append("Breathable stretch layers with a sharp jacket to keep the look intentional")
    else:
        outfits.append("Dark denim or tapered chinos to keep the silhouette balanced")

    wellness = [
        f"Anchor the routine around {wellness_focus.lower()} with a simple morning check-in.",
        "Keep grooming consistent: hair, skin, and outfit should feel like one decision system.",
        "Use the palette accents sparingly so the face stays the visual focus.",
    ]

    if contrast_level == "High":
        wellness.append("High contrast looks can handle stronger color blocking and sharper accessories.")
    elif contrast_level == "Low":
        wellness.append("Low contrast looks work best with softer transitions between hair, skin, and clothing.")
    else:
        wellness.append("Medium contrast gives room for both neutrals and one confident accent color.")

    return {
        "hairstyles": style["hair"],
        "beard": style["beard"],
        "outfits": outfits,
        "glasses": style["glasses"],
        "accessories": list(rules["accessories"]),
        "palette": palette,
        "wellness": wellness,
        "model": {
            "recommendation_rules": STYLE_RULES_PATH.name if STYLE_RULES_PATH.exists() else "built-in fallback",
            "rules_version": rules["version"],
        },
    }
