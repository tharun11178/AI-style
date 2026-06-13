from __future__ import annotations

import sqlite3

from .config import DB_PATH, UPLOAD_DIR
from .models.analysis_model import CREATE_ANALYSES_TABLE_SQL
from .models.feedback_model import CREATE_FEEDBACK_TABLE_SQL
from .models.recommendation_model import CREATE_ADMIN_LOGS_TABLE_SQL, CREATE_RECOMMENDATION_HISTORY_TABLE_SQL
from .models.user_model import CREATE_SESSIONS_TABLE_SQL, CREATE_USERS_TABLE_SQL
from .utils.jwt_handler import hash_password
from .utils.response_handler import now_iso


def connect_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def get_db():
    db = connect_db()
    try:
        yield db
    finally:
        db.close()


def seed_user(db: sqlite3.Connection, name: str, email: str, password: str, role: str) -> None:
    exists = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if exists:
        return

    db.execute(
        """
        INSERT INTO users (name, email, password_hash, role, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, hash_password(password), role, now_iso()),
    )
    db.commit()


def create_schema() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with connect_db() as db:
        db.executescript(
            "\n".join(
                [
                    CREATE_USERS_TABLE_SQL,
                    CREATE_SESSIONS_TABLE_SQL,
                    CREATE_ANALYSES_TABLE_SQL,
                    CREATE_FEEDBACK_TABLE_SQL,
                    CREATE_RECOMMENDATION_HISTORY_TABLE_SQL,
                    CREATE_ADMIN_LOGS_TABLE_SQL,
                ]
            )
        )
        seed_user(db, "Demo User", "demo@example.com", "demo123", "user")
        seed_user(db, "Admin", "admin@example.com", "admin123", "admin")
