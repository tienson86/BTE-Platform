"""Public service API for the BTE priority engine."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from .models import PriorityData, PriorityPipelineResult
from .pipeline import PriorityPipeline
from .rule_loader import PriorityRuleLoader


class PriorityService:
    """Facade used by other BTE engines and API layers."""

    def __init__(self, data: PriorityData) -> None:
        self.data = data
        self.pipeline = PriorityPipeline(data)

    @classmethod
    def from_priority_dir(cls, priority_dir: str | Path) -> "PriorityService":
        """Create a service from a direct ``08_priority_rules`` path."""

        return cls(PriorityRuleLoader(priority_dir).load())

    @classmethod
    def from_project_root(cls, project_root: str | Path) -> "PriorityService":
        """Create a service by searching common Knowledge Base paths."""

        return cls(PriorityRuleLoader.from_project_root(project_root).load())

    def resolve(
        self,
        context: Mapping[str, Any],
        *,
        completed_dependencies: set[str] | None = None,
    ) -> PriorityPipelineResult:
        """Resolve priority rules from a runtime context dictionary."""

        return self.pipeline.run(
            context,
            completed_dependencies=completed_dependencies,
        )

    def resolve_to_dict(
        self,
        context: Mapping[str, Any],
        *,
        completed_dependencies: set[str] | None = None,
    ) -> dict[str, Any]:
        """Resolve priority rules and return an API-friendly dictionary."""

        return self.resolve(
            context,
            completed_dependencies=completed_dependencies,
        ).to_dict()

    def resolve_matched_rules(
        self,
        rule_ids: Iterable[str],
        *,
        completed_dependencies: set[str] | None = None,
    ) -> PriorityPipelineResult:
        """Resolve priority when an upstream Rule Matcher already has rule IDs."""

        return self.pipeline.run_matched_rules(
            rule_ids,
            completed_dependencies=completed_dependencies,
        )

    def resolve_matched_rules_to_dict(
        self,
        rule_ids: Iterable[str],
        *,
        completed_dependencies: set[str] | None = None,
    ) -> dict[str, Any]:
        """Resolve existing matches and return an API-friendly dictionary."""

        return self.resolve_matched_rules(
            rule_ids,
            completed_dependencies=completed_dependencies,
        ).to_dict()
