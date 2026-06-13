CREATE_ANALYSES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_name TEXT NOT NULL,
    face_shape TEXT NOT NULL,
    skin_tone TEXT NOT NULL,
    symmetry_score REAL NOT NULL,
    jawline_score REAL NOT NULL,
    contrast_level TEXT NOT NULL,
    recommendations_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""
