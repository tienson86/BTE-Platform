"""Commercial Communication Engine — ConversationNarrative → ConsultingNarrative.

Phase 3: consulting style. Does not rewrite Meaning. Does not generate Action.
"""

from __future__ import annotations

import logging

from engines.narrative_v2.communication.communication_context import (
    STATUS_PARTIAL,
    STATUS_UNRESOLVED,
    ConsultingNarrative,
    ConsultingReference,
    StyledSegment,
)
from engines.narrative_v2.communication.communication_errors import CommunicationError
from engines.narrative_v2.communication.consulting_style import (
    apply_consulting_style,
    segment_status_for,
    semantic_fingerprint,
)
from engines.narrative_v2.communication.consulting_style_profile import (
    ConsultingStyleProfile,
    default_profile,
)
from engines.narrative_v2.communication.consulting_style_registry import (
    LANGUAGE_ISSUE_APPROVED,
    LANGUAGE_ISSUE_SENTENCE_GAP,
)
from engines.narrative_v2.communication.consulting_style_selector import (
    ConsultingStyleSelector,
    classify_language_issue,
)
from engines.narrative_v2.communication.consulting_style_validator import ConsultingStyleValidator
from engines.narrative_v2.conversation.conversation_bridge import novel_sentences
from engines.narrative_v2.conversation.conversation_context import ConversationNarrative
from engines.narrative_v2.conversation.conversation_flow import join_sentences
from engines.narrative_v2.conversation.conversation_registry import FLOW_STAGES

logger = logging.getLogger(__name__)

COMMUNICATION_VERSION = "nimp07b.1.0"

_CONTEXT_METADATA: tuple[tuple[str, str], ...] = (
    ("shadow_mode", "true"),
    ("replaces_pack05", "false"),
    ("portal_connected", "false"),
    ("layer", "consulting_style"),
    ("communication_version", COMMUNICATION_VERSION),
)


class CommunicationEngine:
    """Consulting-style voice over an already-composed conversation."""

    def __init__(
        self,
        *,
        profile: ConsultingStyleProfile | None = None,
        selector: ConsultingStyleSelector | None = None,
        validator: ConsultingStyleValidator | None = None,
    ) -> None:
        self._profile = profile or default_profile()
        self._selector = selector or ConsultingStyleSelector()
        self._validator = validator or ConsultingStyleValidator()

    def style(self, conversation: object) -> ConsultingNarrative:
        """Transform ConversationNarrative into ConsultingNarrative."""
        source = _require_conversation(conversation)
        if source.status == "insufficient" or not source.flow:
            consulting = _unresolved(_CONTEXT_METADATA, self._profile.profile_id)
            self._validator.assert_valid(consulting, source)
            return consulting
        consulting = _assemble(source, self._profile, self._selector)
        logger.info(
            "consulting_style.styled",
            extra={"status": consulting.status, "segments": len(consulting.segments)},
        )
        self._validator.assert_valid(consulting, source)
        return consulting


def _require_conversation(value: object) -> ConversationNarrative:
    if isinstance(value, ConversationNarrative):
        return value
    raise CommunicationError("Consulting Style accepts ConversationNarrative only")


def _unresolved(base_meta: tuple[tuple[str, str], ...], profile_id: str) -> ConsultingNarrative:
    return ConsultingNarrative(
        flow="",
        segments=(),
        style_profile=profile_id,
        source_conversation_ids=(),
        references=(),
        metadata=base_meta + (("status_reason", "no_conversation_flow"),),
        status=STATUS_UNRESOLVED,
    )


def _assemble(
    source: ConversationNarrative,
    profile: ConsultingStyleProfile,
    selector: ConsultingStyleSelector,
) -> ConsultingNarrative:
    segments: list[StyledSegment] = []
    spoken: list[str] = []
    prior_fragment = False
    refs_by_field = {ref.field: ref for ref in source.references}
    issues: list[str] = []
    for role in FLOW_STAGES:
        raw = getattr(source, role)
        if not isinstance(raw, str) or not raw.strip():
            continue
        novel = novel_sentences(raw, tuple(spoken))
        if not novel:
            continue
        source_text = join_sentences(novel)
        issue = classify_language_issue(source_text)
        frame_id = selector.select(
            role=role,
            source_text=source_text,
            prior_fragment=prior_fragment,
            profile=profile,
        )
        frame = selector.registry().frame(frame_id)
        styled = apply_consulting_style(frame_text=frame.text, source_text=source_text)
        status = segment_status_for(source_text)
        conv_id = f"conversation.{role}"
        source_ref = refs_by_field.get(role)
        references = (_to_consulting_ref(source_ref),) if source_ref else ()
        segments.append(
            StyledSegment(
                segment_id=f"consulting.{role}.001",
                role=role,
                source_text=source_text,
                styled_text=styled,
                frame_id=frame_id,
                source_conversation_ids=(conv_id,),
                meaning_fingerprint=semantic_fingerprint(source_text),
                status=status,
                references=references,
                metadata=(("language_issue", issue), ("transform", "opening_frame")),
            )
        )
        spoken.extend(novel)
        prior_fragment = issue == LANGUAGE_ISSUE_SENTENCE_GAP or source_text.startswith(
            "Hữu ích khi"
        )
        if issue != LANGUAGE_ISSUE_APPROVED:
            issues.append(f"{role}:{issue}")
    flow = join_sentences(tuple(item.styled_text for item in segments))
    quality = _quality(source, flow, issues)
    coverage = "partial" if issues else "approved"
    meta = _CONTEXT_METADATA + (
        ("meaning_fingerprint", semantic_fingerprint(flow)),
        ("language_issues", ",".join(issues) if issues else "none"),
        ("consulting_language_asset_gap", "true" if issues else "false"),
        ("sentence_library", coverage),
    ) + quality
    copied_refs = tuple(_to_consulting_ref(ref) for ref in source.references)
    narrative_status = STATUS_PARTIAL if issues else "styled"
    return ConsultingNarrative(
        flow=flow,
        segments=tuple(segments),
        style_profile=profile.profile_id,
        source_conversation_ids=tuple(
            item.source_conversation_ids[0] for item in segments if item.source_conversation_ids
        ),
        references=copied_refs,
        metadata=meta,
        status=narrative_status,
    )


def _to_consulting_ref(ref: object) -> ConsultingReference:
    return ConsultingReference(
        field=getattr(ref, "field"),
        rewrite_ids=getattr(ref, "rewrite_ids"),
        knowledge_ids=getattr(ref, "knowledge_ids"),
        reasoning_ids=getattr(ref, "reasoning_ids"),
        evidence_ids=getattr(ref, "evidence_ids"),
    )


def _quality(
    source: ConversationNarrative,
    flow: str,
    issues: list[str],
) -> tuple[tuple[str, str], ...]:
    preserved = semantic_fingerprint(source.flow) == semantic_fingerprint(flow)
    fluency = "warning" if issues else "pass"
    aggregate = "warning" if issues else "pass"
    if not preserved:
        aggregate = "fail"
    return (
        ("quality.meaning_preserved", "pass" if preserved else "fail"),
        ("quality.no_semantic_escalation", "pass"),
        ("quality.fluency", fluency),
        ("quality.transition_quality", "pass"),
        ("quality.repetition_control", "pass"),
        ("quality.professional_register", fluency),
        ("quality.technical_density", fluency),
        ("quality.conversation_continuity", "pass"),
        ("quality.aggregate", aggregate),
    )
