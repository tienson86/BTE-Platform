"""Regression: IE-1 / IE-2 / IE-3 remain unchanged after IX-1."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from engines.interpretation_engine.composition.composition_engine import (
    InterpretationCompositionEngine,
)
from engines.interpretation_engine.composition.composition_result import (
    CanonicalInterpretationResult as AssembledInterpretationResult,
)
from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.contracts.interpretation_contracts import (
    empty_interpretation_result,
    interpretation_foundation_contract,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.sentence_candidate_builder import (
    SentenceCandidateBuilder,
)
from engines.interpretation_engine.pipeline.canonical_interpretation_pipeline import (
    CanonicalInterpretationPipeline,
)
from engines.interpretation_engine.pipeline.interpretation_audit import AUDIT_SCHEMA_KEYS
from engines.interpretation_engine.pipeline.interpretation_trace import (
    STEP_SCHEMA_KEYS,
    TRACE_SCHEMA_KEYS,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot
from tests.interpretation_engine.ie3_support import assemble_inputs, frozen_clock

IE1_FOUNDATION_CONTRACT_CHECKSUM = (
    "f3aebc2bfb5cbcb7881fbb7ce760536adcf5b1abfa86c511a7a5c5c39f0a7cd6"
)

IE2_CANDIDATE_FIELDS: tuple[str, ...] = (
    "sentence_id",
    "template_id",
    "placeholder_values",
    "evidence_ids",
    "reasoning_ids",
    "confidence",
    "references",
    "knowledge_id",
)

IE3_TRACE_KEYS: tuple[str, ...] = (
    "assembly_version",
    "candidates_consumed",
    "sections_created",
    "chapters_created",
    "flow_optimization",
    "cross_references",
    "started_at",
    "completed_at",
    "stage_order",
)

IE3_AUDIT_KEYS: tuple[str, ...] = (
    "contract_validation",
    "registry_validation",
    "flow_legality",
    "chapter_legality",
    "section_legality",
    "cross_reference_integrity",
    "version_compatibility",
    "reason_codes",
)


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def _checksum(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def test_ie1_foundation_checksum_and_contract_unchanged() -> None:
    """IE-1 foundation contract, empty shell, and independent context stay sealed."""
    contract = interpretation_foundation_contract()
    assert contract["interpretation_version"] == "1.0.0"
    assert contract["text_generation"] is False
    assert contract["reports"] is False
    assert contract["ai"] is False
    assert contract["packages_loaded"] is False
    assert _checksum(contract) == IE1_FOUNDATION_CONTRACT_CHECKSUM
    shell = empty_interpretation_result()
    payload = shell.to_dict()
    assert payload["status"] == "empty"
    assert payload["sections"] == []
    assert "IE1-EMPTY-SHELL" in payload["diagnostics"]
    context = build_interpretation_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    assert context.to_dict()["interpretation_version"] == "1.0.0"


def test_ie2_knowledge_contract_and_outputs_unchanged() -> None:
    """IE-2 published candidate fields remain independently executable."""
    interpretation = build_interpretation_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    result = SentenceCandidateBuilder().run(
        build_composition_context(
            analysis_result=ax2_snapshot(),
            decision_result=ax3_snapshot(),
            luck_result=ax4_snapshot(),
            interpretation_context=interpretation,
        )
    )
    assert result.success is True
    assert result.composition_version == "1.0.0"
    assert result.ai_rewrite["enabled"] is False
    payload = result.to_dict()
    assert "candidates" in payload
    for candidate in result.candidates:
        assert tuple(candidate.to_dict()) == IE2_CANDIDATE_FIELDS


def test_ie3_composition_contract_trace_and_audit_unchanged() -> None:
    """IE-3 published assembly, trace, and audit remain independently executable."""
    payload = assemble_inputs()
    result = InterpretationCompositionEngine(clock=frozen_clock).run(**payload)
    assert isinstance(result, AssembledInterpretationResult)
    assert result.success is True
    assert result.assembly_version == "1.0.0"
    serialized = result.to_dict()
    for name in (
        "sections",
        "chapters",
        "cross_references",
        "interpretation_trace",
        "interpretation_audit",
    ):
        assert name in serialized
    assert result.interpretation_trace is not None
    assert result.interpretation_audit is not None
    assert tuple(result.interpretation_trace.to_dict()) == IE3_TRACE_KEYS
    assert tuple(result.interpretation_audit.to_dict()) == IE3_AUDIT_KEYS
    assert result.interpretation_audit.contract_validation == "pass"


def test_ix1_trace_and_audit_schemas_stable() -> None:
    """IX-1 trace and audit schemas publish the frozen key sets."""
    result = CanonicalInterpretationPipeline(clock=_clock).run(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    assert result.interpretation_trace is not None
    assert result.interpretation_audit is not None
    assert tuple(result.interpretation_trace.to_dict()) == TRACE_SCHEMA_KEYS
    assert tuple(result.interpretation_audit.to_dict()) == AUDIT_SCHEMA_KEYS
    assert tuple(result.interpretation_trace.steps[0].to_dict()) == STEP_SCHEMA_KEYS
