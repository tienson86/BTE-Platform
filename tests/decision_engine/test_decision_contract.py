"""AX-3 Decision Pipeline contract tests."""

from __future__ import annotations

from engines.decision_engine.contracts.decision_contract import (
    RESULT_FIELDS,
    decision_result_contract,
)
from engines.decision_engine.pipeline.canonical_decision_pipeline import (
    CanonicalDecisionPipeline,
)
from engines.decision_engine.pipeline.stage_registry import (
    ACTIVE_DECISION_STAGES,
    INACTIVE_FUTURE_STAGES,
    DecisionStageRegistry,
)

SNAPSHOT = {
    "season_score": 50,
    "strength_score": 50,
    "temperature_score": 50,
    "pattern_score": 50,
    "pattern_quality": "average",
    "pattern_confidence": "medium",
    "useful_god": "Chính Tài",
    "decision_confidence": "medium",
    "decision_score": 50,
}


def test_registry_declares_required_fields() -> None:
    """Every stage record must expose the AX-3 catalog contract."""
    registry = DecisionStageRegistry.default()
    for record in registry.list_stages():
        assert record.stage_id
        assert record.package_version
        assert isinstance(record.dependencies, tuple)
        assert isinstance(record.published_inputs, tuple)
        assert isinstance(record.published_outputs, tuple)
        assert isinstance(record.enabled, bool)
    assert registry.enabled_stage_ids() == ACTIVE_DECISION_STAGES
    assert registry.disabled_stage_ids() == INACTIVE_FUTURE_STAGES


def test_registry_io_matches_released_packages() -> None:
    """Registry I/O must match published package contracts."""
    registry = DecisionStageRegistry.default()
    pipeline = CanonicalDecisionPipeline()
    packages = pipeline.load_packages()
    mapping = {
        "useful_god_foundation": "bz_06_useful_god_foundation",
        "useful_god_priority": "bz_07_useful_god_priority",
        "useful_god_override": "bz_08_useful_god_override",
    }
    for stage_id, package_id in mapping.items():
        record = registry.get(stage_id)
        package = packages[package_id]
        assert package.package_type == "decision"
        assert package.schema_version == "2.0.0"
        assert record.package_id == package_id


def test_decision_result_contract_fields() -> None:
    """Canonical Decision Result must publish the AX-3 field set."""
    contract = decision_result_contract()
    assert contract["decision_pipeline_version"] == "1.0.0"
    for field_name in RESULT_FIELDS:
        assert field_name in contract["fields"]
    result = CanonicalDecisionPipeline().run(SNAPSHOT)
    payload = result.to_dict()
    for field_name in RESULT_FIELDS:
        assert field_name in payload
    assert result.decision_audit is not None
    assert result.decision_audit.to_dict()["upstream_preserved"] is True
    assert result.decision_trace is not None
    assert len(result.decision_trace.steps) == 5
