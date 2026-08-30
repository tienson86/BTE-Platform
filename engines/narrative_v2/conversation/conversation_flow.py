"""Sentence split/join and meaning digest. No new wording."""

from __future__ import annotations

import hashlib

from engines.narrative_v2.conversation.conversation_transition import strip_transition

PERMITTED_JOIN = " "


def split_sentences(text: str) -> tuple[str, ...]:
    """Split text into sentence units. No new wording."""
    parts: list[str] = []
    current: list[str] = []
    for char in text.strip():
        current.append(char)
        if char in ".!?":
            sentence = "".join(current).strip()
            if sentence:
                parts.append(sentence)
            current = []
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return tuple(parts)


def join_sentences(sentences: tuple[str, ...]) -> str:
    """Join already-complete sentences."""
    cleaned = tuple(part.strip() for part in sentences if part.strip())
    return PERMITTED_JOIN.join(cleaned)


def meaning_hash(text: str | None) -> str:
    """Stable digest of meaning text. Empty text hashes as empty."""
    payload = text or ""
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sentence_set_hash(texts: tuple[str | None, ...]) -> str:
    """Digest of unique sentences in first-seen order."""
    seen: list[str] = []
    known: set[str] = set()
    for text in texts:
        if not text:
            continue
        for sentence in split_sentences(text):
            clean = strip_transition(sentence)
            if not clean or clean in known:
                continue
            known.add(clean)
            seen.append(clean)
    return meaning_hash(join_sentences(tuple(seen)))
