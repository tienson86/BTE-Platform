"""Knowledge Retriever — RuleContext → relevant knowledge entries."""

from __future__ import annotations

import logging
import re
from typing import Any, Mapping

from engines.knowledge_engine.models import (
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
    RetrievalTraceEntry,
)
from engines.knowledge_engine.repository import KnowledgeRepository
from engines.rule_contract.models import normalize_context, resolve_path

logger = logging.getLogger(__name__)

_CONDITION_SPLIT = re.compile(r"\s*;\s*")
_CONDITION_EQ = re.compile(
    r"^\s*(?P<field>[A-Za-z_][\w.]*)\s*(?:=|:|eq)\s*(?P<value>.+?)\s*$",
    re.IGNORECASE,
)
_CONDITION_IN = re.compile(
    r"^\s*(?P<field>[A-Za-z_][\w.]*)\s+in\s+(?P<value>.+?)\s*$",
    re.IGNORECASE,
)
_CONDITION_EXISTS = re.compile(
    r"^\s*(?P<field>[A-Za-z_][\w.]*)\s+exists\s*$",
    re.IGNORECASE,
)
_CONDITION_CONTAINS = re.compile(
    r"^\s*(?P<field>[A-Za-z_][\w.]*)\s+contains\s+(?P<value>.+?)\s*$",
    re.IGNORECASE,
)

# Weighting for relevance (must stay deterministic).
_W_KEYWORD = 0.45
_W_CONDITION = 0.35
_W_PRIORITY = 0.10
_W_CONFIDENCE = 0.10


