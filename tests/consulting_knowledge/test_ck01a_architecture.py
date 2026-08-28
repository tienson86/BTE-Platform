"""CK-01A Consulting Knowledge architecture tests. No engine calculation."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.consulting_knowledge import (
    CONSULTING_DOMAINS,
    CONTRACT_ID,
    DOMAIN_TITLES_VI,
    FORBIDDEN_OPERATIONS,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    KNOWLEDGE_UNIT_FIELDS,
    MATCHING_STAGES,
    SIGNAL_SOURCES,
    ConsultingKnowledgeError,
    ConsultingKnowledgeUnit,
    consulting_knowledge_contract,
    empty_knowledge_pack,
    empty_knowledge_unit,
    match_consulting_knowledge,
    project_signals,
)

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "engines" / "consulting_knowledge"


def _unit(**overrides: object) -> ConsultingKnowledgeUnit:
    payload: dict[str, object] = {
        "unit_id": "ck-career-001",
        "domain": "career",
        "condition": {"strength_level": "Thân vượng"},
        "applicable_scope": {"domain": "career"},
        "consulting_meaning": "Sức gánh cao cần khung trách nhiệm rõ.",
        "customer_wording": ("Ưu tiên dựng khung việc trước khi mở rộng.",),
        "recommended_actions": ("Dựng khung vừa đủ để việc chạy.",),
        "references": ("analysis.strength.strength_level",),
    }
    payload.update(overrides)
    return ConsultingKnowledgeUnit(
        unit_id=str(payload["unit_id"]),
        domain=str(payload["domain"]),
        condition=payload["condition"],  # type: ignore[arg-type]
        applicable_scope=payload["applicable_scope"],  # type: ignore[arg-type]
        consulting_meaning=str(payload["consulting_meaning"]),
        customer_wording=payload["customer_wording"],  # type: ignore[arg-type]
        recommended_actions=payload["recommended_actions"],  # type: ignore[arg-type]
        references=payload["references"],  # type: ignore[arg-type]
        status=str(payload.get("status", "complete")),
    )


def test_contract_surface_is_frozen() -> None:
    """Public contract lists domains, unit fields, and forbids calculation."""
    contract = consulting_knowledge_contract()
    assert contract["contract_id"] == CONTRACT_ID
    assert contract["framework_version"] == FRAMEWORK_VERSION
    assert contract["runtime"] is False
    assert contract["recalculates"] is False
    assert contract["llm"] is False
    assert contract["engine"] is False
    assert contract["input"] == list(SIGNAL_SOURCES)
    assert contract["output"] == "ConsultingKnowledgePack"
    assert contract["unit_fields"] == list(KNOWLEDGE_UNIT_FIELDS)
    assert contract["insufficient_copy"] == INSUFFICIENT_COPY


def test_frozen_consulting_domains() -> None:
    """Ten consulting domains. Not analytical engine topics."""
    assert CONSULTING_DOMAINS == (
        "career",
        "finance",
        "relationship",
        "health",
        "leadership",
        "management",
        "communication",
        "business",
        "personality",
        "action_library",
    )
    assert DOMAIN_TITLES_VI["career"] == "Sự nghiệp"
    assert DOMAIN_TITLES_VI["action_library"] == "Thư viện hành động"
    assert "strength" not in CONSULTING_DOMAINS
    assert "calendar" not in CONSULTING_DOMAINS


def test_knowledge_unit_required_fields() -> None:
    """Every unit carries condition, scope, meaning, wording, actions, references."""
    assert KNOWLEDGE_UNIT_FIELDS == (
        "condition",
        "applicable_scope",
        "consulting_meaning",
        "customer_wording",
        "recommended_actions",
        "references",
    )
    unit = _unit()
    payload = unit.to_dict()
    for field in KNOWLEDGE_UNIT_FIELDS:
        assert field in payload
    assert payload["customer_wording"] == ["Ưu tiên dựng khung việc trước khi mở rộng."]


def test_complete_unit_rejects_empty_customer_wording() -> None:
    """Complete units cannot be generated at match time."""
    with pytest.raises(ConsultingKnowledgeError):
        _unit(customer_wording=())


def test_unknown_domain_is_rejected() -> None:
    """Domains are frozen. Strength is not a consulting domain."""
    with pytest.raises(ConsultingKnowledgeError):
        _unit(domain="strength")


def test_matching_pipeline_order() -> None:
    """Match copies published truth. It does not calculate."""
    assert MATCHING_STAGES == (
        "published_truth",
        "signal_projection",
        "condition_match",
        "scope_filter",
        "consulting_knowledge_pack",
    )
    assert SIGNAL_SOURCES == (
        "integrated_narrative",
        "identity",
        "analysis_result",
    )
    assert FORBIDDEN_OPERATIONS == (
        "calculate",
        "predict",
        "infer",
        "invent",
        "llm",
    )


def test_empty_catalog_is_insufficient() -> None:
    """No catalog and no match never invent a consulting reading."""
    pack = match_consulting_knowledge({"strength_level": "Thân vượng"}, catalog=())
    assert pack.status == "insufficient"
    assert pack.to_dict()["empty_copy"] == INSUFFICIENT_COPY
    assert empty_knowledge_pack().units == ()
    assert empty_knowledge_unit().status == "insufficient"


def test_condition_match_uses_published_signals_only() -> None:
    """A unit matches when published keys equal the stored condition."""
    catalog = (_unit(),)
    hit = match_consulting_knowledge({"strength_level": "Thân vượng"}, catalog)
    miss = match_consulting_knowledge({"strength_level": "Thân nhược"}, catalog)
    assert hit.status == "complete"
    assert hit.units[0].unit_id == "ck-career-001"
    assert miss.status == "insufficient"


def test_project_signals_copies_and_does_not_compute() -> None:
    """Signal projection flattens published inputs. It does not add scores."""
    signals = project_signals(
        analysis_result={"strength": {"strength_level": "Thân vượng"}},
        identity={"person": {"full_name": "Nguyen Tien Son"}},
        integrated_narrative={"executive_summary": {"available": True}},
    )
    assert signals["strength_level"] == "Thân vượng"
    assert signals["full_name"] == "Nguyen Tien Son"
    assert "calculated_score" not in signals


def test_package_does_not_import_engines_or_delivery() -> None:
    """CK-01A is knowledge architecture: no Calendar, Identity runtime, or Report."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE.glob("*.py"))
    assert "from engines.calendar" not in joined
    assert "from engines.bazi" not in joined
    assert "from engines.strength" not in joined
    assert "from engines.pattern" not in joined
    assert "from engines.useful_god" not in joined
    assert "from engines.luck" not in joined
    assert "from engines.identity" not in joined
    assert "from engines.report_engine" not in joined
    assert "from engines.narrative_engine" not in joined
    assert "customer_portal" not in joined
    assert "def calculate(" not in joined
    assert "openai" not in joined.lower()
