"""Knowledge SDK access surface used by Ten Gods Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from engines.analysis_engine.ten_gods_engine.exceptions import TenGodsKnowledgeError

MODULE_ID = "ten_gods_knowledge"

ASSET_IDENTITIES = "ten_gods.identities"
ASSET_STEM_RELATIONS = "ten_gods.stem_relations"
ASSET_RELATIONSHIPS = "ten_gods.relationships"
ASSET_STRENGTH_INTERACTIONS = "ten_gods.strength_interactions"
ASSET_TEMPERATURE_INTERACTIONS = "ten_gods.temperature_interactions"
ASSET_PATTERN_INTERACTIONS = "ten_gods.pattern_interactions"
ASSET_USEFUL_GOD_INTERACTIONS = "ten_gods.useful_god_interactions"
ASSET_FAVORABILITY = "ten_gods.favorability"
ASSET_LIFE_AREAS = "ten_gods.life_areas"
ASSET_PRIORITY = "ten_gods.priority"
ASSET_CONFIDENCE = "ten_gods.confidence"

REQUIRED_ASSETS: tuple[str, ...] = (
    ASSET_IDENTITIES,
    ASSET_STEM_RELATIONS,
    ASSET_RELATIONSHIPS,
    ASSET_STRENGTH_INTERACTIONS,
    ASSET_TEMPERATURE_INTERACTIONS,
    ASSET_PATTERN_INTERACTIONS,
    ASSET_USEFUL_GOD_INTERACTIONS,
    ASSET_FAVORABILITY,
    ASSET_LIFE_AREAS,
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
            raise TenGodsKnowledgeError(
                f"Knowledge module not found: {module_id}",
                details={"module_id": module_id},
            ) from exc

    def get_asset(self, asset_id: str) -> AssetView:
        try:
            return self._assets[asset_id]
        except KeyError as exc:
            raise TenGodsKnowledgeError(
                f"Knowledge asset not found: {asset_id}",
                details={"asset_id": asset_id},
            ) from exc


def require_knowledge_session(session: Any) -> KnowledgeSession:
    """Validate and return a KnowledgeSession from AnalysisContext."""
    if session is None:
        raise TenGodsKnowledgeError(
            "AnalysisContext.knowledge_session is required",
        )
    if not hasattr(session, "get_module") or not hasattr(session, "get_asset"):
        raise TenGodsKnowledgeError(
            "knowledge_session must provide get_module/get_asset",
            details={"session_type": type(session).__name__},
        )
    return session  # type: ignore[return-value]
