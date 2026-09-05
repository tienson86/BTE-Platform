"""Canonical MC-01 / Mệnh Cục reference adapter.

Pack 07 does not own Pattern, Grade, Damage, Rescue, or profiles.
This module copies live upstream structural identifiers into an immutable
snapshot and refuses stale or conflicting lineage.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_str
from engines.detailed_interpretation_engine.constants import (
    MC01_BIND_REJECT_KEY,
    MC01_RULESET_VERSION,
    SCHEMA_MINGJU_DECISION,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.serialization import compute_content_hash
from engines.detailed_interpretation_engine.value_objects import Mc01Reference

REJECT_HASH_MISMATCH: str = "hash_mismatch"
REJECT_LINEAGE_MISMATCH: str = "lineage_mismatch"
REJECT_STALE_REFERENCE: str = "stale_reference"
REJECT_INCOMPLETE: str = "incomplete_structural_refs"

_SNAPSHOT_KEYS: tuple[str, ...] = (
    "schema_version",
    "ruleset_version",
    "pattern",
    "purity",
    "pattern_strength",
    "damage_ids",
    "rescue_ids",
    "integrity",
    "grade",
    "achievement",
    "wealth_profile",
    "career_profile",
    "strength",
    "useful_god",
    "temperature",
    "five_elements",
    "chart_id",
)


@dataclass(frozen=True, slots=True)
class Mc01StructuralSnapshot:
    """Immutable copy of live Mệnh Cục structural identifiers."""

    analysis_id: str = ""
    chart_id: str = ""
    mingju_result_id: str = ""
    schema_version: str = SCHEMA_MINGJU_DECISION
    ruleset_version: str = MC01_RULESET_VERSION
    content_hash: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    pattern: str = ""
    purity: str = ""
    pattern_strength: str = ""
    damage_ids: tuple[str, ...] = ()
    rescue_ids: tuple[str, ...] = ()
    integrity: str = ""
    grade: str = ""
    achievement: str = ""
    wealth_profile: str = ""
    career_profile: str = ""
    strength: str = ""
    useful_god: str = ""
    temperature: str = ""
    five_elements: str = ""
    reject_reason: str = ""
    source_versions: dict[str, str] = field(default_factory=dict)

    @property
    def bound(self) -> bool:
        """True when the snapshot is a usable MC-01 reference."""
        return bool(
            self.mingju_result_id
            and self.content_hash
            and self.pattern
            and self.grade
            and not self.reject_reason
            and self.status is EvaluationStatus.RESOLVED
        )

    def canonical_payload(self) -> dict[str, Any]:
        """Structural content hashed for MC-01 identity. created_at excluded."""
        return {
            "schema_version": self.schema_version,
            "ruleset_version": self.ruleset_version,
            "pattern": self.pattern,
            "purity": self.purity,
            "pattern_strength": self.pattern_strength,
            "damage_ids": list(self.damage_ids),
            "rescue_ids": list(self.rescue_ids),
            "integrity": self.integrity,
            "grade": self.grade,
            "achievement": self.achievement,
            "wealth_profile": self.wealth_profile,
            "career_profile": self.career_profile,
            "strength": self.strength,
            "useful_god": self.useful_god,
            "temperature": self.temperature,
            "five_elements": self.five_elements,
            "chart_id": self.chart_id,
        }

    def reference(self) -> Mc01Reference:
        """Frozen Pack 07 pointer. Not a second structural engine."""
        if not self.bound:
            return Mc01Reference(status=EvaluationStatus.NOT_EVALUATED)
        return Mc01Reference(
            mingju_result_id=self.mingju_result_id,
            schema_version=self.schema_version,
            ruleset_version=self.ruleset_version,
            content_hash=self.content_hash,
            status=self.status,
        )

    def to_payload(self) -> dict[str, Any]:
        """Internal payload block. Stripped from customer JSON."""
        return {
            "mingju_result_id": self.mingju_result_id,
            "schema_version": self.schema_version,
            "ruleset_version": self.ruleset_version,
            "content_hash": self.content_hash,
            "status": self.status.value,
            "analysis_id": self.analysis_id,
            "chart_id": self.chart_id,
            "pattern": self.pattern,
            "purity": self.purity,
            "pattern_strength": self.pattern_strength,
            "damage_ids": list(self.damage_ids),
            "rescue_ids": list(self.rescue_ids),
            "integrity": self.integrity,
            "grade": self.grade,
            "achievement": self.achievement,
            "wealth_profile": self.wealth_profile,
            "career_profile": self.career_profile,
            "strength": self.strength,
            "useful_god": self.useful_god,
            "temperature": self.temperature,
            "five_elements": self.five_elements,
            "source_versions": dict(self.source_versions),
        }


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _first_text(mapping: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        text = as_str(mapping.get(key)).strip()
        if text:
            return text
    return ""


def _id_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str) and value.strip():
        return (value.strip(),)
    if not isinstance(value, (list, tuple)):
        return ()
    found: list[str] = []
    for item in value:
        if isinstance(item, Mapping):
            token = _first_text(item, "id", "damage_id", "rescue_id")
        else:
            token = as_str(item).strip()
        if token and token not in found:
            found.append(token)
    return tuple(found)


def _pattern_strength(pattern: Mapping[str, Any]) -> str:
    level = as_str(pattern.get("qualification_level")).strip()
    if level:
        return level
    score = pattern.get("score")
    if score is None or score == "":
        return ""
    return as_str(score).strip()


def _five_elements_ref(block: Mapping[str, Any]) -> str:
    if not block:
        return ""
    keys = sorted(str(key) for key in block.keys())
    return ",".join(keys) if keys else "five_elements"


def _mingju_result_id(analysis_id: str, chart_id: str, content_hash: str) -> str:
    if analysis_id:
        return f"mc01:{analysis_id}"
    if chart_id:
        return f"mc01:{chart_id}:{content_hash[:16]}"
    return f"mc01:{content_hash[:16]}"


def _snapshot_from_mingju(
    mingju: Mapping[str, Any],
    payload: Mapping[str, Any],
) -> Mc01StructuralSnapshot:
    """Copy canonical MingJuDecisionResult identifiers. Do not use ScoreEngine grade."""
    pattern_block = _mapping(mingju.get("pattern"))
    purity_block = _mapping(mingju.get("purity"))
    strength_block = _mapping(mingju.get("pattern_strength"))
    integrity_block = _mapping(mingju.get("integrity"))
    grade_block = _mapping(mingju.get("grade"))
    achievement_block = _mapping(mingju.get("achievement"))
    wealth_block = _mapping(mingju.get("wealth") or mingju.get("wealth_profile"))
    career_block = _mapping(mingju.get("career") or mingju.get("career_profile"))
    pattern_ref = (
        _first_text(mingju, "pattern")
        if not pattern_block
        else _first_text(pattern_block, "label", "id") or _first_text(mingju, "pattern")
    )
    if isinstance(mingju.get("pattern"), str):
        pattern_ref = as_str(mingju.get("pattern")).strip()
    grade_ref = (
        _first_text(mingju, "grade")
        if not grade_block
        else _first_text(grade_block, "grade")
    )
    if isinstance(mingju.get("grade"), str):
        grade_ref = as_str(mingju.get("grade")).strip()
    purity_ref = (
        _first_text(mingju, "purity")
        if not purity_block
        else _first_text(purity_block, "classification", "state")
    )
    if isinstance(mingju.get("purity"), str):
        purity_ref = as_str(mingju.get("purity")).strip()
    strength_ref = (
        _first_text(mingju, "pattern_strength")
        if not strength_block
        else _first_text(strength_block, "classification", "state")
    )
    if isinstance(mingju.get("pattern_strength"), str):
        strength_ref = as_str(mingju.get("pattern_strength")).strip()
    integrity_ref = (
        _first_text(mingju, "integrity")
        if not integrity_block
        else _first_text(integrity_block, "state", "classification")
    )
    if isinstance(mingju.get("integrity"), str):
        integrity_ref = as_str(mingju.get("integrity")).strip()
    analysis_id = _first_text(mingju, "analysis_id") or _first_text(payload, "analysis_id", "request_id")
    chart_id = _first_text(mingju, "chart_id") or _first_text(payload, "chart_id")
    strength = _mapping(payload.get("strength"))
    useful_god = _mapping(payload.get("useful_god"))
    temperature = _mapping(payload.get("temperature"))
    five_elements = _mapping(payload.get("five_elements"))
    draft = Mc01StructuralSnapshot(
        analysis_id=analysis_id,
        chart_id=chart_id,
        schema_version=_first_text(mingju, "schema_version") or SCHEMA_MINGJU_DECISION,
        ruleset_version=_first_text(mingju, "ruleset_version") or MC01_RULESET_VERSION,
        pattern=pattern_ref,
        purity=purity_ref,
        pattern_strength=strength_ref,
        damage_ids=_id_tuple(mingju.get("damage_ids") or mingju.get("damage")),
        rescue_ids=_id_tuple(mingju.get("rescue_ids") or mingju.get("rescue")),
        integrity=integrity_ref,
        grade=grade_ref,
        achievement=_first_text(mingju, "achievement")
        or _first_text(achievement_block, "state")
        or ",".join(str(item) for item in (achievement_block.get("dominant_capabilities") or []) if item),
        wealth_profile=_first_text(mingju, "wealth_profile")
        or _first_text(wealth_block, "state", "id", "band"),
        career_profile=_first_text(mingju, "career_profile")
        or _first_text(career_block, "state", "id", "band")
        or ",".join(str(item) for item in (career_block.get("dominant_work_styles") or []) if item),
        strength=_first_text(strength, "strength_level", "than_vuong_nhuoc"),
        useful_god=_first_text(
            useful_god, "useful_display", "useful_god", "dung_than", "overall_useful_god"
        ),
        temperature=_first_text(
            temperature, "climate_state", "temperature_level", "temperature_type"
        ),
        five_elements=_five_elements_ref(five_elements),
        source_versions={
            "mingju": "bte.mingju.rules.v1",
            "pattern": "canonical_pattern_engine",
        },
    )
    content_hash = compute_content_hash(draft.canonical_payload())
    return Mc01StructuralSnapshot(
        analysis_id=draft.analysis_id,
        chart_id=draft.chart_id,
        mingju_result_id=_first_text(mingju, "result_id", "mingju_result_id")
        or _mingju_result_id(draft.analysis_id, draft.chart_id, content_hash),
        schema_version=draft.schema_version,
        ruleset_version=draft.ruleset_version,
        content_hash=content_hash,
        status=EvaluationStatus.RESOLVED,
        pattern=draft.pattern,
        purity=draft.purity,
        pattern_strength=draft.pattern_strength,
        damage_ids=draft.damage_ids,
        rescue_ids=draft.rescue_ids,
        integrity=draft.integrity,
        grade=draft.grade,
        achievement=draft.achievement,
        wealth_profile=draft.wealth_profile,
        career_profile=draft.career_profile,
        strength=draft.strength,
        useful_god=draft.useful_god,
        temperature=draft.temperature,
        five_elements=draft.five_elements,
        source_versions=dict(draft.source_versions),
    )


def snapshot_from_live_payload(payload: Mapping[str, Any] | None) -> Mc01StructuralSnapshot | None:
    """Prefer canonical MingJuDecisionResult. Pattern+Score is labeled legacy only."""
    data = payload or {}
    mingju = _mapping(data.get("_mingju")) or _mapping(data.get("mingju"))
    if _first_text(mingju, "pattern", "pattern_id") or _mapping(mingju.get("pattern")):
        grade_present = bool(_first_text(mingju, "grade") or _mapping(mingju.get("grade")))
        pattern_present = bool(
            _first_text(mingju, "pattern", "pattern_id") or _first_text(_mapping(mingju.get("pattern")), "label", "id")
        )
        source = _first_text(mingju, "source")
        schema = _first_text(mingju, "schema_version")
        if pattern_present and grade_present and (
            source == "mingju_decision_engine" or schema == SCHEMA_MINGJU_DECISION or data.get("_mingju")
        ):
            snapshot = _snapshot_from_mingju(mingju, data)
            if snapshot.pattern and snapshot.grade:
                return snapshot
    pattern = _mapping(data.get("pattern"))
    score = _mapping(data.get("score"))
    strength = _mapping(data.get("strength"))
    useful_god = _mapping(data.get("useful_god"))
    temperature = _mapping(data.get("temperature"))
    five_elements = _mapping(data.get("five_elements"))
    integrity = _mapping(data.get("integrity"))
    identity = _mapping(data.get("identity"))
    person = _mapping(identity.get("person"))
    calendar = _mapping(identity.get("calendar")) or _mapping(data.get("calendar"))
    analysis_id = _first_text(data, "analysis_id", "request_id")
    chart_id = (
        _first_text(data, "chart_id")
        or _first_text(calendar, "solar_date")
        or _first_text(person, "solar_birth")
    )
    pattern_ref = _first_text(pattern, "cach_cuc", "pattern", "tong_cach")
    grade_ref = _first_text(pattern, "structural_grade") or _first_text(score, "grade")
    if not pattern_ref or not grade_ref:
        return None
    used_mc01_grade = bool(_first_text(pattern, "structural_grade"))
    draft = Mc01StructuralSnapshot(
        analysis_id=analysis_id,
        chart_id=chart_id,
        schema_version=SCHEMA_MINGJU_DECISION,
        ruleset_version="bte.mingju.rules.v1" if used_mc01_grade else MC01_RULESET_VERSION,
        pattern=pattern_ref,
        purity=_first_text(pattern, "structural_purity", "purity") or _first_text(data, "purity"),
        pattern_strength=_first_text(pattern, "structural_strength") or _pattern_strength(pattern),
        damage_ids=_id_tuple(data.get("damage_ids") or data.get("damage")),
        rescue_ids=_id_tuple(data.get("rescue_ids") or data.get("rescue")),
        integrity=_first_text(pattern, "structural_integrity")
        or _first_text(integrity, "id", "state", "integrity_ref")
        or _first_text(data, "integrity"),
        grade=grade_ref,
        achievement=_first_text(data, "achievement"),
        wealth_profile=_first_text(_mapping(data.get("wealth_profile")), "id", "band", "state")
        or _first_text(data, "wealth_profile"),
        career_profile=_first_text(_mapping(data.get("career_profile")), "id", "band", "state")
        or _first_text(data, "career_profile"),
        strength=_first_text(strength, "strength_level", "than_vuong_nhuoc"),
        useful_god=_first_text(
            useful_god, "useful_display", "useful_god", "dung_than", "overall_useful_god"
        ),
        temperature=_first_text(
            temperature, "climate_state", "temperature_level", "temperature_type"
        ),
        five_elements=_five_elements_ref(five_elements),
        source_versions=(
            {"mingju": "bte.mingju.rules.v1", "pattern": "canonical_pattern_engine"}
            if used_mc01_grade
            else {
                "pattern": "pattern_rule_context_v1",
                "score": "score_rule_context_v1",
                "legacy_surrogate": "pattern_plus_score",
            }
        ),
    )
    content_hash = compute_content_hash(draft.canonical_payload())
    return Mc01StructuralSnapshot(
        analysis_id=draft.analysis_id,
        chart_id=draft.chart_id,
        mingju_result_id=_mingju_result_id(draft.analysis_id, draft.chart_id, content_hash),
        schema_version=draft.schema_version,
        ruleset_version=draft.ruleset_version,
        content_hash=content_hash,
        status=EvaluationStatus.RESOLVED,
        pattern=draft.pattern,
        purity=draft.purity,
        pattern_strength=draft.pattern_strength,
        damage_ids=draft.damage_ids,
        rescue_ids=draft.rescue_ids,
        integrity=draft.integrity,
        grade=draft.grade,
        achievement=draft.achievement,
        wealth_profile=draft.wealth_profile,
        career_profile=draft.career_profile,
        strength=draft.strength,
        useful_god=draft.useful_god,
        temperature=draft.temperature,
        five_elements=draft.five_elements,
        source_versions=dict(draft.source_versions),
    )


def _existing_analysis_id(raw: Mapping[str, Any]) -> str:
    explicit = _first_text(raw, "analysis_id")
    if explicit:
        return explicit
    mingju_id = _first_text(raw, "mingju_result_id", "id")
    if mingju_id.startswith("mc01:"):
        rest = mingju_id[5:]
        if rest and ":" not in rest:
            return rest
    return ""


def validate_existing_mc01(
    payload: Mapping[str, Any],
    computed: Mc01StructuralSnapshot | None,
) -> str:
    """Return a reject reason when an attached MC-01 pointer is stale or foreign."""
    raw = _mapping(payload.get("mc01")) or _mapping(payload.get("mingju"))
    if not raw:
        return ""
    existing_hash = _first_text(raw, "content_hash")
    existing_id = _first_text(raw, "mingju_result_id", "id")
    existing_analysis = _existing_analysis_id(raw)
    payload_analysis = _first_text(payload, "analysis_id", "request_id")
    if not existing_hash and not existing_id:
        return ""
    if computed is None:
        return REJECT_INCOMPLETE
    if existing_hash and existing_hash != computed.content_hash:
        return REJECT_HASH_MISMATCH
    if existing_analysis and payload_analysis and existing_analysis != payload_analysis:
        return REJECT_LINEAGE_MISMATCH
    if existing_id and payload_analysis:
        expected = _mingju_result_id(payload_analysis, computed.chart_id, computed.content_hash)
        if existing_id != expected and existing_id != computed.mingju_result_id:
            return REJECT_STALE_REFERENCE
    return ""


def attach_mc01_reference(payload: dict[str, Any]) -> dict[str, Any]:
    """Bind a fresh current-result snapshot onto an analyze-shaped payload."""
    payload.pop(MC01_BIND_REJECT_KEY, None)
    computed = snapshot_from_live_payload(payload)
    reason = validate_existing_mc01(payload, computed)
    if reason:
        payload.pop("mc01", None)
        payload.pop("mingju", None)
        payload.pop("_mc01_snapshot", None)
        payload[MC01_BIND_REJECT_KEY] = reason
        return payload
    if computed is None or not computed.bound:
        return payload
    payload["mc01"] = computed.to_payload()
    payload["_mc01_snapshot"] = computed.canonical_payload()
    return payload


def snapshot_hash_matches(snapshot: Mapping[str, Any] | str | None, content_hash: str) -> bool:
    """True when an attached snapshot hashes to the MC-01 pointer."""
    if not content_hash:
        return False
    if isinstance(snapshot, str):
        if snapshot == content_hash:
            return True
        try:
            payload = json.loads(snapshot)
        except (TypeError, ValueError):
            return False
    else:
        payload = snapshot
    if not isinstance(payload, Mapping):
        return False
    canonical = {key: payload.get(key) for key in _SNAPSHOT_KEYS if key in payload}
    return compute_content_hash(canonical) == content_hash
