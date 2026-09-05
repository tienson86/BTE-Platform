"""P7-IMP-03 Pack 07 validation layer and diagnostics."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.context_layers import EvidenceContext, TemporalContext
from engines.detailed_interpretation_engine.diagnostics import build_pack07_diagnostics
from engines.detailed_interpretation_engine.domains import (
    AuthorityResult,
    DomainInterpretationResult,
    DomainSection,
)
from engines.detailed_interpretation_engine.enums import (
    BindingState,
    DiagnosticStatus,
    DomainState,
    EvaluationStatus,
    ValidationStatus,
)
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult
from engines.detailed_interpretation_engine.exceptions import DetailedInterpretationValidationError
from engines.detailed_interpretation_engine.factories import (
    api_model_from_runtime,
    build_canonical_analysis_context,
    build_domain_context,
    consulting_model_from_runtime,
    empty_canonical_runtime_result,
    export_model_from_runtime,
)
from engines.detailed_interpretation_engine.runtime import CanonicalExportModel
from engines.detailed_interpretation_engine.serialization import (
    compute_content_hash,
    serialize_runtime_result,
)
from engines.detailed_interpretation_engine.temporal import TemporalActivationResult, TemporalSection
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    payload_unchanged,
    validate_canonical_runtime,
    validate_domain_context,
    validate_evidence_context,
    validate_export_projection,
    validate_pack07_context,
    validate_temporal_context,
)

SAMPLE_PAYLOAD = {
    "analysis_id": "an-p7-val-001",
    "pattern": {"cach_cuc": "Chinh An"},
    "score": {"grade": "B"},
    "identity": {
        "person": {"solar_birth": "1990-05-15", "gender": "male"},
        "calendar": {"solar_date": "1990-05-15"},
        "four_pillars": {"hour": {"stem": "Ky", "branch": "Ti"}},
    },
}


def test_valid_empty_foundation_context() -> None:
    result = validate_pack07_context(build_canonical_analysis_context("an-p7-val-empty"))
    assert result.status in (ValidationStatus.PASS, ValidationStatus.PASS_WITH_WARNINGS)
    assert not result.errors
    assert BindingState.NOT_BOUND.value == "not_bound"


def test_analysis_id_mismatch_fails() -> None:
    context = build_canonical_analysis_context("an-p7-val-a")
    mismatched = replace(context, evidence=replace(context.evidence, analysis_id="an-p7-val-b"))
    result = validate_pack07_context(mismatched)
    assert result.status is ValidationStatus.FAIL
    assert any(item.code == "P7V-CTX-ANALYSIS-ID-MISMATCH" for item in result.errors)
    with pytest.raises(DetailedInterpretationValidationError):
        assert_valid(result)


def test_unsupported_schema_fails() -> None:
    bad = replace(build_canonical_analysis_context("an-p7-val-schema"), schema_version="bte.unknown.v9")
    result = validate_pack07_context(bad)
    assert result.status is ValidationStatus.FAIL
    assert any(item.code == "P7V-VERSION-UNSUPPORTED" for item in result.errors)


def test_pattern_and_grade_ownership_violations() -> None:
    runtime = empty_canonical_runtime_result("an-p7-val-own")
    patterned = serialize_runtime_result(runtime)
    patterned["pattern"] = {"cach_cuc": "owned"}
    graded = serialize_runtime_result(runtime)
    graded["grade"] = "A"
    pattern_result = validate_canonical_runtime(patterned)
    grade_result = validate_canonical_runtime(graded)
    assert any(item.code == "P7V-OWNERSHIP-PATTERN" for item in pattern_result.errors)
    assert any(item.code == "P7V-OWNERSHIP-GRADE" for item in grade_result.errors)


def test_valid_not_evaluated_domain_shells() -> None:
    result = validate_domain_context(build_domain_context("an-p7-val-domains"))
    assert result.status is ValidationStatus.PASS


def test_invalid_evaluated_shell_without_source() -> None:
    natal = DomainInterpretationResult(domain_id="authority", state=DomainState.STRONG)
    context = replace(
        build_domain_context("an-p7-val-eval"),
        domains=DomainSection(authority=AuthorityResult(natal=natal)),
    )
    result = validate_domain_context(context)
    assert any(item.code == "P7V-DOMAIN-EVALUATED-EMPTY" for item in result.errors)


def test_projection_analysis_id_parity_and_mismatch() -> None:
    runtime = empty_canonical_runtime_result("an-p7-val-proj")
    export = export_model_from_runtime(runtime)
    api = api_model_from_runtime(runtime)
    consulting = consulting_model_from_runtime(runtime)
    assert export.analysis_id == api.analysis_id == consulting.analysis_id
    assert validate_export_projection(export, runtime).status is ValidationStatus.PASS
    bad = validate_export_projection(CanonicalExportModel(analysis_id="other"), runtime)
    assert any(item.code == "P7V-PROJECTION-ANALYSIS-ID" for item in bad.errors)


def test_content_hash_stable_when_created_at_changes() -> None:
    first = empty_canonical_runtime_result("an-p7-val-hash", created_at="2026-01-01T00:00:00+00:00")
    second = empty_canonical_runtime_result("an-p7-val-hash", created_at="2026-12-31T23:59:59+00:00")
    left = serialize_runtime_result(first)
    right = deepcopy(left)
    right["metadata"]["created_at"] = "2026-12-31T23:59:59+00:00"
    assert compute_content_hash(left) == compute_content_hash(right)
    assert first.metadata.content_hash == second.metadata.content_hash
    assert validate_canonical_runtime(first).status in (
        ValidationStatus.PASS,
        ValidationStatus.PASS_WITH_WARNINGS,
    )


def test_warning_only_missing_optional_temporal_layer() -> None:
    activation = TemporalActivationResult(requested_layers=("monthly", "hourly"))
    context = TemporalContext(
        analysis_id="an-p7-val-temp",
        temporal=activation,
        section=TemporalSection(temporal_activation=activation, requested_layers=("monthly", "hourly")),
    )
    result = validate_temporal_context(context)
    assert result.status is ValidationStatus.PASS_WITH_WARNINGS
    assert not result.errors


def test_critical_fail_closed_runtime_corruption() -> None:
    result = validate_canonical_runtime({})
    assert result.status is ValidationStatus.FAIL
    with pytest.raises(DetailedInterpretationValidationError):
        assert_valid(result)


def test_evaluated_evidence_without_source_refs_fails() -> None:
    context = EvidenceContext(
        analysis_id="an-p7-val-evi",
        status=EvaluationStatus.RESOLVED,
        evidence=EvidencePriorityResult(status=EvaluationStatus.RESOLVED),
    )
    result = validate_evidence_context(context)
    assert any(item.code == "P7V-EVIDENCE-EVALUATED-EMPTY" for item in result.errors)


def test_builders_do_not_mutate_upstream_payload() -> None:
    original = deepcopy(SAMPLE_PAYLOAD)
    snapshot = deepcopy(SAMPLE_PAYLOAD)
    build_canonical_analysis_context_from_payload(original)
    assert payload_unchanged(snapshot, original)


def test_diagnostics_expected_imp03_states() -> None:
    diagnostics = build_pack07_diagnostics(build_canonical_analysis_context("an-p7-val-diag"))
    assert diagnostics.contracts is DiagnosticStatus.PASS
    assert diagnostics.contexts is DiagnosticStatus.PASS
    assert diagnostics.validators is DiagnosticStatus.PASS
    assert diagnostics.mc01_reference is DiagnosticStatus.NOT_BOUND
    assert diagnostics.ten_gods is DiagnosticStatus.NOT_IMPLEMENTED
    assert diagnostics.shen_sha is DiagnosticStatus.NOT_IMPLEMENTED
    assert diagnostics.evidence_priority is DiagnosticStatus.NOT_IMPLEMENTED
    assert diagnostics.domains is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.luck is DiagnosticStatus.NOT_IMPLEMENTED
    assert diagnostics.temporal is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.optimization is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.narrative is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.runtime_contract is DiagnosticStatus.PASS
    assert diagnostics.overall_status is DiagnosticStatus.PASS
    joined = " ".join(item.message.lower() for item in diagnostics.issues)
    assert "not implemented" not in joined


def test_dev_diagnostics_endpoint_and_analyze_does_not_leak() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/dev/pack07/diagnostics")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["mc01_reference"] == "NOT_BOUND"
    assert data["runtime_contract"] == "PASS"
    analyzed = client.post(
        "/api/v1/analyze",
        json={"year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30, "gender": "male"},
    )
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    assert "pack07_context" not in body
    assert "pack07" not in str(body.get("pipeline"))


def test_dev_diagnostics_hidden_in_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BTE_ENV", "production")
    client = TestClient(create_app())
    assert client.get("/api/v1/dev/pack07/diagnostics").status_code == 404
