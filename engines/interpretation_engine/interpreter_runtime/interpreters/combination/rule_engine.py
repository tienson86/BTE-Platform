"""Combination Interpretation Rule Engine.

Enriches Pack 02 combination facts with Pack 01 quan_he + score rules.
Does not call CombinationEngine.calculate/evaluate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.interpreter_runtime.interpreters.combination.constants import (
    BRANCH_SCORE_TYPES,
    STEM_SCORE_TYPES,
    TRANSFORM_FAIL_TYPE,
    TRANSFORM_SUCCESS_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.extractor import (
    CombinationFacts,
    CombinationRelationFact,
    CombinationTransformFact,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.models import (
    CombinationItemResult,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.rule_loader import (
    CombinationRuleLoader,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class CombinationRuleEngineResult:
    """Rule-engine output for Combination Interpreter."""

    stem_combinations: tuple[CombinationItemResult, ...]
    branch_combinations: tuple[CombinationItemResult, ...]
    transformations: tuple[CombinationItemResult, ...]
    combination_score: float
    matched_rule_ids: tuple[str, ...]
    reasoning: str


class CombinationInterpretationRuleEngine:
    """Rule Engine for Combination Interpreter."""

    def __init__(
        self,
        *,
        loader: CombinationRuleLoader | None = None,
    ) -> None:
        """Initialize with Pack 01 combination rule loader."""
        self.loader = loader or CombinationRuleLoader()

    def evaluate(self, facts: CombinationFacts) -> CombinationRuleEngineResult:
        """Interpret stem/branch/transform facts and compute combination score."""
        score_map = self.loader.score_lookup()
        stem_rules = self.loader.load_stem_rules()
        branch_rules = self.loader.load_branch_rules()

        stems = tuple(
            self._enrich_stem(item, stem_rules, score_map)
            for item in facts.stem_combinations
        )
        branches = tuple(
            self._enrich_branch(item, branch_rules, score_map)
            for item in facts.branch_combinations
        )
        transforms = tuple(
            self._enrich_transform(item, score_map)
            for item in facts.transformations
        )

        # If Pack 02 omitted lists but score rules exist, keep empty lists.
        combination_score = self._compute_score(
            facts=facts,
            stems=stems,
            branches=branches,
            transforms=transforms,
            score_map=score_map,
        )

        matched_ids = list(facts.matched_rules)
        for item in (*stems, *branches, *transforms):
            rule_id = str(item.attributes.get("pack01_rule_id") or "")
            if rule_id:
                matched_ids.append(rule_id)
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
            parts: list[str] = []
            if stems:
                parts.append(f"stem={len(stems)}")
            if branches:
                parts.append(f"branch={len(branches)}")
            if transforms:
                success_n = sum(1 for item in transforms if item.success)
                parts.append(f"transform_success={success_n}/{len(transforms)}")
            reasoning = "Combination interpretation: " + ", ".join(parts) if parts else ""

        logger.info(
            "combination_rule_engine_evaluated",
            extra={
                "stem_count": len(stems),
                "branch_count": len(branches),
                "transform_count": len(transforms),
                "combination_score": combination_score,
            },
        )

        return CombinationRuleEngineResult(
            stem_combinations=stems,
            branch_combinations=branches,
            transformations=transforms,
            combination_score=combination_score,
            matched_rule_ids=tuple(ordered_ids),
            reasoning=reasoning,
        )

    def _enrich_stem(
        self,
        fact: CombinationRelationFact,
        stem_rules: list[dict[str, Any]],
        score_map: dict[str, dict[str, Any]],
    ) -> CombinationItemResult:
        """Enrich stem combination with Pack 01 Thiên Can hợp row + score."""
        matched = self._match_stem_rule(fact.members, stem_rules)
        score_row = self._score_row_for_types(score_map, STEM_SCORE_TYPES)
        result_element = fact.result_element
        description = ""
        pack01_id = ""
        if matched is not None:
            pack01_id = str(matched.get("id") or "")
            result_element = result_element or str(matched.get("ket_qua") or "")
            description = str(matched.get("ghi_chu") or matched.get("dieu_kien") or "")
        score = float(score_row.get("score") or 0.0) if score_row else 0.0
        priority = int(score_row.get("priority") or fact.priority or 0) if score_row else fact.priority
        return CombinationItemResult(
            item_id=fact.relation_id or pack01_id or ",".join(fact.members),
            item_type=fact.relation_type or "stem_combination",
            members=fact.members,
            result_element=result_element,
            status=fact.status or "active",
            score=score,
            priority=priority,
            success=None,
            description=description,
            attributes={
                "pack01_rule_id": pack01_id,
                "score_rule_id": str((score_row or {}).get("id") or ""),
                "pillars": list(fact.pillars),
            },
        )

    def _enrich_branch(
        self,
        fact: CombinationRelationFact,
        branch_rules: list[dict[str, Any]],
        score_map: dict[str, dict[str, Any]],
    ) -> CombinationItemResult:
        """Enrich branch combination with Pack 01 Địa Chi hop row + score."""
        matched = self._match_branch_rule(fact.members, branch_rules)
        group = str((matched or {}).get("branch_group") or "")
        score_type = self._branch_group_to_score_type(group, fact.relation_type)
        score_row = score_map.get(score_type) if score_type else None
        if score_row is None:
            score_row = self._score_row_for_types(score_map, BRANCH_SCORE_TYPES)

        result_element = fact.result_element
        description = ""
        pack01_id = ""
        if matched is not None:
            pack01_id = str(matched.get("id") or matched.get("ma_quan_he") or "")
            result_element = result_element or str(
                matched.get("ngu_hanh_hoa") or matched.get("ngu_hanh") or ""
            )
            description = str(matched.get("mo_ta") or matched.get("ten") or "")

        score = float(score_row.get("score") or 0.0) if score_row else 0.0
        priority = (
            int(score_row.get("priority") or fact.priority or 0)
            if score_row
            else fact.priority
        )
        return CombinationItemResult(
            item_id=fact.relation_id or pack01_id or ",".join(fact.members),
            item_type=fact.relation_type or group or "branch_combination",
            members=fact.members,
            result_element=result_element,
            status=fact.status or "active",
            score=score,
            priority=priority,
            success=None,
            description=description,
            attributes={
                "pack01_rule_id": pack01_id,
                "score_rule_id": str((score_row or {}).get("id") or ""),
                "branch_group": group,
                "pillars": list(fact.pillars),
            },
        )

    def _enrich_transform(
        self,
        fact: CombinationTransformFact,
        score_map: dict[str, dict[str, Any]],
    ) -> CombinationItemResult:
        """Enrich transformation with Pack 01 HUA_SUCCESS / HUA_FAIL score."""
        score_type = TRANSFORM_SUCCESS_TYPE if fact.success else TRANSFORM_FAIL_TYPE
        score_row = score_map.get(score_type) or {}
        return CombinationItemResult(
            item_id=fact.source_relation_id or score_type,
            item_type="transformation",
            members=(),
            result_element=fact.result_element,
            status="success" if fact.success else "fail",
            score=float(score_row.get("score") or 0.0),
            priority=int(score_row.get("priority") or fact.priority or 0),
            success=fact.success,
            description=str(score_row.get("description") or score_row.get("condition") or ""),
            attributes={
                "score_rule_id": str(score_row.get("id") or ""),
                "reason_codes": list(fact.reason_codes),
                "source_relation_id": fact.source_relation_id,
            },
        )

    def _compute_score(
        self,
        *,
        facts: CombinationFacts,
        stems: tuple[CombinationItemResult, ...],
        branches: tuple[CombinationItemResult, ...],
        transforms: tuple[CombinationItemResult, ...],
        score_map: dict[str, dict[str, Any]],
    ) -> float:
        """Aggregate Pack 01 combination scores (respect max_apply)."""
        if facts.combination_score is not None and not (stems or branches or transforms):
            return float(facts.combination_score)

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

        for item in (*stems, *branches, *transforms):
            score_rule_id = str(item.attributes.get("score_rule_id") or "")
            max_apply = 99
            if score_rule_id:
                for row in score_map.values():
                    if str(row.get("id") or "") == score_rule_id:
                        max_apply = int(float(row.get("max_apply") or 99))
                        break
            _add(score_rule_id, float(item.score), max_apply)

        if total == 0.0 and facts.combination_score is not None:
            return float(facts.combination_score)
        return total

    def _match_stem_rule(
        self,
        members: tuple[str, ...],
        stem_rules: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Find Pack 01 stem hop matching member pair."""
        if len(members) < 2:
            return None
        a, b = str(members[0]), str(members[1])
        for row in stem_rules:
            can_1 = str(row.get("can_1") or "")
            can_2 = str(row.get("can_2") or "")
            if {can_1, can_2} == {a, b}:
                return row
        return None

    def _match_branch_rule(
        self,
        members: tuple[str, ...],
        branch_rules: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Find Pack 01 branch hop matching members (pair or triple)."""
        member_set = {str(item) for item in members if item}
        if not member_set:
            return None
        best: dict[str, Any] | None = None
        best_overlap = 0
        for row in branch_rules:
            chis = {
                str(row.get(key) or "")
                for key in ("chi_1", "chi_2", "chi_3")
                if row.get(key) not in (None, "")
            }
            if not chis:
                continue
            overlap = len(member_set & chis)
            if overlap == len(chis) and overlap >= best_overlap:
                best = row
                best_overlap = overlap
        return best

    @staticmethod
    def _branch_group_to_score_type(group: str, relation_type: str) -> str:
        """Map branch group / relation_type to Pack 01 score combination_type."""
        mapping = {
            "luc_hop": "DI_ZHI_LIUHE",
            "tam_hop": "TAM_HOP",
            "tam_hoi": "TAM_HOI",
            "ban_hop": "BAN_HOP",
        }
        if group in mapping:
            return mapping[group]
        text = str(relation_type or "").lower()
        if "luc" in text or "liuhe" in text:
            return "DI_ZHI_LIUHE"
        if "tam_hop" in text or "trine" in text:
            return "TAM_HOP"
        if "tam_hoi" in text or "frame" in text:
            return "TAM_HOI"
        if "ban" in text:
            return "BAN_HOP"
        return "DI_ZHI_LIUHE"

    @staticmethod
    def _score_row_for_types(
        score_map: dict[str, dict[str, Any]],
        types: frozenset[str],
    ) -> dict[str, Any] | None:
        """Pick first matching score row for allowed combination types."""
        for key in types:
            if key in score_map:
                return score_map[key]
        return None
