"""Audit ShenSha name pairs that may be aliases. Do not merge."""

from __future__ import annotations

from dataclasses import dataclass

from engines.report_engine.contracts.report_input_v1 import ReportShenShaItemV1

_CANDIDATE_PAIRS: tuple[tuple[str, str], ...] = (
    ("Thiên Ất", "Thiên Ất Quý Nhân"),
    ("Thiên Đức", "Thiên Đức Quý Nhân"),
    ("Nguyệt Đức", "Nguyệt Đức Quý Nhân"),
)


@dataclass(slots=True)
class ShenShaDuplicateCandidate:
    """A pair of names that may be aliases or distinct gods."""

    left: str
    right: str
    both_present: bool
    note: str


def audit_shensha_duplicates(
    items: list[ReportShenShaItemV1],
) -> list[ShenShaDuplicateCandidate]:
    """Mark duplicate candidates without merging or dropping entries."""
    names = {item.name.strip() for item in items if item.name.strip()}
    results: list[ShenShaDuplicateCandidate] = []
    for left, right in _CANDIDATE_PAIRS:
        if left in names and right in names:
            results.append(
                ShenShaDuplicateCandidate(
                    left=left,
                    right=right,
                    both_present=True,
                    note=(
                        "Both names are present in runtime output. "
                        "They may be aliases of one thần sát or two distinct entries. "
                        "Do not merge without Rule Database confirmation."
                    ),
                )
            )
    return results
