from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "wellness_advisor.db"
UPLOAD_DIR = BASE_DIR / "uploads"

APP_TITLE = "AI Personal Style & Wellness Advisor"

ALLOWED_ORIGINS = {
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://ai-style-kd7p.onrender.com",
}

ALLOWED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
