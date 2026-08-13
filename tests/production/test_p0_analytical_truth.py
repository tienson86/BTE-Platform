"""P0 analytical truth: Strength ownership and Useful God propagation."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest
from engines.pattern_engine.labels import STRENGTH_LEVEL_LABELS
from engines.score_engine.engine import ScoreEngine

HUYNH = {
    "year": 1966,
    "month": 9,
    "day": 24,
    "hour": 4,
    "minute": 15,
    "gender": "male",
}


def test_huynh_strength_remains_strong_downstream() -> None:
    """B. strong / 0.66 remains strong after Score compose."""
    payload = OrchestratorService().analyze(**HUYNH)
    strength = payload["strength"]
    assert strength["strength_level"] == "strong"
    assert abs(float(strength["strength_score"]) - 0.66) < 0.01
    assert strength.get("reasoning") == "Thân vượng"
    assert payload["pattern"]["than_vuong_nhuoc"] == STRENGTH_LEVEL_LABELS["strong"]
    assert payload["pattern"]["than_vuong_nhuoc"] != "Trung hòa"

    published = _published_then_scored()
    assert published["strength"]["level"] == "strong"
    assert abs(float(published["strength"]["score"]) - 0.66) < 0.01


def test_huynh_hy_than_exposed_downstream() -> None:
    """G. Hỷ thần reaches pattern, interpretation, narrative, and report."""
    payload = OrchestratorService().analyze(**HUYNH)
    expected = ["Đinh", "Bính", "Ất"]
    assert payload["useful_god"]["favorable_gods"] == expected
    assert payload["pattern"]["hy_than"] == "Đinh, Bính, Ất"
    assert payload["pattern"]["hy_than"] not in {"", "--"}
    narrative = _narrative_text(payload["narrative_result"])
    interpretation = _section_text(payload["interpretation"], "useful_god")
    assert "Không có Dụng thần" not in interpretation
    assert "Không có Dụng thần" not in narrative
    assert "Đinh" in interpretation
    assert "Đinh" in narrative or "Đinh" in payload["pattern"]["hy_than"]


def test_huynh_ky_than_exposed_downstream() -> None:
    """H. Kỵ thần reaches pattern and useful-god view."""
    payload = OrchestratorService().analyze(**HUYNH)
    assert payload["useful_god"]["unfavorable_gods"] == ["Canh", "Tân"]
    assert payload["pattern"]["ky_than"] == "Canh, Tân"
    assert payload["pattern"]["ky_than"] not in {"", "--"}


def test_huynh_pattern_remains_chinh_tai() -> None:
    """J. Pattern remains Chính Tài for the Lương Ngọc Huỳnh fixture."""
    payload = OrchestratorService().analyze(**HUYNH)
    assert payload["pattern"]["pattern"] == "chinh_tai"
    assert payload["pattern"]["cach_cuc"] == "Chính Tài"


def test_huynh_useful_god_ranking_unchanged() -> None:
    """Useful God ranking remains sea_004 / Đinh."""
    payload = OrchestratorService().analyze(**HUYNH)
    useful = payload["useful_god"]
    assert useful["useful_god"] == "Đinh"
    assert "sea_004" in useful["matched_rules"]
    assert abs(float(useful["confidence"]) - 0.85) < 0.01


def test_huynh_production_trace_p0_invariants() -> None:
    """Production runner keeps Strength + Useful God truth through Score."""
    output = ProductionEngineRunner().run(
        ProductionRequest(
            year=1966,
            month=9,
            day=24,
            hour=4,
            minute=15,
            gender="male",
            full_name="Lương Ngọc Huỳnh",
            birth_place="Hà Nội, Việt Nam",
        )
    )
    analysis = output.analysis
    assert analysis.strength.strength_level == "strong"
    assert abs(float(analysis.strength.strength_score) - 0.66) < 0.01
    assert analysis.pattern.than_vuong_nhuoc == "Thân vượng"
    assert analysis.pattern.cach_cuc == "Chính Tài"
    assert analysis.useful_god.useful_god == "Đinh"
    assert analysis.useful_god.favorable_gods == ["Đinh", "Bính", "Ất"]
    assert analysis.useful_god.unfavorable_gods == ["Canh", "Tân"]
    assert analysis.pattern.dung_than == "Đinh"
    assert analysis.pattern.hy_than == "Đinh, Bính, Ất"
    assert analysis.pattern.ky_than == "Canh, Tân"


def _published_then_scored() -> dict:
    """Compose Score onto the live Huỳnh RuleContext without mutating publish."""
    from engines.bazi_engine.engine import BaziEngine
    from engines.calendar_engine.engine import CalendarEngine
    from engines.pattern_engine.rule_context_bridge import merge_upstream_into_rule_context
    from engines.pattern_engine.utils.context_builder import build_pattern_context
    from engines.strength_engine.utils.context_builder import build_strength_context
    from engines.temperature_engine.utils.context_builder import build_temperature_context
    from engines.useful_god_engine.utils.context_builder import build_useful_god_context

    orch = OrchestratorService()
    calendar = CalendarEngine().build(1966, 9, 24, 4, 15)
    chart = BaziEngine().build(calendar, gender="male")
    pattern_context = build_pattern_context(chart, calendar=calendar)
    strength = orch.strength_engine.calculate(
        build_strength_context(chart, calendar=calendar)
    )
    pattern_context.strength_level = strength.strength_level
    pattern_context.strength_score = strength.strength_score
    temperature = orch.temperature_engine.calculate(
        build_temperature_context(
            chart,
            calendar=calendar,
            strength_level=strength.strength_level,
            strength_score=strength.strength_score,
        )
    )
    pattern_context.temperature_type = temperature.to_pattern_temperature_type()
    pattern = orch.pattern_engine.calculate(pattern_context)
    useful = orch.useful_god_engine.calculate(
        build_useful_god_context(pattern_context, pattern)
    )
    published = dict(pattern.rule_context or {})
    merge_upstream_into_rule_context(
        published,
        useful_god=useful,
        strength=strength,
        temperature=temperature,
    )
    score = ScoreEngine().calculate(published)
    return ScoreEngine().append_score_to_rule_context(published, score)


def _narrative_text(narrative: dict) -> str:
    chunks: list[str] = []
    for section in narrative.get("sections") or []:
        for paragraph in section.get("paragraphs") or []:
            if isinstance(paragraph, dict):
                chunks.append(str(paragraph.get("text") or ""))
            else:
                chunks.append(str(paragraph or ""))
    return " ".join(chunks)


def _section_text(interpretation: dict, section_id: str) -> str:
    sections = interpretation.get("sections") or []
    matched = []
    for section in sections:
        if section.get("id") == section_id or section.get("name") == section_id:
            matched.append(str(section.get("content") or section.get("body") or ""))
    if matched:
        return " ".join(matched)
    return " ".join(
        str(section.get("body") or section.get("content") or "")
        for section in sections
        if isinstance(section, dict)
    )
