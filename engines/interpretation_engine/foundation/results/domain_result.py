"""Domain interpretation result contract stub for Sprint B."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class FoundationDomainInterpretationResult:
    """Structured domain result shell — no long prose in Sprint A."""

    domain: str
    status: DataAvailability
    observations: tuple[str, ...] = ()
    reasoning: tuple[str, ...] = ()
    conclusions: tuple[str, ...] = ()
    impacts: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    confidence: float = 0.0
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize domain result stub."""
        return {
            "domain": self.domain,
            "status": self.status.value,
            "observations": list(self.observations),
            "reasoning": list(self.reasoning),
            "conclusions": list(self.conclusions),
            "impacts": list(self.impacts),
            "recommendations": list(self.recommendations),
            "warnings": list(self.warnings),
            "evidence": list(self.evidence),
            "confidence": self.confidence,
            "diagnostics": list(self.diagnostics),
        }


def stub_domain_result(domain: str, *, status: DataAvailability) -> FoundationDomainInterpretationResult:
    """Create minimal deterministic domain result for pipeline integration."""
    return FoundationDomainInterpretationResult(
        domain=domain,
        status=status,
        diagnostics=(f"{domain}_interpretation_not_implemented",),
    )
