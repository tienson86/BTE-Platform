"""WP5 — resolve conflicts among matched interpretation knowledge rules.

Operates on matched rule dicts (not Priority KB ``PR*`` meta-rules).
Does not load or mutate the Knowledge Base.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


# Lower priority numeric value loses when caps apply.
DEFAULT_MAX_RULES_PER_SECTION = 20

# Lexical opposition pairs for content conflict when polarity is neutral.
_ANTONYM_PAIRS: tuple[tuple[str, str], ...] = (
    ("manh", "yeu"),
    ("vuong", "nhuoc"),
    ("tot", "xau"),
    ("thuan", "nghich"),
    ("loi", "hai"),
    ("nong", "lanh"),
    ("hop", "xung"),
    ("dung", "ky"),
    ("huu dung", "vo dung"),
    ("tang", "giam"),
    ("positive", "negative"),
    ("thuan loi", "bat loi"),
)

_POSITIVE_MARKERS = (
    "thuan loi",
    "huu dung",
    "tot",
    "manh",
    "vuong",
    "positive",
    "favorable",
)
_NEGATIVE_MARKERS = (
    "bat loi",
    "vo dung",
    "xau",
    "yeu",
    "nhuoc",
    "negative",
    "unfavorable",
    "pha",
    "xung",
)


@dataclass(slots=True)
class DiscardedMatchedRule:
    """One matched rule removed during priority resolution."""

    rule_id: str
    reason: str
    kept_rule_id: str | None = None
    detail: str = ""
    section: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize for InterpretationResult / API payloads."""
        return {
            "rule_id": self.rule_id,
            "reason": self.reason,
            "kept_rule_id": self.kept_rule_id,
            "detail": self.detail,
            "section": self.section,
        }


@dataclass(slots=True)
class MatchedRuleResolution:
    """Matched → Resolved → Discarded with reasons (WP5 output)."""

    matched_rules: tuple[dict[str, Any], ...]
    resolved_rules: tuple[dict[str, Any], ...]
    discarded_rules: tuple[DiscardedMatchedRule, ...] = field(default_factory=tuple)

    @property
    def ordered_rule_ids(self) -> tuple[str, ...]:
        """Resolved rule IDs in priority order."""
        return tuple(
            str(rule.get("rule_id", ""))
            for rule in self.resolved_rules
            if rule.get("rule_id") is not None
        )

    @property
    def matched_rule_ids(self) -> tuple[str, ...]:
        """Original matched rule IDs."""
        return tuple(
            str(rule.get("rule_id", ""))
            for rule in self.matched_rules
            if rule.get("rule_id") is not None
        )

    def to_dict(self) -> dict[str, Any]:
        """Compact report for each case."""
        return {
            "matched_rules": list(self.matched_rule_ids),
            "resolved_rules": list(self.ordered_rule_ids),
            "discarded_rules": [item.to_dict() for item in self.discarded_rules],
            "matched_count": len(self.matched_rules),
            "resolved_count": len(self.resolved_rules),
            "discarded_count": len(self.discarded_rules),
            "discard_reasons": dict(Counter(item.reason for item in self.discarded_rules)),
        }


