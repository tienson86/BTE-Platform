"""Dependency resolution for Narrative Runtime (Sprint D1)."""

from __future__ import annotations

import logging

from .models import (
    COMPONENT_DEPENDENCIES,
    OFFICIAL_COMPONENT_ORDER,
    ComponentType,
    NodeStatus,
)

logger = logging.getLogger(__name__)


class DependencyResolver:
    """
    Apply Sprint B conditional dependency rules to node statuses.

    Does not invent evidence. Does not generate prose.
    """

    def resolve(
        self,
        draft_status: dict[ComponentType, NodeStatus],
    ) -> dict[ComponentType, NodeStatus]:
        """
        Return updated statuses after dependency propagation.

        Rules:
        - Observation insufficient → Reasoning and Impact insufficient
        - Dependencies listed as BLOCKED only if upstream INVALID
        """
        status = {component: draft_status.get(component, NodeStatus.INSUFFICIENT_EVIDENCE)
                  for component in OFFICIAL_COMPONENT_ORDER}

        observation = status[ComponentType.OBSERVATION]
        if observation in {NodeStatus.INSUFFICIENT_EVIDENCE, NodeStatus.BLOCKED, NodeStatus.INVALID}:
            if status[ComponentType.REASONING] == NodeStatus.READY:
                status[ComponentType.REASONING] = NodeStatus.INSUFFICIENT_EVIDENCE
            if status[ComponentType.IMPACT] == NodeStatus.READY:
                # Prefer Reasoning path; Impact still blocked from READY if Observation empty.
                status[ComponentType.IMPACT] = NodeStatus.INSUFFICIENT_EVIDENCE
            logger.debug("dependency_resolver.observation_insufficient cascade")

        for component in OFFICIAL_COMPONENT_ORDER:
            deps = COMPONENT_DEPENDENCIES[component]
            for dep in deps:
                if status[dep] == NodeStatus.INVALID:
                    status[component] = NodeStatus.BLOCKED
                    break

        # Conclusion cannot be READY if every body node is insufficient/blocked.
        body = [
            ComponentType.OBSERVATION,
            ComponentType.REASONING,
            ComponentType.IMPACT,
            ComponentType.RECOMMENDATION,
            ComponentType.WARNING,
        ]
        if all(
            status[item] in {
                NodeStatus.INSUFFICIENT_EVIDENCE,
                NodeStatus.BLOCKED,
                NodeStatus.INVALID,
            }
            for item in body
        ):
            if status[ComponentType.CONCLUSION] == NodeStatus.READY:
                status[ComponentType.CONCLUSION] = NodeStatus.INSUFFICIENT_EVIDENCE
            if status[ComponentType.EXECUTIVE_SUMMARY] == NodeStatus.READY:
                # Keep shell; mark insufficient when nothing to summarize.
                status[ComponentType.EXECUTIVE_SUMMARY] = NodeStatus.INSUFFICIENT_EVIDENCE

        return status
