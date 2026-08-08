"""Load and filter allow-listed Knowledge Units from CSV corpora."""

from __future__ import annotations

import csv
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

from .models import WAVE_1_1_ALLOW_LIST
from .signal_projection import bind_placeholders, evaluate_condition, project_analysis_signals
from .commercial_presentation import commercialize_customer_text

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CSV_21 = _REPO_ROOT / "database" / "20_knowledge" / "21_knowledge_units.csv"
_DEFAULT_CSV_22 = _REPO_ROOT / "database" / "20_knowledge" / "22_domain01_career_business.csv"
_DEFAULT_CORPORA: tuple[Path, ...] = (_DEFAULT_CSV_21, _DEFAULT_CSV_22)


class RetrievalService:
    """
    Retrieve allow-listed Knowledge Units and bind commercial text.

    Production loads Wave 1.1 + Domain 01 CSV files; eligibility is allow-list gated
    (Career Selection Assessment units only from Domain 01).
    """

    def __init__(
        self,
        csv_path: Path | None = None,
        *,
        csv_paths: Sequence[Path] | None = None,
    ) -> None:
        """Create retrieval service with optional CSV override (tests)."""
        if csv_paths is not None:
            self._csv_paths = tuple(Path(path) for path in csv_paths)
        elif csv_path is not None:
            self._csv_paths = (Path(csv_path),)
        else:
            self._csv_paths = _DEFAULT_CORPORA

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
        Production callers pass ``PRODUCTION_ALLOW_LIST`` for Career Selection V1.
        """
        signals = project_analysis_signals(analysis)
        rows = _load_units_many(tuple(str(path) for path in self._csv_paths))
        selected: list[dict[str, Any]] = []
        dropped: list[tuple[str, str]] = []
        deny_reason = (
            "not_in_wave_1_1_allow_list"
            if allow_list_ids == WAVE_1_1_ALLOW_LIST
            else "not_in_production_allow_list"
        )

        for row in rows:
            unit_id = (row.get("knowledge_unit_id") or "").strip()
            if unit_id not in allow_list_ids:
                dropped.append((unit_id or "unknown", deny_reason))
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
            bound = commercialize_customer_text(bound)
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
        # One unit per evidence_kind.
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
            "commercial_retrieval.selected=%s dropped=%s scenario=%s corpora=%s",
            len(deduped),
            len(dropped),
            scenario_id,
            len(self._csv_paths),
        )
        return deduped, dropped, signals


@lru_cache(maxsize=8)
def _load_units_many(csv_paths: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for csv_path in csv_paths:
        for row in _load_units(csv_path):
            unit_id = (row.get("knowledge_unit_id") or "").strip()
            if not unit_id or unit_id in seen_ids:
                continue
            seen_ids.add(unit_id)
            rows.append(row)
    return tuple(rows)


@lru_cache(maxsize=8)
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


# Backward-compatible alias used by older call sites / tests.
def clear_unit_caches() -> None:
    """Clear CSV load caches (tests)."""
    _load_units.cache_clear()
    _load_units_many.cache_clear()
