"""Conflict Interpretation Rule Engine.

Enriches Pack 02 conflict facts with Pack 01 quan_he + clash_score rules.
Does not call CombinationEngine.calculate/evaluate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.constants import (
    CLASH_SCORE_TYPES,
    DESTRUCTION_SCORE_TYPES,
    HARM_SCORE_TYPES,
    PUNISHMENT_SCORE_TYPES,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.extractor import (
    ConflictFacts,
    ConflictRelationFact,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.models import (
    ConflictItemResult,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.rule_loader import (
    ConflictRuleLoader,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ConflictRuleEngineResult:
    """Rule-engine output for Conflict Interpreter."""

    clashes: tuple[ConflictItemResult, ...]
    punishments: tuple[ConflictItemResult, ...]
    harms: tuple[ConflictItemResult, ...]
    destructions: tuple[ConflictItemResult, ...]
    conflict_score: float
    matched_rule_ids: tuple[str, ...]
    reasoning: str


class ConflictInterpretationRuleEngine:
    """Rule Engine for Conflict Interpreter."""

    def __init__(
        self,
        *,
        loader: ConflictRuleLoader | None = None,
    ) -> None:
        """Initialize with Pack 01 conflict rule loader."""
        self.loader = loader or ConflictRuleLoader()

    def evaluate(self, facts: ConflictFacts) -> ConflictRuleEngineResult:
        """Interpret clash/punishment/harm/destruction and compute conflict score."""
        score_map = self.loader.score_lookup()

        clashes = tuple(
            self._enrich(
                item,
                pack01_rules=self.loader.load_clash_rules(),
                score_map=score_map,
                score_types=CLASH_SCORE_TYPES,
                default_type="clash",
                preferred_score_type="LIU_CHONG",
            )
            for item in facts.clashes
        )
        punishments = tuple(
            self._enrich(
                item,
                pack01_rules=self.loader.load_punishment_rules(),
                score_map=score_map,
                score_types=PUNISHMENT_SCORE_TYPES,
                default_type="punishment",
                preferred_score_type="XING",
            )
            for item in facts.punishments
        )
        harms = tuple(
            self._enrich(
                item,
                pack01_rules=self.loader.load_harm_rules(),
                score_map=score_map,
                score_types=HARM_SCORE_TYPES,
                default_type="harm",
                preferred_score_type="LIU_HAI",
            )
            for item in facts.harms
        )
        destructions = tuple(
            self._enrich(
                item,
                pack01_rules=self.loader.load_destruction_rules(),
                score_map=score_map,
                score_types=DESTRUCTION_SCORE_TYPES,
                default_type="destruction",
                preferred_score_type="LIU_PO",
            )
            for item in facts.destructions
        )

        conflict_score = self._compute_score(
            facts=facts,
            items=(*clashes, *punishments, *harms, *destructions),
            score_map=score_map,
        )

        matched_ids = list(facts.matched_rules)
        for item in (*clashes, *punishments, *harms, *destructions):
            pack01_id = str(item.attributes.get("pack01_rule_id") or "")
            if pack01_id:
                matched_ids.append(pack01_id)
            score_id = str(item.attributes.get("score_rule_id") or "")
            if score_id:
                matched_ids.append(score_id)

        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        reasoning = facts.reasoning
        if not reasoning:
            parts = [
                f"clash={len(clashes)}",
                f"punishment={len(punishments)}",
                f"harm={len(harms)}",
                f"destruction={len(destructions)}",
            ]
            reasoning = "Conflict interpretation: " + ", ".join(parts)

        logger.info(
            "conflict_rule_engine_evaluated",
            extra={
                "clash_count": len(clashes),
                "punishment_count": len(punishments),
                "harm_count": len(harms),
                "destruction_count": len(destructions),
                "conflict_score": conflict_score,
            },
        )

        return ConflictRuleEngineResult(
            clashes=clashes,
            punishments=punishments,
            harms=harms,
            destructions=destructions,
            conflict_score=conflict_score,
            matched_rule_ids=tuple(ordered_ids),
            reasoning=reasoning,
        )

    def _enrich(
        self,
        fact: ConflictRelationFact,
        *,
        pack01_rules: list[dict[str, Any]],
        score_map: dict[str, dict[str, Any]],
        score_types: frozenset[str],
        default_type: str,
        preferred_score_type: str,
    ) -> ConflictItemResult:
        """Enrich one conflict relation with Pack 01 row + score."""
        matched = self._match_rule(fact.members, pack01_rules)
        score_type = self._resolve_score_type(
            fact=fact,
            matched=matched,
            preferred=preferred_score_type,
            allowed=score_types,
        )
        score_row = score_map.get(score_type) or self._first_score(score_map, score_types)

        description = ""
        pack01_id = ""
        if matched is not None:
            pack01_id = str(
                matched.get("id")
                or matched.get("ma_quan_he")
                or matched.get("ten")
                or ""
            )
            description = str(matched.get("mo_ta") or matched.get("ten") or "")

        score = float(score_row.get("score") or 0.0) if score_row else 0.0
        priority = (
            int(score_row.get("priority") or fact.priority or 0)
            if score_row
            else fact.priority
        )
        return ConflictItemResult(
            item_id=fact.relation_id or pack01_id or ",".join(fact.members),
            item_type=fact.relation_type or default_type,
            members=fact.members,
            status=fact.status or "active",
            score=score,
            priority=priority,
            description=description,
            attributes={
                "pack01_rule_id": pack01_id,
                "score_rule_id": str((score_row or {}).get("id") or ""),
                "clash_type": score_type,
                "pillars": list(fact.pillars),
            },
        )

    def _compute_score(
        self,
        *,
        facts: ConflictFacts,
        items: tuple[ConflictItemResult, ...],
        score_map: dict[str, dict[str, Any]],
    ) -> float:
        """Aggregate Pack 01 clash scores (respect max_apply)."""
        if facts.conflict_score is not None and not items:
            return float(facts.conflict_score)

        total = 0.0
        apply_counts: dict[str, int] = {}

        def _add(score_rule_id: str, score: float, max_apply: int) -> None:
            nonlocal total
            used = apply_counts.get(score_rule_id, 0)
            if score_rule_id and max_apply > 0 and used >= max_apply:
                return
            total += score
            if score_rule_id:
                apply_counts[score_rule_id] = used + 1

        for item in items:
            score_rule_id = str(item.attributes.get("score_rule_id") or "")
            max_apply = 99
            if score_rule_id:
                for row in score_map.values():
                    if str(row.get("id") or "") == score_rule_id:
                        max_apply = int(float(row.get("max_apply") or 99))
                        break
            _add(score_rule_id, float(item.score), max_apply)

        if total == 0.0 and facts.conflict_score is not None:
            return float(facts.conflict_score)
        return total

    def _match_rule(
        self,
        members: tuple[str, ...],
        rules: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Find Pack 01 conflict rule matching members."""
        member_set = {str(item) for item in members if item}
        if not member_set:
            return None
        best: dict[str, Any] | None = None
        best_overlap = 0
        for row in rules:
            chis = {
                str(row.get(key) or "")
                for key in ("chi_1", "chi_2", "chi_3")
                if row.get(key) not in (None, "")
            }
            if not chis:
                continue
            # Self-punishment: single chi rules.
            if len(chis) == 1 and member_set == chis:
                return row
            overlap = len(member_set & chis)
            if overlap == len(chis) and overlap >= best_overlap:
                best = row
                best_overlap = overlap
            elif overlap >= 2 and overlap > best_overlap:
                best = row
                best_overlap = overlap
        return best

    def _resolve_score_type(
        self,
        *,
        fact: ConflictRelationFact,
        matched: dict[str, Any] | None,
        preferred: str,
        allowed: frozenset[str],
    ) -> str:
        """Pick Pack 01 clash_type for scoring."""
        text = f"{fact.relation_type} {matched or {}}".lower()
        if "tu" in text or "self" in text or "zi" in text:
            if "ZI_XING" in allowed:
                return "ZI_XING"
        if preferred in allowed:
            return preferred
        for key in allowed:
            return key
        return preferred

    @staticmethod
    def _first_score(
        score_map: dict[str, dict[str, Any]],
        types: frozenset[str],
    ) -> dict[str, Any] | None:
        """Pick first matching score row for allowed clash types."""
        for key in types:
            if key in score_map:
                return score_map[key]
        return None
