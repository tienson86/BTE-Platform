"""Rank Interpretation sections by importance."""

from __future__ import annotations

from typing import Any


# Canonical narrative weight hints (not hard-coded copy — structural priors only).
_SECTION_WEIGHTS: dict[str, float] = {
    "summary": 1.20,
    "conclusion": 1.15,
    "pattern": 1.10,
    "useful_god": 1.10,
    "strength": 1.05,
    "weakness": 1.00,
    "career": 1.00,
    "wealth": 1.00,
    "relationship": 0.95,
    "health": 0.95,
    "personality": 0.95,
    "luck": 0.90,
    "luck_cycle": 0.90,
    "yearly_fortune": 0.90,
    "children": 0.85,
    "warning": 1.05,
}


class ImportanceRanker:
    """Compute section_scores and important_sections from analysis bag."""

    def __init__(self, *, importance_threshold: float = 25.0) -> None:
        self.importance_threshold = importance_threshold

    def rank(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """
        Return section_scores (0..100) and important_sections (desc).
        """
        grouped = analysis.get("grouped_rules") or {}
        counts = analysis.get("section_rule_counts") or {}
        confidence = float(analysis.get("confidence") or 0.0)
        max_count = max([int(v) for v in counts.values()] + [1])

        scores: dict[str, float] = {}
        for section, rules in grouped.items():
            count = len(rules)
            density = (count / max_count) * 60.0
            priority_boost = self._avg_priority(rules) * 0.25
            section_score_field = self._section_native_score(
                analysis.get("sections") or {},
                section,
            )
            weight = _SECTION_WEIGHTS.get(section, 0.9)
            conf_boost = min(15.0, max(0.0, confidence) * 0.15)
            raw = (density + priority_boost + section_score_field + conf_boost) * weight
            scores[section] = round(min(100.0, max(0.0, raw)), 2)

        important = [
            name
            for name, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)
            if score >= self.importance_threshold
        ]
        return {
            "section_scores": scores,
            "important_sections": important,
        }

    @staticmethod
    def _avg_priority(rules: list[dict[str, Any]]) -> float:
        if not rules:
            return 0.0
        total = 0.0
        for rule in rules:
            try:
                total += float(rule.get("priority") or rule.get("confidence") or 0)
            except (TypeError, ValueError):
                continue
        return total / max(1, len(rules))

    @staticmethod
    def _section_native_score(sections: dict[str, Any], section: str) -> float:
        payload = sections.get(section) or {}
        try:
            return min(20.0, float(payload.get("score") or 0.0))
        except (TypeError, ValueError):
            return 0.0
