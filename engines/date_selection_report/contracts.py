"""PACK 06 Date Selection report contracts.

Reuses PACK 05 foundation identity. Does not duplicate Report Engine.
"""

from __future__ import annotations

from typing import Any, Protocol

from engines.date_selection_report.constants import (
    GENERATOR,
    LOCALE,
    PACK05_REPORT_VERSION,
    REPORT_CONTRACT_ID,
    REPORT_SCHEMA_VERSION,
    REPORT_TYPE,
    TITLE,
)


class CanonicalSearchResult(Protocol):
    """Minimal SearchResult surface consumed by the report adapter."""

    target_year: int
    target_month: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize canonical Date Selection output."""


REPORT_FOUNDATION_CONTRACT: dict[str, str] = {
    "pack": "06",
    "report_type": REPORT_TYPE,
    "schema_version": REPORT_SCHEMA_VERSION,
    "locale": LOCALE,
    "title": TITLE,
    "generator": GENERATOR,
    "pack_05_contract_id": REPORT_CONTRACT_ID,
    "pack_05_report_version": PACK05_REPORT_VERSION,
}
