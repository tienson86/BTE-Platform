"""Deterministic Summary aggregator (no domain recomputation)."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
    StageResult,
)
from engines.analysis_engine.summary_engine.exceptions import (
    SummaryConsistencyError,
    SummaryExecutionError,
)
from engines.analysis_engine.summary_engine.models import (
    UPSTREAM_STAGES,
    ConsistencyIssue,
    ConsolidatedConfidenceSummary,
    CrossStageConsistencyReport,
    DomainSummaryView,
    EvidenceIndexEntry,
    SummaryResult,
)

# Stable highlight keys preferred when present in upstream payloads.
_HIGHLIGHT_CANDIDATES: tuple[str, ...] = (
    "classification",
    "pattern_id",
    "useful_gods",
    "favorable",
    "presence",
    "clashes",
    "auspicious",
    "inauspicious",
    "summary",
    "active_count",
    "presence_count",
    "current_da_yun_index",
    "active_layer_names",
)

_CONFIDENCE_LEVELS: tuple[tuple[float, str], ...] = (
    (0.85, "high"),
    (0.60, "medium"),
    (0.0, "low"),
)


class SummaryAggregator:
    """Aggregate published StageResults into SummaryResult."""

    def aggregate(
        self,
        context: AnalysisContext,
        *,
        upstream: Mapping[str, StageResult],
    ) -> SummaryResult:
        """Run deterministic consolidation."""
        try:
            views = {
                stage_id: self._build_view(upstream[stage_id])
                for stage_id in UPSTREAM_STAGES
            }
            consistency = self._check_consistency(context, upstream)
            if consistency.status == "fail":
                blocking = [
                    issue for issue in consistency.issues if issue.severity == "error"
                ]
                raise SummaryConsistencyError(
                    "Blocking cross-stage inconsistency detected",
                    details={
                        "issues": [issue.code for issue in blocking],
                    },
                )

            evidence_index = self._build_evidence_index(upstream)
            consolidated = self._consolidate_confidence(upstream)
            evidence = (
                RuleEvidence(
                    rule_id="summary:aggregation",
                    version="1.0.0",
                    category="summary",
                    priority=100,
                    reference="summary_engine",
                    details={
                        "upstream_stages": list(UPSTREAM_STAGES),
                        "evidence_index_count": len(evidence_index),
                    },
                ),
            )
            diagnostics = (
                DiagnosticInfo(
                    code="summary_completed",
                    message="Summary aggregation completed",
                    level="info",
                    stage_id="summary",
                    details={
                        "consistency_status": consistency.status,
                        "issue_count": consistency.issue_count,
                    },
                ),
            )
            return SummaryResult(
                strength_summary=views["strength"],
                temperature_summary=views["temperature"],
                pattern_summary=views["pattern"],
                useful_god_summary=views["useful_god"],
                ten_gods_summary=views["ten_gods"],
                combination_summary=views["combination"],
                shensha_summary=views["shensha"],
                luck_summary=views["luck"],
                consistency=consistency,
                consolidated_confidence=consolidated,
                evidence_index=tuple(evidence_index),
                confidence=ConfidenceEvaluation(
                    score=consolidated.score,
                    level=consolidated.level,
                    details=dict(consolidated.details),
                ),
                evidence=evidence,
                diagnostics=diagnostics,
                summary={
                    "upstream_stage_count": len(UPSTREAM_STAGES),
                    "consistency_status": consistency.status,
                    "evidence_index_count": len(evidence_index),
                    "consolidated_confidence_score": consolidated.score,
                    "stage_ids": list(UPSTREAM_STAGES),
                },
            )
        except SummaryConsistencyError:
            raise
        except Exception as exc:
            raise SummaryExecutionError(
                f"Summary aggregation failed: {exc}",
                details={"exception_type": type(exc).__name__},
            ) from exc

    def _build_view(self, result: StageResult) -> DomainSummaryView:
        payload = dict(result.payload or {})
        highlight_keys = tuple(
            key for key in _HIGHLIGHT_CANDIDATES if key in payload
        )
        digest: dict[str, Any] = {}
        for key in highlight_keys:
            value = payload[key]
            digest[key] = self._digest_value(value)

        confidence_score = None
        confidence_level = None
        if result.confidence is not None:
            confidence_score = result.confidence.score
            confidence_level = result.confidence.level
        elif isinstance(payload.get("confidence"), dict):
            confidence_score = payload["confidence"].get("score")
            confidence_level = payload["confidence"].get("level")

        return DomainSummaryView(
            stage_id=result.stage_id,
            status=result.status,
            module_version=result.module_version,
            highlight_keys=highlight_keys,
            payload_digest=digest,
            confidence_score=(
                float(confidence_score) if confidence_score is not None else None
            ),
            confidence_level=confidence_level,
            evidence_count=len(result.evidence),
        )

    def _check_consistency(
        self,
        context: AnalysisContext,
        upstream: Mapping[str, StageResult],
    ) -> CrossStageConsistencyReport:
        issues: list[ConsistencyIssue] = []

        for stage_id, result in upstream.items():
            if result.status != "success":
                issues.append(
                    ConsistencyIssue(
                        code="upstream_not_success",
                        severity="error",
                        message=f"Stage '{stage_id}' status is {result.status}",
                        stages=(stage_id,),
                    )
                )

        # All stages must publish a payload mapping.
        for stage_id, result in upstream.items():
            if not isinstance(result.payload, dict):
                issues.append(
                    ConsistencyIssue(
                        code="invalid_payload_type",
                        severity="error",
                        message=f"Stage '{stage_id}' payload must be a mapping",
                        stages=(stage_id,),
                    )
                )

        # Traceability: stages with empty evidence are warnings only.
        for stage_id, result in upstream.items():
            if not result.evidence:
                payload_evidence = (result.payload or {}).get("evidence")
                if not payload_evidence:
                    issues.append(
                        ConsistencyIssue(
                            code="missing_evidence",
                            severity="warning",
                            message=f"Stage '{stage_id}' has no evidence entries",
                            stages=(stage_id,),
                        )
                    )

        # Request identity alignment when payload embeds request_id.
        for stage_id, result in upstream.items():
            payload_request_id = (result.payload or {}).get("request_id")
            if payload_request_id and str(payload_request_id) != context.request_id:
                issues.append(
                    ConsistencyIssue(
                        code="request_id_mismatch",
                        severity="error",
                        message="Upstream payload request_id does not match context",
                        stages=(stage_id,),
                        details={
                            "expected": context.request_id,
                            "actual": payload_request_id,
                        },
                    )
                )

        has_error = any(issue.severity == "error" for issue in issues)
        has_warning = any(issue.severity == "warning" for issue in issues)
        if has_error:
            status = "fail"
        elif has_warning:
            status = "warn"
        else:
            status = "pass"

        issues_sorted = tuple(
            sorted(issues, key=lambda item: (item.severity, item.code, item.stages))
        )
        return CrossStageConsistencyReport(
            status=status,
            issue_count=len(issues_sorted),
            issues=issues_sorted,
        )

    def _build_evidence_index(
        self,
        upstream: Mapping[str, StageResult],
    ) -> list[EvidenceIndexEntry]:
        entries: list[EvidenceIndexEntry] = []
        for stage_id in UPSTREAM_STAGES:
            result = upstream[stage_id]
            for item in result.evidence:
                entries.append(
                    EvidenceIndexEntry(
                        stage_id=stage_id,
                        rule_id=item.rule_id,
                        category=item.category,
                        priority=item.priority,
                        reference=item.reference,
                        version=item.version,
                        details=dict(item.details),
                    )
                )
            # Also index payload-embedded evidence when StageResult.evidence is empty.
            if not result.evidence:
                for raw in (result.payload or {}).get("evidence") or []:
                    if not isinstance(raw, dict) or "rule_id" not in raw:
                        continue
                    entries.append(
                        EvidenceIndexEntry(
                            stage_id=stage_id,
                            rule_id=str(raw["rule_id"]),
                            category=str(raw.get("category") or ""),
                            priority=int(raw.get("priority", 0)),
                            reference=str(raw.get("reference") or ""),
                            version=str(raw.get("version") or "1.0.0"),
                            details=dict(raw.get("details") or {}),
                        )
                    )
        entries.sort(
            key=lambda item: (
                UPSTREAM_STAGES.index(item.stage_id),
                -item.priority,
                item.rule_id,
                item.category,
            )
        )
        return entries

    def _consolidate_confidence(
        self,
        upstream: Mapping[str, StageResult],
    ) -> ConsolidatedConfidenceSummary:
        stage_scores: dict[str, float] = {}
        for stage_id in UPSTREAM_STAGES:
            result = upstream[stage_id]
            score = None
            if result.confidence is not None and result.confidence.score is not None:
                score = float(result.confidence.score)
            else:
                payload_confidence = (result.payload or {}).get("confidence")
                if isinstance(payload_confidence, dict) and payload_confidence.get(
                    "score"
                ) is not None:
                    score = float(payload_confidence["score"])
            if score is None:
                score = 0.5  # neutral contribution when stage omits confidence
            stage_scores[stage_id] = round(min(1.0, max(0.0, score)), 4)

        values = list(stage_scores.values())
        score = round(sum(values) / len(values), 4)
        level = "low"
        for threshold, name in _CONFIDENCE_LEVELS:
            if score >= threshold:
                level = name
                break
        return ConsolidatedConfidenceSummary(
            score=score,
            level=level,
            stage_scores=stage_scores,
            details={"method": "arithmetic_mean", "stage_count": len(values)},
        )

    @staticmethod
    def _digest_value(value: Any) -> Any:
        """Create a stable, shallow digest of upstream payload values."""
        if isinstance(value, dict):
            keys = sorted(value.keys())
            return {
                "type": "mapping",
                "keys": keys[:20],
                "size": len(keys),
            }
        if isinstance(value, list):
            return {"type": "list", "size": len(value)}
        if isinstance(value, tuple):
            return {"type": "tuple", "size": len(value)}
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return {"type": type(value).__name__}
