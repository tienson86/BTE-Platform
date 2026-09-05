"""P7-IMP-07 MC-01 canonical binding and structural context completion."""

from __future__ import annotations

from copy import deepcopy

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.constants import (
    MC01_BIND_REJECT_KEY,
    MC01_OWNERSHIP_DAMAGE_CODE,
)
from engines.detailed_interpretation_engine.diagnostics import (
    build_pack07_diagnostics,
    diagnostics_from_payload,
)
from engines.detailed_interpretation_engine.enums import (
    CombinationState,
    DiagnosticStatus,
    EvaluationStatus,
    ValidationStatus,
)
from engines.detailed_interpretation_engine.mc01 import (
    REJECT_HASH_MISMATCH,
    REJECT_LINEAGE_MISMATCH,
    attach_mc01_reference,
    snapshot_from_live_payload,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.engine import (
    interpret_ten_god_combinations,
)
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods, interpret_ten_gods
from engines.detailed_interpretation_engine.ten_gods.facts import extract_ten_god_facts
from engines.detailed_interpretation_engine.validators import (
    validate_canonical_runtime,
    validate_interpretation_context,
)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "analysis_id": "an-p7-mc01-001",
        "pattern": {"cach_cuc": "Chính Ấn", "pattern": "Chính Ấn", "score": 86.0, "qualification_level": "established"},
        "score": {"grade": "B"},
        "strength": {"strength_level": "balanced"},
        "useful_god": {"useful_display": "Thủy"},
        "temperature": {"climate_state": "warm"},
        "five_elements": {"wood": {"count": 2}, "water": {"count": 1}},
        "identity": {
            "person": {"solar_birth": "1987-01-21", "gender": "male"},
            "calendar": {"solar_date": "1987-01-21"},
            "four_pillars": {"hour": {"stem": "Bính", "branch": "Dần"}},
        },
        "ten_gods": {
            "source": "engines.ten_gods_engine",
            "visible": [
                {
                    "pillar": "month",
                    "stem": "Ất",
                    "ten_god": "Chính Ấn",
                    "god_id": "zheng_yin",
                    "element": "Mộc",
                }
            ],
            "hidden": [],
        },
    }
    body.update(extra)
    return body


def test_empty_context_stays_unbound() -> None:
    diagnostics = build_pack07_diagnostics(
        build_canonical_analysis_context_from_payload({"analysis_id": "dev-empty"})
    )
    assert diagnostics.mc01_reference is DiagnosticStatus.NOT_BOUND


def test_live_pattern_and_grade_bind_without_inventing_unpublished_layers() -> None:
    payload = attach_mc01_reference(_payload())
    snapshot = snapshot_from_live_payload(payload)
    assert snapshot is not None
    assert snapshot.bound
    assert snapshot.pattern == "Chính Ấn"
    assert snapshot.grade == "B"
    assert snapshot.purity == ""
    assert snapshot.damage_ids == ()
    assert snapshot.rescue_ids == ()
    assert snapshot.integrity == ""
    assert snapshot.achievement == ""
    assert snapshot.wealth_profile == ""
    assert snapshot.career_profile == ""
    assert snapshot.pattern_strength == "established"
    context = build_canonical_analysis_context_from_payload(payload)
    assert context.interpretation.mc01.mingju_result_id == "mc01:an-p7-mc01-001"
    assert context.interpretation.pattern_ref == "Chính Ấn"
    assert context.interpretation.grade_ref == "B"
    assert context.runtime.mc01.content_hash == snapshot.content_hash
    diagnostics = build_pack07_diagnostics(context)
    assert diagnostics.mc01_reference is DiagnosticStatus.PASS


def test_stale_hash_cannot_bind() -> None:
    payload = _payload()
    payload["mc01"] = {
        "mingju_result_id": "mc01:an-p7-mc01-001",
        "analysis_id": "an-p7-mc01-001",
        "content_hash": "0" * 64,
    }
    attach_mc01_reference(payload)
    assert payload.get("mc01") is None
    assert payload[MC01_BIND_REJECT_KEY] == REJECT_HASH_MISMATCH
    context = build_canonical_analysis_context_from_payload(payload)
    assert context.interpretation.mc01.mingju_result_id == ""
    assert build_pack07_diagnostics(context).mc01_reference is DiagnosticStatus.NOT_BOUND


def test_different_analysis_id_fails_closed() -> None:
    fresh = attach_mc01_reference(_payload())
    hash_value = fresh["mc01"]["content_hash"]
    payload = _payload()
    payload["mc01"] = {
        "mingju_result_id": "mc01:other-analysis",
        "analysis_id": "other-analysis",
        "content_hash": hash_value,
    }
    attach_mc01_reference(payload)
    assert payload.get("mc01") is None
    assert payload[MC01_BIND_REJECT_KEY] == REJECT_LINEAGE_MISMATCH


