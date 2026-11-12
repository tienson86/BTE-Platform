"""Course configuration and immutable-price redemption requests."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class CourseSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=160)
    summary: str = Field(max_length=1200)
    price: int = Field(ge=0, le=1000000, strict=True)
    access_days: int | None = Field(default=None, ge=1, le=36500, strict=True)
    status: Literal["draft", "published", "paused"] = "draft"
    expected_revision: int = Field(ge=1, strict=True)


class CourseRedeem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_key: str = Field(pattern=r"^[a-zA-Z0-9_-]{8,100}$")
    expected_revision: int = Field(ge=1, strict=True)


class LessonProgress(BaseModel):
    model_config = ConfigDict(extra="forbid")
    completed: bool = True
