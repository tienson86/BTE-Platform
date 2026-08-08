"""Component ordering for Narrative Runtime (Sprint D1)."""

from __future__ import annotations

from .models import OFFICIAL_COMPONENT_ORDER, ComponentType, NarrativeNode


class ComponentOrdering:
    """Enforce official Sprint B published order."""

    def order(self, nodes: dict[ComponentType, NarrativeNode]) -> tuple[NarrativeNode, ...]:
        """
        Return nodes in official order with priority indices assigned.

        Missing components are not invented here — caller must supply all shells.
        """
        ordered: list[NarrativeNode] = []
        for index, component in enumerate(OFFICIAL_COMPONENT_ORDER):
            node = nodes[component]
            ordered.append(
                NarrativeNode(
                    component_type=node.component_type,
                    evidence_refs=node.evidence_refs,
                    interpretation_refs=node.interpretation_refs,
                    confidence=node.confidence,
                    priority=index,
                    dependencies=node.dependencies,
                    status=node.status,
                )
            )
        return tuple(ordered)
