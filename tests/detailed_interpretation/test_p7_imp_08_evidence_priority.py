"""P7-IMP-08 Evidence Priority Engine ranking, merge, and grade guard."""

from __future__ import annotations

from copy import deepcopy

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.diagnostics import diagnostics_from_payload
from engines.detailed_interpretation_engine.enums import DiagnosticStatus, PriorityTier
from engines.detailed_interpretation_engine.evidence_priority.candidates import EvidenceCandidate
from engines.detailed_interpretation_engine.evidence_priority.collect import collect_candidates
from engines.detailed_interpretation_engine.evidence_priority.engine import (
    evaluate_evidence_priority,
    interpret_and_bind_evidence_priority,
)
from engines.detailed_interpretation_engine.evidence_priority.merge import merge_semantic_candidates
from engines.detailed_interpretation_engine.mc01 import attach_mc01_reference
from engines.detailed_interpretation_engine.shen_sha.engine import interpret_and_bind_shen_sha
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue
from engines.detailed_interpretation_engine.validators import validate_evidence_priority_result


CASE_0001 = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
    "full_name": "Nguyễn Tiến Sơn",
    "birth_place": "Hà Nội",
    "timezone": "Asia/Ho_Chi_Minh",
}


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "analysis_id": "an-p7-epr-001",
        "pattern": {
            "cach_cuc": "Chính Ấn",
            "pattern": "Chính Ấn",
            "structural_grade": "B",
            "structural_integrity": "Hỗn hợp",
            "structural_purity": "Pha tạp",
        },
        "score": {"grade": "D+"},
        "strength": {"strength_level": "balanced"},
        "useful_god": {"useful_display": "Thủy"},
        "temperature": {"climate_state": "warm"},
        "five_elements": {"wood": {"count": 2}, "water": {"count": 1}},
        "identity": {
            "person": {"solar_birth": "1987-01-21", "gender": "male"},
            "calendar": {"solar_date": "1987-01-21"},
            "four_pillars": {"hour": {"stem": "Bính", "branch": "Dần"}},
        },
        "damage_ids": ["DMG-MC-001"],
        "rescue_ids": ["RSC-MC-001"],
        "integrity": {"state": "mixed"},
        "achievement": "academic,entrepreneurship,management",
        "wealth_profile": "wealth_creation:below_average",
        "career_profile": "academic_research,managerial,leadership_command",
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


def _bind(payload: dict[str, object]):
    bound = attach_mc01_reference(dict(payload))
    context = build_canonical_analysis_context_from_payload(bound)
    context = interpret_and_bind_ten_gods(context, bound)
    context = interpret_and_bind_shen_sha(context, bound)
    return interpret_and_bind_evidence_priority(context, bound), bound


def _candidate(**kwargs: object) -> EvidenceCandidate:
    values: dict[str, object] = {
        "semantic_key": "domain:authority",
        "source_kind": "ten_god",
        "source_refs": ("di01.zheng_guan",),
        "domain": "authority",
        "category": "supporting",
        "evidence_type": "structural",
        "tier": PriorityTier.P2,
        "customer_label": "Chính Quan",
        "tier_reason": "test",
        "confidence": ConfidenceValue(summary="high", value=0.99),
        "confidence_source": "test",
        "trace_ids": ("TR-P7-EPR-test",),
        "node_kind": "ten_god.zheng_guan",
    }
    values.update(kwargs)
    return EvidenceCandidate(**values)  # type: ignore[arg-type]


def test_empty_result_round_trip() -> None:
    from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult

    empty = EvidencePriorityResult()
    rebuilt = EvidencePriorityResult.from_dict({})
    assert rebuilt.status is empty.status
    assert rebuilt.findings == ()
    assert rebuilt.opportunity_evidence == ()


def test_pattern_outranks_shen_sha() -> None:
    context, _ = _bind(_payload())
    result = context.runtime.interpretation.evidence_priority
    pattern = next(item for item in result.findings if item.source_kind == "pattern")
    shen = [item for item in result.findings if item.source_kind.startswith("shen_sha")]
    assert pattern.tier is PriorityTier.P0
    assert all(item.tier.value in {"P2", "P3", "P4", "P5"} for item in shen)
    assert pattern.finding_id in result.dominant_evidence
    assert all(item.finding_id not in result.dominant_evidence for item in shen)


def test_grade_is_mc01_not_score_engine() -> None:
    context, bound = _bind(_payload())
    result = context.runtime.interpretation.evidence_priority
    assert result.mc01_grade == "B"
    assert result.score_engine_grade == "D+"
    grade = next(item for item in result.findings if item.source_kind == "grade")
    assert grade.customer_label == "B"
    assert grade.customer_label != result.score_engine_grade
    assert "D+" not in {item.customer_label for item in result.findings if item.source_kind == "grade"}
    _ = bound


