"""NarrativeTree builder (Sprint D1)."""

from __future__ import annotations

import logging

from .models import (
    COMPONENT_DEPENDENCIES,
    OFFICIAL_COMPONENT_ORDER,
    ComponentType,
    NarrativeNode,
    NarrativeTree,
    NodeStatus,
    TreeStatus,
)

logger = logging.getLogger(__name__)


class NarrativeTreeBuilder:
    """Assemble NarrativeNode map into NarrativeTree shells."""

    def build_draft_nodes(
        self,
        bindings: dict[ComponentType, tuple[tuple[str, ...], tuple[str, ...]]],
    ) -> dict[ComponentType, NarrativeNode]:
        """
        Create draft nodes with READY or INSUFFICIENT_EVIDENCE from bindings.

        No prose is attached.
        """
        nodes: dict[ComponentType, NarrativeNode] = {}
        for index, component in enumerate(OFFICIAL_COMPONENT_ORDER):
            evidence_ids, interp_ids = bindings[component]
            has_support = bool(evidence_ids) or bool(interp_ids)
            # Reasoning requires explanation evidence specifically — binding already filtered.
            status = NodeStatus.READY if has_support else NodeStatus.INSUFFICIENT_EVIDENCE
            nodes[component] = NarrativeNode(
                component_type=component,
                evidence_refs=evidence_ids,
                interpretation_refs=interp_ids,
                confidence=0.0,
                priority=index,
                dependencies=COMPONENT_DEPENDENCIES[component],
                status=status,
            )
        return nodes

    def build_tree(
        self,
        ordered_nodes: tuple[NarrativeNode, ...],
        *,
        run_id: str,
        validation_issues: tuple[str, ...] = (),
        metadata: dict | None = None,
    ) -> NarrativeTree:
        """Create NarrativeTree aggregate from ordered nodes."""
        if validation_issues:
            tree_status = TreeStatus.INVALID
        elif any(node.status != NodeStatus.READY for node in ordered_nodes):
            tree_status = TreeStatus.PARTIAL_INSUFFICIENT
        else:
            tree_status = TreeStatus.COMPLETE

        tree = NarrativeTree(
            nodes=ordered_nodes,
            run_id=run_id,
            status=tree_status,
            validation_issues=validation_issues,
            metadata=dict(metadata or {}),
        )
        logger.info(
            "tree_builder.status=%s nodes=%s",
            tree.status.value,
            len(tree.nodes),
        )
        return tree
