"""Output contract for Pack 03 Interpretation Engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InterpretationOutputContract:
    """Declare interpretation output boundaries without implementing content."""

    output_type: str = "InterpretationResult"
    required_fields: tuple[str, ...] = (
        "id",
        "version",
        "metadata",
        "trace",
        "timestamps",
        "source_final_result_id",
        "success",
    )
    optional_fields: tuple[str, ...] = (
        "sections",
        "explanations",
        "report_refs",
        "output_artifacts",
    )