class KnowledgeRetriever:
    """Retrieve knowledge entries relevant to a RuleContext.

    Supports:
    - keyword matching against context signals
    - condition matching against RuleContext paths
    - priority ranking
    - confidence weighting

    Never returns unrelated entries: a hit must pass keyword and/or
    condition evidence (empty keyword+condition rows are always rejected).
    """

    def __init__(
        self,
        repository: KnowledgeRepository | None = None,
        *,
        top_k: int = 20,
        min_relevance: float = 0.15,
    ) -> None:
        """Create a retriever.

        Args:
            repository: Indexed knowledge repository.
            top_k: Maximum accepted hits to return.
            min_relevance: Minimum final relevance score to accept.
        """
        self._repository = repository or KnowledgeRepository()
        self.top_k = max(1, int(top_k))
        self.min_relevance = float(min_relevance)

    @property
    def repository(self) -> KnowledgeRepository:
        """Return the bound repository."""
        return self._repository

    def retrieve(self, rule_context: Mapping[str, Any] | Any) -> KnowledgeResult:
        """Retrieve ranked knowledge entries for a RuleContext.

        Args:
            rule_context: Production RuleContext mapping (or normalizable object).

        Returns:
            ``KnowledgeResult`` with ranked entries and ``metadata.trace``.
        """
        context = normalize_context(rule_context)
        signals = self.extract_signals(context)
        signal_set = set(signals)

        records = self._repository.all()
        hits: list[KnowledgeHit] = []
        trace: list[RetrievalTraceEntry] = []
        rejected = 0

        for record in records:
            keyword_score, matched_keywords = self._keyword_score(record, signal_set)
            condition_score, matched_conditions, condition_error = self._condition_score(
                record, context
            )

            has_keyword_field = bool(record.keyword_tokens())
            has_condition_field = bool(str(record.condition or "").strip())

            if not has_keyword_field and not has_condition_field:
                rejected += 1
                trace.append(
                    self._trace(
                        record,
                        accepted=False,
                        keyword_score=0.0,
                        condition_score=0.0,
                        relevance_score=0.0,
                        reject_reason="empty_keyword_and_condition",
                    )
                )
                continue

            # Non-empty condition must pass (fail closed — never unrelated accepts).
            if has_condition_field and condition_score <= 0.0:
                rejected += 1
                reason = condition_error or "condition_failed"
                trace.append(
                    self._trace(
                        record,
                        accepted=False,
                        keyword_score=keyword_score,
                        condition_score=condition_score,
                        relevance_score=0.0,
                        matched_keywords=matched_keywords,
                        matched_conditions=matched_conditions,
                        reject_reason=reason,
                    )
                )
                continue

            # Keyword-only rows must have keyword evidence.
            if has_keyword_field and not has_condition_field and keyword_score <= 0.0:
                rejected += 1
                trace.append(
                    self._trace(
                        record,
                        accepted=False,
                        keyword_score=keyword_score,
                        condition_score=condition_score,
                        relevance_score=0.0,
                        matched_keywords=matched_keywords,
                        matched_conditions=matched_conditions,
                        reject_reason="no_keyword_match",
                    )
                )
                continue

            priority_norm = min(max(record.priority, 0), 100) / 100.0
            confidence_norm = min(max(record.confidence, 0.0), 1.0)
            relevance = (
                _W_KEYWORD * keyword_score
                + _W_CONDITION * condition_score
                + _W_PRIORITY * priority_norm
                + _W_CONFIDENCE * confidence_norm
            )

            if relevance < self.min_relevance:
                rejected += 1
                trace.append(
                    self._trace(
                        record,
                        accepted=False,
                        keyword_score=keyword_score,
                        condition_score=condition_score,
                        relevance_score=relevance,
                        matched_keywords=matched_keywords,
                        matched_conditions=matched_conditions,
                        reject_reason="below_min_relevance",
                    )
                )
                continue

            hit = KnowledgeHit(
                record=record,
                keyword_score=round(keyword_score, 6),
                condition_score=round(condition_score, 6),
                relevance_score=round(relevance, 6),
                matched_keywords=matched_keywords,
                matched_conditions=matched_conditions,
            )
            hits.append(hit)
            trace.append(
                self._trace(
                    record,
                    accepted=True,
                    keyword_score=keyword_score,
                    condition_score=condition_score,
                    relevance_score=relevance,
                    matched_keywords=matched_keywords,
                    matched_conditions=matched_conditions,
                )
            )

        hits.sort(
            key=lambda item: (
                -item.relevance_score,
                -item.record.priority,
                -item.record.confidence,
                item.record.id,
            )
        )
        ranked = hits[: self.top_k]

        metadata = {
            "trace": [self._trace_to_dict(entry) for entry in trace],
            "signal_count": len(signals),
            "signals": list(signals)[:64],
            "candidate_count": len(records),
            "accepted_count": len(ranked),
            "rejected_count": rejected + max(0, len(hits) - len(ranked)),
            "top_k": self.top_k,
            "min_relevance": self.min_relevance,
        }

        logger.debug(
            "Knowledge retrieval accepted=%s rejected=%s signals=%s",
            len(ranked),
            metadata["rejected_count"],
            len(signals),
        )
        return KnowledgeResult(entries=ranked, metadata=metadata)

    def extract_signals(self, context: Mapping[str, Any]) -> list[str]:
        """Extract normalized retrieval signals from RuleContext."""
        tokens: set[str] = set()

        def add(value: Any) -> None:
            if value is None:
                return
            if isinstance(value, bool):
                return
            if isinstance(value, (int, float)):
                return
            if isinstance(value, (list, tuple, set)):
                for item in value:
                    add(item)
                return
            if isinstance(value, Mapping):
                for key, item in value.items():
                    add(key)
                    add(item)
                return
            text = str(value).strip().lower()
            if not text or text in {"none", "null", "--", "n/a"}:
                return
            tokens.add(text)
            for part in re.split(r"[\s/|,;+]+", text):
                part = part.strip()
                if part and part not in {"none", "null"}:
                    tokens.add(part)

        # Flat aliases
        for key in (
            "day_master",
            "day_master_element",
            "birth_season",
        ):
            add(context.get(key))

        bazi = context.get("bazi") if isinstance(context.get("bazi"), Mapping) else {}
        add(bazi.get("day_master"))
        add(bazi.get("day_master_element"))
        add(bazi.get("day_master_yin_yang"))
        add(bazi.get("ten_gods"))
        add(bazi.get("shensha"))
        add(bazi.get("hidden_stems"))

        wuxing = context.get("wuxing") if isinstance(context.get("wuxing"), Mapping) else {}
        add(wuxing.get("season"))
        for element in ("wood", "fire", "earth", "metal", "water", "mộc", "hỏa", "thổ", "kim", "thủy"):
            node = wuxing.get(element)
            if isinstance(node, Mapping):
                add(element)
                add(node.get("status"))
                add(node.get("label"))
            elif node:
                add(element)
                add(node)

        strength = context.get("strength") if isinstance(context.get("strength"), Mapping) else {}
        add(strength.get("level"))
        add(strength.get("month_status"))
        add(strength.get("root_level"))
        add(strength.get("support_type"))
        add(strength.get("control_type"))

        temperature = (
            context.get("temperature") if isinstance(context.get("temperature"), Mapping) else {}
        )
        add(temperature.get("status"))
        add(temperature.get("result"))
        add(temperature.get("level"))

        pattern = context.get("pattern") if isinstance(context.get("pattern"), Mapping) else {}
        add(pattern.get("main_pattern"))
        add(pattern.get("name"))
        add(pattern.get("status"))
        add(pattern.get("follow_type"))
        add(pattern.get("category"))

        useful = context.get("useful_god") if isinstance(context.get("useful_god"), Mapping) else {}
        add(useful.get("status"))
        add(useful.get("name"))
        add(useful.get("element"))
        add(useful.get("favorable"))
        add(useful.get("unfavorable"))

        ten_gods = context.get("ten_gods") if isinstance(context.get("ten_gods"), Mapping) else {}
        add(ten_gods.get("items"))
        add(ten_gods.get("unique"))
        add(ten_gods.get("status"))
        by_name = ten_gods.get("by_name")
        if isinstance(by_name, Mapping):
            add(list(by_name.keys()))

        shensha = context.get("shensha") if isinstance(context.get("shensha"), Mapping) else {}
        add(shensha.get("stars"))
        add(shensha.get("star"))
        add(shensha.get("status"))
        add(shensha.get("available"))

        # Stable sort for deterministic traces
        return sorted(tokens)

    def _keyword_score(
        self, record: KnowledgeRecord, signals: set[str]
    ) -> tuple[float, tuple[str, ...]]:
        tokens = record.keyword_tokens()
        if not tokens or not signals:
            return 0.0, ()

        matched: list[str] = []
        for token in tokens:
            if token in signals:
                matched.append(token)
                continue
            # Soft substring match against longer signals / tokens
            if any(token in signal or signal in token for signal in signals if len(token) >= 2):
                matched.append(token)

        if not matched:
            return 0.0, ()
        score = len(set(matched)) / float(len(tokens))
        return min(1.0, score), tuple(sorted(set(matched)))

    def _condition_score(
        self, record: KnowledgeRecord, context: Mapping[str, Any]
    ) -> tuple[float, tuple[str, ...], str]:
        raw = str(record.condition or "").strip()
        if not raw:
            return 0.0, (), ""

        parts = [part for part in _CONDITION_SPLIT.split(raw) if part.strip()]
        if not parts:
            return 0.0, (), ""

        matched: list[str] = []
        for part in parts:
            ok, label = self._eval_condition_part(part, context)
            if not ok:
                reason = "unsupported_condition" if label == "unsupported_condition" else "condition_failed"
                return 0.0, tuple(matched), reason
            matched.append(label or part)

        return 1.0, tuple(matched), ""

    def _eval_condition_part(
        self, expression: str, context: Mapping[str, Any]
    ) -> tuple[bool, str]:
        text = expression.strip()
        if not text:
            return True, ""

        exists_match = _CONDITION_EXISTS.match(text)
        if exists_match:
            field = exists_match.group("field")
            value = resolve_path(context, field, default=None)
            return value is not None, f"{field} exists"

        in_match = _CONDITION_IN.match(text)
        if in_match:
            field = in_match.group("field")
            expected_raw = in_match.group("value")
            expected = [item.strip().lower() for item in re.split(r"[|,]", expected_raw) if item.strip()]
            actual = resolve_path(context, field, default=None)
            actual_values = self._as_text_collection(actual)
            ok = any(item in actual_values for item in expected)
            return ok, f"{field} in {expected_raw}"

        contains_match = _CONDITION_CONTAINS.match(text)
        if contains_match:
            field = contains_match.group("field")
            needle = contains_match.group("value").strip().lower()
            actual = resolve_path(context, field, default=None)
            actual_values = self._as_text_collection(actual)
            joined = " ".join(sorted(actual_values))
            ok = needle in actual_values or needle in joined
            return ok, f"{field} contains {needle}"

        eq_match = _CONDITION_EQ.match(text)
        if eq_match:
            field = eq_match.group("field")
            expected = eq_match.group("value").strip().lower()
            actual = resolve_path(context, field, default=None)
            actual_values = self._as_text_collection(actual)
            ok = expected in actual_values or str(actual).strip().lower() == expected
            return ok, f"{field}={expected}"

        # Unsupported expression → fail closed (never unrelated accept).
        return False, "unsupported_condition"

    def _as_text_collection(self, value: Any) -> set[str]:
        out: set[str] = set()
        if value is None:
            return out
        if isinstance(value, Mapping):
            for key, item in value.items():
                out.add(str(key).strip().lower())
                out |= self._as_text_collection(item)
            return out
        if isinstance(value, (list, tuple, set)):
            for item in value:
                out |= self._as_text_collection(item)
            return out
        text = str(value).strip().lower()
        if text:
            out.add(text)
        return out

    def _trace(
        self,
        record: KnowledgeRecord,
        *,
        accepted: bool,
        keyword_score: float,
        condition_score: float,
        relevance_score: float,
        matched_keywords: tuple[str, ...] = (),
        matched_conditions: tuple[str, ...] = (),
        reject_reason: str = "",
    ) -> RetrievalTraceEntry:
        return RetrievalTraceEntry(
            record_id=record.id,
            accepted=accepted,
            keyword_score=round(keyword_score, 6),
            condition_score=round(condition_score, 6),
            priority=record.priority,
            confidence=record.confidence,
            relevance_score=round(relevance_score, 6),
            matched_keywords=matched_keywords,
            matched_conditions=matched_conditions,
            reject_reason=reject_reason,
        )

    def _trace_to_dict(self, entry: RetrievalTraceEntry) -> dict[str, Any]:
        return {
            "record_id": entry.record_id,
            "accepted": entry.accepted,
            "keyword_score": entry.keyword_score,
            "condition_score": entry.condition_score,
            "priority": entry.priority,
            "confidence": entry.confidence,
            "relevance_score": entry.relevance_score,
            "matched_keywords": list(entry.matched_keywords),
            "matched_conditions": list(entry.matched_conditions),
            "reject_reason": entry.reject_reason,
        }
