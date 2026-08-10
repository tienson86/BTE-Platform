"""Service registry and canonical pipeline port.

Services call this port only. The default gateway does not import engines,
knowledge packages, or modify pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from applications.services.analysis_service import AnalysisService
from applications.services.health_service import HealthService
from applications.services.knowledge_service import KnowledgeService
from applications.services.report_service import ReportService
from applications.versioning.version_manager import VersionManager, default_version_manager


class CanonicalPipelinePort(Protocol):
    """Boundary to canonical pipelines. Implementations must not leak engine types."""

    def submit_analysis(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        """Submit a validated analysis payload to the canonical analysis pipeline."""

    def get_analysis(self, analysis_id: str) -> Mapping[str, Any] | None:
        """Fetch an analysis record from the canonical pipeline/store."""

    def get_report(self, report_id: str) -> Mapping[str, Any] | None:
        """Fetch a report record from the canonical report pipeline/store."""

    def get_knowledge(self, knowledge_id: str) -> Mapping[str, Any] | None:
        """Fetch a published knowledge record from the canonical knowledge pipeline."""

    def probe_health(self) -> Mapping[str, Any]:
        """Return pipeline binding/readiness without engine internals."""


class UnboundPipelineGateway:
    """Design-time pipeline gateway.

    Acknowledges validated requests. Does not execute engines, persist data,
    or import knowledge packages. Runtime hosts replace this binding.
    """

    def submit_analysis(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        """Acknowledge a validated analysis request without executing pipelines."""
        return {
            "execution": "not_bound",
            "analysis_id": payload.get("analysis_id"),
            "pipeline": "canonical_analysis_pipeline",
        }

    def get_analysis(self, analysis_id: str) -> Mapping[str, Any] | None:
        """No persistence in the unbound gateway."""
        return None

    def get_report(self, report_id: str) -> Mapping[str, Any] | None:
        """No persistence in the unbound gateway."""
        return None

    def get_knowledge(self, knowledge_id: str) -> Mapping[str, Any] | None:
        """No persistence in the unbound gateway."""
        return None

    def probe_health(self) -> Mapping[str, Any]:
        """Report that the process is up and the pipeline is not bound."""
        return {"ready": True, "bound": False}


@dataclass(slots=True)
class ServiceRegistry:
    """Composition root for public services."""

    analysis: AnalysisService
    report: ReportService
    knowledge: KnowledgeService
    health: HealthService
    pipeline: CanonicalPipelinePort

    @classmethod
    def create_default(
        cls,
        pipeline: CanonicalPipelinePort | None = None,
        version_manager: VersionManager | None = None,
    ) -> ServiceRegistry:
        """Create the default public service graph."""
        gateway = pipeline or UnboundPipelineGateway()
        versions = version_manager or default_version_manager
        return cls(
            analysis=AnalysisService(gateway),
            report=ReportService(gateway),
            knowledge=KnowledgeService(gateway),
            health=HealthService(gateway, version_manager=versions),
            pipeline=gateway,
        )

    def service_names(self) -> tuple[str, ...]:
        """Return registered public service names."""
        return (
            self.analysis.name,
            self.report.name,
            self.knowledge.name,
            self.health.name,
        )


_default_registry: ServiceRegistry | None = None


def get_service_registry() -> ServiceRegistry:
    """Return the process-local default registry.

    Runtime hosts should prefer ``app.state.service_registry`` injection.
    """
    global _default_registry
    if _default_registry is None:
        _default_registry = ServiceRegistry.create_default()
    return _default_registry