def test_different_hash_fails_closed() -> None:
    payload = _payload()
    other = attach_mc01_reference(_payload(pattern={"cach_cuc": "Chính Quan", "pattern": "Chính Quan"}))
    payload["mc01"] = {
        "mingju_result_id": "mc01:an-p7-mc01-001",
        "analysis_id": "an-p7-mc01-001",
        "content_hash": other["mc01"]["content_hash"],
    }
    attach_mc01_reference(payload)
    assert payload[MC01_BIND_REJECT_KEY] == REJECT_HASH_MISMATCH


def test_pack07_does_not_modify_pattern_or_grade() -> None:
    original = _payload()
    snapshot = deepcopy(original)
    bound = attach_mc01_reference(original)
    context = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(bound),
        bound,
    )
    assert bound["pattern"] == snapshot["pattern"]
    assert bound["score"] == snapshot["score"]
    assert context.interpretation.pattern_ref == "Chính Ấn"
    assert context.interpretation.grade_ref == "B"
    serialized = context.runtime.interpretation
    assert getattr(serialized, "pattern", None) in (None, "")
    assert "pattern" not in (serialized.ten_gods.finding_ids or ())


def test_pack07_cannot_create_damage_or_rescue_ids() -> None:
    payload = attach_mc01_reference(_payload())
    facts = extract_ten_god_facts(payload)
    assert facts.damage_ids == ()
    assert facts.rescue_ids == ()
    collection = interpret_ten_gods(payload, analysis_id="an-p7-mc01-001")
    assert all(item.damage_ids == () and item.rescue_ids == () for item in collection.items)
    combos = interpret_ten_god_combinations(
        collection,
        mc01_bound=True,
        damage_ids=facts.damage_ids,
        rescue_ids=facts.rescue_ids,
    )
    assert all(item.damage_ids == () and item.rescue_ids == () for item in combos.items)


def test_history_mc01_cannot_override_current() -> None:
    current = attach_mc01_reference(_payload())
    history = attach_mc01_reference(
        _payload(analysis_id="hist-old", pattern={"cach_cuc": "Thất Sát", "pattern": "Thất Sát"})
    )
    mixed = _payload()
    mixed["mc01"] = history["mc01"]
    attach_mc01_reference(mixed)
    assert mixed.get("mc01") is None
    assert mixed[MC01_BIND_REJECT_KEY] in {REJECT_HASH_MISMATCH, REJECT_LINEAGE_MISMATCH}
    restored = attach_mc01_reference(_payload())
    assert restored["mc01"]["content_hash"] == current["mc01"]["content_hash"]
    assert restored["mc01"]["pattern"] == "Chính Ấn"


def test_presentation_change_does_not_change_mc01_hash() -> None:
    first = snapshot_from_live_payload(_payload())
    second = snapshot_from_live_payload(
        _payload(
            ten_gods={
                "source": "engines.ten_gods_engine",
                "visible": [],
                "hidden": [],
                "detailed": {"label": "changed presentation"},
            }
        )
    )
    assert first is not None and second is not None
    assert first.content_hash == second.content_hash


def test_created_at_excluded_from_mc01_hash() -> None:
    first = snapshot_from_live_payload(_payload(created_at="2020-01-01T00:00:00Z"))
    second = snapshot_from_live_payload(_payload(created_at="2026-09-05T00:00:00Z"))
    assert first is not None and second is not None
    assert first.content_hash == second.content_hash


def test_unbind_falls_back_not_guessed() -> None:
    unbound = _payload()
    context = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(unbound),
        unbound,
    )
    natal = context.runtime.interpretation.ten_gods.natal
    assert natal.state is EvaluationStatus.PARTIALLY_RESOLVED
    assert context.interpretation.mc01.mingju_result_id == ""
    assert build_pack07_diagnostics(context).mc01_reference is DiagnosticStatus.NOT_BOUND
    bound = attach_mc01_reference(_payload())
    restored = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(bound),
        bound,
    )
    assert restored.interpretation.mc01.mingju_result_id
    assert restored.runtime.interpretation.ten_gods.natal.state is EvaluationStatus.RESOLVED
    assert build_pack07_diagnostics(restored).mc01_reference is DiagnosticStatus.PASS


