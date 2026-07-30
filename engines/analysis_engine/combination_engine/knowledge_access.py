"""Knowledge SDK access surface used by Combination Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from engines.analysis_engine.combination_engine.exceptions import (
    CombinationKnowledgeError,
)

MODULE_ID = "combination_knowledge"

ASSET_STEM_COMBINATIONS = "combination.stem_combinations"
ASSET_BRANCH_COMBINATIONS = "combination.branch_combinations"
ASSET_CLASH = "combination.clash"
ASSET_HARM = "combination.harm"
ASSET_PUNISHMENT = "combination.punishment"
ASSET_DESTRUCTION = "combination.destruction"
ASSET_HIDDEN_COMBINATION = "combination.hidden_combination"
ASSET_TRANSFORMATION = "combination.transformation"
ASSET_UPSTREAM_QUALIFIERS = "combination.upstream_qualifiers"
ASSET_PRIORITY = "combination.priority"
ASSET_CONFIDENCE = "combination.confidence"

REQUIRED_ASSETS: tuple[str, ...] = (
    ASSET_STEM_COMBINATIONS,
    ASSET_BRANCH_COMBINATIONS,
    ASSET_CLASH,
    ASSET_HARM,
    ASSET_PUNISHMENT,
    ASSET_DESTRUCTION,
    ASSET_HIDDEN_COMBINATION,
    ASSET_TRANSFORMATION,
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
            raise CombinationKnowledgeError(
                f"Knowledge module not found: {module_id}",
                details={"module_id": module_id},
            ) from exc

    def get_asset(self, asset_id: str) -> AssetView:
        try:
            return self._assets[asset_id]
        except KeyError as exc:
            raise CombinationKnowledgeError(
                f"Knowledge asset not found: {asset_id}",
                details={"asset_id": asset_id},
            ) from exc

    def merge(self, other: "InMemoryKnowledgeSession") -> "InMemoryKnowledgeSession":
        """Return a new session containing modules/assets from both sessions."""
        modules = {**self._modules, **other._modules}
        assets = {**self._assets, **other._assets}
        return InMemoryKnowledgeSession(modules=modules, assets=assets)


def require_knowledge_session(session: Any) -> KnowledgeSession:
    """Validate and return a KnowledgeSession from AnalysisContext."""
    if session is None:
        raise CombinationKnowledgeError(
            "AnalysisContext.knowledge_session is required",
        )
    if not hasattr(session, "get_module") or not hasattr(session, "get_asset"):
        raise CombinationKnowledgeError(
            "knowledge_session must provide get_module/get_asset",
            details={"session_type": type(session).__name__},
        )
    return session  # type: ignore[return-value]
