"""Tests for narrative planner."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.knowledge_loader.loader import KnowledgeCatalogLoader
from engines.interpretation_engine_v2.strength.narrative.planner import NarrativePlanner
from engines.interpretation_engine_v2.strength.reasoner.engine import StrengthReasoner
from engines.interpretation_engine_v2.strength.tests.test_reasoner import _build_input


def test_narrative_planner_adds_claim_traces() -> None:
    loader = KnowledgeCatalogLoader()
    units_by_id = {unit.knowledge_id: unit for unit in loader.load_all()}
    plan = StrengthReasoner().build_plan(_build_input())
    finalized = NarrativePlanner().finalize(plan, units_by_id)
    traces = finalized.diagnostics.get("claim_traces", [])
    assert traces
    assert traces[0]["customer_section"] == "CONCLUSION"
