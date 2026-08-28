"""Apply frozen INT-03B editorial rules. Editor only. No new analytical facts."""

from __future__ import annotations

from engines.commercial_composer.mapping import IntegratedLine
from engines.commercial_composer.rules import (
    EXECUTIVE_FINDING_PRIORITY,
    RECOMMENDATION_MEANING_GROUPS,
    fact_key,
    is_eligible_executive_finding,
    is_forbidden_style,
    is_machine_only,
    is_technical_language,
    keep_strongest_published,
)


def clean_lines(lines: tuple[IntegratedLine, ...]) -> tuple[IntegratedLine, ...]:
    """Drop machine-only, technical-id, compact-score, and forbidden-style wording."""
    return tuple(line for line in lines if _is_customer_ready(line))


def dedupe_lines(lines: tuple[IntegratedLine, ...]) -> tuple[IntegratedLine, ...]:
    """Emit each published fact meaning once. Keep the first published sentence."""
    seen: set[str] = set()
    selected: list[IntegratedLine] = []
    for line in lines:
        key = fact_key(line.text) or f"exact:{line.text}"
        if key in seen:
            continue
        seen.add(key)
        selected.append(line)
    return tuple(selected)


def select_executive(lines: tuple[IntegratedLine, ...]) -> tuple[IntegratedLine, ...]:
    """Select, prioritize, and merge highest-priority published findings. No concat."""
    eligible = [line for line in clean_lines(lines) if is_eligible_executive_finding(line.text, line.source_path)]
    by_key: dict[str, IntegratedLine] = {}
    for line in eligible:
        key = fact_key(line.text)
        if key is None or key in by_key:
            continue
        by_key[key] = line
    return tuple(by_key[key] for key in EXECUTIVE_FINDING_PRIORITY if key in by_key)


def merge_recommendations(lines: tuple[IntegratedLine, ...]) -> tuple[IntegratedLine, ...]:
    """Group published recommendations by meaning and keep the strongest version."""
    grouped: dict[str, list[IntegratedLine]] = {name: [] for name in RECOMMENDATION_MEANING_GROUPS}
    grouped["other"] = []
    for line in clean_lines(lines):
        grouped[_recommendation_group(line)].append(line)
    merged: list[IntegratedLine] = []
    for name in (*RECOMMENDATION_MEANING_GROUPS, "other"):
        winner = _strongest_in_group(grouped[name])
        if winner is not None:
            merged.append(winner)
    return tuple(merged)


def first_cleaned(lines: tuple[IntegratedLine, ...]) -> tuple[IntegratedLine, ...]:
    """Keep the first customer-ready published sentence."""
    cleaned = clean_lines(lines)
    return cleaned[:1]


def _is_customer_ready(line: IntegratedLine) -> bool:
    path = line.source_path.lower()
    if is_machine_only(line.text) or is_technical_language(line.text):
        return False
    if is_forbidden_style(line.text):
        return False
    if "compact" in path or "score" in path:
        return False
    return True


def _recommendation_group(line: IntegratedLine) -> str:
    path = line.source_path.lower()
    text = line.text
    if "unfavorable" in path or "Kỵ" in text or text.startswith("Hạn chế"):
        return "unfavorable"
    if "temperature" in path or "điều hậu" in text.casefold() or "climate" in path:
        return "climate"
    if "Dụng thần" in text or "Hỷ thần" in text or "useful_god" in path:
        return "useful_god"
    return "other"


def _strongest_in_group(lines: list[IntegratedLine]) -> IntegratedLine | None:
    if not lines:
        return None
    winner = lines[0]
    for candidate in lines[1:]:
        kept = keep_strongest_published(winner.text, candidate.text)
        if kept == candidate.text.strip() or kept == candidate.text:
            winner = candidate
    return winner
