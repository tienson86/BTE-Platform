"""Promotion Readiness Assessment — adapter, bundle, merge, portal, golden."""

from __future__ import annotations

import pytest

from applications.api.services.narrative_result_truth import build_narrative_result_dict
from engines.commercial_knowledge import (
    PRODUCTION_ALLOW_LIST,
    PROMOTION_READINESS_ALLOW_LIST,
    WAVE_1_1_ALLOW_LIST,
    CommercialKnowledgeAdapter,
    bundle_to_dict,
    enrich_narrative_inputs,
)

from .conftest import (
    PROMOTION_READINESS_FIELDS,
    assert_promotion_readiness_complete,
    baseline_interpretation,
    mixed_employee_chart,
    strong_employee_chart,
    weak_employee_chart,
)

_PRO_ALLOW = WAVE_1_1_ALLOW_LIST | PROMOTION_READINESS_ALLOW_LIST

PROMOTE_CASES = (
    ("D1-GC-PROMOTE-READY", strong_employee_chart),
    ("D1-GC-PROMOTE-PREPARE", weak_employee_chart),
    ("D1-GC-PROMOTE-MIXED", mixed_employee_chart),
)


def test_promotion_allow_list_excludes_other_domain_caps() -> None:
    """PRO allow-list is Promotion only — no SEL/LED/BU ids."""
    assert "KU-CN-CA-000001" not in PROMOTION_READINESS_ALLOW_LIST
    assert "KU-CN-LE-000001" not in PROMOTION_READINESS_ALLOW_LIST
    assert "KU-AC-BU-000001" not in PROMOTION_READINESS_ALLOW_LIST
    assert "KU-OP-CA-000001" in PROMOTION_READINESS_ALLOW_LIST
    assert len(PROMOTION_READINESS_ALLOW_LIST) == 10


def test_promotion_bundle_maps_all_fields() -> None:
    """Bundle exposes all Promotion Readiness Assessment fields."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=_PRO_ALLOW,
        run_id="pro-bundle-1",
    )
    assert_promotion_readiness_complete(bundle.promotion_readiness)
    assert bundle.promotion_readiness is not None
    assert (
        bundle.promotion_readiness.promotion_readiness.evidence_kind
        == "promotion_readiness"
    )
    assert (
        bundle.promotion_readiness.action_plan_90d.knowledge_unit_id
        == "KU-AC-CA-000020"
    )
    payload = bundle_to_dict(bundle)
    assessment = payload["promotion_readiness_assessment"]
    assert assessment["capability_id"] == "CAP-D1-CA-PRO"
    for field_name in PROMOTION_READINESS_FIELDS:
        assert assessment[field_name]["text"]
        assert (
            assessment[field_name]["knowledge_unit_id"]
            in PROMOTION_READINESS_ALLOW_LIST
        )


def test_promotion_narrative_merge_and_portal() -> None:
    """Promotion enriches Narrative and attaches to narrative_result."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=_PRO_ALLOW,
        run_id="pro-merge-1",
    )
    _analysis, interpretation = enrich_narrative_inputs(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        bundle=bundle,
        payload=payload,
    )
    assert interpretation["promotion_readiness_capability_id"] == "CAP-D1-CA-PRO"
    assert interpretation["promotion_readiness_assessment"]["promotion_readiness"][
        "text"
    ]

    result = build_narrative_result_dict(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        run_id="pro-portal-1",
    )
    assessment = result["promotion_readiness_assessment"]
    assert assessment["capability_id"] == "CAP-D1-CA-PRO"
    assert assessment["action_plan_90d"]["text"].startswith("Kế hoạch 90 ngày thăng tiến")
    assert "Sẵn sàng thăng tiến" in assessment["promotion_readiness"]["text"]


def test_promotion_traceability() -> None:
    """Promotion statements retain KU ids through Portal JSON."""
    result = build_narrative_result_dict(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        run_id="pro-trace-1",
    )
    assessment = result["promotion_readiness_assessment"]
    assert set(assessment["knowledge_unit_ids"]).issubset(PROMOTION_READINESS_ALLOW_LIST)
    assert len(assessment["knowledge_unit_ids"]) == 10
    bundle = result["commercial_knowledge_bundle"]
    assert "CAP-D1-CA-PRO" in bundle["metadata"]["capabilities"]
    assert set(bundle["traceability"]["promotion_readiness_unit_ids"]) == set(
        assessment["knowledge_unit_ids"]
    )


@pytest.mark.parametrize("case_id,factory", PROMOTE_CASES)
def test_promotion_golden_cases(case_id: str, factory) -> None:
    """Each Promotion Golden Case fills all PRO assessment fields."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(
        analysis=factory(),
        allow_list_ids=PRODUCTION_ALLOW_LIST,
        run_id=case_id,
    )
    assert_promotion_readiness_complete(bundle.promotion_readiness)
    assessment = bundle_to_dict(bundle)["promotion_readiness_assessment"]
    for field_name in PROMOTION_READINESS_FIELDS:
        text = assessment[field_name]["text"]
        assert text.strip(), f"{case_id} missing {field_name}"
        assert "kích hoạt khi" not in text.lower()
    assert "Sẵn sàng thăng tiến" in assessment["promotion_readiness"]["text"]
    assert "Nhận vai trò quản lý" in assessment["management_role_posture"]["text"]
    assert "Năng lực còn thiếu" in assessment["competency_gaps"]["text"]
    assert "Rủi ro thăng tiến" in assessment["promotion_risks"]["text"]
    assert "Giảm rủi ro thăng tiến" in assessment["promotion_mitigation"]["text"]
    assert "Kế hoạch 90 ngày thăng tiến" in assessment["action_plan_90d"]["text"]
    assert "Nhịp thăng tiến" in assessment["timing_guidance"]["text"]
