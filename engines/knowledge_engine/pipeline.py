"""Knowledge Pipeline — end-to-end Epic 03 integration orchestrator.

Pipeline order (Milestone 10):

Knowledge → Retriever → Reasoning Graph → Evidence Builder →
Prompt Builder → LLM → Response Validator → Portal payload

Does not modify calculation engines. Does not change public analyze pipeline
order. Portal payload is additive and narrative-compatible.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.knowledge_engine.citation_engine import CitationEngine
from engines.knowledge_engine.discussion_ai import DiscussionAI
from engines.knowledge_engine.discussion_models import DiscussionAnswer
from engines.knowledge_engine.evidence_builder import EvidenceBuilder
from engines.knowledge_engine.evidence_models import EvidencePackage
from engines.knowledge_engine.llm import DeterministicKnowledgeLLM, LLMClient
from engines.knowledge_engine.models import KnowledgeResult
from engines.knowledge_engine.prompt_builder import PromptBuilder
from engines.knowledge_engine.prompt_models import StructuredPrompt
from engines.knowledge_engine.reasoning_graph import ReasoningGraphEngine
from engines.knowledge_engine.reasoning_models import ReasoningGraph
from engines.knowledge_engine.response_validator import AIResponseValidator
from engines.knowledge_engine.retriever import KnowledgeRetriever
from engines.knowledge_engine.validation_models import ValidationReport
from engines.rule_contract.models import normalize_context

logger = logging.getLogger(__name__)

PIPELINE_STAGES: tuple[str, ...] = (
    "knowledge",
    "retriever",
    "reasoning_graph",
    "evidence_builder",
    "prompt_builder",
    "llm",
    "response_validator",
    "portal",
)

PIPELINE_VERSION = "1.0.0"


@dataclass(slots=True)
class KnowledgePipelineResult:
    """Full Knowledge Expert pipeline output."""

    knowledge: KnowledgeResult
    reasoning: ReasoningGraph
    evidence: EvidencePackage
    prompt: StructuredPrompt
    llm_output: str
    validation: ValidationReport
    discussion: DiscussionAnswer | None
    portal_payload: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize pipeline result for API / reports."""
        return {
            "knowledge": self.knowledge.to_dict(),
            "reasoning": self.reasoning.to_dict(),
            "evidence": self.evidence.to_dict(),
            "prompt": self.prompt.to_dict(),
            "llm_output": self.llm_output,
            "validation": self.validation.to_dict(),
            "discussion": self.discussion.to_dict() if self.discussion else None,
            "portal_payload": dict(self.portal_payload),
            "metadata": dict(self.metadata),
        }


