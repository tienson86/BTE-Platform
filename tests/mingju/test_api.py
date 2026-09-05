"""Public API and Pack 07 snapshot contract."""

from __future__ import annotations

from engines.mingju import analyze_mingju, compose_mingju_decision, to_pack07_snapshot, to_public_dict
from tests.mingju.conftest import context_from


def test_root_result_metadata() -> None:
    result = analyze_mingju(context_from())
    assert result.analysis_id == "an-mc01-test-001"
    assert result.chart_id == "1987-01-21"
    assert result.schema_version == "bte.mingju.decision.v1"
    assert result.ruleset_version == "bte.mingju.rules.v1"
    assert result.result_id == "mc01:an-mc01-test-001"
    assert result.content_hash
    assert result.status in {"complete", "partial", "unresolved", "insufficient_evidence", "invalid_input"}
    assert 0 <= result.confidence <= 1
    assert result.trace_ids
    assert result.pattern.source == "canonical_pattern_engine"
    assert result.pattern.pattern_id == "zheng_yin"


def test_public_dict_omits_debug_hashes() -> None:
    public = to_public_dict(analyze_mingju(context_from()))
    assert "content_hash" not in public
    assert "trace_ids" not in public
    assert public["grade"]["grade"]
    assert public["integrity"]["state"]


def test_pack07_snapshot_exposes_structural_ids() -> None:
    snapshot = to_pack07_snapshot(analyze_mingju(context_from()))
    assert snapshot["source"] == "mingju_decision_engine"
    assert snapshot["pattern"]
    assert snapshot["grade"]
    assert snapshot["purity"]
    assert "D+" != snapshot["grade"]


def test_composer_is_structural_not_pack07_narrative() -> None:
    result = analyze_mingju(context_from())
    composed = compose_mingju_decision(result)
    assert composed.composer_version == "bte.mingju.composer.v1"
    assert composed.headline
    assert composed.summary
    assert "Luck activation" not in composed.summary
