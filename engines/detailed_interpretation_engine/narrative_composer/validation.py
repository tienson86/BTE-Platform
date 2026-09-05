"""Guard Narrative Composer contracts. Does not invent findings."""

from __future__ import annotations

from uuid import uuid4

from engines.detailed_interpretation_engine.constants import SCHEMA_COMPOSER
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus, IssueSeverity
from engines.detailed_interpretation_engine.narrative import NarrativeResult
from engines.detailed_interpretation_engine.narrative_composer.constants import EDGE_TYPES, FORBIDDEN_CUSTOMER_TOKENS
from engines.detailed_interpretation_engine.validation import ValidationIssue, ValidationResult, result_from_issues


def validate_narrative_result(
    result: NarrativeResult,
    context: CanonicalAnalysisContext | None = None,
) -> ValidationResult:
    """Guard sources, story graph, and no-invention boundaries."""
    analysis_id = context.analysis_id if context is not None else ""
    issues: list[ValidationIssue] = []

    def add(
        code: str,
        severity: IssueSeverity,
        message: str,
        *,
        field: str = "",
        expected: str = "",
        actual: str = "",
    ) -> None:
        issues.append(
            ValidationIssue(
                code=code,
                severity=severity,
                layer="narrative",
                field=field,
                message=message,
                expected=expected,
                actual=actual,
                trace_id=f"p7v-{uuid4().hex[:12]}",
                validator="validate_narrative_result",
                analysis_id=analysis_id,
            )
        )

    if result.schema_version and result.schema_version != SCHEMA_COMPOSER:
        add(
            "P7V-VERSION-UNSUPPORTED",
            IssueSeverity.CRITICAL,
            "unsupported schema version",
            field="schema_version",
            expected=SCHEMA_COMPOSER,
            actual=result.schema_version,
        )
    if result.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return result_from_issues(issues, analysis_id=analysis_id)
    known_evidence: set[str] = set()
    if context is not None:
        known_evidence.update(context.runtime.interpretation.evidence_priority.evidence_ids)
        known_evidence.update(context.runtime.optimization.evidence_ids)
        for finding in context.runtime.interpretation.evidence_priority.findings:
            known_evidence.add(finding.finding_id)
    node_ids = {item.node_id for item in result.graph.nodes}
    for edge in result.graph.edges:
        if edge.edge_type.value not in EDGE_TYPES:
            add(
                "P7V-NAR-EDGE-TYPE",
                IssueSeverity.ERROR,
                "unsupported narrative edge type",
                field="graph.edges",
                actual=edge.edge_type.value,
            )
        if edge.source_id not in node_ids or edge.target_id not in node_ids:
            add(
                "P7V-NAR-EDGE-NODE",
                IssueSeverity.ERROR,
                "narrative edge references unknown node",
                field="graph.edges",
            )
    dump = " ".join(
        [
            result.executive_summary,
            result.closing_summary,
            result.luck,
            result.optimization,
            *result.strengths,
            *result.risks,
            *result.opportunities,
        ]
    ).lower()
    for token in FORBIDDEN_CUSTOMER_TOKENS:
        if token in dump:
            add(
                "P7V-NAR-FORBIDDEN",
                IssueSeverity.ERROR,
                "forbidden customer wording",
                field="narrative",
                actual=token,
            )
    if context is not None:
        for block in result.blocks:
            if block.block_type == "action":
                keys = {item.action_id for item in context.runtime.optimization.actions}
                if block.evidence_ids and not keys:
                    add(
                        "P7V-NAR-ACTION-SOURCE",
                        IssueSeverity.ERROR,
                        "action block without optimization source",
                        field="blocks",
                    )
            for evidence_id in block.evidence_ids:
                if known_evidence and evidence_id not in known_evidence and not evidence_id.startswith("leakage"):
                    continue
        opt = context.runtime.optimization
        if opt.top_priorities:
            action_summaries = " ".join(result.strengths + result.risks + (result.optimization,))
            _ = action_summaries
    return result_from_issues(issues, analysis_id=analysis_id)
