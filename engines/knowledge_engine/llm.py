"""Deterministic LLM adapter for Knowledge Pipeline (no external dependency).

Production can swap this for a real LLM client later without changing the
pipeline contract. Default behavior composes grounded text from Evidence,
Knowledge, and Reasoning only.
"""

from __future__ import annotations

from typing import Protocol

from engines.knowledge_engine.discussion_ai import DiscussionAI
from engines.knowledge_engine.evidence_models import EvidencePackage
from engines.knowledge_engine.models import KnowledgeResult
from engines.knowledge_engine.prompt_models import StructuredPrompt
from engines.knowledge_engine.reasoning_models import ReasoningGraph


class LLMClient(Protocol):
    """Minimal LLM interface used by KnowledgePipeline."""

    def generate(
        self,
        prompt: StructuredPrompt,
        *,
        question: str,
        evidence: EvidencePackage,
        knowledge: KnowledgeResult,
        reasoning: ReasoningGraph,
    ) -> str:
        """Return model text for the given structured prompt."""


class DeterministicKnowledgeLLM:
    """Local grounded composer used until an external LLM is configured."""

    def __init__(self, discussion_ai: DiscussionAI | None = None) -> None:
        """Optionally inject DiscussionAI for answer composition."""
        self._discussion = discussion_ai or DiscussionAI()

    def generate(
        self,
        prompt: StructuredPrompt,
        *,
        question: str,
        evidence: EvidencePackage,
        knowledge: KnowledgeResult,
        reasoning: ReasoningGraph,
    ) -> str:
        """Compose a grounded reply; ignore ungrounded free-form generation."""
        _ = prompt  # Prompt is retained for future external LLM swap-in.
        answer = self._discussion.ask(
            question or "Why is this conclusion favored?",
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        if answer.refused:
            # Fall back to explicit grounded template from prompt sections.
            facts = prompt.section("facts")
            evidence_section = prompt.section("evidence")
            knowledge_section = prompt.section("knowledge")
            reasoning_section = prompt.section("reasoning")
            return (
                "[Evidence] "
                + ((evidence_section.content if evidence_section else "") or "n/a")
                + " [Knowledge] "
                + ((knowledge_section.content if knowledge_section else "") or "n/a")
                + " [Reasoning] "
                + ((reasoning_section.content if reasoning_section else "") or "n/a")
                + " "
                + ((facts.content if facts else "") or "Grounded synthesis unavailable.")
            )
        return answer.answer
