"""Luck Interpretation Rule Engine.

Enriches Pack 02 Luck facts with Pack 01 dai_van / luck score / interpretation rules.
Does not call LuckEngine.evaluate or ScoreEngine.calculate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.interpreter_runtime.interpreters.luck.constants import (
    ATTACK_EFFECT_TOKENS,
    FAVORABLE_TOKENS,
    SUPPORT_EFFECT_TOKENS,
    UNFAVORABLE_TOKENS,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.extractor import (
    LuckFacts,
    LuckInteractionFact,
    LuckLayerFact,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.models import (
    LuckItemResult,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.rule_loader import (
    LuckRuleLoader,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LuckRuleEngineResult:
    """Rule-engine output for Luck Interpreter."""

    dayun: tuple[LuckItemResult, ...]
    liunian: tuple[LuckItemResult, ...]
    liuyue: tuple[LuckItemResult, ...]
    interactions: tuple[LuckItemResult, ...]
    luck_score: float
    matched_rule_ids: tuple[str, ...]
    reasoning: str


class LuckInterpretationRuleEngine:
    """Rule Engine for Luck Interpreter."""

    def __init__(
        self,
        *,
        loader: LuckRuleLoader | None = None,
    ) -> None:
        """Initialize with Pack 01 Luck rule loader."""
        self.loader = loader or LuckRuleLoader()

    def evaluate(self, facts: LuckFacts) -> LuckRuleEngineResult:
        """Interpret Dayun / Liunian / Liuyue / Interaction."""
        dayun = tuple(
            self._enrich_layer(item, default_type="dayun", luck_type="Đại Vận")
            for item in facts.dayun
        )
        liunian = tuple(
            self._enrich_layer(item, default_type="liunian", luck_type="Lưu Niên")
            for item in facts.liunian
        )
        liuyue = tuple(
            self._enrich_layer(item, default_type="liuyue", luck_type="Lưu Nguyệt")
            for item in facts.liuyue
        )
        interactions = tuple(
            self._enrich_interaction(item) for item in facts.interactions
        )

        luck_score = self._compute_score(
            facts=facts,
            dayun=dayun,
            liunian=liunian,
            liuyue=liuyue,
            interactions=interactions,
        )

        matched_ids = list(facts.matched_rules)
        for item in (*dayun, *liunian, *liuyue, *interactions):
            for key in (
                "pack01_rule_id",
                "score_rule_id",
                "interpretation_rule_id",
                "priority_rule_id",
                "catalog_rule_id",
            ):
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
                f"dayun={len(dayun)}",
                f"liunian={len(liunian)}",
                f"liuyue={len(liuyue)}",
                f"interaction={len(interactions)}",
            ]
            reasoning = "Luck interpretation: " + ", ".join(parts)

        logger.info(
            "luck_rule_engine_evaluated",
            extra={
                "dayun_count": len(dayun),
                "liunian_count": len(liunian),
                "liuyue_count": len(liuyue),
                "interaction_count": len(interactions),
                "luck_score": luck_score,
            },
        )

        return LuckRuleEngineResult(
            dayun=dayun,
            liunian=liunian,
            liuyue=liuyue,
            interactions=interactions,
            luck_score=luck_score,
            matched_rule_ids=tuple(ordered_ids),
            reasoning=reasoning,
        )

    def _enrich_layer(
        self,
        fact: LuckLayerFact,
        *,
        default_type: str,
        luck_type: str,
    ) -> LuckItemResult:
        """Enrich one Dayun/Liunian/Liuyue layer with Pack 01 rules."""
        favorability = fact.favorability or fact.activation or ""
        score_row = self._match_layer_score(favorability, fact.ten_god, default_type)
        interp = self._match_interpretation(luck_type, favorability, fact.ten_god)
        priority_row = self._match_priority_weight(favorability)
        catalog = self._match_catalog(default_type, favorability)

        score = float(score_row.get("score") or 0.0) if score_row else 0.0
        if score == 0.0 and interp is not None:
            score = float(interp.get("score") or 0.0)

        priority = int(
            float(
                (score_row or {}).get("priority")
                or fact.priority
                or (priority_row or {}).get("priority_level")
                or 0
            )
        )
        description = str(
            (interp or {}).get("meaning")
            or (interp or {}).get("title")
            or (score_row or {}).get("description")
            or (catalog or {}).get("mo_ta")
            or ""
        )
        recommendation = str((interp or {}).get("recommendation") or "")
        label = fact.label or fact.ganzhi or f"{fact.stem}{fact.branch}".strip()

        return LuckItemResult(
            item_id=label or default_type,
            item_type=default_type,
            label=label,
            layer=fact.layer or default_type,
            stem=fact.stem,
            branch=fact.branch,
            ganzhi=fact.ganzhi or label,
            favorability=favorability,
            status=fact.status or "active",
            score=score,
            priority=priority,
            description=description,
            recommendation=recommendation,
            attributes={
                "score_rule_id": str((score_row or {}).get("id") or ""),
                "interpretation_rule_id": str((interp or {}).get("rule_id") or ""),
                "priority_rule_id": str((priority_row or {}).get("id") or ""),
                "catalog_rule_id": str((catalog or {}).get("ma_nhom") or ""),
                "priority_weight": float((priority_row or {}).get("weight") or 1.0),
                "ten_god": fact.ten_god,
                "element": fact.element,
                "activation": fact.activation,
                "timing_phase": fact.timing_phase,
                "start_age": fact.start_age,
                "end_age": fact.end_age,
                "year": fact.year,
                "month": fact.month,
                "title": str((interp or {}).get("title") or ""),
            },
        )

    def _enrich_interaction(self, fact: LuckInteractionFact) -> LuckItemResult:
        """Enrich one luck interaction with Pack 01 combination/clash scores."""
        effect = fact.effect or fact.dimension or ""
        score_row = self._match_interaction_score(effect, fact.upstream_class)
        score = float(score_row.get("score") or 0.0) if score_row else 0.0
        priority = int(
            float((score_row or {}).get("priority") or fact.priority or 0)
        )
        label = f"{fact.layer}:{effect}" if fact.layer else effect
        return LuckItemResult(
            item_id=label or "interaction",
            item_type="interaction",
            label=label,
            layer=fact.layer,
            favorability=fact.upstream_class,
            status=effect,
            score=score,
            priority=priority,
            description=str(
                (score_row or {}).get("description") or effect or fact.dimension
            ),
            attributes={
                "score_rule_id": str((score_row or {}).get("id") or ""),
                "dimension": fact.dimension,
                "upstream_class": fact.upstream_class,
                "effect": effect,
                "rule_code": str((score_row or {}).get("rule_code") or ""),
            },
        )

    def _compute_score(
        self,
        *,
        facts: LuckFacts,
        dayun: tuple[LuckItemResult, ...],
        liunian: tuple[LuckItemResult, ...],
        liuyue: tuple[LuckItemResult, ...],
        interactions: tuple[LuckItemResult, ...],
    ) -> float:
        """Aggregate luck layer + interaction scores."""
        items = (*dayun, *liunian, *liuyue, *interactions)
        if facts.luck_score is not None and not items:
            return float(facts.luck_score)

        total = 0.0
        apply_counts: dict[str, int] = {}
        score_lookup = {
            str(row.get("id") or ""): row
            for row in (
                *self.loader.load_support_rules(),
                *self.loader.load_attack_rules(),
                *self.loader.load_combination_rules(),
                *self.loader.load_clash_rules(),
            )
        }

        for item in items:
            rule_id = str(item.attributes.get("score_rule_id") or item.item_id)
            max_apply = 99
            row = score_lookup.get(rule_id)
            if row is not None:
                max_apply = int(float(row.get("max_apply") or 99))
            used = apply_counts.get(rule_id, 0)
            if rule_id and max_apply > 0 and used >= max_apply:
                continue
            weight = float(item.attributes.get("priority_weight") or 1.0)
            total += float(item.score) * weight
            if rule_id:
                apply_counts[rule_id] = used + 1

        if facts.support_level is not None:
            total += float(facts.support_level)
        if facts.attack_level is not None:
            total += float(facts.attack_level)

        if total == 0.0 and facts.luck_score is not None:
            return float(facts.luck_score)
        return total

    def _polarity(self, favorability: str) -> tuple[bool, bool]:
        """Return (use_support, use_attack) from favorability text."""
        fav = self._norm(favorability)
        fav_tokens = self._token_set(favorability)
        support_norms = {self._norm(token) for token in FAVORABLE_TOKENS}
        attack_norms = {self._norm(token) for token in UNFAVORABLE_TOKENS}
        use_support = bool(fav_tokens & support_norms) or any(
            token in fav
            for token in (
                "dung_than",
                "hy_than",
                "favorable",
                "support",
                "useful",
                "good",
                "cat",
            )
        )
        use_attack = bool(fav_tokens & attack_norms) or any(
            token in fav
            for token in (
                "ky_than",
                "unfavorable",
                "attack",
                "clash",
                "destroy",
                "hung",
                "bad",
            )
        )
        if use_attack and use_support and "unfavorable" in fav:
            use_support = False
        if use_attack and use_support and "ky_than" in fav:
            use_support = False
        return use_support, use_attack

    def _match_layer_score(
        self,
        favorability: str,
        ten_god: str,
        layer: str,
    ) -> dict[str, Any] | None:
        """Pick support or attack score row from Pack 01 luck tables."""
        use_support, use_attack = self._polarity(favorability)
        god_tokens = self._token_set(ten_god)
        fav_tokens = self._token_set(favorability)

        # Neutral layers: no forced default support/attack score.
        if not use_support and not use_attack:
            blob = self._norm(f"{favorability} {ten_god} {layer}")
            return self._best_token_match(
                [
                    *self.loader.load_support_rules(),
                    *self.loader.load_attack_rules(),
                ],
                blob,
                extra_tokens=fav_tokens | god_tokens,
            )

        rules = (
            self.loader.load_attack_rules()
            if use_attack and not use_support
            else self.loader.load_support_rules()
        )
        blob = self._norm(f"{favorability} {ten_god} {layer}")
        best = self._best_token_match(rules, blob, extra_tokens=fav_tokens | god_tokens)
        if best is not None:
            return best

        defaults = (
            ("USEFUL_GOD_ATTACK", "DAY_MASTER_ATTACK", "GOOD_LUCK")
            if use_attack and not use_support
            else ("USEFUL_GOD_SUPPORT", "DAY_MASTER_SUPPORT", "GOOD_LUCK")
        )
        pool = (
            self.loader.load_attack_rules()
            if use_attack and not use_support
            else self.loader.load_support_rules()
        )
        for code in defaults:
            for row in pool:
                if str(row.get("rule_code") or "") == code:
                    return row
        return pool[0] if pool else None

    def _match_interpretation(
        self,
        luck_type: str,
        favorability: str,
        ten_god: str,
    ) -> dict[str, Any] | None:
        """Match Pack 01 luck_rules.csv by luck_type + favorability heuristic."""
        type_n = self._norm(luck_type)
        fav = self._norm(favorability)
        use_support, use_attack = self._polarity(favorability)
        want_dung = use_support
        want_ky = use_attack

        candidates = [
            row
            for row in self.loader.load_interpretation_rules()
            if self._norm(str(row.get("luck_type") or "")) == type_n
            or type_n in self._norm(str(row.get("luck_type") or ""))
        ]
        if not candidates:
            candidates = list(self.loader.load_interpretation_rules())

        scored: list[tuple[int, dict[str, Any]]] = []
        for row in candidates:
            condition = self._norm(str(row.get("condition") or ""))
            hits = 0
            if want_dung and "dung_than" in condition:
                hits += 3
            if want_ky and "ky_than" in condition:
                hits += 3
            if ten_god and self._norm(ten_god) in condition:
                hits += 2
            if fav and fav in condition:
                hits += 1
            scored.append((hits, row))
        scored.sort(key=lambda item: (-item[0], str(item[1].get("rule_id") or "")))
        if scored and scored[0][0] > 0:
            return scored[0][1]
        return candidates[0] if candidates else None

    def _match_priority_weight(self, favorability: str) -> dict[str, Any] | None:
        """Map favorability to Pack 01 luck priority weight row."""
        rules = self.loader.load_priority_rules()
        if not rules:
            return None
        fav = self._norm(favorability)
        use_support, use_attack = self._polarity(favorability)
        if use_attack:
            target = 50 if any(token in fav for token in ("destroy", "pha", "phá")) else 60
        elif use_support:
            target = 100 if "dung" in fav or "useful" in fav else 90
        else:
            target = 85
        return min(
            rules,
            key=lambda row: abs(int(float(row.get("priority_level") or 0)) - target),
        )

    def _match_catalog(
        self,
        layer: str,
        favorability: str,
    ) -> dict[str, Any] | None:
        """Map layer / favorability to dai_van catalog group."""
        catalog = self.loader.catalog_by_code()
        layer_n = self._norm(layer)
        fav = self._norm(favorability)
        code = "DV004"
        if layer_n in {"liunian", "liu_nian", "luu_nien", "tieu_van"}:
            code = "DV006"
        elif layer_n in {"liuyue", "liu_yue", "luu_nguyet"}:
            code = "DV005"
        if any(token in fav for token in ("dung", "useful", "support")):
            code = "DV023"
        elif any(token in fav for token in ("ky", "attack", "unfavorable")):
            code = "DV025"
        elif any(token in fav for token in ("cat", "cát", "good")):
            code = "DV036"
        elif any(token in fav for token in ("hung", "bad")):
            code = "DV037"
        return catalog.get(code)

    def _best_token_match(
        self,
        rules: list[dict[str, Any]],
        blob: str,
        *,
        extra_tokens: set[str],
    ) -> dict[str, Any] | None:
        """Pick score rule with strongest token overlap against condition/code."""
        best: dict[str, Any] | None = None
        best_hits = 0
        for row in rules:
            condition = self._norm(str(row.get("condition") or ""))
            rule_code = self._norm(str(row.get("rule_code") or ""))
            description = self._norm(str(row.get("description") or ""))
            hits = 0
            for token in condition.replace("_", " ").split():
                if len(token) >= 3 and token in blob:
                    hits += 1
            for token in extra_tokens:
                if len(token) >= 3 and (
                    token in condition or token in rule_code or token in description
                ):
                    hits += 1
            if rule_code and rule_code in blob:
                hits += 2
            if hits > best_hits:
                best = row
                best_hits = hits
        return best if best_hits > 0 else None

    def _token_set(self, value: str) -> set[str]:
        """Normalize text into comparable token set."""
        normed = self._norm(value)
        return {part for part in normed.replace(",", "_").split("_") if part}

    @staticmethod
    def _norm(value: str) -> str:
        return value.strip().lower().replace(" ", "_").replace("-", "_")
