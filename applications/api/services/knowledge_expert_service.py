"""Applications-layer Knowledge Expert service (Epic 03 Milestone 10).

Additive integration:
- Does not change PUBLIC_PIPELINE_ORDER
- Does not mutate narrative/report contracts
- Exposes Discussion via dedicated API using KnowledgePipeline
"""

from __future__ import annotations

import logging
from typing import Any

from applications.api.services.orchestrator import OrchestratorService
from engines.knowledge_engine import (
    DiscussionAI,
    KnowledgePipeline,
    KnowledgePipelineResult,
    KnowledgeResult,
)

logger = logging.getLogger(__name__)


def rule_context_from_analyze_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Derive a RuleContext-like mapping from public analyze payload fields.

    Uses only public stage outputs already returned by OrchestratorService.
    Does not re-expose stripped internal ``rule_context``.
    """
    bazi = dict(data.get("bazi") or {})
    pattern = dict(data.get("pattern") or {})
    strength = dict(data.get("strength") or {})
    temperature = dict(data.get("temperature") or {})
    useful_god = dict(data.get("useful_god") or {})
    score = dict(data.get("score") or {})

    ten_gods_items: list[Any] = []
    if isinstance(bazi.get("ten_gods"), list):
        ten_gods_items = list(bazi.get("ten_gods") or [])
    else:
        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            pillar = bazi.get(key) or {}
            if isinstance(pillar, dict) and pillar.get("ten_god"):
                ten_gods_items.append(pillar.get("ten_god"))

    shensha_stars: list[Any] = []
    raw_shensha = bazi.get("shensha")
    if isinstance(raw_shensha, list):
        shensha_stars = list(raw_shensha)
    elif isinstance(raw_shensha, dict):
        stars = raw_shensha.get("stars") or raw_shensha.get("items") or []
        if isinstance(stars, list):
            shensha_stars = list(stars)

    return {
        "day_master": bazi.get("day_master"),
        "day_master_element": bazi.get("day_master_element") or bazi.get("element"),
        "bazi": bazi,
        "ten_gods": {"items": ten_gods_items, "status": "ok" if ten_gods_items else "unknown"},
        "pattern": {
            "main_pattern": pattern.get("pattern") or pattern.get("main_pattern"),
            "name": pattern.get("cach_cuc") or pattern.get("name") or pattern.get("pattern"),
            "status": "ok" if pattern else "unknown",
            "success": pattern.get("success"),
        },
        "strength": {
            "level": strength.get("level") or strength.get("strength_level"),
            "status": strength.get("status"),
        },
        "temperature": {
            "status": temperature.get("status") or temperature.get("climate"),
        },
        "useful_god": {
            "element": useful_god.get("element") or useful_god.get("useful_god"),
            "name": useful_god.get("name") or useful_god.get("useful_god"),
            "status": "ok" if useful_god else "unknown",
        },
        "shensha": {"stars": shensha_stars, "status": "ok" if shensha_stars else "unknown"},
        "wuxing": {"season": bazi.get("season") or data.get("calendar", {}).get("season")},
        "score": {
            "total_score": score.get("total_score"),
            "grade": score.get("grade"),
        },
    }


class KnowledgeExpertService:
    """Run KnowledgePipeline against orchestrated analysis outputs."""

    def __init__(
        self,
        orchestrator: OrchestratorService | None = None,
        pipeline: KnowledgePipeline | None = None,
    ) -> None:
        """Create service with optional injected orchestrator/pipeline."""
        self._orchestrator = orchestrator or OrchestratorService()
        self._pipeline = pipeline or KnowledgePipeline(discussion_ai=DiscussionAI())

    def discuss(
        self,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        gender: str | None = None,
        timezone: str = "Asia/Ho_Chi_Minh",
        question: str,
        show_citations: bool = False,
        knowledge: KnowledgeResult | None = None,
    ) -> dict[str, Any]:
        """Answer one discussion question through the Knowledge Pipeline.

        Runs analyze for chart/context derivation, then KnowledgePipeline.
        Public analyze contract remains unchanged for existing clients.
        """
        analyze_data = self._orchestrator.analyze(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=gender,
            timezone=timezone,
        )
        rule_context = rule_context_from_analyze_payload(analyze_data)
        result = self._pipeline.run(
            rule_context=rule_context,
            question=question,
            chart=analyze_data.get("bazi"),
            knowledge=knowledge,
            show_citations=show_citations,
        )
        return self._to_api_payload(result, analyze_data)

    def converse(
        self,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        gender: str | None = None,
        timezone: str = "Asia/Ho_Chi_Minh",
        questions: list[str],
        show_citations: bool = False,
        knowledge: KnowledgeResult | None = None,
    ) -> dict[str, Any]:
        """Run multi-turn discussion with shared analysis context."""
        analyze_data = self._orchestrator.analyze(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=gender,
            timezone=timezone,
        )
        rule_context = rule_context_from_analyze_payload(analyze_data)
        turns = []
        shared_result: KnowledgePipelineResult | None = None
        for question in questions:
            shared_result = self._pipeline.run(
                rule_context=rule_context,
                question=question,
                chart=analyze_data.get("bazi"),
                knowledge=knowledge,
                show_citations=show_citations,
            )
            turns.append(shared_result.portal_payload)

        return {
            "pipeline": list(analyze_data.get("pipeline") or []),
            "knowledge_expert": KnowledgePipeline.portal_status(
                corpus_ready=bool(knowledge and knowledge.entries)
            ),
            "turns": turns,
            "turn_count": len(turns),
            "all_grounded": all(bool(turn.get("grounded")) for turn in turns),
            "replaces_narrative": False,
            "metadata": shared_result.metadata if shared_result else {},
        }

    def _to_api_payload(
        self,
        result: KnowledgePipelineResult,
        analyze_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Shape Discussion API response without breaking analyze clients."""
        payload = {
            "pipeline": list(analyze_data.get("pipeline") or []),
            "knowledge_expert": result.portal_payload,
            "validation": result.validation.to_dict(),
            "discussion": result.discussion.to_dict() if result.discussion else None,
            "prompt_sections": list(result.prompt.sections.keys()),
            "summary": {
                "evidence_count": len(result.evidence.items),
                "knowledge_count": len(result.knowledge.entries),
                "reasoning_conclusions": list(result.reasoning.conclusions),
                "validation_passed": result.validation.passed,
            },
            "replaces_narrative": False,
            "metadata": result.metadata,
        }
        logger.debug(
            "Knowledge expert discussion grounded=%s validation=%s",
            (result.discussion.grounded if result.discussion else False),
            result.validation.passed,
        )
        return payload
