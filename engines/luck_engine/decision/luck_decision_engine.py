"""Luck Decision Engine (LE-3). Normalized decisions only. Never raises to API."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from engines.luck_engine.decision.decision_context import (
    LuckDecisionContext,
    LuckDecisionDiagnostic,
    diagnostic,
)
from engines.luck_engine.decision.decision_registry import LuckDecisionRegistry
from engines.luck_engine.decision.decision_result import (
    LuckDecisionAudit,
    LuckDecisionResult,
    LuckDecisionTrace,
    build_decision_trace,
)
from engines.luck_engine.decision.package_loader import LuckDecisionPackageLoader
from engines.luck_engine.decision.validation import validate_result_payload
from engines.luck_engine.decision_constants import (
    DECISION_VERSION,
    DIAG_ANALYSIS_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_DECISION_MISSING,
    DIAG_DEP_VIOLATION,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_TIMELINE_MISSING,
    OUTPUT_AUDIT,
    OUTPUT_CONFIDENCE,
    OUTPUT_OPPORTUNITY,
    OUTPUT_OVERALL,
    OUTPUT_PRIORITY,
    OUTPUT_REASONING,
    OUTPUT_RISK,
    OUTPUT_TRACE,
    OUTPUT_VERSION,
    PUBLISHED_OUTPUTS,
    STAGE_CONFIDENCE,
    STAGE_OPPORTUNITY,
    STAGE_PRIORITY,
    STAGE_PUBLICATION,
    STAGE_RISK,
)
from engines.luck_engine.exceptions import (
    DuplicateDecisionError,
    LuckDecisionDependencyError,
    LuckDecisionError,
    LuckDecisionValidationError,
    LuckPackageLoadError,
)
from engines.luck_engine.integration.confidence_stage import ConfidenceStage
from engines.luck_engine.integration.opportunity_stage import OpportunityStage
from engines.luck_engine.integration.priority_stage import PriorityStage
from engines.luck_engine.integration.publication_stage import PublicationStage
from engines.luck_engine.integration.risk_stage import RiskStage

logger = logging.getLogger(__name__)

_STAGE_OUTPUT = {
    STAGE_OPPORTUNITY: OUTPUT_OPPORTUNITY,
    STAGE_RISK: OUTPUT_RISK,
    STAGE_CONFIDENCE: OUTPUT_CONFIDENCE,
    STAGE_PRIORITY: OUTPUT_PRIORITY,
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def snapshot_input(value: Any, *, label: str) -> dict[str, Any] | None:
    """Copy an upstream object into an isolated mapping."""
    if value is None:
        return None
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError(f"invalid_{label}")


class LuckDecisionEngine:
    """Only supported LE-3 execution model for luck opportunity / risk decisions."""

    decision_version: str = DECISION_VERSION

    def __init__(
        self,
        *,
        registry: LuckDecisionRegistry | None = None,
        loader: LuckDecisionPackageLoader | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize registry, optional package loader, and clock."""
        self.registry = registry or LuckDecisionRegistry()
        self.loader = loader or LuckDecisionPackageLoader()
        self.clock = clock or _utc_now
        self._stages = {
            STAGE_OPPORTUNITY: OpportunityStage(),
            STAGE_RISK: RiskStage(),
            STAGE_CONFIDENCE: ConfidenceStage(),
            STAGE_PRIORITY: PriorityStage(),
            STAGE_PUBLICATION: PublicationStage(),
        }

    def run(
        self,
        *,
        timeline_result: Any,
        luck_analysis_result: Any,
        analysis_result: Any,
        decision_result: Any,
    ) -> LuckDecisionResult:
        """Decide from timeline + luck analysis + AX-2 + AX-3. Diagnostics only at the boundary."""
        started = _iso(self.clock())
        diagnostics: list[LuckDecisionDiagnostic] = []
        errors: list[str] = []
        try:
            return self._run_inner(
                timeline_result=timeline_result,
                luck_analysis_result=luck_analysis_result,
                analysis_result=analysis_result,
                decision_result=decision_result,
                started=started,
                diagnostics=diagnostics,
                errors=errors,
            )
        except LuckDecisionError as exc:
            logger.warning("luck_decision_failed %s", exc)
            errors.append(str(exc))
            diagnostics.append(
                diagnostic(DIAG_PIPE_FAIL, "Luck Decision failed", details={"error": str(exc)})
            )
            return self._empty_result(diagnostics, errors, started, _iso(self.clock()))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("luck_decision_unexpected")
            errors.append(str(exc))
            diagnostics.append(
                diagnostic(DIAG_PIPE_FAIL, "Luck Decision failed", details={"error": str(exc)})
            )
            return self._empty_result(diagnostics, errors, started, _iso(self.clock()))

    def _run_inner(
        self,
        *,
        timeline_result: Any,
        luck_analysis_result: Any,
        analysis_result: Any,
        decision_result: Any,
        started: str,
        diagnostics: list[LuckDecisionDiagnostic],
        errors: list[str],
    ) -> LuckDecisionResult:
        timeline_snap = self._require_snapshot(
            timeline_result,
            label="timeline",
            code=DIAG_TIMELINE_MISSING,
            diagnostics=diagnostics,
            errors=errors,
        )
        luck_snap = self._require_snapshot(
            luck_analysis_result,
            label="luck_analysis",
            code=DIAG_ANALYSIS_MISSING,
            diagnostics=diagnostics,
            errors=errors,
        )
        analysis_snap = self._require_snapshot(
            analysis_result,
            label="canonical_analysis",
            code=DIAG_ANALYSIS_MISSING,
            diagnostics=diagnostics,
            errors=errors,
        )
        decision_snap = self._require_snapshot(
            decision_result,
            label="canonical_decision",
            code=DIAG_DECISION_MISSING,
            diagnostics=diagnostics,
            errors=errors,
        )
        if None in (timeline_snap, luck_snap, analysis_snap, decision_snap):
            diagnostics.append(diagnostic(DIAG_PIPE_FAIL, "Required Luck Decision inputs missing"))
            return self._empty_result(diagnostics, errors, started, _iso(self.clock()))

        try:
            self.loader.load()
        except LuckPackageLoadError as exc:
            diagnostics.append(
                diagnostic(
                    DIAG_CONTRACT_VIOLATION,
                    "Luck Foundation package not admitted",
                    severity="warning",
                    details={"error": str(exc)},
                )
            )

        context = LuckDecisionContext(
            timeline_snapshot=timeline_snap,
            luck_analysis_snapshot=luck_snap,
            analysis_snapshot=analysis_snap,
            decision_snapshot=decision_snap,
            started_at=started,
            diagnostics=diagnostics,
        )
        self._execute_stages(context, errors)
        return self._finalize(context, errors, started)

    def _require_snapshot(
        self,
        value: Any,
        *,
        label: str,
        code: str,
        diagnostics: list[LuckDecisionDiagnostic],
        errors: list[str],
    ) -> dict[str, Any] | None:
        if value is None:
            diagnostics.append(diagnostic(code, f"Missing {label} input", details={"input": label}))
            errors.append(f"missing_{label}")
            return None
        try:
            return snapshot_input(value, label=label)
        except TypeError as exc:
            diagnostics.append(
                diagnostic(DIAG_CONTRACT_VIOLATION, f"Invalid {label} input", details={"error": str(exc)})
            )
            errors.append(str(exc))
            return None

    def _execute_stages(self, context: LuckDecisionContext, errors: list[str]) -> None:
        for stage_id in self.registry.canonical_order():
            stage = self._stages[stage_id]
            try:
                payload = stage.execute(context)
                if stage_id == STAGE_PUBLICATION:
                    for name, value in payload.items():
                        context.publish(str(name), value)
                else:
                    context.publish(_STAGE_OUTPUT[stage_id], payload)
                context.record_stage(stage_id)
            except LuckDecisionDependencyError as exc:
                errors.append(str(exc))
                context.add_diagnostic(diagnostic(DIAG_DEP_VIOLATION, str(exc), stage_id=stage_id))
                break
            except DuplicateDecisionError as exc:
                errors.append(str(exc))
                context.add_diagnostic(diagnostic(DIAG_OUT_DUPLICATE, str(exc), stage_id=stage_id))
                break

    def _finalize(
        self,
        context: LuckDecisionContext,
        errors: list[str],
        started: str,
    ) -> LuckDecisionResult:
        completed = _iso(self.clock())
        trace = build_decision_trace(
            timeline_snapshot=context.timeline_snapshot,
            luck_analysis_snapshot=context.luck_analysis_snapshot,
            analysis_snapshot=context.analysis_snapshot,
            decision_snapshot=context.decision_snapshot,
            executed_stages=context.executed_stages,
            outputs_published=(),
            started_at=started,
            completed_at=completed,
        )
        audit_ok = not errors
        audit = LuckDecisionAudit(
            contract_validation="pass" if audit_ok else "pending",
            dependency_validation="pass" if audit_ok else "fail",
            priority_legality="pass" if context.has_published(OUTPUT_PRIORITY) else "not_run",
            confidence_validation="pass" if context.has_published(OUTPUT_CONFIDENCE) else "not_run",
            deterministic_execution=True,
            version_compatibility="pending",
            reason_codes=tuple(
                item.get("code")
                for item in (context.get_published(OUTPUT_REASONING) or [])
                if isinstance(item, dict) and item.get("code")
            ),
        )
        published = context.published_copy()
        payload = {name: published.get(name) for name in PUBLISHED_OUTPUTS}
        payload[OUTPUT_TRACE] = trace.to_dict()
        payload[OUTPUT_AUDIT] = audit.to_dict()
        payload[OUTPUT_VERSION] = published.get(OUTPUT_VERSION) or DECISION_VERSION
        try:
            validate_result_payload(
                payload,
                executed=context.executed_stages,
                expected_order=self.registry.canonical_order(),
                published_names=tuple(name for name in context.published_names() if name in PUBLISHED_OUTPUTS),
                timeline_version=str(context.timeline_snapshot.get("timeline_version") or ""),
                luck_analysis_version=str(context.luck_analysis_snapshot.get("analysis_version") or ""),
                analysis_pipeline_version=str(context.analysis_snapshot.get("pipeline_version") or ""),
                decision_pipeline_version=str(
                    context.decision_snapshot.get("decision_pipeline_version") or ""
                ),
            )
            audit.contract_validation = "pass"
            audit.version_compatibility = "pass"
        except LuckDecisionValidationError as exc:
            errors.append(str(exc))
            context.add_diagnostic(diagnostic(DIAG_CONTRACT_VIOLATION, str(exc)))
            audit.contract_validation = "fail"
            audit.version_compatibility = "fail"

        success = not errors
        context.add_diagnostic(
            diagnostic(
                DIAG_PIPE_OK if success else DIAG_PIPE_FAIL,
                "Luck Decision completed" if success else "Luck Decision failed",
                severity="info" if success else "error",
            )
        )
        trace.outputs_published = tuple(name for name in PUBLISHED_OUTPUTS if payload.get(name) is not None or name in published or name in {OUTPUT_TRACE, OUTPUT_AUDIT, OUTPUT_VERSION})
        audit.details = {"error_count": len(errors)}
        return LuckDecisionResult(
            success=success,
            decision_version=DECISION_VERSION,
            opportunity_score=published.get(OUTPUT_OPPORTUNITY),
            risk_score=published.get(OUTPUT_RISK),
            luck_priority=published.get(OUTPUT_PRIORITY),
            decision_confidence=published.get(OUTPUT_CONFIDENCE),
            decision_reasoning=published.get(OUTPUT_REASONING),
            decision_trace=trace,
            decision_audit=audit,
            overall_luck_decision=published.get(OUTPUT_OVERALL),
            diagnostics=tuple(context.diagnostics),
            errors=tuple(errors),
        )

    def _empty_result(
        self,
        diagnostics: list[LuckDecisionDiagnostic],
        errors: list[str],
        started: str,
        completed: str,
    ) -> LuckDecisionResult:
        trace = LuckDecisionTrace(started_at=started, completed_at=completed)
        audit = LuckDecisionAudit(
            contract_validation="fail",
            dependency_validation="not_run",
            priority_legality="not_run",
            confidence_validation="not_run",
            deterministic_execution=True,
            version_compatibility="not_run",
            reason_codes=(),
        )
        return LuckDecisionResult(
            success=False,
            decision_version=DECISION_VERSION,
            decision_trace=trace,
            decision_audit=audit,
            diagnostics=tuple(diagnostics),
            errors=tuple(errors),
        )
