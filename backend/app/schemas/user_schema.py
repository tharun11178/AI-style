from __future__ import annotations

from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    favorite_style: str | None = None
    profession: str | None = None
    occasion_preference: str | None = None
    wellness_focus: str | None = None
    created_at: str


class ProfileUpdate(BaseModel):
    name: str | None = None
    favorite_style: str | None = None
    profession: str | None = None
    occasion_preference: str | None = None
    wellness_focus: str | None = None
