"""Ten Gods Interpretation Rule Engine.

Enriches Pack 02 Ten Gods facts with Pack 01 identity / strength / score rules.
Does not call TenGodsEngine.evaluate or ScoreEngine.calculate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.constants import (
    FAVORABLE_TOKENS,
    GOD_ID_TO_LABEL,
    STRENGTH_DIMENSIONS,
    UNFAVORABLE_TOKENS,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.extractor import (
    TenGodFavorabilityFact,
    TenGodInteractionFact,
    TenGodPresenceFact,
    TenGodsFacts,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.models import (
    TenGodsItemResult,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.rule_loader import (
    TenGodsRuleLoader,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class TenGodsRuleEngineResult:
    """Rule-engine output for Ten Gods Interpreter."""

    ten_gods: tuple[TenGodsItemResult, ...]
    distribution: tuple[TenGodsItemResult, ...]
    strength: tuple[TenGodsItemResult, ...]
    interactions: tuple[TenGodsItemResult, ...]
    ten_gods_score: float
    dominant_god: str
    matched_rule_ids: tuple[str, ...]
    reasoning: str


class TenGodsInterpretationRuleEngine:
    """Rule Engine for Ten Gods Interpreter."""

    def __init__(
        self,
        *,
        loader: TenGodsRuleLoader | None = None,
    ) -> None:
        """Initialize with Pack 01 Ten Gods rule loader."""
        self.loader = loader or TenGodsRuleLoader()

    def evaluate(self, facts: TenGodsFacts) -> TenGodsRuleEngineResult:
        """Interpret Ten Gods / Distribution / Strength / Interaction."""
        identity_lookup = self.loader.identity_by_label()
        strength_lookup = self.loader.strength_by_label()
        favor_map = {item.god_id: item for item in facts.favorability}

        ten_gods = tuple(
            self._enrich_presence(
                item,
                favor=favor_map.get(item.god_id),
                identity_lookup=identity_lookup,
            )
            for item in facts.presence
        )
        distribution = self._build_distribution(facts, ten_gods)
        strength = self._build_strength(
            facts=facts,
            ten_gods=ten_gods,
            strength_lookup=strength_lookup,
        )
        interactions = self._build_interactions(facts)

        ten_gods_score = self._compute_score(
            facts=facts,
            ten_gods=ten_gods,
            strength=strength,
            interactions=interactions,
        )
        dominant = facts.dominant_god
        if not dominant and distribution:
            dominant = max(distribution, key=lambda item: item.count).item_id

        matched_ids = list(facts.matched_rules)
        for item in (*ten_gods, *distribution, *strength, *interactions):
            for key in ("pack01_rule_id", "score_rule_id", "interpretation_rule_id"):
                rule_id = str(item.attributes.get(key) or "")
                if rule_id:
                    matched_ids.append(rule_id)

        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        reasoning = facts.reasoning
        if not reasoning:
            parts = [
                f"ten_gods={len(ten_gods)}",
                f"distribution={len(distribution)}",
                f"strength={len(strength)}",
                f"interaction={len(interactions)}",
            ]
            reasoning = "Ten Gods interpretation: " + ", ".join(parts)

        logger.info(
            "ten_gods_rule_engine_evaluated",
            extra={
                "ten_gods_count": len(ten_gods),
                "distribution_count": len(distribution),
                "strength_count": len(strength),
                "interaction_count": len(interactions),
                "ten_gods_score": ten_gods_score,
            },
        )

        return TenGodsRuleEngineResult(
            ten_gods=ten_gods,
            distribution=distribution,
            strength=strength,
            interactions=interactions,
            ten_gods_score=ten_gods_score,
            dominant_god=dominant,
            matched_rule_ids=tuple(ordered_ids),
            reasoning=reasoning,
        )

    def _enrich_presence(
        self,
        fact: TenGodPresenceFact,
        *,
        favor: TenGodFavorabilityFact | None,
        identity_lookup: dict[str, dict[str, Any]],
    ) -> TenGodsItemResult:
        """Enrich one presence fact with Pack 01 identity + score rules."""
        # Prefer canonical Pack 01 label from god_id when known.
        label = GOD_ID_TO_LABEL.get(fact.god_id) or fact.label or fact.god_id
        identity = self._lookup_identity(label, fact.god_id, identity_lookup)
        favorability = favor.favorability if favor else ""
        score_row = self._match_god_score(label, favorability)
        interp = self._match_interpretation(label, fact.count, favorability)

        score = float(score_row.get("score") or 0.0) if score_row else 0.0
        if score == 0.0 and interp is not None:
            score = float(interp.get("score") or 0.0)

        priority = int(float((score_row or {}).get("priority") or 0))
        description = ""
        if identity is not None:
            description = str(identity.get("ten") or identity.get("ma_thap_than") or "")
        if interp is not None and interp.get("title"):
            description = str(interp.get("title") or description)

        return TenGodsItemResult(
            item_id=fact.god_id or label,
            item_type="ten_god",
            label=label,
            count=fact.count,
            score=score,
            priority=priority,
            status=favorability or str((identity or {}).get("loai") or ""),
            description=description,
            attributes={
                "pack01_rule_id": str(
                    (identity or {}).get("ma_thap_than")
                    or (identity or {}).get("ten")
                    or ""
                ),
                "score_rule_id": str((score_row or {}).get("id") or ""),
                "interpretation_rule_id": str((interp or {}).get("rule_id") or ""),
                "source_pillar": fact.source_pillar,
                "source_stem": fact.source_stem,
                "polarity_class": fact.polarity_class,
                "favorability": favorability,
                "loai": str((identity or {}).get("loai") or ""),
            },
        )

    def _build_distribution(
        self,
        facts: TenGodsFacts,
        ten_gods: tuple[TenGodsItemResult, ...],
    ) -> tuple[TenGodsItemResult, ...]:
        """Build distribution items from counts."""
        counts: dict[str, int] = dict(facts.distribution)
        labels: dict[str, str] = {}
        for item in ten_gods:
            key = item.item_id
            labels[key] = item.label
            counts[key] = max(counts.get(key, 0), item.count)

        items: list[TenGodsItemResult] = []
        total = sum(counts.values()) or 1
        for god_id, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
            label = labels.get(god_id) or GOD_ID_TO_LABEL.get(god_id, god_id)
            ratio = round(count / total, 4)
            items.append(
                TenGodsItemResult(
                    item_id=god_id,
                    item_type="distribution",
                    label=label,
                    count=count,
                    score=float(count),
                    priority=count,
                    status="dominant" if god_id == facts.dominant_god else "present",
                    description=f"{label} x{count}",
                    attributes={"ratio": ratio},
                )
            )
        return tuple(items)

    def _build_strength(
        self,
        *,
        facts: TenGodsFacts,
        ten_gods: tuple[TenGodsItemResult, ...],
        strength_lookup: dict[str, dict[str, Any]],
    ) -> tuple[TenGodsItemResult, ...]:
        """Build strength contribution items from diem_thap_than + strength interactions."""
        items: list[TenGodsItemResult] = []
        for god in ten_gods:
            row = strength_lookup.get(self._norm(god.label))
            if row is None:
                continue
            unit = float(row.get("diem") or 0.0)
            score = unit * max(1, god.count)
            items.append(
                TenGodsItemResult(
                    item_id=god.item_id,
                    item_type="strength",
                    label=god.label,
                    count=god.count,
                    score=score,
                    priority=int(abs(score)),
                    status=str(row.get("anh_huong") or ""),
                    description=str(row.get("anh_huong") or ""),
                    attributes={
                        "pack01_rule_id": str(row.get("thap_than") or ""),
                        "unit_score": unit,
                        "anh_huong": str(row.get("anh_huong") or ""),
                    },
                )
            )

        for interaction in facts.interactions:
            if self._norm(interaction.dimension) not in {
                self._norm(token) for token in STRENGTH_DIMENSIONS
            } and "strength" not in interaction.dimension.lower():
                continue
            label = GOD_ID_TO_LABEL.get(
                interaction.god_id, interaction.god_id or interaction.upstream_class
            )
            items.append(
                TenGodsItemResult(
                    item_id=f"strength_ix_{interaction.god_id}_{interaction.upstream_class}",
                    item_type="strength_interaction",
                    label=label,
                    count=1,
                    score=0.0,
                    priority=interaction.priority,
                    status=interaction.effect,
                    description=interaction.effect,
                    attributes={
                        "dimension": interaction.dimension,
                        "upstream_class": interaction.upstream_class,
                        "effect": interaction.effect,
                    },
                )
            )
        return tuple(items)

    def _build_interactions(
        self,
        facts: TenGodsFacts,
    ) -> tuple[TenGodsItemResult, ...]:
        """Build interaction items from relationships + interactions + Pack 01 combos."""
        combo_rules = self.loader.load_combination_rules()
        items: list[TenGodsItemResult] = []

        for relation in facts.relationships:
            left = GOD_ID_TO_LABEL.get(relation.left_god_id, relation.left_god_id)
            right = GOD_ID_TO_LABEL.get(relation.right_god_id, relation.right_god_id)
            matched = self._match_combination(
                relation.relation, left, right, combo_rules
            )
            score = float(matched.get("score") or 0.0) if matched else 0.0
            items.append(
                TenGodsItemResult(
                    item_id=f"{relation.left_god_id}_{relation.right_god_id}",
                    item_type="relationship",
                    label=f"{left}-{right}",
                    count=1,
                    score=score,
                    priority=int(
                        float((matched or {}).get("priority") or relation.priority or 0)
                    ),
                    status=relation.relation,
                    description=str((matched or {}).get("description") or relation.relation),
                    attributes={
                        "score_rule_id": str((matched or {}).get("id") or ""),
                        "rule_code": str((matched or {}).get("rule_code") or ""),
                        "left_god_id": relation.left_god_id,
                        "right_god_id": relation.right_god_id,
                        "relation": relation.relation,
                    },
                )
            )

        for interaction in facts.interactions:
            if "strength" in interaction.dimension.lower():
                continue
            label = GOD_ID_TO_LABEL.get(interaction.god_id, interaction.god_id)
            matched = self._match_combination(
                f"{interaction.effect} {interaction.upstream_class}",
                label,
                "",
                combo_rules,
            )
            score = float(matched.get("score") or 0.0) if matched else 0.0
            items.append(
                TenGodsItemResult(
                    item_id=f"{interaction.dimension}_{interaction.god_id}",
                    item_type="interaction",
                    label=label,
                    count=1,
                    score=score,
                    priority=int(
                        float(
                            (matched or {}).get("priority") or interaction.priority or 0
                        )
                    ),
                    status=interaction.effect,
                    description=str(
                        (matched or {}).get("description") or interaction.effect
                    ),
                    attributes={
                        "score_rule_id": str((matched or {}).get("id") or ""),
                        "dimension": interaction.dimension,
                        "upstream_class": interaction.upstream_class,
                        "effect": interaction.effect,
                    },
                )
            )
        return tuple(items)

    def _compute_score(
        self,
        *,
        facts: TenGodsFacts,
        ten_gods: tuple[TenGodsItemResult, ...],
        strength: tuple[TenGodsItemResult, ...],
        interactions: tuple[TenGodsItemResult, ...],
    ) -> float:
        """Aggregate Ten Gods / strength / interaction scores."""
        if facts.ten_gods_score is not None and not (
            ten_gods or strength or interactions
        ):
            return float(facts.ten_gods_score)

        total = 0.0
        apply_counts: dict[str, int] = {}

        def _add(rule_id: str, score: float, max_apply: int = 99) -> None:
            nonlocal total
            used = apply_counts.get(rule_id, 0)
            if rule_id and max_apply > 0 and used >= max_apply:
                return
            total += score
            if rule_id:
                apply_counts[rule_id] = used + 1

        for item in ten_gods:
            _add(str(item.attributes.get("score_rule_id") or item.item_id), item.score)
        for item in strength:
            if item.item_type == "strength":
                _add(str(item.attributes.get("pack01_rule_id") or item.item_id), item.score)
        for item in interactions:
            _add(str(item.attributes.get("score_rule_id") or item.item_id), item.score)

        if total == 0.0 and facts.ten_gods_score is not None:
            return float(facts.ten_gods_score)
        return total

    def _match_god_score(
        self,
        label: str,
        favorability: str,
    ) -> dict[str, Any] | None:
        """Pick positive or negative Pack 01 score row for a Ten God."""
        fav = self._norm(favorability)
        fav_tokens = {part for part in fav.replace(",", "_").split("_") if part}
        use_negative = bool(fav_tokens & {self._norm(token) for token in UNFAVORABLE_TOKENS})
        use_positive = bool(fav_tokens & {self._norm(token) for token in FAVORABLE_TOKENS})
        # Exact whole-string match as fallback (covers single-token values).
        if not use_negative and fav in {self._norm(token) for token in UNFAVORABLE_TOKENS}:
            use_negative = True
        if not use_positive and fav in {self._norm(token) for token in FAVORABLE_TOKENS}:
            use_positive = True
        # Prefer explicit unfavorable over substring collisions (e.g. un+favorable).
        if use_negative and use_positive and "unfavorable" in fav:
            use_positive = False
        rules = (
            self.loader.load_negative_rules()
            if use_negative and not use_positive
            else self.loader.load_positive_rules()
        )
        label_n = self._norm(label)
        for row in rules:
            if self._norm(str(row.get("ten_god") or "")) == label_n:
                return row
        if use_negative:
            for row in self.loader.load_negative_rules():
                if self._norm(str(row.get("ten_god") or "")) == label_n:
                    return row
        return None

    def _match_interpretation(
        self,
        label: str,
        count: int,
        favorability: str,
    ) -> dict[str, Any] | None:
        """Match Pack 01 interpretation_rules row by god + status heuristic."""
        label_n = self._norm(label)
        status_hint = "Vượng" if count > 2 else "Cân bằng"
        fav = self._norm(favorability)
        fav_tokens = {part for part in fav.replace(",", "_").split("_") if part}
        if fav_tokens & {self._norm(token) for token in UNFAVORABLE_TOKENS} or fav in {
            self._norm(token) for token in UNFAVORABLE_TOKENS
        }:
            status_hint = "Vượng"
        candidates = [
            row
            for row in self.loader.load_interpretation_rules()
            if self._norm(str(row.get("ten_god") or "")) == label_n
        ]
        if not candidates:
            return None
        for row in candidates:
            if str(row.get("status") or "") == status_hint:
                return row
        return candidates[0]

    def _match_combination(
        self,
        text: str,
        left: str,
        right: str,
        rules: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Match combination score rule by condition / description overlap."""
        blob = self._norm(f"{text} {left} {right}")
        if not blob.strip("_"):
            return None
        best: dict[str, Any] | None = None
        best_hits = 0
        for row in rules:
            condition = self._norm(str(row.get("condition") or ""))
            rule_code = self._norm(str(row.get("rule_code") or ""))
            hits = 0
            for token in condition.replace("_", " ").split():
                if len(token) >= 3 and token in blob:
                    hits += 1
            if rule_code and rule_code in blob:
                hits += 2
            if hits > best_hits:
                best = row
                best_hits = hits
        return best if best_hits > 0 else None

    def _lookup_identity(
        self,
        label: str,
        god_id: str,
        identity_lookup: dict[str, dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Resolve Pack 01 identity row for a god."""
        for key in (label, god_id, GOD_ID_TO_LABEL.get(god_id, "")):
            row = identity_lookup.get(self._norm(key))
            if row is not None:
                return row
        # ASCII Pack 01 ten values use underscores without diacritics.
        ascii_map = {
            "bi_jian": "ty_kien",
            "jie_cai": "kiep_tai",
            "shi_shen": "thuc_than",
            "shang_guan": "thuong_quan",
            "pian_cai": "thien_tai",
            "zheng_cai": "chinh_tai",
            "qi_sha": "that_sat",
            "zheng_guan": "chinh_quan",
            "pian_yin": "thien_an",
            "zheng_yin": "chinh_an",
        }
        ascii_key = ascii_map.get(god_id)
        if ascii_key:
            return identity_lookup.get(ascii_key)
        return None

    @staticmethod
    def _norm(value: str) -> str:
        return value.strip().lower().replace(" ", "_").replace("-", "_")
