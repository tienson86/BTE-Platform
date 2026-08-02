"""Discussion AI — grounded answers from Evidence, Knowledge, and ReasoningGraph.

Supported question families:
- Why?
- How?
- Evidence?
- Alternative interpretation?
- What if birth time changes?
- What if Useful God changes?

Never answers from raw chart alone.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Mapping

from engines.knowledge_engine.citation_engine import CitationEngine
from engines.knowledge_engine.discussion_models import (
    SUPPORTED_QUESTION_TYPES,
    ConversationResult,
    DiscussionAnswer,
    QuestionType,
)
from engines.knowledge_engine.evidence_builder import EvidenceBuilder
from engines.knowledge_engine.evidence_models import EvidencePackage
from engines.knowledge_engine.models import KnowledgeResult
from engines.knowledge_engine.reasoning_graph import ReasoningGraphEngine
from engines.knowledge_engine.reasoning_models import ReasoningGraph
from engines.knowledge_engine.retriever import KnowledgeRetriever
from engines.rule_contract.models import normalize_context

logger = logging.getLogger(__name__)

_WHY_RE = re.compile(r"(?i)\b(why|tại sao|tai sao|vì sao|vi sao)\b")
_HOW_RE = re.compile(r"(?i)\b(how|như thế nào|nhu the nao|bằng cách nào|bang cach nao)\b")
_EVIDENCE_RE = re.compile(
    r"(?i)\b(evidence|bằng chứng|bang chung|căn cứ|can cu|dựa vào đâu|dua vao dau)\b"
)
_ALT_RE = re.compile(
    r"(?i)\b(alternative|diễn giải khác|dien giai khac|cách hiểu khác|"
    r"cach hieu khac|khác cách|other interpretation)\b"
)
_BIRTH_TIME_RE = re.compile(
    r"(?i)\b(birth\s*time|giờ sinh|gio sinh|hour pillar|giờ thay đổi|"
    r"gio thay doi|if.+hour|nếu.+giờ|neu.+gio)\b"
)
_USEFUL_GOD_RE = re.compile(
    r"(?i)\b(useful\s*god|dụng thần|dung than|nếu.+dụng|neu.+dung|"
    r"if.+useful|useful god changes|đổi dụng thần|doi dung than)\b"
)

# Signals that indicate RuleContext-derived packages rather than bare pillars.
_CONTEXT_SIGNAL_KEYS: tuple[str, ...] = (
    "ten_gods",
    "useful_god",
    "pattern",
    "strength",
    "temperature",
    "shensha",
    "wuxing",
    "score",
)


class DiscussionAI:
    """Conversational expert that answers only from Evidence/Knowledge/Reasoning."""

    def __init__(
        self,
        *,
        evidence_builder: EvidenceBuilder | None = None,
        retriever: KnowledgeRetriever | None = None,
        reasoning_engine: ReasoningGraphEngine | None = None,
        citation_engine: CitationEngine | None = None,
    ) -> None:
        """Wire optional dependencies for grounded discussion."""
        self._evidence_builder = evidence_builder or EvidenceBuilder()
        self._retriever = retriever
        self._reasoning_engine = reasoning_engine or ReasoningGraphEngine(
            retriever=retriever
        )
        self._citation_engine = citation_engine or CitationEngine()

    def classify(self, question: str) -> QuestionType:
        """Classify a user question into a supported Discussion type."""
        text = str(question or "").strip()
        if not text:
            return "unsupported"
        if _BIRTH_TIME_RE.search(text):
            return "what_if_birth_time"
        if _USEFUL_GOD_RE.search(text):
            return "what_if_useful_god"
        if _ALT_RE.search(text):
            return "alternative_interpretation"
        if _EVIDENCE_RE.search(text):
            return "evidence"
        if _WHY_RE.search(text):
            return "why"
        if _HOW_RE.search(text):
            return "how"
        return "unsupported"

    def ask(
        self,
        question: str,
        *,
        rule_context: Mapping[str, Any] | Any | None = None,
        chart: Mapping[str, Any] | Any | None = None,
        knowledge: KnowledgeResult | None = None,
        evidence: EvidencePackage | None = None,
        reasoning: ReasoningGraph | None = None,
    ) -> DiscussionAnswer:
        """Answer one discussion question with Evidence/Knowledge/Reasoning only.

        Args:
            question: User question text.
            rule_context: Production RuleContext (preferred grounding input).
            chart: Optional raw chart. Alone is never sufficient.
            knowledge: Optional precomputed knowledge result.
            evidence: Optional precomputed evidence package.
            reasoning: Optional precomputed reasoning graph.

        Returns:
            ``DiscussionAnswer`` (may be refused when grounding is incomplete).
        """
        question_type = self.classify(question)
        if question_type == "unsupported":
            return self._refuse(
                question,
                question_type,
                "unsupported_question_type",
                "Question type is not supported by Discussion AI.",
            )

        if chart is not None and rule_context is None and evidence is None and reasoning is None:
            return self._refuse(
                question,
                question_type,
                "raw_chart_only",
                "Discussion AI never answers from raw chart alone.",
            )

        context = normalize_context(rule_context) if rule_context is not None else {}
        if not context and evidence is None and reasoning is None:
            return self._refuse(
                question,
                question_type,
                "missing_rule_context",
                "RuleContext (or prebuilt Evidence/Reasoning) is required.",
            )

        if context and not self._has_analysis_signals(context) and evidence is None:
            # Bare pillar-only context is treated as raw chart.
            if self._looks_like_raw_chart(context):
                return self._refuse(
                    question,
                    question_type,
                    "raw_chart_only",
                    "Discussion AI never answers from raw chart alone.",
                )

        evidence_pkg = evidence or (
            self._evidence_builder.build(context) if context else EvidencePackage([], {})
        )
        knowledge_result = knowledge
        if knowledge_result is None and self._retriever is not None and context:
            knowledge_result = self._retriever.retrieve(context)
        if knowledge_result is None:
            knowledge_result = KnowledgeResult(entries=[], metadata={})

        reasoning_graph = reasoning or (
            self._reasoning_engine.build(
                context,
                knowledge_result=knowledge_result,
            )
            if context
            else ReasoningGraph(nodes=[], edges=[], conclusions=[], metadata={})
        )

        used_evidence = bool(evidence_pkg.items)
        used_knowledge = bool(knowledge_result.entries)
        used_reasoning = bool(reasoning_graph.nodes or reasoning_graph.conclusions)

        if not (used_evidence and used_knowledge and used_reasoning):
            missing = []
            if not used_evidence:
                missing.append("Evidence")
            if not used_knowledge:
                missing.append("Knowledge")
            if not used_reasoning:
                missing.append("Reasoning")
            return self._refuse(
                question,
                question_type,
                "incomplete_grounding",
                "Answer requires Evidence, Knowledge, and Reasoning Graph; missing: "
                + ", ".join(missing),
                metadata={
                    "evidence_count": len(evidence_pkg.items),
                    "knowledge_count": len(knowledge_result.entries),
                    "reasoning_nodes": len(reasoning_graph.nodes),
                },
            )

        answer_text = self._compose_answer(
            question_type,
            evidence=evidence_pkg,
            knowledge=knowledge_result,
            reasoning=reasoning_graph,
        )
        citations = self._citation_engine.build(knowledge_result)
        confidence = self._confidence(evidence_pkg, knowledge_result, reasoning_graph)

        result = DiscussionAnswer(
            question=str(question or "").strip(),
            question_type=question_type,
            answer=answer_text,
            grounded=True,
            used_evidence=True,
            used_knowledge=True,
            used_reasoning=True,
            refused=False,
            confidence=confidence,
            metadata={
                "supported_types": list(SUPPORTED_QUESTION_TYPES),
                "evidence_count": len(evidence_pkg.items),
                "knowledge_count": len(knowledge_result.entries),
                "reasoning_conclusions": list(reasoning_graph.conclusions),
                "citation_count": len(citations.citations),
                "citations_visible": False,
            },
        )
        logger.debug(
            "Discussion answered type=%s confidence=%.3f",
            question_type,
            confidence,
        )
        return result

    def converse(
        self,
        questions: list[str],
        *,
        rule_context: Mapping[str, Any] | Any | None = None,
        chart: Mapping[str, Any] | Any | None = None,
        knowledge: KnowledgeResult | None = None,
        evidence: EvidencePackage | None = None,
        reasoning: ReasoningGraph | None = None,
    ) -> ConversationResult:
        """Run a multi-turn grounded conversation."""
        # Build shared packages once for stable conversation grounding.
        context = normalize_context(rule_context) if rule_context is not None else {}
        shared_evidence = evidence
        shared_knowledge = knowledge
        shared_reasoning = reasoning

        if context and shared_evidence is None:
            shared_evidence = self._evidence_builder.build(context)
        if context and shared_knowledge is None and self._retriever is not None:
            shared_knowledge = self._retriever.retrieve(context)
        if context and shared_reasoning is None:
            shared_reasoning = self._reasoning_engine.build(
                context,
                knowledge_result=shared_knowledge,
            )

        turns: list[DiscussionAnswer] = []
        for question in questions:
            turns.append(
                self.ask(
                    question,
                    rule_context=rule_context,
                    chart=chart,
                    knowledge=shared_knowledge,
                    evidence=shared_evidence,
                    reasoning=shared_reasoning,
                )
            )

        return ConversationResult(
            turns=turns,
            metadata={
                "turn_count": len(turns),
                "grounded_turns": sum(1 for turn in turns if turn.grounded),
                "refused_turns": sum(1 for turn in turns if turn.refused),
            },
        )

    # ------------------------------------------------------------------
    # Answer composition
    # ------------------------------------------------------------------

    def _compose_answer(
        self,
        question_type: QuestionType,
        *,
        evidence: EvidencePackage,
        knowledge: KnowledgeResult,
        reasoning: ReasoningGraph,
    ) -> str:
        evidence_line = self._evidence_summary(evidence)
        knowledge_line = self._knowledge_summary(knowledge)
        reasoning_line = self._reasoning_summary(reasoning)
        conclusions = list(reasoning.conclusions) or [
            node.label for node in reasoning.nodes if node.kind == "conclusion"
        ]
        primary = conclusions[0] if conclusions else "the current conclusion"
        alternative = conclusions[1] if len(conclusions) > 1 else None

        if question_type == "why":
            body = (
                f"The chart reading favors {primary} because the reasoning chain "
                f"is supported by observed evidence and classical knowledge."
            )
        elif question_type == "how":
            body = (
                f"The conclusion {primary} is reached by moving from evidence to "
                f"intermediate rules, then reasoning, then conclusion in the graph."
            )
        elif question_type == "evidence":
            body = (
                "The decisive evidence items are listed below and must be read "
                "together with knowledge and reasoning before any claim is accepted."
            )
        elif question_type == "alternative_interpretation":
            if alternative:
                body = (
                    f"An alternative interpretation from the same graph is {alternative}. "
                    f"It remains secondary to {primary} unless new evidence appears."
                )
            else:
                body = (
                    f"No competing conclusion is currently stronger than {primary}. "
                    "An alternative would require additional Evidence or Knowledge."
                )
        elif question_type == "what_if_birth_time":
            body = (
                "If birth time changes, hour-pillar evidence and dependent reasoning "
                "edges may shift. Re-evaluate with updated RuleContext Evidence, "
                "Knowledge, and Reasoning Graph rather than raw pillars alone."
            )
        else:  # what_if_useful_god
            body = (
                "If Useful God changes, Useful-God evidence and related reasoning "
                "conclusions must be rebuilt. Do not keep old conclusions without "
                "fresh Evidence, Knowledge, and Reasoning Graph support."
            )

        # Every answer paragraph cites Evidence, Knowledge, and Reasoning.
        return (
            f"[Evidence] {evidence_line} "
            f"[Knowledge] {knowledge_line} "
            f"[Reasoning] {reasoning_line} {body}"
        )

    def _evidence_summary(self, evidence: EvidencePackage) -> str:
        top = evidence.items[:3]
        if not top:
            return "No evidence items available."
        bits = [f"{item.rule} ({item.reason})" for item in top]
        return "Key evidence: " + "; ".join(bits) + "."

    def _knowledge_summary(self, knowledge: KnowledgeResult) -> str:
        if not knowledge.entries:
            return "No knowledge entries available."
        record = knowledge.entries[0].record
        classical = record.classical_text or record.modern_interpretation or record.topic
        return f"Classical support ({record.topic or 'knowledge'}): {classical}."

    def _reasoning_summary(self, reasoning: ReasoningGraph) -> str:
        if reasoning.conclusions:
            joined = "; ".join(reasoning.conclusions[:3])
            return f"Graph conclusions: {joined}."
        evidence_nodes = [node for node in reasoning.nodes if node.kind == "evidence"]
        if evidence_nodes:
            paths = reasoning.path_labels(evidence_nodes[0].id)
            if paths:
                return "Reasoning chain: " + " → ".join(paths[0]) + "."
        return "Reasoning graph is present but has no explicit conclusion labels."

    def _confidence(
        self,
        evidence: EvidencePackage,
        knowledge: KnowledgeResult,
        reasoning: ReasoningGraph,
    ) -> float:
        scores: list[float] = [float(item.confidence) for item in evidence.items]
        scores.extend(float(hit.confidence) for hit in knowledge.entries)
        scores.extend(float(edge.confidence) for edge in reasoning.edges)
        if not scores:
            return 0.0
        return round(sum(scores) / float(len(scores)), 4)

    # ------------------------------------------------------------------
    # Guards
    # ------------------------------------------------------------------

    def _refuse(
        self,
        question: str,
        question_type: QuestionType,
        reason: str,
        message: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> DiscussionAnswer:
        return DiscussionAnswer(
            question=str(question or "").strip(),
            question_type=question_type,
            answer=message,
            grounded=False,
            used_evidence=False,
            used_knowledge=False,
            used_reasoning=False,
            refused=True,
            refuse_reason=reason,
            confidence=0.0,
            metadata=dict(metadata or {}),
        )

    def _has_analysis_signals(self, context: Mapping[str, Any]) -> bool:
        for key in _CONTEXT_SIGNAL_KEYS:
            value = context.get(key)
            if value not in (None, "", [], {}):
                return True
        return False

    def _looks_like_raw_chart(self, context: Mapping[str, Any]) -> bool:
        chart_keys = {
            "year_pillar",
            "month_pillar",
            "day_pillar",
            "hour_pillar",
            "day_master",
            "bazi",
            "four_pillars",
        }
        return any(key in context for key in chart_keys)
