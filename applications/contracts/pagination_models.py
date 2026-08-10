"""Pagination contracts for future list endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


class PaginationRequest(BaseModel):
    """List query parameters. Validation only."""

    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=DEFAULT_PAGE, ge=1, description="1-based page index.")
    page_size: int = Field(
        default=DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        description="Number of items per page.",
    )


class PaginationMeta(BaseModel):
    """Pagination metadata returned with list payloads."""

    model_config = ConfigDict(extra="forbid")

    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=MAX_PAGE_SIZE)
    total_items: int | None = Field(default=None, ge=0)
    total_pages: int | None = Field(default=None, ge=0)
    has_next: bool = False
    has_previous: bool = False
