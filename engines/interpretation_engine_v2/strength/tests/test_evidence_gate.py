"""Tests for evidence gate."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import GateState
from engines.interpretation_engine_v2.strength.knowledge_loader.loader import KnowledgeCatalogLoader
from engines.interpretation_engine_v2.strength.runtime.case_0001 import load_case_0001_facts
from engines.interpretation_engine_v2.strength.selector.evidence_gate import EvidenceGate


def test_drain_inactive_rejects_drain_cause() -> None:
    loader = KnowledgeCatalogLoader()
    units = {unit.knowledge_id: unit for unit in loader.load_all()}
    published = load_case_0001_facts()
    gate = EvidenceGate()
    result = gate.evaluate(units["IK-STR-CAUS-0013"], published)
    assert result.state == GateState.INELIGIBLE
    assert result.reason_code == "REJECTED_FACT_INACTIVE"


def test_season_cause_eligible_for_case_0001() -> None:
    loader = KnowledgeCatalogLoader()
    units = {unit.knowledge_id: unit for unit in loader.load_all()}
    published = load_case_0001_facts()
    gate = EvidenceGate()
    result = gate.evaluate(units["IK-STR-CAUS-0002"], published)
    assert result.state == GateState.ELIGIBLE
