"""Contradiction Checker — drop opposing claims in the same section."""

from __future__ import annotations

from .models import NarrativeIssue, NarrativeUnit
from .redundancy_reducer import normalize_text

_ANTONYM_PAIRS: tuple[tuple[str, str], ...] = (
    ("manh", "yeu"),
    ("vuong", "nhuoc"),
    ("tot", "xau"),
    ("thuan", "nghich"),
    ("loi", "hai"),
    ("nong", "lanh"),
    ("hop", "xung"),
    ("thuan loi", "bat loi"),
    ("positive", "negative"),
)

_TONE_CONFLICT = {
    frozenset({"positive", "negative"}),
    frozenset({"positive", "serious"}),
    frozenset({"friendly", "serious"}),
}


class ContradictionChecker:
    """Detect and remove contradictory units within a section (keep higher priority)."""

    def __init__(self) -> None:
        self.issues: list[NarrativeIssue] = []

    def check(self, units: list[NarrativeUnit]) -> list[NarrativeUnit]:
        """Return non-contradictory units."""
        self.issues = []
        by_section: dict[str, list[NarrativeUnit]] = {}
        for unit in units:
            by_section.setdefault(unit.section_id, []).append(unit)

        survivors: list[NarrativeUnit] = []
        for section_id, group in by_section.items():
            ordered = sorted(group, key=lambda u: u.priority, reverse=True)
            accepted: list[NarrativeUnit] = []
            for candidate in ordered:
                conflict = self._conflicts_with(candidate, accepted)
                if conflict is not None:
                    self.issues.append(
                        NarrativeIssue(
                            kind="contradiction",
                            detail=(
                                f"Conflicts with higher-priority unit "
                                f"({conflict.rule_id or conflict.source})."
                            ),
                            section_id=section_id,
                            action="drop",
                        )
                    )
                    continue
                accepted.append(candidate)
            survivors.extend(accepted)

        ids = {id(unit) for unit in survivors}
        return [unit for unit in units if id(unit) in ids]

    def _conflicts_with(
        self,
        candidate: NarrativeUnit,
        accepted: list[NarrativeUnit],
    ) -> NarrativeUnit | None:
        cand_tone = candidate.tone
        cand_text = normalize_text(candidate.text)
        for kept in accepted:
            if frozenset({cand_tone, kept.tone}) in _TONE_CONFLICT:
                return kept
            if self._antonym_clash(cand_text, normalize_text(kept.text)):
                return kept
        return None

    @staticmethod
    def _antonym_clash(left: str, right: str) -> bool:
        if not left or not right:
            return False
        for a, b in _ANTONYM_PAIRS:
            left_a, left_b = a in left, b in left
            right_a, right_b = a in right, b in right
            if (left_a and left_b) or (right_a and right_b):
                continue
            if (left_a and right_b) or (left_b and right_a):
                return True
        return False
