"""Public service API for the BTE priority engine."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from .matched_rule_resolver import MatchedRuleResolution, MatchedRuleResolver
from .models import PriorityData, PriorityPipelineResult
from .pipeline import PriorityPipeline
from .rule_loader import PriorityRuleLoader


class PriorityService:
    """Facade used by other BTE engines and API layers."""

    def __init__(
        self,
        data: PriorityData | None = None,
        *,
        matched_rule_resolver: MatchedRuleResolver | None = None,
    ) -> None:
        self.data = data
        self.pipeline = PriorityPipeline(data) if data is not None else None
        self.matched_rule_resolver = matched_rule_resolver or MatchedRuleResolver()

    @classmethod
    def for_matched_rules(
        cls,
        *,
        max_rules_per_section: int = 20,
    ) -> "PriorityService":
        """Create a service for WP5 matched-knowledge-rule resolution (no KB load)."""
        return cls(
            data=None,
            matched_rule_resolver=MatchedRuleResolver(
                max_rules_per_section=max_rules_per_section,
            ),
        )

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

        if self.pipeline is None:
            raise RuntimeError(
                "PriorityService has no PriorityData; use from_project_root "
                "or from_priority_dir for PR* pipeline resolution."
            )

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

        if self.pipeline is None:
            raise RuntimeError(
                "PriorityService has no PriorityData; use from_project_root "
                "or from_priority_dir for PR* pipeline resolution."
            )

        return self.pipeline.run_matched_rules(
            rule_ids,
            completed_dependencies=completed_dependencies,
        )

    def resolve_matched_interpretation_rules(
        self,
        matched_rules: Sequence[Mapping[str, Any]],
    ) -> MatchedRuleResolution:
        """
        WP5: resolve conflicts among matched knowledge rules.

        Detects duplicate content, contradictions, and subsumption; keeps
        higher priority; preserves section diversity.
        """
        return self.matched_rule_resolver.resolve(matched_rules)

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