def test_damage_ids_from_mc01_may_resolve_combination() -> None:
    payload = attach_mc01_reference(_payload(damage_ids=["DMG-HO-001"]))
    payload["ten_gods"] = {
        "source": "engines.ten_gods_engine",
        "visible": [
            {
                "pillar": "year",
                "stem": "Giáp",
                "ten_god": "Thương Quan",
                "god_id": "shang_guan",
                "element": "Mộc",
            },
            {
                "pillar": "month",
                "stem": "Ất",
                "ten_god": "Chính Quan",
                "god_id": "zheng_guan",
                "element": "Mộc",
            },
        ],
        "hidden": [],
    }
    collection = interpret_ten_gods(payload, analysis_id="an-p7-mc01-001")
    facts = extract_ten_god_facts(payload)
    combos = interpret_ten_god_combinations(
        collection,
        mc01_bound=True,
        damage_ids=facts.damage_ids,
        rescue_ids=facts.rescue_ids,
    )
    hurting = next(item for item in combos.items if item.combination_id == "hurting_officer_meets_officer")
    assert hurting.state is not CombinationState.UNRESOLVED
    assert hurting.damage_ids == ("DMG-HO-001",)


def test_co_presence_without_damage_ids_stays_unresolved() -> None:
    payload = attach_mc01_reference(_payload())
    payload["ten_gods"] = {
        "source": "engines.ten_gods_engine",
        "visible": [
            {
                "pillar": "year",
                "stem": "Giáp",
                "ten_god": "Thương Quan",
                "god_id": "shang_guan",
                "element": "Mộc",
            },
            {
                "pillar": "month",
                "stem": "Ất",
                "ten_god": "Chính Quan",
                "god_id": "zheng_guan",
                "element": "Mộc",
            },
        ],
        "hidden": [],
    }
    collection = interpret_ten_gods(payload, analysis_id="an-p7-mc01-001")
    combos = interpret_ten_god_combinations(collection, mc01_bound=True)
    hurting = next(item for item in combos.items if item.combination_id == "hurting_officer_meets_officer")
    assert hurting.state is CombinationState.UNRESOLVED
    assert hurting.damage_ids == ()


def test_bound_context_validation_and_invented_damage_fails() -> None:
    payload = attach_mc01_reference(_payload())
    context = build_canonical_analysis_context_from_payload(payload)
    result = validate_interpretation_context(context.interpretation)
    assert result.status is not ValidationStatus.FAIL
    runtime_ok = validate_canonical_runtime(context.runtime)
    assert runtime_ok.status is not ValidationStatus.FAIL
    mutated = interpret_and_bind_ten_gods(context, payload)
    natal = mutated.runtime.interpretation.ten_gods.natal
    from dataclasses import replace

    poisoned_items = tuple(
        replace(item, damage_ids=("P7-FAKE-DMG",)) if item.ten_god_id == "zheng_yin" else item
        for item in natal.items
    )
    poisoned_natal = replace(natal, items=poisoned_items)
    shell = mutated.runtime.interpretation.ten_gods
    poisoned_shell = replace(shell, natal=poisoned_natal)
    section = replace(mutated.runtime.interpretation, ten_gods=poisoned_shell)
    poisoned_runtime = replace(mutated.runtime, interpretation=section)
    failed = validate_canonical_runtime(poisoned_runtime)
    assert any(item.code == MC01_OWNERSHIP_DAMAGE_CODE for item in failed.issues)
    assert failed.status is ValidationStatus.FAIL


def test_public_analyze_does_not_leak_mc01_metadata() -> None:
    client = TestClient(create_app())
    analyzed = client.post(
        "/api/v1/analyze",
        json={"year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30, "gender": "male"},
    )
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    assert "mc01" not in body
    assert "mingju" not in body
    assert "_mc01_snapshot" not in body
    assert "pack07_context" not in body
    diagnostics = client.post(
        "/api/v1/dev/pack07/diagnostics",
        json={"year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30, "gender": "male"},
    )
    assert diagnostics.status_code == 200
    data = diagnostics.json()["data"]
    assert data["mc01_reference"] == "PASS"
    empty = client.get("/api/v1/dev/pack07/diagnostics")
    assert empty.json()["data"]["mc01_reference"] == "NOT_BOUND"


def test_diagnostics_from_payload_binds_current_result() -> None:
    diagnostics = diagnostics_from_payload(_payload())
    assert diagnostics.mc01_reference is DiagnosticStatus.PASS
    assert diagnostics.ten_gods in {DiagnosticStatus.PASS, DiagnosticStatus.PARTIAL}
    assert diagnostics.evidence_priority is DiagnosticStatus.PASS
    assert diagnostics.domains is DiagnosticStatus.PASS
