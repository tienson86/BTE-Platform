"""Shensha Interpretation Rule Engine.

Enriches Pack 02 Shensha facts with Pack 01 identity / score / explanation rules.
Does not call ShenShaEngine.evaluate or ScoreEngine.calculate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, replace
from typing import Any

from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.constants import (
    IMPORTANCE_RANK,
    NEGATIVE_LOAI,
    POSITIVE_LOAI,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.extractor import (
    ShenshaFacts,
    ShenshaPresenceFact,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.models import (
    ShenshaItemResult,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.rule_loader import (
    ShenshaRuleLoader,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ShenshaRuleEngineResult:
    """Rule-engine output for Shensha Interpreter."""

    detected: tuple[ShenshaItemResult, ...]
    importance: tuple[ShenshaItemResult, ...]
    priorities: tuple[ShenshaItemResult, ...]
    explanations: tuple[ShenshaItemResult, ...]
    shensha_score: float
    matched_rule_ids: tuple[str, ...]
    reasoning: str


class ShenshaInterpretationRuleEngine:
    """Rule Engine for Shensha Interpreter."""

    def __init__(
        self,
        *,
        loader: ShenshaRuleLoader | None = None,
    ) -> None:
        """Initialize with Pack 01 Shensha rule loader."""
        self.loader = loader or ShenshaRuleLoader()

    def evaluate(self, facts: ShenshaFacts) -> ShenshaRuleEngineResult:
        """Interpret detected Shensha / Importance / Priority / Explanation."""
        identity_lookup = self.loader.identity_by_label()
        explanation_lookup = self.loader.explanation_by_label()

        detected = tuple(
            self._enrich_presence(
                item,
                identity_lookup=identity_lookup,
                explanation_lookup=explanation_lookup,
            )
            for item in facts.presence
        )

        # Apply danh_gia combination evaluations when multiple stars present.
        eval_bonus = self._match_evaluations(detected)
        if eval_bonus:
            detected = tuple(
                replace(
                    item,
                    score=item.score + eval_bonus.get(item.item_id, 0.0),
                    attributes={
                        **dict(item.attributes),
                        "evaluation_bonus": eval_bonus.get(item.item_id, 0.0),
                    },
                )
                for item in detected
            )

        importance = self._build_importance(detected)
        priorities = self._build_priorities(detected)
        explanations = self._build_explanations(detected)

        shensha_score = self._compute_score(facts=facts, detected=detected)

        matched_ids = list(facts.matched_rules)
        for item in (*detected, *importance, *priorities, *explanations):
            for key in (
                "pack01_rule_id",
                "score_rule_id",
                "explanation_rule_id",
                "evaluation_rule_id",
                "priority_rule_id",
            ):
                rule_id = str(item.attributes.get(key) or "")
                if rule_id:
                    matched_ids.append(rule_id)
        for rule_id in eval_bonus.get("__rules__", ()):
            matched_ids.append(str(rule_id))

        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        reasoning = facts.reasoning
        if not reasoning:
            parts = [
                f"detected={len(detected)}",
                f"importance={len(importance)}",
                f"priority={len(priorities)}",
                f"explanation={len(explanations)}",
            ]
            reasoning = "Shensha interpretation: " + ", ".join(parts)

        logger.info(
            "shensha_rule_engine_evaluated",
            extra={
                "detected_count": len(detected),
                "importance_count": len(importance),
                "priority_count": len(priorities),
                "explanation_count": len(explanations),
                "shensha_score": shensha_score,
            },
        )

        return ShenshaRuleEngineResult(
            detected=detected,
            importance=importance,
            priorities=priorities,
            explanations=explanations,
            shensha_score=shensha_score,
            matched_rule_ids=tuple(ordered_ids),
            reasoning=reasoning,
        )

    def _enrich_presence(
        self,
        fact: ShenshaPresenceFact,
        *,
        identity_lookup: dict[str, dict[str, Any]],
        explanation_lookup: dict[str, dict[str, Any]],
    ) -> ShenshaItemResult:
        """Enrich one detected Shensha with Pack 01 identity / score / explanation."""
        label = fact.label or fact.shensha_id
        identity = self._lookup_row(label, fact.shensha_id, identity_lookup)
        if identity is not None and identity.get("ten_han_viet"):
            label = str(identity.get("ten_han_viet") or label)

        explanation = self._lookup_row(label, fact.shensha_id, explanation_lookup)
        polarity = fact.polarity or str((identity or {}).get("loai") or "")
        score_row = self._match_score(label, polarity)
        priority_row = self._match_priority_weight(polarity, explanation)

        score = float(score_row.get("score") or 0.0) if score_row else 0.0
        priority = int(
            float(
                (score_row or {}).get("priority")
                or fact.priority
                or (priority_row or {}).get("priority_level")
                or 0
            )
        )
        importance = str(
            (explanation or {}).get("muc_do")
            or (identity or {}).get("loai")
            or polarity
            or ""
        )
        importance_rank = self._importance_rank(importance)
        explanation_text = str(
            (explanation or {}).get("mau_giai_thich")
            or (identity or {}).get("mo_ta_ngan")
            or ""
        )
        recommendation = str((explanation or {}).get("goi_y") or "")
        description = str(
            (identity or {}).get("mo_ta_ngan")
            or (score_row or {}).get("description")
            or ""
        )

        return ShenshaItemResult(
            item_id=fact.shensha_id or label,
            item_type="detected",
            label=label,
            score=score,
            priority=priority,
            importance=importance,
            importance_rank=importance_rank,
            explanation=explanation_text,
            recommendation=recommendation,
            status=fact.status or "active",
            polarity=polarity,
            description=description,
            attributes={
                "pack01_rule_id": str((identity or {}).get("id") or ""),
                "score_rule_id": str((score_row or {}).get("id") or ""),
                "explanation_rule_id": str((explanation or {}).get("rule_id") or ""),
                "priority_rule_id": str((priority_row or {}).get("id") or ""),
                "priority_weight": float((priority_row or {}).get("weight") or 1.0),
                "nhom_than_sat": str((identity or {}).get("nhom_than_sat") or ""),
                "linh_vuc": str(
                    (explanation or {}).get("linh_vuc")
                    or (identity or {}).get("linh_vuc_anh_huong")
                    or ""
                ),
                "location_pillar": fact.location_pillar,
                "location_value": fact.location_value,
                "anchor": fact.anchor,
                "anchor_value": fact.anchor_value,
            },
        )

    def _build_importance(
        self,
        detected: tuple[ShenshaItemResult, ...],
    ) -> tuple[ShenshaItemResult, ...]:
        """Build importance-ranked view of detected Shensha."""
        items = [
            ShenshaItemResult(
                item_id=item.item_id,
                item_type="importance",
                label=item.label,
                score=float(item.importance_rank),
                priority=item.importance_rank,
                importance=item.importance,
                importance_rank=item.importance_rank,
                explanation=item.explanation,
                recommendation=item.recommendation,
                status=item.status,
                polarity=item.polarity,
                description=item.importance or item.description,
                attributes={
                    "pack01_rule_id": item.attributes.get("pack01_rule_id", ""),
                    "explanation_rule_id": item.attributes.get(
                        "explanation_rule_id", ""
                    ),
                    "linh_vuc": item.attributes.get("linh_vuc", ""),
                },
            )
            for item in detected
        ]
        items.sort(key=lambda row: (-row.importance_rank, -row.priority, row.label))
        return tuple(items)

    def _build_priorities(
        self,
        detected: tuple[ShenshaItemResult, ...],
    ) -> tuple[ShenshaItemResult, ...]:
        """Build priority-ordered view using Pack 01 priority weights."""
        items = [
            ShenshaItemResult(
                item_id=item.item_id,
                item_type="priority",
                label=item.label,
                score=float(item.priority)
                * float(item.attributes.get("priority_weight") or 1.0),
                priority=item.priority,
                importance=item.importance,
                importance_rank=item.importance_rank,
                explanation=item.explanation,
                recommendation=item.recommendation,
                status=item.status,
                polarity=item.polarity,
                description=f"priority={item.priority}",
                attributes={
                    "score_rule_id": item.attributes.get("score_rule_id", ""),
                    "priority_rule_id": item.attributes.get("priority_rule_id", ""),
                    "priority_weight": item.attributes.get("priority_weight", 1.0),
                    "weighted_priority": float(item.priority)
                    * float(item.attributes.get("priority_weight") or 1.0),
                },
            )
            for item in detected
        ]
        items.sort(key=lambda row: (-row.score, -row.priority, row.label))
        return tuple(items)

    def _build_explanations(
        self,
        detected: tuple[ShenshaItemResult, ...],
    ) -> tuple[ShenshaItemResult, ...]:
        """Build explanation view from Pack 01 giai thich templates."""
        return tuple(
            ShenshaItemResult(
                item_id=item.item_id,
                item_type="explanation",
                label=item.label,
                score=item.score,
                priority=item.priority,
                importance=item.importance,
                importance_rank=item.importance_rank,
                explanation=item.explanation,
                recommendation=item.recommendation,
                status=item.status,
                polarity=item.polarity,
                description=item.explanation or item.description,
                attributes={
                    "explanation_rule_id": item.attributes.get(
                        "explanation_rule_id", ""
                    ),
                    "pack01_rule_id": item.attributes.get("pack01_rule_id", ""),
                    "linh_vuc": item.attributes.get("linh_vuc", ""),
                    "goi_y": item.recommendation,
                },
            )
            for item in detected
            if item.explanation or item.recommendation or item.description
        )

    def _match_evaluations(
        self,
        detected: tuple[ShenshaItemResult, ...],
    ) -> dict[str, Any]:
        """Apply Pack 01 danh_gia combination bonuses across detected labels."""
        labels = {self._norm(item.label) for item in detected if item.label}
        ids_by_norm = {self._norm(item.label): item.item_id for item in detected}
        bonus: dict[str, Any] = {"__rules__": []}
        for row in self.loader.load_evaluation_rules():
            condition = str(row.get("dieu_kien") or "")
            parts = [
                self._norm(part)
                for part in condition.replace("AND", "|").replace("and", "|").split("|")
                if part.strip()
            ]
            if len(parts) < 2:
                continue
            if not all(part in labels for part in parts):
                continue
            points = float(row.get("diem") or 0.0)
            share = points / len(parts)
            for part in parts:
                item_id = ids_by_norm.get(part)
                if item_id:
                    bonus[item_id] = float(bonus.get(item_id, 0.0)) + share
            bonus["__rules__"].append(str(row.get("rule_id") or ""))
        return bonus

    def _compute_score(
        self,
        *,
        facts: ShenshaFacts,
        detected: tuple[ShenshaItemResult, ...],
    ) -> float:
        """Aggregate Shensha scores with max_apply awareness."""
        if facts.shensha_score is not None and not detected:
            return float(facts.shensha_score)

        total = 0.0
        apply_counts: dict[str, int] = {}
        score_lookup = {
            str(row.get("id") or ""): row
            for row in (
                *self.loader.load_positive_rules(),
                *self.loader.load_negative_rules(),
                *self.loader.load_domain_score_rules(),
            )
        }

        for item in detected:
            rule_id = str(item.attributes.get("score_rule_id") or item.item_id)
            max_apply = 99
            row = score_lookup.get(rule_id)
            if row is not None:
                max_apply = int(float(row.get("max_apply") or 99))
            used = apply_counts.get(rule_id, 0)
            if rule_id and max_apply > 0 and used >= max_apply:
                continue
            total += float(item.score)
            if rule_id:
                apply_counts[rule_id] = used + 1

        if total == 0.0 and facts.shensha_score is not None:
            return float(facts.shensha_score)
        return total

    def _match_score(
        self,
        label: str,
        polarity: str,
    ) -> dict[str, Any] | None:
        """Pick positive/negative/domain score row for a star label."""
        label_n = self._norm(label)
        pol_n = self._norm(polarity)
        prefer_negative = bool(
            {pol_n} & {self._norm(token) for token in NEGATIVE_LOAI}
            or any(token in pol_n for token in ("hung", "negative", "inauspicious"))
        )
        prefer_positive = bool(
            {pol_n} & {self._norm(token) for token in POSITIVE_LOAI}
            or any(token in pol_n for token in ("cat", "cát", "auspicious", "positive"))
        )

        primary = (
            self.loader.load_negative_rules()
            if prefer_negative and not prefer_positive
            else self.loader.load_positive_rules()
        )
        for row in primary:
            if self._norm(str(row.get("star_name") or "")) == label_n:
                return row

        secondary = (
            self.loader.load_positive_rules()
            if prefer_negative
            else self.loader.load_negative_rules()
        )
        for row in secondary:
            if self._norm(str(row.get("star_name") or "")) == label_n:
                return row

        for row in self.loader.load_domain_score_rules():
            if self._norm(str(row.get("star_name") or "")) == label_n:
                return row
        return None

    def _match_priority_weight(
        self,
        polarity: str,
        explanation: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Map polarity / muc_do to Pack 01 priority weight row."""
        text = self._norm(
            f"{polarity} {(explanation or {}).get('muc_do') or ''}"
        )
        rules = self.loader.load_priority_rules()
        if not rules:
            return None

        # Heuristic mapping from Pack 01 priority conditions.
        if any(token in text for token in ("dai_hung", "phá", "pha")):
            target = 50
        elif any(token in text for token in ("hung", "negative")):
            target = 60 if "manh" in text or "strong" in text else 70
        elif any(token in text for token in ("dai_cat", "rat_cat", "rất_cát")):
            target = 90
        elif any(token in text for token in ("cat", "cát", "auspicious")):
            target = 90
        else:
            target = 80

        best = min(
            rules,
            key=lambda row: abs(int(float(row.get("priority_level") or 0)) - target),
        )
        return best

    def _importance_rank(self, importance: str) -> int:
        """Resolve importance rank from Pack 01 muc_do / loai tokens."""
        key = self._norm(importance)
        if key in IMPORTANCE_RANK:
            return IMPORTANCE_RANK[key]
        for token, rank in IMPORTANCE_RANK.items():
            if token in key or key in token:
                return rank
        return 50

    def _lookup_row(
        self,
        label: str,
        shensha_id: str,
        lookup: dict[str, dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Resolve Pack 01 row by label or id."""
        for key in (label, shensha_id):
            row = lookup.get(self._norm(key))
            if row is not None:
                return row
        # Fuzzy: strip spaces / compare without diacritics-ish underscore form.
        label_n = self._norm(label)
        for key, row in lookup.items():
            if key.replace("_", "") == label_n.replace("_", ""):
                return row
        return None

    @staticmethod
    def _norm(value: str) -> str:
        return value.strip().lower().replace(" ", "_").replace("-", "_")
