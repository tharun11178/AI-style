from __future__ import annotations

import sqlite3
from typing import Any


CREATE_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    favorite_style TEXT DEFAULT 'Smart casual',
    profession TEXT DEFAULT 'Student',
    occasion_preference TEXT DEFAULT 'Everyday',
    wellness_focus TEXT DEFAULT 'Energy',
    created_at TEXT NOT NULL
);
"""

CREATE_SESSIONS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""


def row_to_user(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "role": row["role"],
        "favorite_style": row["favorite_style"],
        "profession": row["profession"],
        "occasion_preference": row["occasion_preference"],
        "wellness_focus": row["wellness_focus"],
        "created_at": row["created_at"],
    }
