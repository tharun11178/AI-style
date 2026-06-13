from __future__ import annotations

import secrets
from datetime import datetime, timezone
from pathlib import Path

from ..config import ALLOWED_IMAGE_SUFFIXES, UPLOAD_DIR


def safe_image_name(original_filename: str | None) -> str:
    suffix = Path(original_filename or "upload.jpg").suffix.lower()
    if suffix not in ALLOWED_IMAGE_SUFFIXES:
        suffix = ".jpg"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{timestamp}-{secrets.token_hex(4)}{suffix}"


def save_upload_bytes(contents: bytes, original_filename: str | None) -> str:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    image_name = safe_image_name(original_filename)
    (UPLOAD_DIR / image_name).write_bytes(contents)
    return image_name
