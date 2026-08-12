"""Select customer-facing interpretation sentences; drop Rule Engine instructions."""

from __future__ import annotations

import re
import unicodedata

from engines.report_engine.localization.display import localize_tokens

_RULE_PREFIXES: tuple[str, ...] = (
    "áp dụng",
    "ưu tiên",
    "nếu ",
    "nếu chưa",
    "nếu có",
    "kiểm tra",
    "kích hoạt",
    "tháng âm lịch chỉ",
)

_ASCII_RULE_HINTS: tuple[str, ...] = (
    "cach cuc",
    "dung than",
    "hien tai",
    "kich hoat",
    "ngu hanh",
    "than can bang",
    "sinh tro",
)

_VIETNAMESE_CHARS = re.compile(
    r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
    re.IGNORECASE,
)


def is_rule_engine_sentence(sentence: str) -> bool:
    """True when the sentence is instructional Rule Engine text, not a conclusion."""
    text = sentence.strip()
    if not text:
        return True
    lowered = text.lower()
    if any(lowered.startswith(prefix) for prefix in _RULE_PREFIXES):
        return True
    ascii_form = unicodedata.normalize("NFKD", lowered)
    ascii_form = "".join(ch for ch in ascii_form if not unicodedata.combining(ch))
    if not _VIETNAMESE_CHARS.search(lowered) and any(
        hint in ascii_form for hint in _ASCII_RULE_HINTS
    ):
        return True
    return False


def customer_paragraphs(text: str) -> list[str]:
    """Keep conclusion sentences only; localize leftover internal tokens."""
    if not text or not text.strip():
        return []
    kept: list[str] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        sentences = _split_sentences(block)
        selected = [
            localize_tokens(sentence.strip())
            for sentence in sentences
            if sentence.strip() and not is_rule_engine_sentence(sentence)
        ]
        if selected:
            kept.append(" ".join(selected))
    return kept


def customer_text(text: str) -> str:
    """Join filtered customer paragraphs with blank lines."""
    return "\n\n".join(customer_paragraphs(text))


def _split_sentences(block: str) -> list[str]:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if len(lines) > 1:
        return lines
    return [block.strip()]
