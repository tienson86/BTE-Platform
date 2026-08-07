"""Evidence stage — collect evidence refs from AnalysisResult."""

from __future__ import annotations

from .narrative_context import NarrativeContext


class EvidenceCollector:
    """Stage — Evidence extraction (read-only from AnalysisResult)."""

    def collect(self, context: NarrativeContext) -> list[str]:
        """Return ordered evidence ids attached to the analysis aggregate."""
        evidence = context.analysis.evidence
        ids: list[str] = []
        for item in evidence.items:
            evidence_id = str(getattr(item, "evidence_id", "") or "")
            if evidence_id:
                ids.append(evidence_id)
        context.evidence_ids = ids
        return ids
