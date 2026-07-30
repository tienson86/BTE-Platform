"""Knowledge SDK access surface used by Luck Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from engines.analysis_engine.luck_engine.exceptions import LuckKnowledgeError

MODULE_ID = "luck_knowledge"

ASSET_DA_YUN = "luck.da_yun"
ASSET_LIU_NIAN = "luck.liu_nian"
ASSET_LIU_YUE = "luck.liu_yue"
ASSET_LIU_RI = "luck.liu_ri"
ASSET_LIU_SHI = "luck.liu_shi"
ASSET_INTERACTION = "luck.interaction"
ASSET_TIMING = "luck.timing"
ASSET_ACTIVATION = "luck.activation"
ASSET_FAVORABILITY = "luck.favorability"
ASSET_PRIORITY = "luck.priority"
ASSET_CONFIDENCE = "luck.confidence"

REQUIRED_ASSETS: tuple[str, ...] = (
    ASSET_DA_YUN,
    ASSET_LIU_NIAN,
    ASSET_LIU_YUE,
    ASSET_LIU_RI,
    ASSET_LIU_SHI,
    ASSET_INTERACTION,
    ASSET_TIMING,
    ASSET_ACTIVATION,
    ASSET_FAVORABILITY,
    ASSET_PRIORITY,
    ASSET_CONFIDENCE,
)

LAYER_ORDER: tuple[str, ...] = (
    "da_yun",
    "liu_nian",
    "liu_yue",
    "liu_ri",
    "liu_shi",
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
            raise LuckKnowledgeError(
                f"Knowledge module not found: {module_id}",
                details={"module_id": module_id},
            ) from exc

    def get_asset(self, asset_id: str) -> AssetView:
        try:
            return self._assets[asset_id]
        except KeyError as exc:
            raise LuckKnowledgeError(
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
        raise LuckKnowledgeError(
            "AnalysisContext.knowledge_session is required",
        )
    if not hasattr(session, "get_module") or not hasattr(session, "get_asset"):
        raise LuckKnowledgeError(
            "knowledge_session must provide get_module/get_asset",
            details={"session_type": type(session).__name__},
        )
    return session  # type: ignore[return-value]
