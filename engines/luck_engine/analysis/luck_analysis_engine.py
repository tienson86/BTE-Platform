"""Luck Analysis Engine (LE-2). Analytical impacts only. Never raises to API."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from engines.luck_engine.analysis.analysis_context import (
    AnalysisDiagnostic,
    LuckAnalysisContext,
    diagnostic,
)
from engines.luck_engine.analysis.analysis_result import (
    LuckAnalysisResult,
    LuckAnalysisTrace,
    build_analysis_trace,
)
from engines.luck_engine.analysis.impact_registry import ImpactRegistry
from engines.luck_engine.analysis.package_loader import LuckAnalysisPackageLoader
from engines.luck_engine.analysis.validation import validate_result_payload
from engines.luck_engine.analysis_constants import (
    ANALYSIS_VERSION,
    CANONICAL_IMPACT_ORDER,
    CONFIDENCE_NONE,
    DIAG_ANALYSIS_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_DECISION_MISSING,
    DIAG_DEP_VIOLATION,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_TIMELINE_MISSING,
    DIRECTION_UNRESOLVED,
    PUBLISHED_OUTPUTS,
    STAGE_PATTERN,
    STAGE_PATTERN_EVALUATION,
    STAGE_SEASONAL,
    STAGE_STRENGTH,
    STAGE_TEMPERATURE,
    STAGE_USEFUL_GOD,
)
from engines.luck_engine.exceptions import (
    DuplicateImpactError,
    ImpactDependencyError,
    LuckAnalysisError,
    LuckAnalysisValidationError,
    LuckPackageLoadError,
)
from engines.luck_engine.integration.pattern_evaluation_impact_stage import (
    PatternEvaluationImpactStage,
)
from engines.luck_engine.integration.pattern_impact_stage import PatternImpactStage
from engines.luck_engine.integration.seasonal_impact_stage import SeasonalImpactStage
from engines.luck_engine.integration.strength_impact_stage import StrengthImpactStage
from engines.luck_engine.integration.temperature_impact_stage import TemperatureImpactStage
from engines.luck_engine.integration.useful_god_impact_stage import UsefulGodImpactStage

logger = logging.getLogger(__name__)


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


def _majority_direction(values: list[str]) -> str:
    counted = [item for item in values if item != DIRECTION_UNRESOLVED]
    if not counted:
        return DIRECTION_UNRESOLVED
    return max(sorted(set(counted)), key=counted.count)


def _min_confidence(values: list[str]) -> str:
    rank = {"none": 0, "low": 1, "medium": 2, "high": 3}
    if not values:
        return CONFIDENCE_NONE
    return min(values, key=lambda item: rank.get(item, 0))


def build_overall_impact(stage_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate stage impacts without introducing fortune meaning."""
    scores = [float(item["score"]["value"]) for item in stage_payloads]
    deltas = [float(item["delta"]["value"]) for item in stage_payloads]
    directions = [str(item["direction"]["value"]) for item in stage_payloads]
    confidences = [str(item["confidence"]["value"]) for item in stage_payloads]
    count = len(stage_payloads) or 1
    return {
        "direction": {"value": _majority_direction(directions)},
        "score": {
            "value": round(sum(scores) / count, 4) if stage_payloads else 0.0,
            "unit": "overlap_intensity",
        },
        "delta": {"value": round(sum(deltas) / count, 4) if stage_payloads else 0.0},
        "confidence": {"value": _min_confidence(confidences)},
        "stage_count": len(stage_payloads),
        "analysis_version": ANALYSIS_VERSION,
    }


