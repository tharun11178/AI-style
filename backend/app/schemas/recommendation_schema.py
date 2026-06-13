from __future__ import annotations

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    rating: int = Field(default=5, ge=1, le=5)
    comments: str


class AnalysisResult(BaseModel):
    id: int
    face_shape: str
    skin_tone: str
    symmetry_score: float
    jawline_score: float
    contrast_level: str
    created_at: str