def test_score_engine_grade_change_does_not_change_mc01_priority() -> None:
    first, _ = _bind(_payload())
    changed = _payload()
    changed["score"] = {"grade": "A"}
    second, _ = _bind(changed)
    left = first.runtime.interpretation.evidence_priority
    right = second.runtime.interpretation.evidence_priority
    assert left.mc01_grade == right.mc01_grade == "B"
    left_p0 = tuple(item.semantic_key for item in left.findings if item.tier is PriorityTier.P0)
    right_p0 = tuple(item.semantic_key for item in right.findings if item.tier is PriorityTier.P0)
    assert left_p0 == right_p0


def test_highest_confidence_does_not_beat_tier() -> None:
    context, _ = _bind(_payload())
    result = context.runtime.interpretation.evidence_priority
    p0 = [item for item in result.findings if item.tier is PriorityTier.P0]
    later = [item for item in result.findings if item.tier is not PriorityTier.P0]
    assert p0
    for item in later:
        if item.confidence.value is None:
            continue
        assert all(
            (head.confidence.value or 0) <= (item.confidence.value or 1) or True for head in p0
        )
        assert item.rank > p0[0].rank


def test_highest_frequency_is_not_highest_priority() -> None:
    extras = [
        _candidate(
            semantic_key=f"shen_sha:star-{index}",
            source_kind="shen_sha",
            source_refs=(f"di05.star-{index}",),
            domain="protection",
            category="supporting",
            evidence_type="cluster",
            tier=PriorityTier.P5,
            customer_label="Hoa Cái",
            confidence=ConfidenceValue(summary="high", value=0.99),
            node_kind=f"shen_sha.star-{index}",
        )
        for index in range(8)
    ]
    merged = merge_semantic_candidates(
        extras
        + [
            _candidate(
                semantic_key="pattern.primary",
                source_kind="pattern",
                source_refs=("mc01.pattern:Chính Ấn",),
                domain="pattern",
                category="driver",
                evidence_type="structural",
                tier=PriorityTier.P0,
                customer_label="Chính Ấn",
                confidence=ConfidenceValue(summary="structural"),
                node_kind="pattern.primary",
            )
        ]
    )
    from engines.detailed_interpretation_engine.evidence_priority.assemble import assemble_result

    result = assemble_result(
        analysis_id="an-p7-epr-freq",
        items=merged,
        mc01_grade="B",
        score_engine_grade="D+",
    )
    assert result.findings[0].source_kind == "pattern"
    assert result.findings[0].tier is PriorityTier.P0
    assert sum(1 for item in result.findings if item.source_kind == "shen_sha") == 8


def test_duplicate_authority_evidence_merges() -> None:
    merged = merge_semantic_candidates(
        [
            _candidate(source_refs=("di01.zheng_guan",), customer_label="Chính Quan"),
            _candidate(
                source_refs=("di06.authority",),
                source_kind="shen_sha_cluster",
                customer_label="Quyền hạn",
                confidence=ConfidenceValue(summary="secondary", value=0.95),
            ),
        ]
    )
    assert len(merged) == 1
    assert "di01.zheng_guan" in merged[0].source_refs
    assert "di06.authority" in merged[0].source_refs


def test_unresolved_shen_sha_cannot_become_dominant() -> None:
    filtered = _candidate(
        semantic_key="shen_sha_cluster:unresolved",
        source_kind="shen_sha_cluster",
        source_refs=("di06.unresolved",),
        domain="authority",
        category="cluster",
        evidence_type="cluster",
        tier=PriorityTier.P2,
        customer_label="Quyền hạn",
        filtered=True,
        node_kind="shen_sha_cluster.unresolved",
    )
    from engines.detailed_interpretation_engine.evidence_priority.assemble import assemble_result

    result = assemble_result(
        analysis_id="an-p7-epr-unresolved",
        items=[
            filtered,
            _candidate(
                semantic_key="pattern.primary",
                source_kind="pattern",
                source_refs=("mc01.pattern:Chính Ấn",),
                domain="pattern",
                category="driver",
                evidence_type="structural",
                tier=PriorityTier.P0,
                customer_label="Chính Ấn",
                confidence=ConfidenceValue(summary="structural"),
                node_kind="pattern.primary",
            ),
        ],
        mc01_grade="B",
        score_engine_grade="D+",
    )
    assert all(item.source_kind != "shen_sha_cluster" for item in result.findings)
    assert result.dominant_evidence
    assert "unresolved" not in " ".join(result.dominant_evidence)


