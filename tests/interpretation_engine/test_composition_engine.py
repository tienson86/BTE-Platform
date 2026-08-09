"""IE-3 composition engine integration, serialization, and determinism tests."""

from __future__ import annotations

import json

from engines.interpretation_engine.composition.composition_engine import (
    InterpretationCompositionEngine,
)
from engines.interpretation_engine.composition.composition_result import (
    DIAG_PIPE_OK,
    CanonicalInterpretationResult,
)
from tests.interpretation_engine.ie3_support import assemble_inputs, frozen_clock


def test_composition_engine_assembles_canonical_result() -> None:
    """Engine publishes sections, chapters, xrefs, trace, audit, and diagnostics."""
    payload = assemble_inputs()
    result = InterpretationCompositionEngine(clock=frozen_clock).run(**payload)
    assert isinstance(result, CanonicalInterpretationResult)
    assert result.success is True
    assert result.interpretation_version == "1.0.0"
    assert result.assembly_version == "1.0.0"
    assert [item.section_id for item in result.sections] == [
        "SEC-overview",
        "SEC-luck",
        "SEC-summary",
    ]
    assert len(result.chapters) == 9
    assert result.cross_references
    assert result.interpretation_trace is not None
    assert result.interpretation_trace.started_at == "2026-08-09T12:00:00Z"
    assert "SC-KN-IE2-AN-SEASONAL" in result.interpretation_trace.candidates_consumed
    assert result.interpretation_audit is not None
    assert result.interpretation_audit.contract_validation == "pass"
    assert result.interpretation_audit.flow_legality == "pass"
    assert result.interpretation_audit.cross_reference_integrity == "pass"
    assert any(item.code == DIAG_PIPE_OK for item in result.diagnostics)
    assert result.metadata is not None
    assert result.metadata["reports"] is False
    assert result.metadata["presentation"] is False


def test_serialization_and_determinism() -> None:
    """Repeated runs with a frozen clock yield identical JSON."""
    payload = assemble_inputs()
    engine = InterpretationCompositionEngine(clock=frozen_clock)
    first = json.dumps(engine.run(**payload).to_dict(), sort_keys=True, ensure_ascii=False)
    second = json.dumps(
        InterpretationCompositionEngine(clock=frozen_clock).run(**payload).to_dict(),
        sort_keys=True,
        ensure_ascii=False,
    )
    assert first == second
    decoded = json.loads(first)
    assert "html" not in decoded
    assert "markdown" not in decoded
    assert decoded["sections"]
    assert decoded["interpretation_trace"]["flow_optimization"]["operations"]


def test_missing_selection_fails_without_raising() -> None:
    """Missing IE-2 composition result becomes PIPE-FAIL diagnostics only."""
    payload = assemble_inputs()
    result = InterpretationCompositionEngine(clock=frozen_clock).run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_context=payload["interpretation_context"],
        composition_result=None,
    )
    assert result.success is False
    assert any(item.code == "PIPE-FAIL" for item in result.diagnostics)
    assert result.errors
