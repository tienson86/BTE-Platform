"""Knowledge SDK access surface used by ShenSha Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from engines.analysis_engine.shensha_engine.exceptions import ShenShaKnowledgeError

MODULE_ID = "shensha_knowledge"

ASSET_CALCULATION_REFERENCES = "shensha.calculation_references"
ASSET_LOOKUP_TABLES = "shensha.lookup_tables"
ASSET_MAPPING_TABLES = "shensha.mapping_tables"
ASSET_IDENTITIES = "shensha.identities"
ASSET_INTERACTIONS = "shensha.interactions"
ASSET_COMPATIBILITY = "shensha.compatibility"
ASSET_EXCEPTIONS = "shensha.exceptions"
ASSET_UPSTREAM_QUALIFIERS = "shensha.upstream_qualifiers"
ASSET_PRIORITY = "shensha.priority"
ASSET_CONFIDENCE = "shensha.confidence"

REQUIRED_ASSETS: tuple[str, ...] = (
    ASSET_CALCULATION_REFERENCES,
    ASSET_LOOKUP_TABLES,
    ASSET_MAPPING_TABLES,
    ASSET_IDENTITIES,
    ASSET_INTERACTIONS,
    ASSET_COMPATIBILITY,
    ASSET_EXCEPTIONS,
    ASSET_UPSTREAM_QUALIFIERS,
    ASSET_PRIORITY,
    ASSET_CONFIDENCE,
)


@dataclass(slots=True, frozen=True)
class AssetView:
    """Resolved knowledge asset view."""

    asset_id: str
    version: str
    data: Mapping[str, Any]
    module_id: str = MODULE_ID


@dataclass(slots=True, frozen=True)
class ModuleView:
    """Resolved knowledge module view."""

    module_id: str
    version: str
    assets: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class KnowledgeSession(Protocol):
    """Minimal Knowledge SDK session contract consumed by this engine."""

    def get_module(self, module_id: str) -> ModuleView:
        """Return a frozen ModuleView."""

    def get_asset(self, asset_id: str) -> AssetView:
        """Return a frozen AssetView."""


class InMemoryKnowledgeSession:
    """Deterministic in-memory KnowledgeSession for runtime binding and tests."""

    def __init__(
        self,
        *,
        modules: Mapping[str, ModuleView],
        assets: Mapping[str, AssetView],
    ) -> None:
        self._modules = dict(modules)
        self._assets = dict(assets)

    def get_module(self, module_id: str) -> ModuleView:
        try:
            return self._modules[module_id]
        except KeyError as exc:
            raise ShenShaKnowledgeError(
                f"Knowledge module not found: {module_id}",
                details={"module_id": module_id},
            ) from exc

    def get_asset(self, asset_id: str) -> AssetView:
        try:
            return self._assets[asset_id]
        except KeyError as exc:
            raise ShenShaKnowledgeError(
                f"Knowledge asset not found: {asset_id}",
                details={"asset_id": asset_id},
            ) from exc

    def merge(self, other: "InMemoryKnowledgeSession") -> "InMemoryKnowledgeSession":
        """Return a new session containing modules/assets from both sessions."""
        return InMemoryKnowledgeSession(
            modules={**self._modules, **other._modules},
            assets={**self._assets, **other._assets},
        )


def require_knowledge_session(session: Any) -> KnowledgeSession:
    """Validate and return a KnowledgeSession from AnalysisContext."""
    if session is None:
        raise ShenShaKnowledgeError(
            "AnalysisContext.knowledge_session is required",
        )
    if not hasattr(session, "get_module") or not hasattr(session, "get_asset"):
        raise ShenShaKnowledgeError(
            "knowledge_session must provide get_module/get_asset",
            details={"session_type": type(session).__name__},
        )
    return session  # type: ignore[return-value]
