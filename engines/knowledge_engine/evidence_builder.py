"""Evidence Builder — RuleContext → deduplicated EvidencePackage."""

from __future__ import annotations

import logging
from typing import Any, Mapping

from engines.knowledge_engine.evidence_models import (
    CATEGORY_LABELS,
    EVIDENCE_CATEGORIES,
    EvidenceItem,
    EvidencePackage,
)
from engines.rule_contract.models import normalize_context, resolve_path

logger = logging.getLogger(__name__)


class EvidenceBuilder:
    """Build an evidence package from RuleContext.

    Categories:
    BaZi, Five Elements, Ten Gods, Useful God, Pattern, Strength, Temperature, ShenSha.

    Each item stores: rule, reason, confidence, source.
    Duplicate evidence (same category + rule + source) is discarded.
    """

    def build(self, rule_context: Mapping[str, Any] | Any) -> EvidencePackage:
        """Extract categorized evidence from RuleContext.

        Args:
            rule_context: Production RuleContext mapping.

        Returns:
            ``EvidencePackage`` with deduplicated items and metadata.trace.
        """
        context = normalize_context(rule_context)
        collected: list[EvidenceItem] = []
        trace: list[dict[str, Any]] = []

        collectors = (
            ("bazi", self._collect_bazi),
            ("five_elements", self._collect_five_elements),
            ("ten_gods", self._collect_ten_gods),
            ("useful_god", self._collect_useful_god),
            ("pattern", self._collect_pattern),
            ("strength", self._collect_strength),
            ("temperature", self._collect_temperature),
            ("shensha", self._collect_shensha),
        )

        for category, collector in collectors:
            before = len(collected)
            collector(context, collected)
            added = collected[before:]
            trace.append(
                {
                    "category": category,
                    "category_label": CATEGORY_LABELS[category],
                    "candidate_count": len(added),
                    "rules": [item.rule for item in added],
                }
            )

        unique_items, duplicate_count = self._dedupe(collected)
        categories = {key: [] for key in EVIDENCE_CATEGORIES}
        for item in unique_items:
            categories.setdefault(item.category, []).append(item)

        package = EvidencePackage(
            items=unique_items,
            categories=categories,
            metadata={
                "trace": trace,
                "category_count": len(EVIDENCE_CATEGORIES),
                "item_count": len(unique_items),
                "duplicate_removed": duplicate_count,
                "categories_present": [
                    key for key, rows in categories.items() if rows
                ],
            },
        )
        logger.debug(
            "Evidence package built items=%s duplicates_removed=%s",
            len(unique_items),
            duplicate_count,
        )
        return package

    def _dedupe(self, items: list[EvidenceItem]) -> tuple[list[EvidenceItem], int]:
        seen: set[str] = set()
        unique: list[EvidenceItem] = []
        duplicates = 0
        for item in items:
            key = item.dedupe_key
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
            unique.append(item)
        return unique, duplicates

    def _add(
        self,
        bucket: list[EvidenceItem],
        *,
        category: str,
        rule: str,
        reason: str,
        confidence: float,
        source: str,
    ) -> None:
        text_rule = str(rule or "").strip()
        if not text_rule:
            return
        conf = float(confidence)
        if conf < 0.0:
            conf = 0.0
        if conf > 1.0:
            conf = 1.0
        bucket.append(
            EvidenceItem(
                category=category,
                rule=text_rule,
                reason=str(reason or "").strip(),
                confidence=conf,
                source=str(source or "").strip(),
            )
        )

    def _as_list(self, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, Mapping):
            out: list[str] = []
            for key, item in value.items():
                if item is True or item not in (None, False, "", 0):
                    out.append(str(key))
                out.extend(self._as_list(item))
            return [text.strip() for text in out if str(text).strip()]
        if isinstance(value, (list, tuple, set)):
            out = []
            for item in value:
                out.extend(self._as_list(item))
            return out
        text = str(value).strip()
        return [text] if text else []

    def _first(self, *values: Any) -> str | None:
        for value in values:
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                for item in value:
                    text = str(item).strip()
                    if text:
                        return text
                continue
            text = str(value).strip()
            if text and text.lower() not in {"none", "null", "--"}:
                return text
        return None

    def _collect_bazi(self, context: Mapping[str, Any], out: list[EvidenceItem]) -> None:
        bazi = context.get("bazi") if isinstance(context.get("bazi"), Mapping) else {}
        day_master = self._first(context.get("day_master"), bazi.get("day_master"))
        if day_master:
            self._add(
                out,
                category="bazi",
                rule=f"day_master={day_master}",
                reason=f"Day Master is {day_master}.",
                confidence=0.98,
                source="rule_context:bazi.day_master",
            )

        element = self._first(
            context.get("day_master_element"),
            bazi.get("day_master_element"),
        )
        if element:
            self._add(
                out,
                category="bazi",
                rule=f"day_master_element={element}",
                reason=f"Day Master element is {element}.",
                confidence=0.97,
                source="rule_context:bazi.day_master_element",
            )

        yin_yang = self._first(bazi.get("day_master_yin_yang"), bazi.get("yin_yang"))
        if yin_yang:
            self._add(
                out,
                category="bazi",
                rule=f"day_master_yin_yang={yin_yang}",
                reason=f"Day Master polarity is {yin_yang}.",
                confidence=0.95,
                source="rule_context:bazi.day_master_yin_yang",
            )

        for pillar_key, label in (
            ("year_pillar", "Year"),
            ("month_pillar", "Month"),
            ("day_pillar", "Day"),
            ("hour_pillar", "Hour"),
        ):
            pillar = bazi.get(pillar_key)
            text = self._pillar_text(pillar)
            if text:
                self._add(
                    out,
                    category="bazi",
                    rule=f"{pillar_key}={text}",
                    reason=f"{label} pillar is {text}.",
                    confidence=0.94,
                    source=f"rule_context:bazi.{pillar_key}",
                )

    def _pillar_text(self, pillar: Any) -> str | None:
        if pillar is None:
            return None
        if isinstance(pillar, Mapping):
            stem = self._first(pillar.get("stem"), pillar.get("thien_can"))
            branch = self._first(pillar.get("branch"), pillar.get("dia_chi"))
            if stem and branch:
                return f"{stem} {branch}"
            return self._first(stem, branch, pillar.get("name"), pillar.get("label"))
        return self._first(pillar)

    def _collect_five_elements(
        self, context: Mapping[str, Any], out: list[EvidenceItem]
    ) -> None:
        wuxing = context.get("wuxing") if isinstance(context.get("wuxing"), Mapping) else {}
        season = self._first(context.get("birth_season"), wuxing.get("season"))
        if season:
            self._add(
                out,
                category="five_elements",
                rule=f"season={season}",
                reason=f"Birth season signal is {season}.",
                confidence=0.9,
                source="rule_context:wuxing.season",
            )

        for element in ("wood", "fire", "earth", "metal", "water", "mộc", "hỏa", "thổ", "kim", "thủy"):
            node = wuxing.get(element)
            if node is None:
                continue
            if isinstance(node, Mapping):
                status = self._first(node.get("status"), node.get("label"), node.get("level"))
                count = node.get("count", node.get("value"))
                if status:
                    self._add(
                        out,
                        category="five_elements",
                        rule=f"{element}.status={status}",
                        reason=f"Five-element {element} status is {status}.",
                        confidence=0.88,
                        source=f"rule_context:wuxing.{element}.status",
                    )
                if count is not None and str(count).strip() != "":
                    self._add(
                        out,
                        category="five_elements",
                        rule=f"{element}.count={count}",
                        reason=f"Five-element {element} count is {count}.",
                        confidence=0.86,
                        source=f"rule_context:wuxing.{element}.count",
                    )
            else:
                self._add(
                    out,
                    category="five_elements",
                    rule=f"{element}={node}",
                    reason=f"Five-element {element} signal is {node}.",
                    confidence=0.84,
                    source=f"rule_context:wuxing.{element}",
                )

    def _collect_ten_gods(self, context: Mapping[str, Any], out: list[EvidenceItem]) -> None:
        ten_gods = context.get("ten_gods") if isinstance(context.get("ten_gods"), Mapping) else {}
        bazi = context.get("bazi") if isinstance(context.get("bazi"), Mapping) else {}
        items = self._as_list(ten_gods.get("items")) or self._as_list(ten_gods.get("unique"))
        if not items:
            items = self._as_list(bazi.get("ten_gods"))

        status = self._first(ten_gods.get("status"))
        if status:
            self._add(
                out,
                category="ten_gods",
                rule=f"status={status}",
                reason=f"Ten Gods status is {status}.",
                confidence=0.9,
                source="rule_context:ten_gods.status",
            )

        for god in items:
            self._add(
                out,
                category="ten_gods",
                rule=f"present={god}",
                reason=f"Ten God '{god}' is present in the chart.",
                confidence=0.92,
                source="rule_context:ten_gods.items",
            )

        by_name = ten_gods.get("by_name")
        if isinstance(by_name, Mapping):
            for name, flag in by_name.items():
                if flag in (False, None, "", 0):
                    continue
                self._add(
                    out,
                    category="ten_gods",
                    rule=f"present={name}",
                    reason=f"Ten God '{name}' is marked present.",
                    confidence=0.9,
                    source="rule_context:ten_gods.by_name",
                )

    def _collect_useful_god(
        self, context: Mapping[str, Any], out: list[EvidenceItem]
    ) -> None:
        useful = context.get("useful_god") if isinstance(context.get("useful_god"), Mapping) else {}
        status = self._first(useful.get("status"))
        name = self._first(useful.get("name"))
        element = self._first(useful.get("element"))
        if status:
            self._add(
                out,
                category="useful_god",
                rule=f"status={status}",
                reason=f"Useful God status is {status}.",
                confidence=0.9,
                source="rule_context:useful_god.status",
            )
        if name:
            self._add(
                out,
                category="useful_god",
                rule=f"name={name}",
                reason=f"Useful God name is {name}.",
                confidence=0.93,
                source="rule_context:useful_god.name",
            )
        if element:
            self._add(
                out,
                category="useful_god",
                rule=f"element={element}",
                reason=f"Useful God element is {element}.",
                confidence=0.93,
                source="rule_context:useful_god.element",
            )
        for key, label in (("favorable", "Favorable"), ("unfavorable", "Unfavorable")):
            values = self._as_list(useful.get(key))
            for value in values:
                self._add(
                    out,
                    category="useful_god",
                    rule=f"{key}={value}",
                    reason=f"{label} factor '{value}' is indicated.",
                    confidence=0.86,
                    source=f"rule_context:useful_god.{key}",
                )

    def _collect_pattern(self, context: Mapping[str, Any], out: list[EvidenceItem]) -> None:
        pattern = context.get("pattern") if isinstance(context.get("pattern"), Mapping) else {}
        main = self._first(pattern.get("main_pattern"), pattern.get("name"))
        if main:
            self._add(
                out,
                category="pattern",
                rule=f"main_pattern={main}",
                reason=f"Main pattern is {main}.",
                confidence=0.94,
                source="rule_context:pattern.main_pattern",
            )
        status = self._first(pattern.get("status"))
        if status:
            self._add(
                out,
                category="pattern",
                rule=f"status={status}",
                reason=f"Pattern status is {status}.",
                confidence=0.88,
                source="rule_context:pattern.status",
            )
        follow = self._first(pattern.get("follow_type"), pattern.get("tong_cach"))
        if follow:
            self._add(
                out,
                category="pattern",
                rule=f"follow_type={follow}",
                reason=f"Follow pattern signal is {follow}.",
                confidence=0.86,
                source="rule_context:pattern.follow_type",
            )
        category = self._first(pattern.get("category"))
        if category:
            self._add(
                out,
                category="pattern",
                rule=f"category={category}",
                reason=f"Pattern category is {category}.",
                confidence=0.84,
                source="rule_context:pattern.category",
            )

    def _collect_strength(self, context: Mapping[str, Any], out: list[EvidenceItem]) -> None:
        strength = context.get("strength") if isinstance(context.get("strength"), Mapping) else {}
        level = self._first(strength.get("level"), resolve_path(context, "strength.level"))
        if level:
            self._add(
                out,
                category="strength",
                rule=f"level={level}",
                reason=f"Day Master strength level is {level}.",
                confidence=0.94,
                source="rule_context:strength.level",
            )
        for key, label in (
            ("month_status", "Month status"),
            ("root_level", "Root level"),
            ("support_type", "Support type"),
            ("control_type", "Control type"),
        ):
            value = self._first(strength.get(key))
            if value:
                self._add(
                    out,
                    category="strength",
                    rule=f"{key}={value}",
                    reason=f"{label} is {value}.",
                    confidence=0.87,
                    source=f"rule_context:strength.{key}",
                )

    def _collect_temperature(
        self, context: Mapping[str, Any], out: list[EvidenceItem]
    ) -> None:
        temperature = (
            context.get("temperature") if isinstance(context.get("temperature"), Mapping) else {}
        )
        status = self._first(
            temperature.get("status"),
            temperature.get("result"),
            temperature.get("level"),
        )
        if status:
            self._add(
                out,
                category="temperature",
                rule=f"status={status}",
                reason=f"Temperature status is {status}.",
                confidence=0.9,
                source="rule_context:temperature.status",
            )
        for key in ("cold_score", "hot_score", "damp_score", "dry_score"):
            value = temperature.get(key)
            if value is None and key in context:
                value = context.get(key)
            if value is None or str(value).strip() == "":
                continue
            self._add(
                out,
                category="temperature",
                rule=f"{key}={value}",
                reason=f"Temperature metric {key} is {value}.",
                confidence=0.85,
                source=f"rule_context:temperature.{key}",
            )

    def _collect_shensha(self, context: Mapping[str, Any], out: list[EvidenceItem]) -> None:
        shensha = context.get("shensha") if isinstance(context.get("shensha"), Mapping) else {}
        bazi = context.get("bazi") if isinstance(context.get("bazi"), Mapping) else {}
        stars = self._as_list(shensha.get("stars")) or self._as_list(shensha.get("star"))
        if not stars:
            stars = self._as_list(bazi.get("shensha"))

        status = self._first(shensha.get("status"))
        if status:
            self._add(
                out,
                category="shensha",
                rule=f"status={status}",
                reason=f"ShenSha status is {status}.",
                confidence=0.88,
                source="rule_context:shensha.status",
            )

        for star in stars:
            self._add(
                out,
                category="shensha",
                rule=f"present={star}",
                reason=f"ShenSha '{star}' is present.",
                confidence=0.91,
                source="rule_context:shensha.stars",
            )

        available = shensha.get("available")
        if isinstance(available, Mapping):
            for name, flag in available.items():
                if flag in (False, None, "", 0):
                    continue
                self._add(
                    out,
                    category="shensha",
                    rule=f"present={name}",
                    reason=f"ShenSha '{name}' is marked available.",
                    confidence=0.9,
                    source="rule_context:shensha.available",
                )
