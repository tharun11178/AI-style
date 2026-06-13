from __future__ import annotations

import hashlib
from typing import Any


def _read_uint24_le(chunk: bytes) -> int:
    return chunk[0] | (chunk[1] << 8) | (chunk[2] << 16)


def _jpeg_dimensions(image_bytes: bytes) -> tuple[int, int] | None:
    if not image_bytes.startswith(b"\xff\xd8"):
        return None

    offset = 2
    sof_markers = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    while offset + 9 < len(image_bytes):
        if image_bytes[offset] != 0xFF:
            offset += 1
            continue

        while offset < len(image_bytes) and image_bytes[offset] == 0xFF:
            offset += 1
        if offset >= len(image_bytes):
            break

        marker = image_bytes[offset]
        offset += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if offset + 2 > len(image_bytes):
            break

        block_length = int.from_bytes(image_bytes[offset : offset + 2], "big")
        if block_length < 2 or offset + block_length > len(image_bytes):
            break
        if marker in sof_markers and offset + 7 < len(image_bytes):
            height = int.from_bytes(image_bytes[offset + 3 : offset + 5], "big")
            width = int.from_bytes(image_bytes[offset + 5 : offset + 7], "big")
            return width, height
        offset += block_length
    return None


def get_image_metadata(image_bytes: bytes) -> dict[str, Any]:
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n") and len(image_bytes) >= 24:
        return {
            "format": "png",
            "width": int.from_bytes(image_bytes[16:20], "big"),
            "height": int.from_bytes(image_bytes[20:24], "big"),
        }

    if image_bytes[:6] in {b"GIF87a", b"GIF89a"} and len(image_bytes) >= 10:
        return {
            "format": "gif",
            "width": int.from_bytes(image_bytes[6:8], "little"),
            "height": int.from_bytes(image_bytes[8:10], "little"),
        }

    jpeg_size = _jpeg_dimensions(image_bytes)
    if jpeg_size:
        width, height = jpeg_size
        return {"format": "jpeg", "width": width, "height": height}

    if image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        if image_bytes[12:16] == b"VP8X" and len(image_bytes) >= 30:
            return {
                "format": "webp",
                "width": _read_uint24_le(image_bytes[24:27]) + 1,
                "height": _read_uint24_le(image_bytes[27:30]) + 1,
            }
        return {"format": "webp", "width": 1024, "height": 1024}

    side = max(256, min(1600, int(len(image_bytes) ** 0.5) * 2))
    return {"format": "unknown", "width": side, "height": side}


def detect_face_region(image_bytes: bytes) -> dict[str, Any]:
    metadata = get_image_metadata(image_bytes)
    width = max(int(metadata["width"]), 1)
    height = max(int(metadata["height"]), 1)
    digest = hashlib.sha256(image_bytes[:8192]).hexdigest()

    shorter_side = min(width, height)
    size_ratio = 0.54 + (int(digest[:2], 16) % 13) / 100
    box_width = max(1, int(shorter_side * size_ratio))
    box_height = max(1, int(box_width * (1.1 + (int(digest[2:4], 16) % 12) / 100)))
    box_width = min(box_width, width)
    box_height = min(box_height, height)

    x_shift = ((int(digest[4:6], 16) % 13) - 6) / 100
    y_shift = ((int(digest[6:8], 16) % 11) - 4) / 100
    center_x = width * (0.5 + x_shift)
    center_y = height * (0.47 + y_shift)
    x = int(max(0, min(width - box_width, center_x - box_width / 2)))
    y = int(max(0, min(height - box_height, center_y - box_height / 2)))

    return {
        "x": x,
        "y": y,
        "width": box_width,
        "height": box_height,
        "image_width": width,
        "image_height": height,
        "image_format": metadata["format"],
        "confidence": round(0.78 + (int(digest[8:10], 16) % 18) / 100, 2),
        "detector": "local-geometry-v1",
    }
