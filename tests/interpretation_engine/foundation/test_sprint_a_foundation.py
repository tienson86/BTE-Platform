"""Sprint A — Interpretation Foundation tests (A–L)."""

from __future__ import annotations

import copy

import pytest

from applications.api.services.orchestrator import OrchestratorService
from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import (
    CASE_0001_EXPECTED_STRENGTH,
    CASE_0001_REQUEST,
)
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation import build_interpretation_foundation
from engines.interpretation_engine.foundation import diagnostics as diag
from engines.interpretation_engine.foundation.builders.analysis_context_builder import (
    build_canonical_analysis_context,
)
from engines.interpretation_engine.foundation.status import DataAvailability, ReadinessLevel
from engines.interpretation_engine.foundation.validation.score_truth_guard import (
    validate_score_not_used_as_truth,
)

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
    full_name="Lương Ngọc Huỳnh",
    birth_place="Hà Nội, Việt Nam",
)


@pytest.fixture(scope="module")
def huynh_output():
    """Production pipeline output for Lương Ngọc Huỳnh."""
    return ProductionEngineRunner().run(HUYNH)


@pytest.fixture(scope="module")
def huynh_foundation(huynh_output):
    """Interpretation foundation bundle for Huỳnh."""
    assert huynh_output.interpretation_foundation is not None
    return huynh_output.interpretation_foundation


@pytest.fixture(scope="module")
def case0001_foundation():
    """Interpretation foundation bundle for CASE-0001."""
    output = ProductionEngineRunner().run(CASE_0001_REQUEST)
    assert output.interpretation_foundation is not None
    return output.interpretation_foundation


def test_a_canonical_context_preserves_engine_truth(huynh_foundation) -> None:
    """A. CanonicalAnalysisContext preserves engine truth."""
    ctx = huynh_foundation.context
    assert ctx.strength.level == "strong"
    assert abs(ctx.strength.score - 0.66) < 0.01
    assert ctx.strength.label == "Thân vượng"
    assert ctx.pattern.label == "Chính Tài"
    assert ctx.useful_god.selected == "Đinh"
    assert ctx.temperature.level == "cool"
    assert abs(ctx.temperature.score - 0.4767) < 0.001
    assert ctx.temperature.label == "Khí mát"
    assert ctx.five_elements.wood == 2
    assert ctx.five_elements.fire == 7
    assert ctx.score.total_score == 61.25
    assert ctx.score.grade == "C"


def test_b_score_fields_cannot_replace_analytical_truth(huynh_foundation, huynh_output) -> None:
    """B. Score fields cannot replace analytical truth."""
    guard = huynh_foundation.score_guard
    assert guard.passed is True
    assert diag.SCORE_USED_AS_WUXING_TRUTH not in guard.violations

    score = huynh_output.analysis.score.to_dict()
    empty_payload = {
        "strength": {},
        "pattern": {},
        "useful_god": {},
        "temperature": {},
        "bazi": huynh_output.analysis.bazi.to_dict(),
        "score": score,
        "five_elements": {},
    }
    ctx = build_canonical_analysis_context(payload=empty_payload)
    from engines.interpretation_engine.foundation.builders.interpretation_facts_builder import (
        build_interpretation_facts,
    )

    facts = build_interpretation_facts(ctx)
    guard_fail = validate_score_not_used_as_truth(ctx, facts, score_payload=score)
    assert guard_fail.passed is False
    assert diag.SCORE_USED_AS_WUXING_TRUTH in guard_fail.violations


def test_c_useful_god_facts_huynh(huynh_foundation) -> None:
    """C. UsefulGodInterpretationFacts includes selected, Hỷ, Kỵ, candidates, reason."""
    ug = huynh_foundation.facts.useful_god
    assert ug.selected == "Đinh"
    assert list(ug.favorable_gods) == ["Đinh", "Bính", "Ất"]
    assert list(ug.unfavorable_gods) == ["Canh", "Tân"]
    assert ug.confidence == pytest.approx(0.85, abs=0.01)
    assert "sea_004" in ug.rule_ids
    assert "Thu kim vượng cần hỏa tôi luyện" in ug.reason
    assert len(ug.candidates) > 0
    sea = [item for item in ug.candidates if item.rule_id == "sea_004"]
    assert sea and sea[0].useful_god == "Đinh"
    assert ug.month_branch == "Dậu"
    assert ug.season == "Thu"


def test_d_strength_facts_ownership(huynh_foundation) -> None:
    """D. StrengthInterpretationFacts preserves strong/weak ownership."""
    strength = huynh_foundation.facts.strength
    assert strength.level == "strong"
    assert strength.score == pytest.approx(0.66, abs=0.01)
    assert strength.label == "Thân vượng"
    assert strength.owner == "StrengthEngine"
    assert strength.status == DataAvailability.AVAILABLE


def test_e_temperature_facts_real_engine(huynh_foundation) -> None:
    """E. TemperatureInterpretationFacts uses real TemperatureEngine output."""
    temp = huynh_foundation.facts.temperature
    assert temp.level == "cool"
    assert temp.score == pytest.approx(0.4767, abs=0.001)
    assert temp.label == "Khí mát"
    assert temp.owner == "TemperatureEngine"
    assert diag.TEMPERATURE_CONTAMINATED_BY_PATTERN not in temp.diagnostics


