"""Evidence Builder — CanonicalAnalysis → NarrativeEvidenceContext.

Extracts published facts only. Does not interpret, calculate, or write prose.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_v2.evidence.evidence_context import (
    EvidenceContractGap,
    NarrativeEvidenceContext,
)
from engines.narrative_v2.evidence.evidence_errors import EvidenceError, EvidenceValidationError
from engines.narrative_v2.evidence.evidence_item import (
    STATUS_AVAILABLE,
    STATUS_MISSING,
    STATUS_UNSUPPORTED,
    EvidenceItem,
    EvidenceValue,
)
from engines.narrative_v2.evidence.evidence_reference import EvidenceReference
from engines.narrative_v2.evidence.evidence_registry import (
    FORBIDDEN_SOURCE_PREFIXES,
    EvidenceFieldSpec,
    EvidenceRegistry,
)
from engines.narrative_v2.evidence.evidence_validator import EvidenceValidator

_MISSING = object()

FALLBACK_PATHS: dict[str, tuple[str, ...]] = {
    "identity.person.gender": ("input.gender",),
    "identity.person.timezone": ("calendar.timezone", "input.timezone"),
    "analysis_id": ("request_id", "result_meta.analysis_id"),
    "calendar.timezone": ("identity.person.timezone", "calendar.timezone_name"),
}

GAP_IF_MISSING: frozenset[str] = frozenset(
    {
        "evidence.identity.name",
        "evidence.identity.birth_place",
        "evidence.identity.analysis_id",
    }
)


class EvidenceBuilder:
    """Canonical evidence extraction. Shadow mode. No narrative."""

    def __init__(
        self,
        *,
        registry: EvidenceRegistry | None = None,
        validator: EvidenceValidator | None = None,
    ) -> None:
        self._registry = registry or EvidenceRegistry()
        self._validator = validator or EvidenceValidator()

    def build(self, canonical_analysis: object) -> NarrativeEvidenceContext:
        """Extract EvidenceContext from published CanonicalAnalysis."""
        payload = _as_mapping(canonical_analysis)
        items: list[EvidenceItem] = []
        for spec in self._registry.specs():
            items.append(self._extract_spec(payload, spec))
        items.extend(self._extract_ten_gods(payload))
        items.extend(self._extract_shensha(payload))
        items.extend(self._extract_luck_periods(payload))
        items.sort(key=lambda item: item.evidence_id)
        context = self._assemble(items)
        self._validator.assert_valid(context)
        return context

    def _extract_spec(
        self,
        payload: Mapping[str, Any],
        spec: EvidenceFieldSpec,
    ) -> EvidenceItem:
        raw, path = _read_with_fallback(payload, spec.source_path)
        return _item_from_raw(spec=spec, raw=raw, source_path=path)

    def _extract_ten_gods(self, payload: Mapping[str, Any]) -> tuple[EvidenceItem, ...]:
        section = payload.get("ten_gods")
        if not isinstance(section, Mapping):
            return (
                _missing_item(
                    "evidence.ten_gods.visible",
                    "ten_gods",
                    "visible",
                    "visible ten gods",
                    "ten_gods.visible",
                ),
            )
        items: list[EvidenceItem] = []
        items.append(
            _item_from_raw(
                spec=EvidenceFieldSpec(
                    evidence_id="evidence.ten_gods.visible_labels",
                    domain="ten_gods",
                    key="visible_labels",
                    label="visible ten gods",
                    source_path="ten_gods.visible_labels",
                ),
                raw=section.get("visible_labels", _MISSING),
                source_path="ten_gods.visible_labels",
            )
        )
        items.append(
            _item_from_raw(
                spec=EvidenceFieldSpec(
                    evidence_id="evidence.ten_gods.hidden_labels",
                    domain="ten_gods",
                    key="hidden_labels",
                    label="hidden ten gods",
                    source_path="ten_gods.hidden_labels",
                ),
                raw=section.get("hidden_labels", _MISSING),
                source_path="ten_gods.hidden_labels",
            )
        )
        visible = section.get("visible") or []
        if isinstance(visible, list):
            for entry in visible:
                if not isinstance(entry, Mapping):
                    continue
                pillar = str(entry.get("pillar") or "").strip()
                ten_god = entry.get("ten_god")
                if not pillar:
                    continue
                items.append(
                    _item_from_raw(
                        spec=EvidenceFieldSpec(
                            evidence_id=f"evidence.ten_gods.visible.{pillar}",
                            domain="ten_gods",
                            key=f"visible.{pillar}",
                            label=f"visible {pillar}",
                            source_path=f"ten_gods.visible.{pillar}.ten_god",
                        ),
                        raw=ten_god if ten_god not in (None, "") else _MISSING,
                        source_path=f"ten_gods.visible.{pillar}.ten_god",
                    )
                )
        return tuple(items)

    def _extract_shensha(self, payload: Mapping[str, Any]) -> tuple[EvidenceItem, ...]:
        bazi = payload.get("bazi")
        if not isinstance(bazi, Mapping):
            return (
                _missing_item(
                    "evidence.shensha.names",
                    "shensha",
                    "names",
                    "shensha names",
                    "bazi.shensha",
                ),
            )
        items: list[EvidenceItem] = []
        names = bazi.get("shensha")
        items.append(
            _item_from_raw(
                spec=EvidenceFieldSpec(
                    evidence_id="evidence.shensha.names",
                    domain="shensha",
                    key="names",
                    label="shensha names",
                    source_path="bazi.shensha",
                ),
                raw=names if names is not None else _MISSING,
                source_path="bazi.shensha",
            )
        )
        matches = bazi.get("shensha_matches") or []
        if isinstance(matches, list):
            for match in matches:
                if not isinstance(match, Mapping):
                    continue
                match_id = str(match.get("id") or match.get("canonical_name") or "").strip()
                if not match_id:
                    continue
                placement = str(match.get("pillar") or match.get("location") or "").strip()
                suffix = f".{placement}" if placement else ""
                items.append(
                    _item_from_raw(
                        spec=EvidenceFieldSpec(
                            evidence_id=f"evidence.shensha.{match_id}{suffix}",
                            domain="shensha",
                            key=f"{match_id}{suffix}",
                            label=str(match.get("canonical_name") or match_id),
                            source_path=f"bazi.shensha_matches.{match_id}",
                        ),
                        raw=placement or str(match.get("canonical_name") or match_id),
                        source_path=f"bazi.shensha_matches.{match_id}",
                    )
                )
        return tuple(items)

    def _extract_luck_periods(self, payload: Mapping[str, Any]) -> tuple[EvidenceItem, ...]:
        luck = payload.get("luck")
        if not isinstance(luck, Mapping):
            return ()
        items: list[EvidenceItem] = []
        cycles = luck.get("cycles") or []
        if not isinstance(cycles, list):
            return ()
        current = luck.get("current_cycle")
        current_index: int | None = None
        if isinstance(current, Mapping) and current.get("index") is not None:
            current_index = int(current["index"])
        for entry in cycles:
            if not isinstance(entry, Mapping):
                continue
            index = int(entry.get("index") if entry.get("index") is not None else len(items))
            gan_zhi = str(entry.get("gan_zhi") or "").strip()
            items.append(
                _item_from_raw(
                    spec=EvidenceFieldSpec(
                        evidence_id=f"evidence.luck.cycle.{index}",
                        domain="luck",
                        key=f"cycle.{index}",
                        label=f"luck cycle {index}",
                        source_path=f"luck.cycles.{index}.gan_zhi",
                    ),
                    raw=gan_zhi or _MISSING,
                    source_path=f"luck.cycles.{index}.gan_zhi",
                )
            )
        if current_index is not None:
            nxt = current_index + 1
            next_entry = next(
                (
                    entry
                    for entry in cycles
                    if isinstance(entry, Mapping) and int(entry.get("index") or -1) == nxt
                ),
                None,
            )
            next_value = (
                str(next_entry.get("gan_zhi") or "").strip()
                if isinstance(next_entry, Mapping)
                else ""
            )
            items.append(
                _item_from_raw(
                    spec=EvidenceFieldSpec(
                        evidence_id="evidence.luck.next_cycle",
                        domain="luck",
                        key="next_cycle",
                        label="next luck cycle",
                        source_path=f"luck.cycles.{nxt}.gan_zhi",
                    ),
                    raw=next_value or _MISSING,
                    source_path=f"luck.cycles.{nxt}.gan_zhi",
                )
            )
        return tuple(items)

    def _assemble(self, items: list[EvidenceItem]) -> NarrativeEvidenceContext:
        by_domain = {domain: [] for domain in self._registry.allowed_domains()}
        references: list[EvidenceReference] = []
        for item in items:
            by_domain.setdefault(item.domain, []).append(item)
            if item.source_path:
                references.append(
                    EvidenceReference(source_path=item.source_path, domain=item.domain)
                )
        gaps = tuple(_contract_gaps(items))
        available = sum(1 for item in items if item.status == STATUS_AVAILABLE)
        metadata = (
            ("builder_version", "0.1.0-evidence"),
            ("shadow_mode", "true"),
            ("item_count", str(len(items))),
            ("available_count", str(available)),
            ("gap_count", str(len(gaps))),
        )
        return NarrativeEvidenceContext(
            identity=tuple(by_domain.get("identity", ())),
            calendar=tuple(by_domain.get("calendar", ())),
            bazi=tuple(by_domain.get("bazi", ())),
            strength=tuple(by_domain.get("strength", ())),
            temperature=tuple(by_domain.get("temperature", ())),
            pattern=tuple(by_domain.get("pattern", ())),
            useful_god=tuple(by_domain.get("useful_god", ())),
            five_elements=tuple(by_domain.get("five_elements", ())),
            ten_gods=tuple(by_domain.get("ten_gods", ())),
            shensha=tuple(by_domain.get("shensha", ())),
            luck=tuple(by_domain.get("luck", ())),
            references=tuple(references),
            metadata=metadata,
            items=tuple(items),
            contract_gaps=gaps,
        )


def _as_mapping(canonical_analysis: object) -> dict[str, Any]:
    if canonical_analysis is None:
        return {}
    if isinstance(canonical_analysis, Mapping):
        return _public_payload(dict(canonical_analysis))
    raise EvidenceError("CanonicalAnalysis must be a published mapping")


def _public_payload(payload: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(payload)
    for prefix in FORBIDDEN_SOURCE_PREFIXES:
        cleaned.pop(prefix, None)
    return cleaned


def _read_path(payload: Mapping[str, Any], path: str) -> object:
    current: object = payload
    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return _MISSING
        current = current[part]
    return current


def _read_with_fallback(
    payload: Mapping[str, Any],
    source_path: str,
) -> tuple[object, str]:
    raw = _read_path(payload, source_path)
    raw, path = _unwrap_named(raw, source_path)
    if raw is not _MISSING and not _is_empty(raw):
        return raw, path
    for fallback in FALLBACK_PATHS.get(source_path, ()):
        candidate = _read_path(payload, fallback)
        candidate, candidate_path = _unwrap_named(candidate, fallback)
        if candidate is not _MISSING and not _is_empty(candidate):
            return candidate, candidate_path
    return raw, path


def _unwrap_named(raw: object, path: str) -> tuple[object, str]:
    """Read a published name wrapper. Does not invent values."""
    if not isinstance(raw, Mapping):
        return raw, path
    allowed = {"name", "offset_hours", "index"}
    if "name" in raw and set(raw).issubset(allowed):
        return raw.get("name"), f"{path}.name"
    return raw, path


def _is_empty(raw: object) -> bool:
    if raw is None:
        return True
    if isinstance(raw, str) and not raw.strip():
        return True
    if isinstance(raw, (list, tuple)) and len(raw) == 0:
        return True
    return False


def _normalize_value(raw: object) -> tuple[EvidenceValue, str]:
    if raw is _MISSING or _is_empty(raw):
        return None, STATUS_MISSING
    if isinstance(raw, (str, int, float, bool)):
        return raw, STATUS_AVAILABLE
    if isinstance(raw, (list, tuple)):
        parts: list[str | int | float | bool] = []
        for entry in raw:
            if isinstance(entry, (str, int, float, bool)):
                parts.append(entry)
            else:
                raise EvidenceValidationError("Raw runtime/debug objects are rejected")
        if not parts:
            return None, STATUS_MISSING
        return tuple(parts), STATUS_AVAILABLE
    raise EvidenceValidationError("Raw runtime/debug objects are rejected")


def _item_from_raw(
    *,
    spec: EvidenceFieldSpec,
    raw: object,
    source_path: str,
) -> EvidenceItem:
    value, status = _normalize_value(raw)
    return EvidenceItem(
        evidence_id=spec.evidence_id,
        domain=spec.domain,
        key=spec.key,
        label=spec.label,
        value=value,
        source_path=source_path,
        status=status,
        references=(EvidenceReference(source_path=source_path, domain=spec.domain),),
    )


def _missing_item(
    evidence_id: str,
    domain: str,
    key: str,
    label: str,
    source_path: str,
) -> EvidenceItem:
    return EvidenceItem(
        evidence_id=evidence_id,
        domain=domain,
        key=key,
        label=label,
        value=None,
        source_path=source_path,
        status=STATUS_UNSUPPORTED,
        references=(EvidenceReference(source_path=source_path, domain=domain),),
    )


def _contract_gaps(items: list[EvidenceItem]) -> list[EvidenceContractGap]:
    gaps: list[EvidenceContractGap] = []
    for item in items:
        if item.evidence_id not in GAP_IF_MISSING:
            continue
        if item.status in {STATUS_MISSING, STATUS_UNSUPPORTED}:
            gaps.append(
                EvidenceContractGap(
                    field=item.key,
                    reason="EVIDENCE CONTRACT GAP: field is not published by CanonicalAnalysis",
                    source_path=item.source_path,
                )
            )
    return gaps
