"""Public PresentationMetadata. Customer-safe only."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.presentation.presentation_status import (
    DEFAULT_LANGUAGE,
    FROZEN_CREATED_AT,
    PRESENTATION_VERSION,
)


@dataclass(frozen=True, slots=True)
class PresentationMetadata:
    """Public-safe metadata. Not runtime internals."""

    status: str
    language: str = DEFAULT_LANGUAGE
    version: str = PRESENTATION_VERSION
    created_at: str = FROZEN_CREATED_AT