class KnowledgePipeline:
    """Orchestrate the Epic 03 Knowledge Expert chain."""

    def __init__(
        self,
        *,
        retriever: KnowledgeRetriever | None = None,
        reasoning_engine: ReasoningGraphEngine | None = None,
        evidence_builder: EvidenceBuilder | None = None,
        prompt_builder: PromptBuilder | None = None,
        llm: LLMClient | None = None,
        validator: AIResponseValidator | None = None,
        citation_engine: CitationEngine | None = None,
        discussion_ai: DiscussionAI | None = None,
    ) -> None:
        """Wire pipeline stages with optional dependency injection."""
        self._retriever = retriever
        self._reasoning_engine = reasoning_engine or ReasoningGraphEngine(
            retriever=retriever
        )
        self._evidence_builder = evidence_builder or EvidenceBuilder()
        self._prompt_builder = prompt_builder or PromptBuilder()
        self._discussion_ai = discussion_ai or DiscussionAI(
            evidence_builder=self._evidence_builder,
            retriever=retriever,
            reasoning_engine=self._reasoning_engine,
            citation_engine=citation_engine,
        )
        self._llm = llm or DeterministicKnowledgeLLM(self._discussion_ai)
        self._validator = validator or AIResponseValidator()
        self._citation_engine = citation_engine or CitationEngine()

    @staticmethod
    def portal_status(*, corpus_ready: bool = False) -> dict[str, Any]:
        """Additive portal/analyze status block (does not alter public pipeline)."""
        return {
            "version": PIPELINE_VERSION,
            "status": "ready" if corpus_ready else "available",
            "stages": list(PIPELINE_STAGES),
            "endpoint": "/api/v1/discussion",
            "alters_public_pipeline": False,
            "alters_narrative": False,
        }

    def run(
        self,
        *,
        rule_context: Mapping[str, Any] | Any,
        question: str | None = None,
        chart: Mapping[str, Any] | Any | None = None,
        knowledge: KnowledgeResult | None = None,
        show_citations: bool = False,
    ) -> KnowledgePipelineResult:
        """Execute the full Knowledge → … → Portal pipeline.

        Args:
            rule_context: Analysis RuleContext (never raw chart alone).
            question: Optional discussion question for LLM/Discussion step.
            chart: Optional chart facts for Prompt Builder Facts section.
            knowledge: Optional precomputed knowledge hits.
            show_citations: Forwarded to Prompt Builder (default hidden).

        Returns:
            ``KnowledgePipelineResult`` including portal-ready payload.
        """
        context = normalize_context(rule_context)
        trace: list[dict[str, Any]] = []

        # 1–2 Knowledge + Retriever
        knowledge_result = knowledge
        if knowledge_result is None:
            if self._retriever is not None:
                knowledge_result = self._retriever.retrieve(context)
                trace.append(
                    {
                        "stage": "retriever",
                        "hit_count": len(knowledge_result.entries),
                    }
                )
            else:
                knowledge_result = KnowledgeResult(entries=[], metadata={})
                trace.append({"stage": "retriever", "hit_count": 0, "skipped": True})
        else:
            trace.append(
                {
                    "stage": "retriever",
                    "hit_count": len(knowledge_result.entries),
                    "precomputed": True,
                }
            )
        trace.append(
            {
                "stage": "knowledge",
                "record_count": len(knowledge_result.records),
            }
        )

        # 3 Reasoning Graph
        reasoning = self._reasoning_engine.build(
            context,
            knowledge_result=knowledge_result,
        )
        trace.append(
            {
                "stage": "reasoning_graph",
                "node_count": len(reasoning.nodes),
                "conclusion_count": len(reasoning.conclusions),
            }
        )

        # 4 Evidence Builder
        evidence = self._evidence_builder.build(context)
        trace.append(
            {
                "stage": "evidence_builder",
                "item_count": len(evidence.items),
            }
        )

        # 5 Prompt Builder (+ internal citations)
        citations = self._citation_engine.build(knowledge_result)
        prompt = self._prompt_builder.build(
            evidence=evidence,
            knowledge=knowledge_result,
            reasoning=reasoning,
            chart=chart if chart is not None else context,
            citations=citations,
            show_citations=show_citations,
        )
        trace.append(
            {
                "stage": "prompt_builder",
                "citation_count": len(citations.citations),
                "citations_visible": show_citations,
            }
        )

        # 6 LLM
        ask_question = (question or "").strip() or "Why is this conclusion favored?"
        llm_output = self._llm.generate(
            prompt,
            question=ask_question,
            evidence=evidence,
            knowledge=knowledge_result,
            reasoning=reasoning,
        )
        trace.append({"stage": "llm", "output_chars": len(llm_output)})

        # 7 Response Validator
        validation = self._validator.validate(
            llm_output,
            evidence=evidence,
            knowledge=knowledge_result,
            reasoning=reasoning,
        )
        trace.append(
            {
                "stage": "response_validator",
                "passed": validation.passed,
                "confidence": validation.confidence,
                "warning_count": len(validation.warnings),
            }
        )

        # Discussion answer (same grounding contract)
        discussion = self._discussion_ai.ask(
            ask_question,
            rule_context=context,
            chart=chart,
            knowledge=knowledge_result,
            evidence=evidence,
            reasoning=reasoning,
        )

        # 8 Portal payload (additive; does not replace narrative/report)
        portal_payload = self._portal_payload(
            discussion=discussion,
            validation=validation,
            llm_output=llm_output,
            reasoning=reasoning,
            evidence=evidence,
            knowledge=knowledge_result,
        )
        trace.append({"stage": "portal", "keys": sorted(portal_payload.keys())})

        result = KnowledgePipelineResult(
            knowledge=knowledge_result,
            reasoning=reasoning,
            evidence=evidence,
            prompt=prompt,
            llm_output=llm_output,
            validation=validation,
            discussion=discussion,
            portal_payload=portal_payload,
            metadata={
                "version": PIPELINE_VERSION,
                "stages": list(PIPELINE_STAGES),
                "trace": trace,
                "question": ask_question,
            },
        )
        logger.debug(
            "Knowledge pipeline complete validation_passed=%s grounded=%s",
            validation.passed,
            discussion.grounded if discussion else False,
        )
        return result

    def _portal_payload(
        self,
        *,
        discussion: DiscussionAnswer,
        validation: ValidationReport,
        llm_output: str,
        reasoning: ReasoningGraph,
        evidence: EvidencePackage,
        knowledge: KnowledgeResult,
    ) -> dict[str, Any]:
        """Build additive portal block; never mutates narrative/report contracts."""
        return {
            "version": PIPELINE_VERSION,
            "kind": "knowledge_expert_discussion",
            "question": discussion.question,
            "question_type": discussion.question_type,
            "answer": discussion.answer if discussion.grounded else llm_output,
            "grounded": discussion.grounded and validation.checks.get(
                "missing_evidence", {}
            ).get("passed", False),
            "confidence": min(discussion.confidence, validation.confidence),
            "validation": {
                "passed": validation.passed,
                "confidence": validation.confidence,
                "warning_count": len(validation.warnings),
            },
            "summary": {
                "evidence_count": len(evidence.items),
                "knowledge_count": len(knowledge.entries),
                "reasoning_conclusions": list(reasoning.conclusions),
            },
            "citations_visible": False,
            "replaces_narrative": False,
        }
