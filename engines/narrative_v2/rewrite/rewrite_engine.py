"""Commercial Rewrite Engine — KnowledgeContext → CommercialRewriteContext.

Transforms approved meaning into customer-language units. Does not invent meaning.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Mapping

from engines.narrative_v2.knowledge.knowledge_context import (
    KnowledgeUnresolved,
    NarrativeKnowledgeContext,
)
from engines.narrative_v2.knowledge.knowledge_item import KnowledgeItem
from engines.narrative_v2.knowledge.knowledge_status import STATUS_APPROVED
from engines.narrative_v2.language.language_asset_status import SENTENCE_LIBRARY_VERSION
from engines.narrative_v2.rewrite.language_profile import LanguageProfile
from engines.narrative_v2.rewrite.rewrite_context import (
    CommercialRewriteContext,
    RewriteContractGap,
    RewriteUnresolved,
)
from engines.narrative_v2.rewrite.rewrite_errors import RewriteError
from engines.narrative_v2.rewrite.rewrite_item import RewriteItem, RewriteReference
from engines.narrative_v2.rewrite.rewrite_registry import RewriteRegistry
from engines.narrative_v2.rewrite.rewrite_selector import RewriteSelector
from engines.narrative_v2.rewrite.rewrite_strategy import (
    CUSTOMER_ADDRESS,
    ENGINE_LEAK,
    FEAR_LANGUAGE,
    FORBIDDEN_ADDRESS,
    FORTUNE_ABSOLUTES,
    REASON_KNOWLEDGE_UNRESOLVED,
    REASON_NO_CUSTOMER_MEANING,
    REASON_UNSAFE_SOURCE,
    REWRITE_VERSION,
    STATUS_PASSTHROUGH,
    STATUS_REWRITTEN,
)
from engines.narrative_v2.rewrite.rewrite_validator import RewriteValidator
from engines.narrative_v2.rewrite.sentence_selector import SentenceSelector

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[3]

_SOURCE_LIBRARY = "sentence_library"
_SOURCE_WRAP = "address_wrap"
_COVERAGE_APPROVED = "approved"
_COVERAGE_PARTIAL = "partial"
_COVERAGE_GAP = "runtime_gap"

_SOURCE_CACHE: dict[str, Mapping[str, Any] | None] = {}


class RewriteEngine:
    """Unit-level commercial rewrite. Shadow mode. No full Narrative."""

    def __init__(
        self,
        *,
        profile: LanguageProfile | None = None,
        selector: RewriteSelector | None = None,
        sentences: SentenceSelector | None = None,
        registry: RewriteRegistry | None = None,
        validator: RewriteValidator | None = None,
    ) -> None:
        self._profile = profile or LanguageProfile()
        self._selector = selector or RewriteSelector()
        self._sentences = sentences or SentenceSelector()
        self._registry = registry or RewriteRegistry()
        self._validator = validator or RewriteValidator()

    def rewrite(
        self,
        knowledge_context: object,
        reasoning_context: object | None = None,
        evidence_context: object | None = None,
    ) -> CommercialRewriteContext:
        """Rewrite approved knowledge units into customer language."""
        del reasoning_context, evidence_context
        knowledge = _require_knowledge(knowledge_context)
        items: list[RewriteItem] = []
        unresolved: list[RewriteUnresolved] = []
        gaps = [
            RewriteContractGap(
                field="grammar_assembly",
                reason="REWRITE CONTRACT GAP: paragraph grammar is out of N-IMP-05 scope",
            ),
            RewriteContractGap(
                field="template_assembly",
                reason="REWRITE CONTRACT GAP: template composition is out of N-IMP-05 scope",
            ),
        ]
        for knowledge_item in knowledge.items:
            rewritten = self._rewrite_item(knowledge_item)
            if rewritten is None:
                unresolved.append(
                    RewriteUnresolved(
                        semantic_key=knowledge_item.semantic_key,
                        reason=_unresolved_reason(knowledge_item),
                        knowledge_ids=(knowledge_item.knowledge_id,),
                        source_meaning=knowledge_item.technical_meaning,
                    )
                )
            else:
                items.append(rewritten)
        for entry in knowledge.unresolved:
            unresolved.append(_from_knowledge_gap(entry))
        ordered = tuple(sorted(items, key=lambda item: item.rewrite_id))
        ordered_unresolved = tuple(
            sorted(unresolved, key=lambda entry: (entry.semantic_key, entry.reason))
        )
        coverage = _library_coverage(ordered)
        gaps.extend(_library_gaps(coverage))
        context = CommercialRewriteContext(
            items=ordered,
            unresolved=ordered_unresolved,
            references=tuple(item.references[0] for item in ordered if item.references),
            metadata=_context_metadata(coverage),
            status=_context_status(ordered, ordered_unresolved),
            contract_gaps=tuple(gaps),
        )
        self._validator.assert_valid(context, knowledge)
        return context

    def _rewrite_item(self, knowledge_item: KnowledgeItem) -> RewriteItem | None:
        source = _select_source_meaning(knowledge_item)
        if source is None:
            return None
        if not _is_customer_safe(source):
            return None
        asset = self._sentences.select(
            knowledge_item.semantic_key,
            profile=self._profile,
            category="meaning",
            domain=knowledge_item.domain,
            meaning_key=knowledge_item.knowledge_id,
        )
        strategy = self._selector.select(source_meaning=source, profile=self._profile)
        if not self._registry.contains(strategy):
            return None
        if asset is not None:
            customer = asset.text.strip()
            status = STATUS_REWRITTEN
            extra = (
                ("sentence_source", _SOURCE_LIBRARY),
                ("sentence_id", asset.sentence_id),
            )
        else:
            customer, status = _to_customer_language(source, self._profile.address)
            extra = (("sentence_source", _SOURCE_WRAP),)
        terminology = _terminology(knowledge_item, extra)
        ref = knowledge_item.references[0] if knowledge_item.references else None
        reasoning_ids = ref.reasoning_ids if ref is not None else ()
        evidence_ids = ref.evidence_ids if ref is not None else ()
        rewrite_id = _rewrite_id(knowledge_item)
        return RewriteItem(
            rewrite_id=rewrite_id,
            semantic_key=knowledge_item.semantic_key,
            domain=knowledge_item.domain,
            source_knowledge_ids=(knowledge_item.knowledge_id,),
            source_reasoning_ids=reasoning_ids,
            source_evidence_ids=evidence_ids,
            source_meaning=source,
            normalized_meaning=customer,
            customer_language=customer,
            strategy=strategy,
            style=self._profile.style,
            status=status,
            references=(
                RewriteReference(
                    knowledge_id=knowledge_item.knowledge_id,
                    source_path=knowledge_item.source_path,
                    reasoning_ids=reasoning_ids,
                    evidence_ids=evidence_ids,
                ),
            ),
            metadata=terminology,
        )


def _require_knowledge(value: object) -> NarrativeKnowledgeContext:
    if isinstance(value, NarrativeKnowledgeContext):
        return value
    raise RewriteError("Rewrite Engine accepts NarrativeKnowledgeContext only")


def _select_source_meaning(item: KnowledgeItem) -> str | None:
    candidate = (item.customer_meaning_candidate or "").strip()
    if candidate:
        return candidate
    positive = _load_positive_meaning(item.source_path)
    if positive:
        return positive
    technical = (item.technical_meaning or "").strip()
    if technical and _is_customer_safe(technical):
        return technical
    return None


def _load_positive_meaning(source_path: str) -> str | None:
    if not source_path:
        return None
    if source_path in _SOURCE_CACHE:
        payload = _SOURCE_CACHE[source_path]
    else:
        payload = _read_source(source_path)
        _SOURCE_CACHE[source_path] = payload
    if payload is None:
        return None
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    if metadata.get("status") != STATUS_APPROVED:
        return None
    text = payload.get("positive_meaning")
    if isinstance(text, str) and text.strip():
        return text.strip()
    return None


def _read_source(source_path: str) -> Mapping[str, Any] | None:
    path = Path(source_path)
    if not path.is_absolute():
        path = _REPO_ROOT / source_path
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.debug("Rewrite source unreadable: %s", source_path)
        return None
    if isinstance(raw, Mapping):
        return raw
    return None


def _is_customer_safe(text: str) -> bool:
    for token in ENGINE_LEAK + FORBIDDEN_ADDRESS + FORTUNE_ABSOLUTES + FEAR_LANGUAGE:
        if token in text:
            return False
    return True


def _to_customer_language(source: str, address: str) -> tuple[str, str]:
    text = source.strip()
    if not text.endswith("."):
        text = text + "."
    if text.startswith(address):
        return text, STATUS_PASSTHROUGH
    body = text
    if body[:1].isupper():
        body = body[:1].lower() + body[1:]
    return f"{address} {body}", STATUS_REWRITTEN


def _terminology(
    item: KnowledgeItem,
    extra: tuple[tuple[str, str], ...],
) -> tuple[tuple[str, str], ...]:
    slug = item.knowledge_id.rsplit(".", 1)[-1]
    return (("terminology", slug), ("knowledge_id", item.knowledge_id)) + extra


def _library_coverage(items: tuple[RewriteItem, ...]) -> str:
    if not items:
        return _COVERAGE_GAP
    library_hits = sum(
        1 for item in items if dict(item.metadata).get("sentence_source") == _SOURCE_LIBRARY
    )
    if library_hits == 0:
        return _COVERAGE_GAP
    if library_hits == len(items):
        return _COVERAGE_APPROVED
    return _COVERAGE_PARTIAL


def _library_gaps(coverage: str) -> list[RewriteContractGap]:
    if coverage == _COVERAGE_APPROVED:
        return []
    if coverage == _COVERAGE_PARTIAL:
        return [
            RewriteContractGap(
                field="sentence_library",
                reason="SENTENCE LIBRARY PARTIAL: remaining rewritten units still use address wrap",
            )
        ]
    return [
        RewriteContractGap(
            field="sentence_library",
            reason="SENTENCE LIBRARY RUNTIME GAP: no approved runtime sentence library keyed to Narrative V2 semantic_key",
        )
    ]


def _context_metadata(coverage: str) -> tuple[tuple[str, str], ...]:
    return (
        ("shadow_mode", "true"),
        ("replaces_pack05", "false"),
        ("portal_connected", "false"),
        ("layer", "rewrite"),
        ("rewrite_version", REWRITE_VERSION),
        ("sentence_library", coverage),
        ("sentence_library_version", SENTENCE_LIBRARY_VERSION),
    )


def _rewrite_id(item: KnowledgeItem) -> str:
    slug = item.knowledge_id.removeprefix("knowledge.")
    return f"rewrite.{slug}.001"


def _unresolved_reason(item: KnowledgeItem) -> str:
    if item.customer_meaning_candidate:
        return REASON_UNSAFE_SOURCE
    if _load_positive_meaning(item.source_path):
        return REASON_UNSAFE_SOURCE
    return REASON_NO_CUSTOMER_MEANING


def _from_knowledge_gap(entry: KnowledgeUnresolved) -> RewriteUnresolved:
    return RewriteUnresolved(
        semantic_key=entry.semantic_key,
        reason=REASON_KNOWLEDGE_UNRESOLVED,
        knowledge_ids=(),
        source_meaning=None,
    )


def _context_status(
    items: tuple[RewriteItem, ...],
    unresolved: tuple[RewriteUnresolved, ...],
) -> str:
    if items and unresolved:
        return "partial"
    if items:
        return "rewritten"
    return "unresolved"
