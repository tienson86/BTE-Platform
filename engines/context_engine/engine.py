"""Context Engine V2 — Unified Analysis Context."""

from __future__ import annotations

import time
from dataclasses import asdict
from typing import Any

from engines.pattern_engine.rule_context_bridge import enrich_rule_context_summaries

from .adapters import to_rule_context
from .builder import UnifiedContextBuilder
from .models import ContextTraceEntry, UnifiedAnalysisContext
from .serializers import serialize_context, write_analysis_context_json
from .validators import ContextValidator


class ContextEngine:
    """
    Unified Analysis Context V2.

    Single aggregator between analysis engines and downstream consumers
    (RuleContext, Interpretation, Report).
    """

    def __init__(self) -> None:
        self._builder = UnifiedContextBuilder()
        self._validator = ContextValidator()

    def build(
        self,
        *,
        calendar: Any = None,
        bazi: Any = None,
        strength: Any = None,
        temperature: Any = None,
        pattern: Any = None,
        useful_god: Any = None,
        engine_traces: list[ContextTraceEntry] | None = None,
        extra_metadata: dict[str, Any] | None = None,
        validate: bool = True,
    ) -> UnifiedAnalysisContext:
        """Build and optionally validate UnifiedAnalysisContext."""
        unified = self._builder.build(
            calendar=calendar,
            bazi=bazi,
            strength=strength,
            temperature=temperature,
            pattern=pattern,
            useful_god=useful_god,
            trace=list(engine_traces or []),
            extra_metadata=extra_metadata,
        )
        if validate:
            self._validator.validate(unified)
        return unified

    def to_rule_context(
        self,
        unified: UnifiedAnalysisContext,
        *,
        calendar: Any = None,
        bazi: Any = None,
        pattern: Any = None,
        score: Any = None,
        luck: Any = None,
        shensha: Any = None,
        enrich: bool = True,
    ) -> dict[str, Any]:
        """Convert unified context to RuleContext and optionally enrich summaries."""
        started = time.perf_counter()
        rule_context = to_rule_context(
            unified,
            calendar=calendar,
            bazi=bazi,
            pattern=pattern,
            score=score,
            luck=luck,
            shensha=shensha,
        )
        if enrich:
            rule_context = enrich_rule_context_summaries(rule_context, pattern=pattern)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        unified.metadata.trace.append(
            ContextTraceEntry(
                engine="context_engine.adapter",
                input_keys=["unified_context"],
                output_keys=sorted(str(k) for k in rule_context.keys()),
                duration_ms=round(elapsed_ms, 3),
                success=True,
            )
        )
        rule_context["metadata"] = {
            **dict(rule_context.get("metadata") or {}),
            "trace": [asdict(entry) for entry in unified.metadata.trace],
        }
        return rule_context

    def build_and_publish(
        self,
        *,
        calendar: Any = None,
        bazi: Any = None,
        strength: Any = None,
        temperature: Any = None,
        pattern: Any = None,
        useful_god: Any = None,
        score: Any = None,
        luck: Any = None,
        shensha: Any = None,
        engine_traces: list[ContextTraceEntry] | None = None,
    ) -> tuple[UnifiedAnalysisContext, dict[str, Any]]:
        """Build unified context and publish RuleContext in one call."""
        unified = self.build(
            calendar=calendar,
            bazi=bazi,
            strength=strength,
            temperature=temperature,
            pattern=pattern,
            useful_god=useful_god,
            engine_traces=engine_traces,
        )
        rule_context = self.to_rule_context(
            unified,
            calendar=calendar,
            bazi=bazi,
            pattern=pattern,
            score=score,
            luck=luck,
            shensha=shensha,
        )
        return unified, rule_context

    def serialize(self, unified: UnifiedAnalysisContext) -> dict[str, Any]:
        """Serialize unified context for API / storage."""
        return serialize_context(unified)

    def write_json(self, unified: UnifiedAnalysisContext, path: str) -> None:
        """Write analysis_context.json."""
        write_analysis_context_json(unified, path)

    def validate(self, unified: UnifiedAnalysisContext) -> dict[str, Any]:
        """Validate unified context."""
        return self._validator.validate(unified)