def test_f_ten_god_facts_positions(huynh_foundation) -> None:
    """F. TenGodInterpretationFacts preserve positions."""
    tg = huynh_foundation.facts.ten_gods
    assert len(tg.visible) == 4
    pillars = {item.pillar for item in tg.visible}
    assert pillars == {"year", "month", "day", "hour"}
    names = {item.name for item in tg.visible}
    assert "Thiên Tài" in names
    assert tg.status == DataAvailability.AVAILABLE


def test_g_shensha_never_fabricates_evidence(huynh_foundation) -> None:
    """G. ShenShaInterpretationFacts copy engine evidence and never invent stars."""
    ss = huynh_foundation.facts.shensha
    assert ss.items
    names = {item.name for item in ss.items}
    assert "Thiên Ất Quý Nhân" in names
    assert "Thiên Ất" not in names
    assert "available" not in names
    for item in ss.items:
        assert item.evidence
        assert item.evidence != item.name
        assert item.evidence_status.value == "available"
        assert item.rule_id
    assert diag.SHENSHA_EVIDENCE_UNAVAILABLE not in ss.diagnostics


def test_h_luck_facts_all_cycles(huynh_foundation) -> None:
    """H. LuckInterpretationFacts contain all cycles."""
    luck = huynh_foundation.facts.luck
    assert len(luck.cycles) == 10
    assert luck.start_age == 5
    assert luck.current_cycle is not None
    assert luck.current_cycle.gan_zhi == "Quý Mão"
    assert luck.current_cycle.year_start == 2021
    assert luck.current_cycle.year_end == 2030


def test_i_missing_data_explicit_status() -> None:
    """I. Missing analytical data produces explicit status/diagnostic."""
    ctx = build_canonical_analysis_context(
        payload={
            "bazi": {},
            "strength": {},
            "pattern": {},
            "useful_god": {},
            "temperature": {},
            "score": {},
            "five_elements": {},
        }
    )
    from engines.interpretation_engine.foundation.builders.interpretation_facts_builder import (
        build_interpretation_facts,
    )

    facts = build_interpretation_facts(ctx)
    assert facts.strength.status == DataAvailability.MISSING
    assert facts.useful_god.status == DataAvailability.MISSING
    assert diag.STRENGTH_TRUTH_MISSING in facts.strength.diagnostics
    assert diag.USEFUL_GOD_NOT_AVAILABLE in facts.useful_god.diagnostics


def test_j_no_silent_semantic_fallback(huynh_foundation) -> None:
    """J. No silent semantic fallback for missing useful god."""
    ug = huynh_foundation.facts.useful_god
    assert ug.presence == DataAvailability.AVAILABLE
    assert ug.selected != ""
    assert diag.USEFUL_GOD_NOT_AVAILABLE not in ug.diagnostics or ug.selected


def test_k_existing_narrative_still_works() -> None:
    """K. Existing NarrativeResult still works during Sprint A."""
    payload = OrchestratorService().analyze(
        year=1966,
        month=9,
        day=24,
        hour=4,
        minute=15,
        gender="male",
    )
    assert "narrative_result" in payload
    narrative = payload["narrative_result"]
    assert narrative
    sections = narrative.get("sections") or narrative.get("chapters") or []
    assert sections or narrative.get("executive_summary") or narrative.get("body")


def test_l_portal_payload_unchanged(huynh_output) -> None:
    """L. Production analysis contract unchanged — Portal/PDF inputs stable."""
    analysis = huynh_output.analysis
    assert analysis.strength.strength_level == "strong"
    assert analysis.useful_god.useful_god == "Đinh"
    assert analysis.pattern.cach_cuc == "Chính Tài"
    assert analysis.score.grade == "C"
    assert huynh_output.interpretation is not None


def test_case0001_generic_contract(case0001_foundation) -> None:
    """CASE-0001 proves contracts are generic, not Huỳnh-hardcoded."""
    strength = case0001_foundation.facts.strength
    assert strength.level == CASE_0001_EXPECTED_STRENGTH["strength_level"]
    assert strength.score == pytest.approx(
        CASE_0001_EXPECTED_STRENGTH["strength_score"],
        abs=0.01,
    )
    readiness = case0001_foundation.readiness
    assert readiness.strength == ReadinessLevel.READY


def test_huynh_readiness_matrix(huynh_foundation) -> None:
    """Huỳnh interpretation readiness expectations."""
    readiness = huynh_foundation.readiness.to_dict()["interpretation_readiness"]
    assert readiness["strength"] == "ready"
    assert readiness["pattern"] == "ready"
    assert readiness["useful_god"] == "ready"
    assert readiness["temperature"] == "ready"
    assert readiness["luck"] == "ready"
    assert readiness["ten_gods"] in {"ready", "partial"}
    assert readiness["shensha"] in {"ready", "partial"}


def test_domain_result_stubs(huynh_foundation) -> None:
    """Domain interpretation result stubs exist for Sprint B."""
    results = huynh_foundation.domain_results
    assert set(results) >= {
        "strength",
        "pattern",
        "useful_god",
        "ten_gods",
        "shensha",
        "luck",
        "temperature",
    }
    for domain, result in results.items():
        assert result.domain == domain
        assert result.status in DataAvailability


def test_canonical_context_immutable(huynh_foundation) -> None:
    """CanonicalAnalysisContext is frozen."""
    ctx = huynh_foundation.context
    with pytest.raises(Exception):
        ctx.score = ctx.score  # type: ignore[misc]
