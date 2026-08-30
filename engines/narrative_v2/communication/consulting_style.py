"""Consulting style transforms. Surface language only."""

from __future__ import annotations

from engines.narrative_v2.communication.consulting_style_registry import (
    APPROVED_FRAMES,
    LANGUAGE_ISSUE_APPROVED,
    LANGUAGE_ISSUE_SENTENCE_GAP,
    LANGUAGE_ISSUE_SHORTHAND,
)
from engines.narrative_v2.communication.consulting_style_selector import classify_language_issue
from engines.narrative_v2.conversation.conversation_flow import meaning_hash, split_sentences
from engines.narrative_v2.conversation.conversation_transition import strip_transition

_FRAME_PREFIXES: tuple[str, ...] = tuple(
    sorted((frame.text for frame in APPROVED_FRAMES), key=len, reverse=True)
)


def semantic_fingerprint(text: str | None) -> str:
    """Digest of meaning-bearing sentences after frames/transitions are removed."""
    if not text:
        return meaning_hash("")
    cores: list[str] = []
    known: set[str] = set()
    for sentence in split_sentences(text):
        core = _core_sentence(sentence)
        if not core or core in known:
            continue
        known.add(core)
        cores.append(core)
    return meaning_hash(" ".join(cores))


_COMMA_FRAMES: frozenset[str] = frozenset(
    {
        "Trong thực tế",
        "Ở mặt tích cực",
        "Ở góc nhìn tổng thể",
        "Tuy nhiên, cũng cần lưu ý",
    }
)


def apply_consulting_style(*, frame_text: str, source_text: str) -> str:
    """Wrap approved meaning in a consulting frame. Does not add facts."""
    body = _normalize_address_case(strip_transition(source_text.strip()))
    if not body:
        return ""
    if frame_text in _COMMA_FRAMES:
        return f"{frame_text}, {body}"
    return f"{frame_text} {body}"


def _core_sentence(text: str) -> str:
    stripped = text.strip()
    for prefix in _FRAME_PREFIXES:
        if stripped.startswith(prefix):
            remainder = stripped[len(prefix) :].strip()
            if remainder.startswith(","):
                remainder = remainder[1:].strip()
            stripped = remainder
            break
    stripped = strip_transition(stripped)
    return _canonical_address(stripped).casefold()


def _normalize_address_case(text: str) -> str:
    if text.startswith("Bạn "):
        return "bạn " + text[4:]
    if text.startswith("Bạn,"):
        return "bạn," + text[4:]
    return text[:1].lower() + text[1:] if text else text


def _canonical_address(text: str) -> str:
    if text.startswith("bạn "):
        return "Bạn " + text[4:]
    return text


def segment_status_for(source_text: str) -> str:
    """styled if clean; partial if a language asset is still missing."""
    issue = classify_language_issue(source_text)
    if issue == LANGUAGE_ISSUE_APPROVED:
        return "styled"
    if issue in {LANGUAGE_ISSUE_SENTENCE_GAP, LANGUAGE_ISSUE_SHORTHAND}:
        return "partial"
    return "unresolved"
