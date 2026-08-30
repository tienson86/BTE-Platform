"""ReasoningValidator — contract checks only. No astrology interpretation."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.evidence.evidence_context import NarrativeEvidenceContext
from engines.narrative_v2.reasoning.reasoning_context import NarrativeReasoningContext
from engines.narrative_v2.reasoning.reasoning_edge import (
    ALLOWED_EDGE_STATUSES,
    ALLOWED_RELATION_TYPES,
    ReasoningEdge,
)
from engines.narrative_v2.reasoning.reasoning_errors import ReasoningValidationError
from engines.narrative_v2.reasoning.reasoning_node import (
    ALLOWED_KINDS,
    ALLOWED_NODE_STATUSES,
    ReasoningNode,
)
from engines.narrative_v2.reasoning.reasoning_registry import ReasoningRegistry

CUSTOMER_PROSE_MARKERS: tuple[str, ...] = (
    "Bạn có",
    "Bạn làm",
    "Bạn nên",
    "nên bổ",
    "tình duyên",
    "vận tốt",
    "vận thuận lợi",
    "nội lực tốt",
    "làm việc có hệ thống",
    "làm việc theo hệ thống",
)

FORBIDDEN_FIELD_TOKENS: tuple[str, ...] = (
    "customer_text",
    "customer_meaning",
    "headline",
    "summary",
    "recommendation",
    "action",
    "warning",
    "insight",
)

FORBIDDEN_CONTEXT_ATTRS: tuple[str, ...] = (
    "canonical_analysis",
    "customer_text",
    "headline",
    "summary",
    "recommendation",
    "action",
    "warning",
)


@dataclass(slots=True)
class ReasoningValidationOutcome:
    """Reasoning contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class ReasoningValidator:
    """Validate ReasoningContext against N-IMP-03 contract rules."""

    def __init__(self, *, registry: ReasoningRegistry | None = None) -> None:
        self._registry = registry or ReasoningRegistry()

    def validate(
        self,
        context: NarrativeReasoningContext,
        evidence: NarrativeEvidenceContext,
    ) -> ReasoningValidationOutcome:
        """PASS unless the reasoning contract is violated."""
        try:
            self.assert_valid(context, evidence)
        except ReasoningValidationError as exc:
            return ReasoningValidationOutcome(passed=False, reason=exc.message)
        return ReasoningValidationOutcome(passed=True)

    def assert_valid(
        self,
        context: NarrativeReasoningContext,
        evidence: NarrativeEvidenceContext,
    ) -> None:
        """Raise if the context violates the reasoning contract."""
        self._reject_canonical_access(context)
        self._check_ids(context.nodes)
        self._check_ordering(context.nodes)
        evidence_ids = {item.evidence_id for item in evidence.items}
        node_ids = {node.reasoning_id for node in context.nodes}
        for node in context.nodes:
            self._check_node(node, evidence_ids)
        for edge in context.edges:
            self._check_edge(edge, node_ids)
        self._assert_acyclic(context.edges)

    def _reject_canonical_access(self, context: NarrativeReasoningContext) -> None:
        for attr in FORBIDDEN_CONTEXT_ATTRS:
            if hasattr(context, attr):
                raise ReasoningValidationError(
                    f"Reasoning must not expose {attr}"
                )

    def _check_ids(self, nodes: tuple[ReasoningNode, ...]) -> None:
        seen: set[str] = set()
        for node in nodes:
            if not node.reasoning_id.startswith("reasoning."):
                raise ReasoningValidationError(
                    f"Reasoning id is not deterministic: {node.reasoning_id}"
                )
            if node.reasoning_id in seen:
                raise ReasoningValidationError(
                    f"Duplicate reasoning_id: {node.reasoning_id}"
                )
            seen.add(node.reasoning_id)

    def _check_ordering(self, nodes: tuple[ReasoningNode, ...]) -> None:
        ordered = tuple(
            sorted(nodes, key=lambda node: (node.priority, node.reasoning_id))
        )
        if nodes != ordered:
            raise ReasoningValidationError("Reasoning nodes are not deterministically ordered")

    def _check_node(self, node: ReasoningNode, evidence_ids: set[str]) -> None:
        if node.kind not in ALLOWED_KINDS:
            raise ReasoningValidationError(f"Unsupported reasoning kind: {node.kind}")
        if node.status not in ALLOWED_NODE_STATUSES:
            raise ReasoningValidationError(f"Invalid reasoning status: {node.status}")
        if node.kind != "boundary" and not node.evidence_ids:
            raise ReasoningValidationError(
                f"Reasoning node is not traceable to Evidence: {node.reasoning_id}"
            )
        for evidence_id in node.evidence_ids:
            if evidence_id not in evidence_ids:
                raise ReasoningValidationError(
                    f"Unknown evidence_id: {evidence_id}"
                )
        self._reject_forbidden_tokens(node.reasoning_id)
        self._reject_forbidden_tokens(node.semantic_key)
        self._reject_prose(node)
        self._check_known_rule(node)
        if node.relation and node.relation not in ALLOWED_RELATION_TYPES:
            raise ReasoningValidationError(
                f"Unsupported relation type: {node.relation}"
            )

    def _check_known_rule(self, node: ReasoningNode) -> None:
        rule_id = _metadata_value(node.metadata, "rule_id")
        if rule_id is None:
            return
        if not self._registry.contains(rule_id):
            raise ReasoningValidationError(f"Unknown reasoning rule: {rule_id}")

    def _check_edge(self, edge: ReasoningEdge, node_ids: set[str]) -> None:
        if edge.relation_type not in ALLOWED_RELATION_TYPES:
            raise ReasoningValidationError(
                f"Unsupported relation type: {edge.relation_type}"
            )
        if edge.status not in ALLOWED_EDGE_STATUSES:
            raise ReasoningValidationError(f"Invalid edge status: {edge.status}")
        if edge.target_id not in node_ids:
            raise ReasoningValidationError(f"Edge target missing: {edge.target_id}")
        for source_id in edge.source_ids:
            if source_id not in node_ids:
                raise ReasoningValidationError(f"Edge source missing: {source_id}")
        self._reject_forbidden_tokens(edge.edge_id)

    def _assert_acyclic(self, edges: tuple[ReasoningEdge, ...]) -> None:
        graph: dict[str, list[str]] = {}
        for edge in edges:
            for source_id in edge.source_ids:
                graph.setdefault(source_id, []).append(edge.target_id)
        visiting: set[str] = set()
        visited: set[str] = set()

        def _walk(node_id: str) -> None:
            if node_id in visited:
                return
            if node_id in visiting:
                raise ReasoningValidationError("Circular reasoning dependency is not allowed")
            visiting.add(node_id)
            for nxt in graph.get(node_id, ()):
                _walk(nxt)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in graph:
            _walk(node_id)

    def _reject_forbidden_tokens(self, token: str) -> None:
        lowered = token.lower()
        for banned in FORBIDDEN_FIELD_TOKENS:
            if banned in lowered:
                raise ReasoningValidationError(
                    f"Presentation token is forbidden: {token}"
                )

    def _reject_prose(self, node: ReasoningNode) -> None:
        texts = [node.semantic_key, node.reasoning_id, node.relation, node.domain]
        texts.extend(value for _, value in node.metadata)
        blob = " ".join(texts)
        for marker in CUSTOMER_PROSE_MARKERS:
            if marker in blob:
                raise ReasoningValidationError(
                    f"Customer prose is not reasoning: {node.reasoning_id}"
                )


def _metadata_value(metadata: tuple[tuple[str, str], ...], key: str) -> str | None:
    for name, value in metadata:
        if name == key:
            return value
    return None
