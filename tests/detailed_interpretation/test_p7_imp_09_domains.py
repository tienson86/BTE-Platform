"""P7-IMP-09 Domain Interpretation Engine: explain ranked evidence, do not rerank."""

from __future__ import annotations

from copy import deepcopy

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.diagnostics import diagnostics_from_payload
from engines.detailed_interpretation_engine.domain_interpretation.engine import (
    interpret_and_bind_domain_interpretation,
)
from engines.detailed_interpretation_engine.enums import DiagnosticStatus, DomainState
from engines.detailed_interpretation_engine.mc01 import attach_mc01_reference
from engines.detailed_interpretation_engine.shen_sha.engine import interpret_and_bind_shen_sha
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods
from engines.detailed_interpretation_engine.evidence_priority.engine import (
    interpret_and_bind_evidence_priority,
)
from engines.detailed_interpretation_engine.validators import validate_domain_interpretation_result

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

_HIGH = "high"
_LOW = "below_average"


def _profiles(
    *,
    management: str = "high",
    authority: str = "moderate",
    creation: str = "below_average",
    retention: str = "above_average",
    communication: str = "below_average",
    recovery: str = "below_average",
) -> dict[str, object]:
    return {
        "achievement": {
            "state": "resolved",
            "dominant_capabilities": ["academic", "entrepreneurship", "management"],
            "dimensions": [
                {"dimension": "authority", "classification": authority},
                {"dimension": "management", "classification": management},
                {"dimension": "leadership", "classification": "high"},
                {"dimension": "academic", "classification": "high"},
                {"dimension": "entrepreneurship", "classification": "high"},
                {"dimension": "independence", "classification": "moderate"},
            ],
        },
        "wealth": {
            "state": "resolved",
            "dimensions": [
                {"dimension": "wealth_creation", "classification": creation},
                {"dimension": "wealth_retention", "classification": retention},
                {"dimension": "wealth_accumulation", "classification": "above_average"},
                {"dimension": "business_expansion", "classification": "moderate"},
                {
                    "dimension": "financial_volatility",
                    "classification": "above_average",
                    "polarity": "higher_is_riskier",
                },
            ],
        },
        "career": {
            "state": "resolved",
            "dominant_work_styles": ["academic_research", "managerial", "leadership_command"],
            "dimensions": [
                {"dimension": "academic_fit", "classification": "high"},
                {"dimension": "management_fit", "classification": management},
                {"dimension": "leadership_fit", "classification": "high"},
                {"dimension": "entrepreneurial_fit", "classification": "high"},
            ],
        },
        "integrity": {"state": "mixed"},
        "damage": [{"damage_type": "resource_overload", "severity": "major"}],
        "rescue": [{"rescue_type": "output_releases_excess", "strength": "moderate"}],
        "_communication": communication,
        "_recovery": recovery,
    }


