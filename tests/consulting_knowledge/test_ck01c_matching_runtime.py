"""CK-01C matching runtime tests. Deterministic match. No calculation."""

from __future__ import annotations

from pathlib import Path

from engines.consulting_knowledge import (
    CATALOG_ID,
    INSUFFICIENT_COPY,
    MATCHING_RUNTIME_ID,
    MATCHING_STAGES,
    SIGNAL_SOURCES,
    consulting_matching_contract,
    get_catalog_unit,
    match_published_knowledge,
)

PACKAGE = Path(__file__).resolve().parents[2] / "engines" / "consulting_knowledge"
RUNTIME_FILES = (PACKAGE / "runtime.py", PACKAGE / "matching.py")

_STRONG_IDS = (
    "ck-career-001",
    "ck-finance-001",
    "ck-relationship-001",
    "ck-health-001",
    "ck-leadership-002",
    "ck-management-001",
    "ck-communication-001",
    "ck-business-001",
    "ck-personality-001",
)
_WEAK_IDS = (
    "ck-career-002",
    "ck-finance-002",
    "ck-relationship-002",
    "ck-health-002",
    "ck-management-002",
    "ck-communication-002",
    "ck-business-002",
    "ck-personality-002",
)


def test_matching_runtime_contract() -> None:
    """Matching runtime copies published truth. It is not an analytical engine."""
    contract = consulting_matching_contract()
    assert contract["contract_id"] == MATCHING_RUNTIME_ID
    assert contract["catalog_id"] == CATALOG_ID
    assert contract["matching_runtime"] is True
    assert contract["recalculates"] is False
    assert contract["llm"] is False
    assert contract["engine"] is False
    assert contract["input"] == list(SIGNAL_SOURCES)
    assert contract["output"] == "ConsultingKnowledgePack"
    assert contract["stages"] == list(MATCHING_STAGES)
    assert contract["insufficient_copy"] == INSUFFICIENT_COPY


def test_strong_signals_match_strong_units_in_catalog_order() -> None:
    """Thân vượng matches stored strong units. Weak units stay out."""
    pack = match_published_knowledge(
        analysis_result={"strength": {"strength_level": "Thân vượng"}},
        identity={"person": {"full_name": "Nguyen Tien Son"}},
        integrated_narrative={"executive_summary": {"available": True}},
    )
    ids = tuple(unit.unit_id for unit in pack.units)
    assert pack.status == "complete"
    assert ids == _STRONG_IDS
    assert "ck-career-002" not in ids
    assert "ck-action-001" not in ids


def test_weak_signals_match_weak_units_only() -> None:
    """Thân nhược matches stored weak units. Strong units stay out."""
    pack = match_published_knowledge(
        analysis_result={"strength": {"strength_level": "Thân nhược"}},
        identity={},
        integrated_narrative={},
    )
    ids = tuple(unit.unit_id for unit in pack.units)
    assert pack.status == "complete"
    assert ids == _WEAK_IDS
    assert "ck-career-001" not in ids
    assert "ck-leadership-002" not in ids


def test_useful_god_membership_adds_leadership_unit() -> None:
    """Chính Quan matches the stored leadership unit. No inference of other gods."""
    pack = match_published_knowledge(
        analysis_result={
            "strength": {"strength_level": "Thân vượng"},
            "useful_god": {"useful_god": "Chính Quan"},
        },
    )
    ids = tuple(unit.unit_id for unit in pack.units)
    assert "ck-leadership-001" in ids
    assert ids.index("ck-leadership-001") < ids.index("ck-leadership-002")
    assert pack.units[ids.index("ck-leadership-001")].customer_wording == (
        get_catalog_unit("ck-leadership-001").customer_wording
    )


def test_empty_published_truth_is_insufficient() -> None:
    """No published condition keys never invent a consulting pack."""
    pack = match_published_knowledge(
        analysis_result={},
        identity={},
        integrated_narrative={},
    )
    assert pack.status == "insufficient"
    assert pack.units == ()
    assert pack.to_dict()["empty_copy"] == INSUFFICIENT_COPY


def test_matching_is_deterministic() -> None:
    """Same published inputs return the same ordered pack."""
    payload = {
        "analysis_result": {"strength": {"strength_level": "Thân vượng"}},
        "identity": {"person": {"full_name": "Nguyen Tien Son"}},
        "integrated_narrative": {"summary": {"available": True}},
    }
    first = match_published_knowledge(**payload)
    second = match_published_knowledge(**payload)
    assert tuple(unit.unit_id for unit in first.units) == tuple(
        unit.unit_id for unit in second.units
    )
    assert first.status == second.status
    assert first.units[0].customer_wording == (
        "Ưu tiên dựng khung việc trước khi mở rộng.",
    )


def test_scope_filter_drops_out_of_scope_units() -> None:
    """Applicable scope is a filter. It does not rewrite the unit."""
    pack = match_published_knowledge(
        analysis_result={
            "strength": {"strength_level": "Thân vượng"},
            "domain": "career",
        },
    )
    ids = tuple(unit.unit_id for unit in pack.units)
    assert ids == ("ck-career-001",)
    assert get_catalog_unit("ck-career-001").applicable_scope["domain"] == "career"


def test_pack_uses_stored_wording_not_generated_copy() -> None:
    """Matched units keep catalog wording and actions."""
    pack = match_published_knowledge(
        analysis_result={"strength": {"strength_level": "Thân vượng"}},
    )
    stored = get_catalog_unit("ck-career-001")
    matched = pack.units[0]
    assert matched.consulting_meaning == stored.consulting_meaning
    assert matched.customer_wording == stored.customer_wording
    assert matched.recommended_actions == stored.recommended_actions
    assert matched.references == stored.references


def test_runtime_does_not_calculate_or_call_engines() -> None:
    """Matching runtime copies signals. It does not import engines or LLMs."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in RUNTIME_FILES)
    assert "from engines.calendar" not in joined
    assert "from engines.bazi" not in joined
    assert "from engines.strength" not in joined
    assert "from engines.identity" not in joined
    assert "from engines.narrative_framework" not in joined
    assert "from engines.report_engine" not in joined
    assert "customer_portal" not in joined
    assert "def calculate(" not in joined
    assert "openai" not in joined.lower()
    assert "from engines.consulting_knowledge.catalog import" not in joined