class MatchedRuleResolver:
    """Resolve duplicate, conflict, covered, and diversity among matched rules."""

    REASON_PRIORITY = "priority"
    REASON_CONFLICT = "conflict"
    REASON_DUPLICATE = "duplicate"
    REASON_COVERED = "covered"

    def __init__(
        self,
        *,
        max_rules_per_section: int = DEFAULT_MAX_RULES_PER_SECTION,
    ) -> None:
        """
        Parameters
        ----------
        max_rules_per_section:
            Soft diversity cap — lower-priority extras discarded as ``priority``.
        """
        self.max_rules_per_section = max(1, int(max_rules_per_section))

    def resolve(
        self,
        matched_rules: Sequence[Mapping[str, Any]],
    ) -> MatchedRuleResolution:
        """
        Keep higher-priority rules; drop duplicates, conflicts, and subsumed rules.

        Section diversity:
        1. Seed one highest-priority survivor per section.
        2. Fill remaining slots by priority with a per-section cap.
        """
        matched = [dict(rule) for rule in matched_rules]
        ordered = sorted(matched, key=self._sort_key, reverse=True)

        accepted: list[dict[str, Any]] = []
        discarded: list[DiscardedMatchedRule] = []
        section_counts: Counter[str] = Counter()
        seen_ids: set[str] = set()
        seeded_sections: set[str] = set()

        # Phase 1 — diversity seed (one rule per section)
        for candidate in ordered:
            section = self._section(candidate)
            if section in seeded_sections:
                continue
            if not self._try_accept(
                candidate,
                accepted,
                discarded,
                section_counts,
                seen_ids,
                enforce_cap=False,
            ):
                continue
            seeded_sections.add(section)

        # Phase 2 — fill by priority with section cap
        for candidate in ordered:
            rule_id = self._rule_id(candidate)
            if rule_id and rule_id in seen_ids:
                continue
            # Already accepted in phase 1 (same object identity may differ — use id)
            if rule_id and any(self._rule_id(item) == rule_id for item in accepted):
                continue
            if not rule_id and any(
                self._content_key(item) == self._content_key(candidate)
                for item in accepted
            ):
                continue
            self._try_accept(
                candidate,
                accepted,
                discarded,
                section_counts,
                seen_ids,
                enforce_cap=True,
            )

        # Re-order resolved by priority for stable builder input
        accepted.sort(key=self._sort_key, reverse=True)

        return MatchedRuleResolution(
            matched_rules=tuple(matched),
            resolved_rules=tuple(accepted),
            discarded_rules=tuple(discarded),
        )

    def _try_accept(
        self,
        candidate: Mapping[str, Any],
        accepted: list[dict[str, Any]],
        discarded: list[DiscardedMatchedRule],
        section_counts: Counter[str],
        seen_ids: set[str],
        *,
        enforce_cap: bool,
    ) -> bool:
        """Attempt to accept a candidate; append discard reason on failure."""
        rule_id = self._rule_id(candidate)
        section = self._section(candidate)
        content = self._content_key(candidate)
        candidate_dict = dict(candidate)

        if rule_id and rule_id in seen_ids:
            discarded.append(
                DiscardedMatchedRule(
                    rule_id=rule_id,
                    reason=self.REASON_DUPLICATE,
                    kept_rule_id=rule_id,
                    detail="Duplicate rule_id already resolved.",
                    section=section,
                )
            )
            return False

        drop = self._find_drop_reason(candidate_dict, accepted)
        if drop is not None:
            discarded.append(drop)
            return False

        if enforce_cap and section_counts[section] >= self.max_rules_per_section:
            kept = self._best_in_section(accepted, section)
            discarded.append(
                DiscardedMatchedRule(
                    rule_id=rule_id or content[:40],
                    reason=self.REASON_PRIORITY,
                    kept_rule_id=self._rule_id(kept) if kept else None,
                    detail=(
                        f"Section '{section}' diversity cap "
                        f"({self.max_rules_per_section})."
                    ),
                    section=section,
                )
            )
            return False

        accepted.append(candidate_dict)
        section_counts[section] += 1
        if rule_id:
            seen_ids.add(rule_id)
        return True

    def _find_drop_reason(
        self,
        candidate: Mapping[str, Any],
        accepted: Sequence[Mapping[str, Any]],
    ) -> DiscardedMatchedRule | None:
        """Return discard record if candidate loses to an already-kept rule."""
        cand_id = self._rule_id(candidate)
        cand_section = self._section(candidate)
        cand_content = self._content_key(candidate)

        for kept in accepted:
            kept_id = self._rule_id(kept)
            kept_content = self._content_key(kept)
            kept_section = self._section(kept)

            if cand_content and cand_content == kept_content:
                return DiscardedMatchedRule(
                    rule_id=cand_id or cand_content[:40],
                    reason=self.REASON_DUPLICATE,
                    kept_rule_id=kept_id or None,
                    detail="Identical content as higher-priority rule.",
                    section=cand_section,
                )

            if self._is_covered(cand_content, kept_content):
                return DiscardedMatchedRule(
                    rule_id=cand_id or cand_content[:40],
                    reason=self.REASON_COVERED,
                    kept_rule_id=kept_id or None,
                    detail="Content subsumed by higher-priority rule.",
                    section=cand_section,
                )

            if cand_section == kept_section and self._is_conflict(candidate, kept):
                return DiscardedMatchedRule(
                    rule_id=cand_id or cand_content[:40],
                    reason=self.REASON_CONFLICT,
                    kept_rule_id=kept_id or None,
                    detail=f"Contradicts higher-priority rule in section '{cand_section}'.",
                    section=cand_section,
                )

        return None

    @staticmethod
    def _is_covered(candidate_content: str, kept_content: str) -> bool:
        """True when one non-trivial text subsumes the other."""
        if not candidate_content or not kept_content:
            return False
        if candidate_content == kept_content:
            return False
        # Require meaningful length so short tokens do not falsely cover.
        if len(candidate_content) < 12 or len(kept_content) < 12:
            return False
        return (
            candidate_content in kept_content
            or kept_content in candidate_content
        )

    def _is_conflict(
        self,
        left: Mapping[str, Any],
        right: Mapping[str, Any],
    ) -> bool:
        """Detect polarity or lexical contradiction within one section."""
        left_pol = self._effective_polarity(left)
        right_pol = self._effective_polarity(right)
        if {left_pol, right_pol} == {"positive", "negative"}:
            return True
        if {left_pol, right_pol} == {"warning", "positive"}:
            # Soft: warning vs strong positive in same section → conflict
            return True

        left_text = self._content_key(left)
        right_text = self._content_key(right)
        return self._has_antonym_clash(left_text, right_text)

    def _effective_polarity(self, rule: Mapping[str, Any]) -> str:
        """Normalize polarity; infer from text/tags when stored as neutral."""
        raw = str(rule.get("polarity") or "neutral").strip().lower()
        if raw in {"positive", "pos", "+"}:
            return "positive"
        if raw in {"negative", "neg", "-"}:
            return "negative"
        if raw in {"warning", "warn"}:
            return "warning"

        text = self._content_key(rule)
        tags = " ".join(str(t) for t in (rule.get("tags") or []))
        blob = self._normalize_text(f"{text} {tags}")
        has_pos = any(marker in blob for marker in _POSITIVE_MARKERS)
        has_neg = any(marker in blob for marker in _NEGATIVE_MARKERS)
        if has_pos and not has_neg:
            return "positive"
        if has_neg and not has_pos:
            return "negative"
        return "neutral"

    @staticmethod
    def _has_antonym_clash(left: str, right: str) -> bool:
        """True when each side carries opposite markers from a known pair."""
        if not left or not right:
            return False
        for a, b in _ANTONYM_PAIRS:
            left_has_a = a in left
            left_has_b = b in left
            right_has_a = a in right
            right_has_b = b in right
            if (left_has_a and right_has_b) or (left_has_b and right_has_a):
                # Avoid clash when both sides mention both poles (balanced text).
                if (left_has_a and left_has_b) or (right_has_a and right_has_b):
                    continue
                return True
        return False

    @staticmethod
    def _best_in_section(
        rules: Sequence[Mapping[str, Any]],
        section: str,
    ) -> Mapping[str, Any] | None:
        for rule in rules:
            if MatchedRuleResolver._section(rule) == section:
                return rule
        return None

    @staticmethod
    def _sort_key(rule: Mapping[str, Any]) -> tuple[float, float, str]:
        try:
            priority = float(rule.get("priority", 0) or 0)
        except (TypeError, ValueError):
            priority = 0.0
        try:
            confidence = float(
                rule.get(
                    "confidence",
                    rule.get("final_score", rule.get("score", 0)),
                )
                or 0
            )
        except (TypeError, ValueError):
            confidence = 0.0
        rule_id = str(rule.get("rule_id") or "")
        return (priority, confidence, rule_id)

    @staticmethod
    def _rule_id(rule: Mapping[str, Any]) -> str:
        value = rule.get("rule_id")
        return "" if value is None else str(value)

    @staticmethod
    def _section(rule: Mapping[str, Any]) -> str:
        return str(rule.get("section") or "summary")

    @classmethod
    def _content_key(cls, rule: Mapping[str, Any]) -> str:
        text = (
            rule.get("sentence")
            or rule.get("description")
            or rule.get("message")
            or rule.get("rule_name")
            or ""
        )
        return cls._normalize_text(str(text))

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Fold accents and whitespace for duplicate / cover comparison."""
        decomposed = unicodedata.normalize("NFD", text.strip().lower())
        without_marks = "".join(
            ch for ch in decomposed if unicodedata.category(ch) != "Mn"
        )
        collapsed = re.sub(r"\s+", " ", without_marks)
        return collapsed.strip()