class LuckAnalysisEngine:
    """Only supported LE-2 execution model for analytical luck impacts."""

    analysis_version: str = ANALYSIS_VERSION

    def __init__(
        self,
        *,
        registry: ImpactRegistry | None = None,
        loader: LuckAnalysisPackageLoader | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize registry, optional package loader, and clock."""
        self.registry = registry or ImpactRegistry()
        self.loader = loader or LuckAnalysisPackageLoader()
        self.clock = clock or _utc_now
        self._stages = {
            STAGE_SEASONAL: SeasonalImpactStage(),
            STAGE_STRENGTH: StrengthImpactStage(),
            STAGE_TEMPERATURE: TemperatureImpactStage(),
            STAGE_PATTERN: PatternImpactStage(),
            STAGE_PATTERN_EVALUATION: PatternEvaluationImpactStage(),
            STAGE_USEFUL_GOD: UsefulGodImpactStage(),
        }

    def run(
        self,
        *,
        timeline: Any,
        analysis_result: Any,
        decision_result: Any,
    ) -> LuckAnalysisResult:
        """Analyze timeline × analysis × decision. Diagnostics only at the boundary."""
        started = _iso(self.clock())
        diagnostics: list[AnalysisDiagnostic] = []
        errors: list[str] = []
        try:
            return self._run_inner(
                timeline=timeline,
                analysis_result=analysis_result,
                decision_result=decision_result,
                started=started,
                diagnostics=diagnostics,
                errors=errors,
            )
        except LuckAnalysisError as exc:
            logger.warning("luck_analysis_failed %s", exc)
            errors.append(str(exc))
            diagnostics.append(
                diagnostic(DIAG_PIPE_FAIL, "Luck Analysis failed", details={"error": str(exc)})
            )
            return self._empty_result(diagnostics, errors, started, _iso(self.clock()))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("luck_analysis_unexpected")
            errors.append(str(exc))
            diagnostics.append(
                diagnostic(DIAG_PIPE_FAIL, "Luck Analysis failed", details={"error": str(exc)})
            )
            return self._empty_result(diagnostics, errors, started, _iso(self.clock()))

    def _run_inner(
        self,
        *,
        timeline: Any,
        analysis_result: Any,
        decision_result: Any,
        started: str,
        diagnostics: list[AnalysisDiagnostic],
        errors: list[str],
    ) -> LuckAnalysisResult:
        timeline_snap = self._require_snapshot(
            timeline, label="timeline", code=DIAG_TIMELINE_MISSING, diagnostics=diagnostics, errors=errors
        )
        analysis_snap = self._require_snapshot(
            analysis_result,
            label="analysis",
            code=DIAG_ANALYSIS_MISSING,
            diagnostics=diagnostics,
            errors=errors,
        )
        decision_snap = self._require_snapshot(
            decision_result,
            label="decision",
            code=DIAG_DECISION_MISSING,
            diagnostics=diagnostics,
            errors=errors,
        )
        if timeline_snap is None or analysis_snap is None or decision_snap is None:
            diagnostics.append(diagnostic(DIAG_PIPE_FAIL, "Required Luck Analysis inputs missing"))
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

        context = LuckAnalysisContext(
            timeline_snapshot=timeline_snap,
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
        diagnostics: list[AnalysisDiagnostic],
        errors: list[str],
    ) -> dict[str, Any] | None:
        if value is None:
            diagnostics.append(diagnostic(code, f"Missing {label} input"))
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

    def _execute_stages(self, context: LuckAnalysisContext, errors: list[str]) -> None:
        for stage_id in self.registry.canonical_order():
            stage = self._stages[stage_id]
            try:
                impact = stage.execute(context)
                payload = impact.to_dict()
                context.publish(stage_id, payload)
                context.record_stage(stage_id)
            except ImpactDependencyError as exc:
                errors.append(str(exc))
                context.add_diagnostic(
                    diagnostic(DIAG_DEP_VIOLATION, str(exc), stage_id=stage_id)
                )
                break
            except DuplicateImpactError as exc:
                errors.append(str(exc))
                context.emit_duplicate(stage_id, stage_id)
                break

    def _finalize(
        self,
        context: LuckAnalysisContext,
        errors: list[str],
        started: str,
    ) -> LuckAnalysisResult:
        completed = _iso(self.clock())
        stage_payloads = [
            context.get_published(stage_id)
            for stage_id in CANONICAL_IMPACT_ORDER
            if isinstance(context.get_published(stage_id), dict)
        ]
        if stage_payloads and not context.has_published("overall_analysis_impact"):
            context.publish("overall_analysis_impact", build_overall_impact(stage_payloads))
        if not context.has_published("analysis_version"):
            context.publish("analysis_version", ANALYSIS_VERSION)
        pending_names = tuple(
            name
            for name in (*context.published_names(), "analysis_trace", "analysis_diagnostics")
            if name in (*PUBLISHED_OUTPUTS, "analysis_trace", "analysis_diagnostics")
        )
        trace = build_analysis_trace(
            timeline_snapshot=context.timeline_snapshot,
            analysis_snapshot=context.analysis_snapshot,
            decision_snapshot=context.decision_snapshot,
            executed_stages=context.executed_stages,
            outputs_published=tuple(name for name in PUBLISHED_OUTPUTS if name in pending_names or name in context.published_names()),
            started_at=started,
            completed_at=completed,
        )
        if not context.has_published("analysis_trace"):
            context.publish("analysis_trace", trace.to_dict())
        if not context.has_published("analysis_diagnostics"):
            context.publish("analysis_diagnostics", [item.to_dict() for item in context.diagnostics])

        published = context.published_copy()
        trace.outputs_published = tuple(name for name in PUBLISHED_OUTPUTS if name in published)
        published["analysis_trace"] = trace.to_dict()
        payload = {
            **{name: published.get(name) for name in PUBLISHED_OUTPUTS},
            "success": not errors,
            "errors": list(errors),
        }
        try:
            validate_result_payload(
                payload,
                executed=context.executed_stages,
                expected_order=self.registry.canonical_order(),
                published_names=context.published_names(),
                timeline_version=str(context.timeline_snapshot.get("timeline_version") or ""),
                analysis_pipeline_version=str(context.analysis_snapshot.get("pipeline_version") or ""),
                decision_pipeline_version=str(
                    context.decision_snapshot.get("decision_pipeline_version") or ""
                ),
            )
        except LuckAnalysisValidationError as exc:
            errors.append(str(exc))
            context.add_diagnostic(
                diagnostic(DIAG_CONTRACT_VIOLATION, str(exc))
            )

        success = not errors
        context.add_diagnostic(
            diagnostic(
                DIAG_PIPE_OK if success else DIAG_PIPE_FAIL,
                "Luck Analysis completed" if success else "Luck Analysis failed",
                severity="info" if success else "error",
            )
        )
        published["analysis_diagnostics"] = [item.to_dict() for item in context.diagnostics]
        published["analysis_trace"] = trace.to_dict()
        return LuckAnalysisResult(
            success=success,
            analysis_version=ANALYSIS_VERSION,
            seasonal_impact=published.get(STAGE_SEASONAL),
            strength_impact=published.get(STAGE_STRENGTH),
            temperature_impact=published.get(STAGE_TEMPERATURE),
            pattern_impact=published.get(STAGE_PATTERN),
            pattern_evaluation_impact=published.get(STAGE_PATTERN_EVALUATION),
            useful_god_impact=published.get(STAGE_USEFUL_GOD),
            overall_analysis_impact=published.get("overall_analysis_impact"),
            analysis_trace=trace,
            analysis_diagnostics=tuple(context.diagnostics),
            errors=tuple(errors),
        )

    def _empty_result(
        self,
        diagnostics: list[AnalysisDiagnostic],
        errors: list[str],
        started: str,
        completed: str,
    ) -> LuckAnalysisResult:
        trace = LuckAnalysisTrace(started_at=started, completed_at=completed)
        return LuckAnalysisResult(
            success=False,
            analysis_version=ANALYSIS_VERSION,
            analysis_trace=trace,
            analysis_diagnostics=tuple(diagnostics),
            errors=tuple(errors),
        )
