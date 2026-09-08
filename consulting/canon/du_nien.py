"""Canonical Du Niên 8×8 lookup. Reads knowledge/canon/du_nien_8x8.yaml only."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

CANON_PATH = Path(__file__).resolve().parents[2] / "knowledge" / "canon" / "du_nien_8x8.yaml"
PALACES = ("Khảm", "Khôn", "Chấn", "Tốn", "Càn", "Đoài", "Cấn", "Ly")
RELATIONSHIP_IDS = (
    "sinh_khi",
    "thien_y",
    "dien_nien",
    "phuc_vi",
    "tuyet_menh",
    "ngu_quy",
    "luc_sat",
    "hoa_hai",
)
FAVORABLE_IDS = frozenset({"sinh_khi", "thien_y", "dien_nien", "phuc_vi"})
UNFAVORABLE_IDS = frozenset({"tuyet_menh", "ngu_quy", "luc_sat", "hoa_hai"})


@dataclass(frozen=True, slots=True)
class DuNienRelation:
    """One ordered Cung Phi pair from the canonical matrix."""

    source_palace: str
    target_palace: str
    relationship_id: str
    relationship_label: str
    category: str
    customer_summary: str
    expert_summary: str


class DuNienCanonError(ValueError):
    """Raised when the canonical Du Niên matrix is missing or invalid."""


@lru_cache(maxsize=1)
def load_matrix() -> dict[tuple[str, str], DuNienRelation]:
    """Load and validate the frozen 8×8 matrix. Lookup only."""
    if not CANON_PATH.is_file():
        raise DuNienCanonError(f"missing_du_nien_canon:{CANON_PATH}")
    payload = yaml.safe_load(CANON_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise DuNienCanonError("du_nien_canon_must_be_mapping")
    palaces = tuple(payload.get("palaces") or ())
    if palaces != PALACES:
        raise DuNienCanonError("du_nien_palace_set_invalid")
    catalog = payload.get("relationships") or {}
    matrix = payload.get("matrix") or {}
    if not isinstance(catalog, dict) or not isinstance(matrix, dict):
        raise DuNienCanonError("du_nien_canon_shape_invalid")
    _validate_catalog(catalog)
    entries: dict[tuple[str, str], DuNienRelation] = {}
    for source in PALACES:
        row = matrix.get(source)
        if not isinstance(row, dict):
            raise DuNienCanonError(f"missing_source_row:{source}")
        if set(row) != set(PALACES):
            raise DuNienCanonError(f"incomplete_target_row:{source}")
        seen_ids: set[str] = set()
        for target in PALACES:
            rel_id = str(row[target])
            if rel_id in seen_ids:
                raise DuNienCanonError(f"duplicate_relationship_in_row:{source}:{rel_id}")
            seen_ids.add(rel_id)
            spec = catalog.get(rel_id)
            if not isinstance(spec, dict):
                raise DuNienCanonError(f"unknown_relationship_id:{rel_id}")
            entries[(source, target)] = DuNienRelation(
                source_palace=source,
                target_palace=target,
                relationship_id=rel_id,
                relationship_label=str(spec["label"]),
                category=str(spec["category"]),
                customer_summary=str(spec["customer_summary"]),
                expert_summary=str(spec.get("expert_summary") or spec["customer_summary"]),
            )
        if seen_ids != set(RELATIONSHIP_IDS):
            raise DuNienCanonError(f"row_relationship_set_invalid:{source}")
    if len(entries) != 64:
        raise DuNienCanonError(f"expected_64_pairs:{len(entries)}")
    return entries


def lookup(source_palace: str, target_palace: str) -> DuNienRelation | None:
    """Return the canonical relation of an ordered palace pair."""
    key = (_normalize_palace(source_palace), _normalize_palace(target_palace))
    if not key[0] or not key[1]:
        return None
    return load_matrix().get(key)


def summary_for_label(label: str) -> str:
    """Return customer summary for a Vietnamese relationship label."""
    wanted = (label or "").strip()
    for item in load_matrix().values():
        if item.relationship_label == wanted:
            return item.customer_summary
    return "Cung Phi là tín hiệu phụ, không thay thế đánh giá chính."


def is_favorable(label_or_id: str) -> bool:
    """True when the relationship is one of the four favorable names/ids."""
    text = (label_or_id or "").strip()
    if text in FAVORABLE_IDS:
        return True
    for item in load_matrix().values():
        if item.relationship_label == text:
            return item.relationship_id in FAVORABLE_IDS
    return False


def _normalize_palace(value: str) -> str:
    """Trim a palace name. Does not alias unknown labels."""
    return (value or "").strip()


def _validate_catalog(catalog: dict[str, Any]) -> None:
    """Require the eight relationship definitions."""
    if set(catalog) != set(RELATIONSHIP_IDS):
        raise DuNienCanonError("relationship_catalog_incomplete")
    for rel_id, spec in catalog.items():
        if not isinstance(spec, dict):
            raise DuNienCanonError(f"relationship_spec_invalid:{rel_id}")
        if spec.get("id") != rel_id:
            raise DuNienCanonError(f"relationship_id_mismatch:{rel_id}")
        label = str(spec.get("label") or "")
        category = str(spec.get("category") or "")
        if not label or not spec.get("customer_summary"):
            raise DuNienCanonError(f"relationship_fields_missing:{rel_id}")
        expected_category = "favorable" if rel_id in FAVORABLE_IDS else "unfavorable"
        if category != expected_category:
            raise DuNienCanonError(f"relationship_category_mismatch:{rel_id}")
        if rel_id in UNFAVORABLE_IDS and category != "unfavorable":
            raise DuNienCanonError(f"unfavorable_category_required:{rel_id}")
