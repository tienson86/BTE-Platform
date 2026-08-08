"""NarrativeTree validator (Sprint D1)."""

from __future__ import annotations

import logging

from .models import (
    OFFICIAL_COMPONENT_ORDER,
    ComponentType,
    NarrativeNode,
    NarrativeTree,
    NodeStatus,
    TreeStatus,
)

logger = logging.getLogger(__name__)

# Hard guarantee: nodes must not carry prose-like attributes.
_FORBIDDEN_NODE_ATTRS = frozenset(
    {
        "text",
        "body",
        "paragraph",
        "paragraphs",
        "prose",
        "sentence",
        "sentences",
        "markdown",
        "html",
    }
)


class NarrativeValidator:
    """
    Validate NarrativeTree integrity against Sprint B grammar.

    Rejects trees that include prose payloads or broken order.
    """

    def validate_ordered_nodes(
        self,
        nodes: tuple[NarrativeNode, ...],
    ) -> tuple[str, ...]:
        """Return validation issue codes (empty means OK)."""
        issues: list[str] = []
        if len(nodes) != len(OFFICIAL_COMPONENT_ORDER):
            issues.append("node_count_mismatch")
        for index, expected in enumerate(OFFICIAL_COMPONENT_ORDER):
            if index >= len(nodes):
                issues.append(f"missing:{expected.value}")
                continue
            node = nodes[index]
            if node.component_type != expected:
                issues.append(
                    f"order_violation:{index}:{node.component_type.value}!={expected.value}"
                )
            if node.priority != index:
                issues.append(f"priority_mismatch:{expected.value}")
            issues.extend(_validate_node_shape(node))
            if node.status == NodeStatus.READY and not (
                node.evidence_refs or node.interpretation_refs
            ):
                issues.append(f"ready_without_refs:{expected.value}")
        return tuple(issues)

    def apply_tree_status(
        self,
        tree: NarrativeTree,
        issues: tuple[str, ...],
    ) -> NarrativeTree:
        """Return tree with validation issues and corrected aggregate status."""
        if issues:
            status = TreeStatus.INVALID
        elif any(node.status != NodeStatus.READY for node in tree.nodes):
            status = TreeStatus.PARTIAL_INSUFFICIENT
        else:
            status = TreeStatus.COMPLETE
        logger.info("narrative_validator.status=%s issues=%s", status.value, len(issues))
        return NarrativeTree(
            nodes=tree.nodes,
            run_id=tree.run_id,
            status=status,
            validation_issues=issues,
            metadata=dict(tree.metadata),
        )


def _validate_node_shape(node: NarrativeNode) -> list[str]:
    """Ensure node has no prose-bearing attributes."""
    issues: list[str] = []
    for attr in _FORBIDDEN_NODE_ATTRS:
        if hasattr(node, attr):
            issues.append(f"prose_attr_forbidden:{node.component_type.value}:{attr}")
    if not isinstance(node.component_type, ComponentType):
        issues.append("invalid_component_type")
    if not isinstance(node.status, NodeStatus):
        issues.append(f"invalid_status:{node.component_type.value}")
    if node.confidence < 0.0 or node.confidence > 1.0:
        issues.append(f"confidence_out_of_range:{node.component_type.value}")
    return issues
