"""Extract keywords and repeated topics from Interpretation content."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict
from typing import Any

_TOKEN_RE = re.compile(r"[a-zA-ZÀ-ỹ0-9_]+", re.UNICODE)

_STOPWORDS = frozenset(
    {
        "va",
        "và",
        "cua",
        "của",
        "cac",
        "các",
        "mot",
        "một",
        "nhung",
        "những",
        "la",
        "là",
        "cho",
        "voi",
        "với",
        "trong",
        "khi",
        "neu",
        "nếu",
        "the",
        "and",
        "or",
        "to",
        "of",
        "a",
        "an",
        "in",
        "on",
        "for",
        "from",
        "this",
        "that",
        "co",
        "có",
        "khong",
        "không",
        "duoc",
        "được",
        "se",
        "sẽ",
        "thi",
        "thì",
        "nhu",
        "như",
        "de",
        "để",
        "tai",
        "tại",
        "section",
        "rule",
        "tieu",
        "tiêu",
        "de",
    }
)


class KeywordExtractor:
    """Extract keywords and cross-section repeated topics."""

    def __init__(self, *, min_token_length: int = 3, top_k: int = 30) -> None:
        self.min_token_length = min_token_length
        self.top_k = top_k

    def extract(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Return keywords and repeated_topics lists."""
        grouped = analysis.get("grouped_rules") or {}
        global_counts: Counter[str] = Counter()
        section_tokens: dict[str, Counter[str]] = {}

        for section, rules in grouped.items():
            local: Counter[str] = Counter()
            for rule in rules:
                text = " ".join(
                    str(rule.get(key) or "")
                    for key in ("sentence", "description", "message", "rule_name", "rule_id")
                )
                for token in self._tokenize(text):
                    local[token] += 1
                    global_counts[token] += 1
            # Include summary once under summary section
            section_tokens[section] = local

        summary = str(analysis.get("summary") or "")
        for token in self._tokenize(summary):
            global_counts[token] += 1
            section_tokens.setdefault("summary", Counter())[token] += 1

        keywords = [
            {"keyword": token, "count": count}
            for token, count in global_counts.most_common(self.top_k)
        ]

        topic_sections: dict[str, set[str]] = defaultdict(set)
        for section, counter in section_tokens.items():
            for token, count in counter.items():
                if count <= 0:
                    continue
                topic_sections[token].add(section)

        repeated = []
        for token, sections in topic_sections.items():
            if len(sections) < 2:
                continue
            repeated.append(
                {
                    "topic": token,
                    "sections": sorted(sections),
                    "section_count": len(sections),
                    "total_count": int(global_counts.get(token, 0)),
                }
            )
        repeated.sort(
            key=lambda item: (item["section_count"], item["total_count"]),
            reverse=True,
        )
        return {
            "keywords": keywords,
            "repeated_topics": repeated[: self.top_k],
        }

    def _tokenize(self, text: str) -> list[str]:
        folded = self._fold(text)
        tokens: list[str] = []
        for match in _TOKEN_RE.findall(folded):
            token = match.lower()
            if len(token) < self.min_token_length:
                continue
            if token in _STOPWORDS:
                continue
            if token.isdigit():
                continue
            tokens.append(token)
        return tokens

    @staticmethod
    def _fold(text: str) -> str:
        decomposed = unicodedata.normalize("NFD", text)
        return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
