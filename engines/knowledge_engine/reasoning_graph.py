"""Reasoning Graph Engine — Evidence → Intermediate → Reasoning → Conclusion."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Mapping

from engines.knowledge_engine.models import KnowledgeHit, KnowledgeResult
from engines.knowledge_engine.reasoning_models import (
    ReasoningEdge,
    ReasoningGraph,
    ReasoningNode,
)
from engines.knowledge_engine.retriever import KnowledgeRetriever
from engines.rule_contract.models import normalize_context, resolve_path

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class _ChainStep:
    """One step template in a reasoning chain."""

    kind: str
    label: str
    reason: str
    priority: int
    confidence: float
    domain: str = ""


@dataclass(frozen=True, slots=True)
class _ReasoningTemplate:
    """Deterministic template fired by RuleContext evidence."""

    template_id: str
    evidence_label: str
    domain: str
    matchers: tuple[tuple[str, str], ...]  # (path, expected_contains_lower)
    steps: tuple[_ChainStep, ...]  # intermediate → reasoning → conclusion
    priority: int = 50
    confidence: float = 0.85
    source: str = "rule:template"


# Evidence → Intermediate → Reasoning → Conclusion templates.
# These explain existing RuleContext signals; they do not recalculate engines.
_TEMPLATES: tuple[_ReasoningTemplate, ...] = (
    _ReasoningTemplate(
        template_id="career_officer_strong",
        evidence_label="Strong Officer",
        domain="career",
        matchers=(
            ("ten_gods.items", "chính quan"),
            ("ten_gods.items", "chinh quan"),
            ("ten_gods.items", "zheng_guan"),
            ("pattern.main_pattern", "chinh_quan"),
            ("pattern.name", "chính quan"),
        ),
        steps=(
            _ChainStep(
                "intermediate_rule",
                "Career Leadership",
                "Officer star supports authority and organizational role.",
                80,
                0.9,
                "career",
            ),
            _ChainStep(
                "reasoning",
                "Management Potential",
                "Leadership signal implies capacity to manage people and process.",
                75,
                0.86,
                "career",
            ),
            _ChainStep(
                "conclusion",
                "Suitable Career",
                "Management, administration, education, or consulting roles are favored.",
                70,
                0.84,
                "career",
            ),
        ),
        priority=90,
        confidence=0.9,
        source="rule:career_officer_strong",
    ),
    _ReasoningTemplate(
        template_id="career_qi_sha",
        evidence_label="Seven Killings Present",
        domain="career",
        matchers=(
            ("ten_gods.items", "thất sát"),
            ("ten_gods.items", "that sat"),
            ("ten_gods.items", "qi_sha"),
            ("pattern.main_pattern", "that_sat"),
        ),
        steps=(
            _ChainStep(
                "intermediate_rule",
                "Decisive Authority",
                "Seven Killings indicates decisive force and competitive drive.",
                78,
                0.88,
                "career",
            ),
            _ChainStep(
                "reasoning",
                "High-Pressure Roles",
                "Competitive drive suits demanding execution environments.",
                72,
                0.82,
                "career",
            ),
            _ChainStep(
                "conclusion",
                "Suitable Career",
                "Operations, security, entrepreneurship, or high-stakes execution roles.",
                68,
                0.8,
                "career",
            ),
        ),
        priority=85,
        confidence=0.86,
        source="rule:career_qi_sha",
    ),
    _ReasoningTemplate(
        template_id="wealth_direct",
        evidence_label="Direct Wealth Present",
        domain="wealth",
        matchers=(
            ("ten_gods.items", "chính tài"),
            ("ten_gods.items", "chinh tai"),
            ("ten_gods.items", "zheng_cai"),
        ),
        steps=(
            _ChainStep(
                "intermediate_rule",
                "Stable Income Pattern",
                "Direct Wealth supports steady earning channels.",
                76,
                0.87,
                "wealth",
            ),
            _ChainStep(
                "reasoning",
                "Resource Management",
                "Stable income favors disciplined financial planning.",
                70,
                0.83,
                "wealth",
            ),
            _ChainStep(
                "conclusion",
                "Wealth Outlook",
                "Prefer structured income and asset accumulation over speculative risk.",
                66,
                0.8,
                "wealth",
            ),
        ),
        priority=80,
        confidence=0.85,
        source="rule:wealth_direct",
    ),
    _ReasoningTemplate(
        template_id="shensha_hoa_cai",
        evidence_label="Hoa Cái Present",
        domain="career",
        matchers=(
            ("shensha.stars", "hoa cái"),
            ("shensha.stars", "hoa cai"),
            ("shensha.stars", "hua gai"),
        ),
        steps=(
            _ChainStep(
                "intermediate_rule",
                "Academic Talent",
                "Hoa Cái is classically linked to learning and specialty skill.",
                74,
                0.86,
                "career",
            ),
            _ChainStep(
                "reasoning",
                "Knowledge Craft",
                "Academic talent supports research, teaching, or expert craft.",
                70,
                0.83,
                "career",
            ),
            _ChainStep(
                "conclusion",
                "Suitable Career",
                "Education, research, consulting, arts, or specialized expertise.",
                65,
                0.8,
                "career",
            ),
        ),
        priority=78,
        confidence=0.84,
        source="rule:shensha_hoa_cai",
    ),
    _ReasoningTemplate(
        template_id="useful_god_support",
        evidence_label="Useful God Active",
        domain="useful_god",
        matchers=(
            ("useful_god.status", "ok"),
            ("useful_god.status", "present"),
            ("useful_god.status", "active"),
            ("useful_god.element", "mộc"),
            ("useful_god.element", "hỏa"),
            ("useful_god.element", "thổ"),
            ("useful_god.element", "kim"),
            ("useful_god.element", "thủy"),
            ("useful_god.element", "wood"),
            ("useful_god.element", "fire"),
            ("useful_god.element", "earth"),
            ("useful_god.element", "metal"),
            ("useful_god.element", "water"),
        ),
        steps=(
            _ChainStep(
                "intermediate_rule",
                "Remedial Focus",
                "Useful God identifies the element that balances the chart.",
                77,
                0.88,
                "useful_god",
            ),
            _ChainStep(
                "reasoning",
                "Support Strategy",
                "Favor environments and timing that strengthen the Useful God.",
                71,
                0.84,
                "useful_god",
            ),
            _ChainStep(
                "conclusion",
                "Guidance",
                "Align career, health, and luck choices with Useful God support.",
                67,
                0.81,
                "useful_god",
            ),
        ),
        priority=82,
        confidence=0.86,
        source="rule:useful_god_support",
    ),
    _ReasoningTemplate(
        template_id="strength_strong",
        evidence_label="Day Master Strong",
        domain="strength",
        matchers=(
            ("strength.level", "strong"),
            ("strength.level", "vượng"),
            ("strength.level", "vuong"),
        ),
        steps=(
            _ChainStep(
                "intermediate_rule",
                "Body Capacity High",
                "Strong Day Master indicates higher capacity to take on pressure.",
                73,
                0.86,
                "strength",
            ),
            _ChainStep(
                "reasoning",
                "Output Orientation",
                "High capacity favors expression, wealth, and officer outputs when regulated.",
                69,
                0.82,
                "strength",
            ),
            _ChainStep(
                "conclusion",
                "Strength Outlook",
                "Can pursue assertive paths if Useful God and climate remain balanced.",
                64,
                0.8,
                "strength",
            ),
        ),
        priority=76,
        confidence=0.84,
        source="rule:strength_strong",
    ),
    _ReasoningTemplate(
        template_id="strength_weak",
        evidence_label="Day Master Weak",
        domain="strength",
        matchers=(
            ("strength.level", "weak"),
            ("strength.level", "nhược"),
            ("strength.level", "nhuoc"),
        ),
        steps=(
            _ChainStep(
                "intermediate_rule",
                "Support Needed",
                "Weak Day Master needs resource and protection from Useful God.",
                73,
                0.86,
                "strength",
            ),
            _ChainStep(
                "reasoning",
                "Conservation Strategy",
                "Avoid excessive drain; prioritize support elements and stable timing.",
                69,
                0.82,
                "strength",
            ),
            _ChainStep(
                "conclusion",
                "Strength Outlook",
                "Favor supportive roles, alliances, and Useful God remediation.",
                64,
                0.8,
                "strength",
            ),
        ),
        priority=76,
        confidence=0.84,
        source="rule:strength_weak",
    ),
)


class ReasoningGraphEngine:
    """Build explainable reasoning graphs from RuleContext (+ optional knowledge).

    Pipeline per conclusion:
    Evidence → Intermediate Rule → Reasoning → Conclusion

    Does not recalculate engines. Does not modify UI.
    """

    def __init__(
        self,
        retriever: KnowledgeRetriever | None = None,
        *,
        templates: tuple[_ReasoningTemplate, ...] | None = None,
    ) -> None:
        """Create a reasoning graph engine.

        Args:
            retriever: Optional knowledge retriever for citation enrichment.
            templates: Optional override templates (tests).
        """
        self._retriever = retriever
        self._templates = templates if templates is not None else _TEMPLATES

    def build(
        self,
        rule_context: Mapping[str, Any] | Any,
        knowledge_result: KnowledgeResult | None = None,
        *,
        retrieve_knowledge: bool = False,
    ) -> ReasoningGraph:
        """Build a reasoning graph for the given RuleContext.

        Args:
            rule_context: Production RuleContext.
            knowledge_result: Optional precomputed knowledge hits.
            retrieve_knowledge: When True and no knowledge_result, call retriever.

        Returns:
            ``ReasoningGraph`` with nodes, edges, conclusions, and metadata.trace.
        """
        context = normalize_context(rule_context)
        knowledge = knowledge_result
        if knowledge is None and retrieve_knowledge and self._retriever is not None:
            knowledge = self._retriever.retrieve(context)

        nodes: dict[str, ReasoningNode] = {}
        edges: list[ReasoningEdge] = []
        conclusions: list[str] = []
        trace: list[dict[str, Any]] = []
        edge_seq = 0

        fired = 0
        for template in sorted(self._templates, key=lambda item: (-item.priority, item.template_id)):
            matched_path, matched_value = self._match_template(template, context)
            if matched_path is None:
                trace.append(
                    {
                        "template_id": template.template_id,
                        "accepted": False,
                        "reject_reason": "evidence_not_found",
                    }
                )
                continue

            fired += 1
            evidence_id = f"ev:{template.template_id}"
            self._add_node(
                nodes,
                ReasoningNode(
                    id=evidence_id,
                    label=template.evidence_label,
                    kind="evidence",
                    domain=template.domain,
                    payload={
                        "path": matched_path,
                        "value": matched_value,
                        "template_id": template.template_id,
                    },
                ),
            )

            previous_id = evidence_id
            chain_labels = [template.evidence_label]
            for index, step in enumerate(template.steps, start=1):
                node_id = f"{step.kind}:{template.template_id}:{index}"
                self._add_node(
                    nodes,
                    ReasoningNode(
                        id=node_id,
                        label=step.label,
                        kind=step.kind,  # type: ignore[arg-type]
                        domain=step.domain or template.domain,
                        payload={"template_id": template.template_id, "step": index},
                    ),
                )
                edge_seq += 1
                edge = ReasoningEdge(
                    id=f"e{edge_seq:04d}",
                    source_id=previous_id,
                    target_id=node_id,
                    reason=step.reason,
                    priority=step.priority,
                    confidence=step.confidence,
                    source=template.source,
                )
                edges.append(edge)
                chain_labels.append(step.label)
                previous_id = node_id
                if step.kind == "conclusion" and step.label not in conclusions:
                    conclusions.append(step.label)

            # Attach knowledge citations as optional side evidence edges.
            for hit in self._related_knowledge(knowledge, template):
                kn_id = f"knowledge:{hit.id}"
                self._add_node(
                    nodes,
                    ReasoningNode(
                        id=kn_id,
                        label=hit.record.topic or hit.id,
                        kind="evidence",
                        domain=template.domain,
                        payload={
                            "knowledge_id": hit.id,
                            "reference": hit.record.reference,
                            "modern_interpretation": hit.record.modern_interpretation,
                        },
                    ),
                )
                edge_seq += 1
                edges.append(
                    ReasoningEdge(
                        id=f"e{edge_seq:04d}",
                        source_id=kn_id,
                        target_id=evidence_id,
                        reason="Retrieved classical knowledge supports this evidence.",
                        priority=hit.priority,
                        confidence=hit.confidence,
                        source=f"knowledge:{hit.id}",
                    )
                )

            trace.append(
                {
                    "template_id": template.template_id,
                    "accepted": True,
                    "matched_path": matched_path,
                    "matched_value": matched_value,
                    "chain": chain_labels,
                    "priority": template.priority,
                    "confidence": template.confidence,
                    "source": template.source,
                }
            )

        graph = ReasoningGraph(
            nodes=list(nodes.values()),
            edges=edges,
            conclusions=conclusions,
            metadata={
                "trace": trace,
                "template_count": len(self._templates),
                "fired_count": fired,
                "node_count": len(nodes),
                "edge_count": len(edges),
                "knowledge_attached": bool(knowledge and knowledge.entries),
            },
        )
        logger.debug(
            "Reasoning graph built fired=%s nodes=%s edges=%s",
            fired,
            len(nodes),
            len(edges),
        )
        return graph

    def _match_template(
        self, template: _ReasoningTemplate, context: Mapping[str, Any]
    ) -> tuple[str | None, str | None]:
        for path, expected in template.matchers:
            actual = resolve_path(context, path, default=None)
            if self._value_contains(actual, expected):
                return path, expected
        return None, None

    def _value_contains(self, actual: Any, expected: str) -> bool:
        needle = expected.strip().lower()
        if not needle:
            return False
        if actual is None:
            return False
        if isinstance(actual, Mapping):
            return any(self._value_contains(item, needle) for item in actual.values()) or any(
                needle in str(key).lower() for key in actual.keys()
            )
        if isinstance(actual, (list, tuple, set)):
            return any(self._value_contains(item, needle) for item in actual)
        text = str(actual).strip().lower()
        if not text:
            return False
        if text == needle or needle in text:
            return True
        # Underscore / spacing variants
        compact = re.sub(r"[\s_]+", "", text)
        needle_compact = re.sub(r"[\s_]+", "", needle)
        return needle_compact in compact

    def _related_knowledge(
        self, knowledge: KnowledgeResult | None, template: _ReasoningTemplate
    ) -> list[KnowledgeHit]:
        if knowledge is None or not knowledge.entries:
            return []
        domain = template.domain.lower()
        evidence_tokens = {
            token
            for token in re.split(r"[\s/|,;]+", template.evidence_label.lower())
            if token
        }
        related: list[KnowledgeHit] = []
        for hit in knowledge.entries:
            topic = (hit.record.topic or "").lower()
            keywords = set(hit.record.keyword_tokens())
            if domain and domain in topic:
                related.append(hit)
                continue
            if keywords & evidence_tokens:
                related.append(hit)
                continue
            if any(token in " ".join(keywords) for token in evidence_tokens if len(token) > 2):
                related.append(hit)
        return related[:3]

    def _add_node(self, bucket: dict[str, ReasoningNode], node: ReasoningNode) -> None:
        if node.id not in bucket:
            bucket[node.id] = node
