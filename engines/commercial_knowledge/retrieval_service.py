"""Load and filter Wave 1.1 Knowledge Units from CSV corpus."""

from __future__ import annotations

import csv
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

from .models import WAVE_1_1_ALLOW_LIST
from .signal_projection import bind_placeholders, evaluate_condition, project_analysis_signals

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CSV = _REPO_ROOT / "database" / "20_knowledge" / "21_knowledge_units.csv"


class RetrievalService:
    """
    Retrieve allow-listed Knowledge Units and bind commercial text.

    Wave 1.1: only KU-ID-001 … KU-RC-001 are eligible.
    """

    def __init__(self, csv_path: Path | None = None) -> None:
        """Create retrieval service with optional CSV override (tests)."""
        self._csv_path = csv_path or _DEFAULT_CSV

    def retrieve(
        self,
        *,
        analysis: dict[str, Any] | None,
        scenario_id: str = "default",
        allow_list_ids: frozenset[str] = WAVE_1_1_ALLOW_LIST,
        target_components: tuple[str, ...] | None = None,
    ) -> tuple[list[dict[str, Any]], list[tuple[str, str]], dict[str, Any]]:
        """
        Return (selected_bound_rows, dropped, signals).

        Selected rows include bound `commercial_text` and never leave the allow-list.
        """
        signals = project_analysis_signals(analysis)
        rows = _load_units(str(self._csv_path))
        selected: list[dict[str, Any]] = []
        dropped: list[tuple[str, str]] = []

        for row in rows:
            unit_id = (row.get("knowledge_unit_id") or "").strip()
            if unit_id not in allow_list_ids:
                dropped.append((unit_id or "unknown", "not_in_wave_1_1_allow_list"))
                continue
            if not _scenario_match(row.get("scenarios") or "", scenario_id):
                dropped.append((unit_id, "scenario_mismatch"))
                continue
            if target_components and not _component_intersect(
                row.get("narrative_targets") or "",
                target_components,
            ):
                dropped.append((unit_id, "component_mismatch"))
                continue
            if not evaluate_condition(row.get("condition") or "", signals):
                dropped.append((unit_id, "condition_fail"))
                continue
            try:
                confidence = float(row.get("confidence") or 0.0)
                requirement = float(row.get("confidence_requirement") or 0.0)
            except ValueError:
                dropped.append((unit_id, "confidence_parse_fail"))
                continue
            if confidence < requirement:
                dropped.append((unit_id, "confidence_gate"))
                continue
            bound = bind_placeholders(row.get("modern_interpretation") or "", signals)
            if not bound:
                dropped.append((unit_id, "placeholder_bind_fail"))
                continue
            if _looks_technical(bound):
                dropped.append((unit_id, "technical_wording"))
                continue
            enriched = dict(row)
            enriched["commercial_text"] = bound
            enriched["bind_signals"] = signals
            selected.append(enriched)

        selected.sort(
            key=lambda item: (
                -_safe_int(item.get("priority"), 0),
                -float(item.get("confidence") or 0.0),
                item.get("knowledge_unit_id") or "",
            )
        )
        # One unit per evidence_kind (Wave 1.1).
        deduped: list[dict[str, Any]] = []
        seen_kinds: set[str] = set()
        for item in selected:
            kind = (item.get("evidence_kind") or "").strip()
            if kind in seen_kinds:
                dropped.append((item["knowledge_unit_id"], "duplicate_evidence_kind"))
                continue
            seen_kinds.add(kind)
            deduped.append(item)

        logger.info(
            "commercial_retrieval.selected=%s dropped=%s scenario=%s",
            len(deduped),
            len(dropped),
            scenario_id,
        )
        return deduped, dropped, signals


@lru_cache(maxsize=4)
def _load_units(csv_path: str) -> tuple[dict[str, str], ...]:
    path = Path(csv_path)
    if not path.is_file():
        logger.warning("commercial_retrieval.missing_csv path=%s", path)
        return ()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(dict(row) for row in reader)


def _scenario_match(scenarios: str, scenario_id: str) -> bool:
    tokens = {item.strip() for item in scenarios.replace(",", ";").split(";") if item.strip()}
    if not tokens:
        return True
    if scenario_id in tokens:
        return True
    if scenario_id == "default" and "default" in tokens:
        return True
    return False


def _component_intersect(targets: str, wanted: tuple[str, ...]) -> bool:
    have = {item.strip() for item in targets.replace(",", ";").split(";") if item.strip()}
    return bool(have.intersection(wanted))


def _looks_technical(text: str) -> bool:
    lowered = text.lower()
    markers = (
        "kích hoạt khi",
        "matched rules",
        "matched_rules",
        "(mock)",
        "placeholder",
    )
    return any(marker in lowered for marker in markers)


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
