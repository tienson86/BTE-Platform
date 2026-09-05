"""Pack 07 context builders.

Builders assemble frozen containers. They do not interpret or score.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.detailed_interpretation_engine.context import InterpretationContext
from engines.detailed_interpretation_engine.context_layers import (
    CanonicalAnalysisContext,
    DomainContext,
    EvidenceContext,
    NarrativeContext,
    OptimizationContext,
    TemporalContext,
)
from engines.detailed_interpretation_engine.factories import (
    build_canonical_analysis_context,
    build_domain_context,
    build_evidence_context,
    build_interpretation_context,
    build_narrative_context,
    build_optimization_context,
    build_temporal_context,
)
from engines.detailed_interpretation_engine.upstream import (
    UpstreamStructuralRefs,
    extract_upstream_refs,
)


class InterpretationContextBuilder:
    """Collect immutable upstream references. No interpretation."""

    def build(self, refs: UpstreamStructuralRefs) -> InterpretationContext:
        """Build InterpretationContext from upstream IDs."""
        return build_interpretation_context(
            refs.analysis_id,
            chart_id=refs.chart_id,
            mingju_result_id=refs.mingju_result_id,
            mingju_content_hash=refs.mingju_content_hash,
            locale=refs.locale,
            mc01=refs.mc01,
            pattern_ref=refs.pattern_ref,
            grade_ref=refs.grade_ref,
            integrity_ref=refs.integrity_ref,
            strength_ref=refs.strength_ref,
            useful_god_ref=refs.useful_god_ref,
            temperature_ref=refs.temperature_ref,
            five_elements_ref=refs.five_elements_ref,
            chart_identity=refs.chart_identity,
        )

    def build_from_payload(self, payload: Mapping[str, Any]) -> InterpretationContext:
        """Build InterpretationContext from an analyze payload mapping."""
        return self.build(extract_upstream_refs(payload))


class EvidenceContextBuilder:
    """Prepare evidence containers. No Evidence Priority calculation."""

    def build(self, analysis_id: str) -> EvidenceContext:
        """Return empty evidence context."""
        return build_evidence_context(analysis_id)


class DomainContextBuilder:
    """Prepare Authority / Career / Wealth / Relationship / Legacy / Vitality."""

    def build(self, analysis_id: str) -> DomainContext:
        """Return empty domain context."""
        return build_domain_context(analysis_id)


class TemporalContextBuilder:
    """Prepare luck / interaction / temporal containers. No activation."""

    def build(self, analysis_id: str) -> TemporalContext:
        """Return empty temporal context."""
        return build_temporal_context(analysis_id)


class OptimizationContextBuilder:
    """Prepare optimization inputs. No optimization decisions."""

    def build(self, analysis_id: str) -> OptimizationContext:
        """Return empty optimization context."""
        return build_optimization_context(analysis_id)


class NarrativeContextBuilder:
    """Prepare narrative inputs. No composer."""

    def build(self, analysis_id: str) -> NarrativeContext:
        """Return empty narrative context."""
        return build_narrative_context(analysis_id)


class CanonicalAnalysisContextBuilder:
    """Assemble the canonical context chain after MC-01 / structural truth."""

    def build(self, refs: UpstreamStructuralRefs) -> CanonicalAnalysisContext:
        """Build CanonicalAnalysisContext from upstream refs."""
        return build_canonical_analysis_context(refs=refs)

    def build_from_payload(self, payload: Mapping[str, Any]) -> CanonicalAnalysisContext:
        """Build CanonicalAnalysisContext from an analyze payload mapping."""
        return build_canonical_analysis_context(payload=payload)


def build_canonical_analysis_context_from_payload(
    payload: Mapping[str, Any],
) -> CanonicalAnalysisContext:
    """Factory helper used by runtime wiring."""
    return CanonicalAnalysisContextBuilder().build_from_payload(payload)