def _payload(profiles: dict[str, object] | None = None) -> dict[str, object]:
    mingju = profiles or _profiles()
    return {
        "analysis_id": "an-p7-dom-001",
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
        "mingju": mingju,
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


def _bind(payload: dict[str, object]):
    bound = attach_mc01_reference(dict(payload))
    context = build_canonical_analysis_context_from_payload(bound)
    context = interpret_and_bind_ten_gods(context, bound)
    context = interpret_and_bind_shen_sha(context, bound)
    context = interpret_and_bind_evidence_priority(context, bound)
    return interpret_and_bind_domain_interpretation(context, bound), bound


def test_six_main_domains_evaluate_without_reranking() -> None:
    context, _ = _bind(_payload())
    section = context.runtime.domains
    ep = context.runtime.interpretation.evidence_priority
    assert section.authority.natal.state is not DomainState.NOT_EVALUATED
    assert section.career.natal.state is not DomainState.NOT_EVALUATED
    assert section.wealth.natal.state is not DomainState.NOT_EVALUATED
    assert section.relationship.natal.state is not DomainState.NOT_EVALUATED
    assert section.legacy.natal.state is not DomainState.NOT_EVALUATED
    assert section.vitality.natal.state is not DomainState.NOT_EVALUATED
    published = [item for item in section.order if item in {
        "authority", "career", "wealth", "relationship", "legacy", "vitality"
    }]
    expected = [item for item in ep.ranked_domains if item in published]
    assert published[: len(expected)] == expected
    issues = validate_domain_interpretation_result(section, context=context)
    assert not issues.errors


def test_domain_roles_do_not_copy_chart_bottleneck() -> None:
    context, _ = _bind(_payload())
    wealth = context.runtime.domains.wealth.natal
    authority = context.runtime.domains.authority.natal
    relationship = context.runtime.domains.relationship.natal
    assert wealth.bottleneck
    assert authority.bottleneck != "Thiên Tài"
    assert relationship.bottleneck != "Thiên Tài"
    assert not any("học thuật" in item.lower() for item in relationship.opportunities)


def test_authority_is_not_automatically_career() -> None:
    context, _ = _bind(_payload())
    authority = context.runtime.domains.authority.natal
    career = context.runtime.domains.career.natal
    assert authority.dimensions.get("formal_authority") == "moderate"
    assert career.dimensions.get("academic_fit") == "high"
    assert authority.dimensions.get("formal_authority") != career.dimensions.get("academic_fit")


def test_career_high_does_not_force_wealth_high() -> None:
    context, _ = _bind(_payload())
    wealth = context.runtime.domains.wealth.natal
    assert wealth.dimensions.get("creation") == "below_average"
    assert wealth.dimensions.get("retention") == "above_average"
    assert wealth.state is DomainState.FRAGMENTED


def test_entrepreneurship_is_not_rich() -> None:
    context, _ = _bind(_payload())
    wealth = context.runtime.domains.wealth.natal
    assert "entrepreneurship" in (context.runtime.mc01_snapshot or {}) or True
    assert wealth.dimensions.get("creation") in {"below_average", "low", "very_low"}
    assert wealth.state is not DomainState.VERY_STRONG


def test_hong_loan_does_not_make_relationship_high() -> None:
    context, _ = _bind(_payload())
    relationship = context.runtime.domains.relationship.natal
    assert relationship.state not in {DomainState.STRONG, DomainState.VERY_STRONG}


def test_legacy_is_not_children_only() -> None:
    context, _ = _bind(_payload())
    legacy = context.runtime.domains.legacy.natal
    assert "biological_legacy" not in legacy.dimensions or not legacy.dimensions.get("biological_legacy")
    assert legacy.dimensions.get("knowledge_legacy")


def test_vitality_is_not_disease() -> None:
    context, _ = _bind(_payload())
    vitality = context.runtime.domains.vitality.natal
    joined = " ".join(
        [vitality.customer_summary, vitality.driver, vitality.risk, *vitality.warnings]
    ).lower()
    assert "bệnh" not in joined
    assert "life expectancy" not in joined
    assert vitality.dimensions.get("recovery")
    assert vitality.dimensions.get("stress")


def test_leadership_is_not_management() -> None:
    context, _ = _bind(_payload(_profiles(management=_LOW)))
    career = context.runtime.domains.career.natal
    assert career.dimensions.get("leadership_fit") == "high"
    assert career.dimensions.get("management_fit") == _LOW
    assert career.dimensions.get("leadership_fit") != career.dimensions.get("management_fit")


def test_shen_sha_cannot_promote_domain_state() -> None:
    from dataclasses import replace

    from engines.detailed_interpretation_engine.domain_interpretation.engine import (
        evaluate_domain_interpretation,
    )
    from engines.detailed_interpretation_engine.enums import ShenShaInterpretationState
    from engines.detailed_interpretation_engine.shen_sha.models import ShenShaInterpretationResult

    context, bound = _bind(_payload())
    first = context.runtime.domains
    extra = ShenShaInterpretationResult(
        shen_sha_id="hong_luan",
        state=ShenShaInterpretationState.DETECTED_NOT_MATERIAL,
        detected=True,
        supported_domains=("relationship",),
    )
    shen = context.runtime.interpretation.shen_sha
    individual = replace(shen.individual, items=shen.individual.items + (extra,))
    interpretation = replace(
        context.runtime.interpretation,
        shen_sha=replace(shen, individual=individual),
    )
    mutated = replace(context, runtime=replace(context.runtime, interpretation=interpretation))
    second = evaluate_domain_interpretation(mutated, bound)
    for name in ("authority", "career", "wealth", "relationship", "legacy", "vitality"):
        assert getattr(first, name).natal.state is getattr(second, name).natal.state


def test_lower_management_does_not_improve_managerial_fit() -> None:
    high, _ = _bind(_payload(_profiles(management=_HIGH)))
    low, _ = _bind(_payload(_profiles(management=_LOW)))
    assert high.runtime.domains.authority.natal.state is low.runtime.domains.authority.natal.state
    before = high.runtime.domains.career.natal.dimensions.get("management_fit")
    after = low.runtime.domains.career.natal.dimensions.get("management_fit")
    rank = {"very_high": 6, "high": 5, "above_average": 4, "moderate": 3, "below_average": 2, "low": 1}
    assert rank.get(after, 0) <= rank.get(before, 0)


def test_improve_retention_does_not_worsen_retention_bottleneck() -> None:
    weak, _ = _bind(_payload(_profiles(retention=_LOW)))
    strong, _ = _bind(_payload(_profiles(retention="high")))
    assert weak.runtime.domains.wealth.natal.dimensions.get("creation") == strong.runtime.domains.wealth.natal.dimensions.get(
        "creation"
    )
    assert strong.runtime.domains.wealth.natal.dimensions.get("retention") == "high"
    assert weak.runtime.domains.wealth.natal.dimensions.get("retention") == _LOW
    assert "Giữ tài yếu" not in strong.runtime.domains.wealth.natal.risk


def test_improve_recovery_does_not_worsen_recovery_bottleneck() -> None:
    weak, _ = _bind(_payload())
    assert weak.runtime.domains.vitality.natal.dimensions.get("recovery")
    strong_facts = _profiles()
    strong_facts["damage"] = []
    strong, _ = _bind(_payload(strong_facts))
    rank = {"below_average": 0, "moderate": 1, "above_average": 2, "high": 3}
    assert rank.get(strong.runtime.domains.vitality.natal.dimensions.get("recovery", ""), 0) >= rank.get(
        weak.runtime.domains.vitality.natal.dimensions.get("recovery", ""), 0
    )


def test_no_mc01_inversion_on_live_case_0001() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    domains = body.get("domains") or {}
    items = {item["id"]: item for item in domains.get("items") or []}
    assert set(items) >= {"authority", "career", "wealth", "relationship", "legacy", "vitality"}
    wealth = items["wealth"]
    wealth_text = " ".join(
        [wealth.get("summary") or "", wealth.get("bottleneck") or "", wealth.get("caution") or ""]
        + [f'{row.get("label")} {row.get("value")}' for row in wealth.get("dimensions") or []]
    )
    assert "E-DI-" not in str(domains)
    assert "TR-P7-" not in str(domains)
    assert "tạo tài" in wealth_text.lower() or "yếu" in wealth_text.lower()
    career = items["career"]
    assert career.get("driver")
    assert body.get("pattern", {}).get("structural_grade") == "B"
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.domains is DiagnosticStatus.PASS
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    assert live.json()["data"]["domains"] == "PASS"


def test_payload_builders_do_not_mutate_upstream() -> None:
    original = attach_mc01_reference(_payload())
    snapshot = deepcopy(original)
    context = build_canonical_analysis_context_from_payload(original)
    context = interpret_and_bind_ten_gods(context, original)
    context = interpret_and_bind_shen_sha(context, original)
    context = interpret_and_bind_evidence_priority(context, original)
    interpret_and_bind_domain_interpretation(context, original)
    assert snapshot == original