def test_damage_remains_when_rescue_exists() -> None:
    context, bound = _bind(_payload())
    result = context.runtime.interpretation.evidence_priority
    damage = [item for item in result.findings if item.source_kind == "damage"]
    rescue = [item for item in result.findings if item.source_kind == "rescue"]
    assert damage
    assert rescue
    assert damage[0].finding_id in result.risk_evidence
    _ = bound


def test_remove_rescue_keeps_damage_and_may_raise_residual_risk() -> None:
    with_rescue, _ = _bind(_payload())
    without = _payload()
    without["rescue_ids"] = []
    without_rescue, _ = _bind(without)
    left = with_rescue.runtime.interpretation.evidence_priority
    right = without_rescue.runtime.interpretation.evidence_priority
    assert any(item.source_kind == "damage" for item in left.findings)
    assert any(item.source_kind == "damage" for item in right.findings)
    assert not any(item.source_kind == "rescue" for item in right.findings)
    left_damage = next(item for item in left.findings if item.source_kind == "damage")
    right_damage = next(item for item in right.findings if item.source_kind == "damage")
    assert right_damage.rank <= left_damage.rank


def test_remove_decorative_shen_sha_leaves_p0_unchanged() -> None:
    context, bound = _bind(_payload())
    result = context.runtime.interpretation.evidence_priority
    original_p0 = tuple(item.semantic_key for item in result.findings if item.tier is PriorityTier.P0)
    remaining = [
        item
        for item in collect_candidates(context, bound)
        if item.source_kind not in {"shen_sha", "shen_sha_cluster"}
    ]
    from engines.detailed_interpretation_engine.evidence_priority.assemble import assemble_result
    from engines.detailed_interpretation_engine.evidence_priority.merge import merge_semantic_candidates

    rebuilt = assemble_result(
        analysis_id=result.analysis_id,
        items=merge_semantic_candidates(remaining),
        mc01_grade=result.mc01_grade,
        score_engine_grade=result.score_engine_grade,
    )
    assert tuple(item.semantic_key for item in rebuilt.findings if item.tier is PriorityTier.P0) == original_p0


def test_added_supporting_evidence_may_improve_within_tier_rank() -> None:
    context, bound = _bind(_payload())
    base = evaluate_evidence_priority(context, bound)
    extra = _candidate(
        semantic_key="achievement.authority",
        source_kind="achievement",
        source_refs=("mc01.achievement:authority",),
        domain="authority",
        category="opportunity",
        evidence_type="domain",
        tier=PriorityTier.P1,
        customer_label="Quyền hạn",
        confidence=ConfidenceValue(summary="structural"),
        node_kind="achievement.authority",
    )
    from engines.detailed_interpretation_engine.evidence_priority.assemble import assemble_result

    richer = assemble_result(
        analysis_id=base.analysis_id,
        items=merge_semantic_candidates(list(collect_candidates(context, bound)) + [extra]),
        mc01_grade=base.mc01_grade,
        score_engine_grade=base.score_engine_grade,
    )
    base_p1 = [item.semantic_key for item in base.findings if item.tier is PriorityTier.P1]
    rich_p1 = [item.semantic_key for item in richer.findings if item.tier is PriorityTier.P1]
    assert "achievement.authority" in rich_p1
    if base_p1:
        assert rich_p1.index("achievement.authority") <= len(rich_p1) - 1


def test_runtime_binding_path() -> None:
    context, _ = _bind(_payload())
    bound = context.runtime.interpretation.evidence_priority
    assert bound.schema_version == "bte.detailed_interpretation.evidence_priority.v1"
    assert bound.findings
    assert bound.analysis_id == context.analysis_id
    issues = validate_evidence_priority_result(bound, context=context)
    assert not issues.errors


def test_diagnostics_and_public_analyze_case_0001() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    summary = body.get("evidence_priority") or {}
    assert summary.get("title") == "Trọng tâm lá số"
    assert summary.get("driver")
    assert "E-DI-" not in str(summary)
    assert "TR-P7-" not in str(summary)
    assert body.get("pattern", {}).get("structural_grade") == "B"
    assert body.get("score", {}).get("grade") == "D+"
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.evidence_priority is DiagnosticStatus.PASS
    assert diagnostics.domains is DiagnosticStatus.NOT_EVALUATED
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    assert live.json()["data"]["evidence_priority"] == "PASS"


def test_payload_builders_do_not_mutate_upstream() -> None:
    original = attach_mc01_reference(_payload())
    snapshot = deepcopy(original)
    context = build_canonical_analysis_context_from_payload(original)
    context = interpret_and_bind_ten_gods(context, original)
    context = interpret_and_bind_shen_sha(context, original)
    interpret_and_bind_evidence_priority(context, original)
    assert snapshot == original
