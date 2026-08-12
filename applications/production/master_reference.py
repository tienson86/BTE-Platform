"""Golden master interpretation access — regression/comparison only."""

from __future__ import annotations

from applications.production.master_interpretation_loader import (
    load_all_master_parts,
    load_executive_consulting,
)

GOLDEN_CASE_IDS = frozenset({"CASE-0001", "CASE_0001"})


def is_golden_reference_case(case_id: str) -> bool:
    """Return True when case_id maps to a golden reference case."""
    normalized = case_id.upper().replace("_", "-")
    return normalized in GOLDEN_CASE_IDS


def load_golden_master_parts_for_comparison(case_id: str) -> dict[str, str]:
    """Load frozen master parts for golden comparison — never for customer delivery."""
    if not is_golden_reference_case(case_id):
        raise ValueError(
            f"Golden master parts only available for reference cases, got {case_id}"
        )
    return load_all_master_parts(case_id)


def load_golden_executive_for_comparison(case_id: str) -> str:
    """Load Part 08 for golden comparison — never for customer delivery."""
    if not is_golden_reference_case(case_id):
        raise ValueError(
            f"Golden executive consulting only available for reference cases, got {case_id}"
        )
    return load_executive_consulting(case_id)
