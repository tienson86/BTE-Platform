"""Narrative Composer V2 — compose validated reasoning into customer sections."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.foundation.narrative.application import (
    compose_applications,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    NARRATIVE_SECTIONS,
)
from engines.interpretation_engine.foundation.narrative.dedup import merge_evidence_nodes
from engines.interpretation_engine.foundation.narrative.evidence import compose_evidence
from engines.interpretation_engine.foundation.narrative.input import NarrativeComposerInput
from engines.interpretation_engine.foundation.narrative.metrics import build_metrics
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    NarrativeComposerResult,
)
from engines.interpretation_engine.foundation.narrative.reason import compose_reasons
from engines.interpretation_engine.foundation.narrative.recommendation import (
    compose_recommendations,
    compose_warnings,
)
from engines.interpretation_engine.foundation.narrative.renderer import render_sections


class NarrativeComposerV2:
    """Canonical composition layer. Does not calculate, decide, or own knowledge."""

    def compose(self, source: NarrativeComposerInput) -> NarrativeComposerResult:
        """Run the frozen pipeline and return narrative sections.

        Evidence Composer → Reason Composer → Application Composer →
        Recommendation Composer → Narrative Renderer.
        """
        collected = compose_evidence(source)
        merged = merge_evidence_nodes(collected.nodes)
        evidence = EvidenceGraph(
            nodes=merged.nodes,
            raw_count=collected.raw_count,
            merged_count=merged.merged_count,
        )
        chains = compose_reasons(evidence)
        applications = compose_applications(evidence)
        recommendations = compose_recommendations(evidence)
        warnings = compose_warnings(evidence)
        sections, traces = render_sections(
            graph=evidence,
            chains=chains,
            applications=applications,
            recommendations=recommendations,
            warnings=warnings,
        )
        diagnostics = _section_diagnostics(sections)
        metrics = build_metrics(
            graph=evidence,
            chains=chains,
            recommendations=recommendations,
            warnings=warnings,
            sections=sections,
            traceability=traces,
        )
        return NarrativeComposerResult(
            sections=sections,
            evidence=evidence,
            reasoning_chains=chains,
            applications=applications,
            recommendations=recommendations,
            warnings=warnings,
            traceability=traces,
            metrics=metrics,
            diagnostics=diagnostics,
        )


def compose_narrative_v2(source: NarrativeComposerInput) -> NarrativeComposerResult:
    """Compose narrative sections from frozen bundle input."""
    return NarrativeComposerV2().compose(source)


def compose_narrative_v2_from_production(output: Any) -> NarrativeComposerResult:
    """Compose from production output without replacing Pack 05 rendering."""
    from engines.interpretation_engine.foundation.narrative.production import (
        build_composer_input_from_production,
    )

    return compose_narrative_v2(build_composer_input_from_production(output))


def _section_diagnostics(sections) -> tuple[str, ...]:
    """Report missing canonical sections. Do not invent filler text."""
    present = {section.name for section in sections if section.sentences}
    missing = [name for name in NARRATIVE_SECTIONS if name not in present]
    return tuple(f"missing_section:{name}" for name in missing)
