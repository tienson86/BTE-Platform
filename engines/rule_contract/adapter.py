"""
Rule Adapter — convert legacy rule schemas to Rule Contract V1.

Does not modify CSV / Knowledge Base. All conversion is in-memory.
"""

from __future__ import annotations

import json
import re
from typing import Any, Mapping

from .models import ConditionPredicate, RuleContract

# ---------------------------------------------------------------------------
# Status phrase → canonical value
# ---------------------------------------------------------------------------

STATUS_VALUE_MAP: dict[str, str] = {
    # Pattern / success family
    "cách thành": "SUCCESS",
    "thành cách": "SUCCESS",
    "hợp cách": "SUCCESS",
    "hữu chế": "CONTROLLED",
    "thành công": "SUCCESS",
    "không thành": "FAIL",
    "phá hoàn toàn": "DESTROYED",
    "phá cách": "DESTROYED",
    "bị phá": "DESTROYED",
    "không đủ điều kiện": "INCOMPLETE",
    # Presence
    "hiện diện": "PRESENT",
    # Useful god family (kept as slug)
    "hữu_dụng": "USEFUL",
    "vô_dụng": "USELESS",
    "hữu_chế": "CONTROLLED",
    "vô_chế": "UNCONTROLLED",
}

# Implicit CSV columns used when `condition` is missing
IMPLICIT_FIELD_MAP: dict[str, str] = {
    "month_status": "strength.month_status",
    "root_level": "strength.root_level",
    "support_type": "strength.support_type",
    "control_type": "strength.control_type",
    "pattern_type": "pattern.type",
    "case_name": "special.case_name",
    "structure": "ten_gods.structure",
    "balance_level": "wuxing.balance_level",
    "star_name": "shensha.star",
    "ten_god": "ten_gods.name",
    "follow_type": "pattern.follow_type",
    "pattern_name": "pattern.name",
    "element": "wuxing.element",
    "season": "wuxing.season",
    "combination_type": "wuxing.combination_type",
    "clash_type": "wuxing.clash_type",
    "special_case": "wuxing.special_case",
}

FIELD_COMPARE_RE = re.compile(
    r"^([A-Za-z_][\w.]*)\s*(>=|<=|==|!=|=|>|<)\s*(.+)$"
)

ASCII_ENUM_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

OBJECT_MAP_HINTS: dict[str, tuple[str, str]] = {
    # key → (field, operator)
    "month_branch_contains": ("bazi.month_branch", "contains"),
    "day_master_strength": ("strength.level", "in"),
    "zheng_guan_visible": ("ten_gods.zheng_guan.visible", "eq"),
    "qi_sha_visible": ("ten_gods.qi_sha.visible", "eq"),
    "has_control": ("pattern.has_control", "eq"),
    "has_zheng_guan": ("ten_gods.zheng_guan.present", "eq"),
    "has_qi_sha": ("ten_gods.qi_sha.present", "eq"),
    "not_destroyed": ("pattern.not_destroyed", "eq"),
}


class RuleAdapter:
    """
    Convert legacy rule rows / JSON conditions into RuleContract V1.
    """

    def adapt(self, rule: Mapping[str, Any] | Any) -> RuleContract:
        """
        Adapt one rule (dict-like or pandas Series) to RuleContract.
        """
        data = self._as_dict(rule)

        # 1) Explicit V1 / JSON array in conditions or condition
        for key in ("conditions", "condition"):
            if key not in data:
                continue
            raw = data.get(key)
            contract = self._try_structured(raw, data)
            if contract is not None:
                return contract

        # 2) Priority-style required_conditions list
        if "required_conditions" in data:
            return self._from_priority_terms(
                data.get("required_conditions") or [],
                data,
            )

        # 3) Scalar condition / enum / status phrase
        if "condition" in data:
            return self._from_scalar_condition(data["condition"], data)

        # 4) No condition column → implicit metadata
        return self._from_implicit_metadata(data)

    def adapt_many(self, rules: list[Mapping[str, Any]]) -> list[RuleContract]:
        """Adapt a list of rules."""
        return [self.adapt(rule) for rule in rules]

    # =========================================================
    # Structured forms
    # =========================================================

    def _try_structured(
        self,
        raw: Any,
        rule: dict[str, Any],
    ) -> RuleContract | None:
        if raw is None:
            return None

        # Already list of predicates / empty collection
        if isinstance(raw, list):
            return self._from_json_array(raw, rule)

        if isinstance(raw, dict):
            # V1 envelope
            if "conditions" in raw and isinstance(raw["conditions"], list):
                group = str(raw.get("condition_group", "AND")).upper()
                preds = [
                    self._predicate_from_mapping(item, index, rule)
                    for index, item in enumerate(raw["conditions"])
                ]
                return RuleContract(
                    condition_group=group,
                    conditions=preds,
                    source_type="JSON_V1_ENVELOPE",
                    metadata=self._meta(rule),
                )
            # JSON object map
            return self._from_json_object_map(raw, rule)

        if isinstance(raw, str):
            text = raw.strip()
            if text in {"", "[]", "{}"}:
                return RuleContract(
                    condition_group="AND",
                    conditions=[],
                    source_type="EMPTY_COLLECTION",
                    metadata=self._meta(rule),
                )
            if text.startswith("[") or text.startswith("{"):
                try:
                    parsed = json.loads(text)
                except json.JSONDecodeError:
                    return None
                return self._try_structured(parsed, rule)

        return None

    def _from_json_array(
        self,
        items: list[Any],
        rule: dict[str, Any],
    ) -> RuleContract:
        if not items:
            return RuleContract(
                condition_group="AND",
                conditions=[],
                source_type="EMPTY_COLLECTION",
                metadata=self._meta(rule),
            )

        if all(isinstance(item, dict) for item in items):
            preds = [
                self._predicate_from_mapping(item, index, rule)
                for index, item in enumerate(items)
            ]
            return RuleContract(
                condition_group="AND",
                conditions=preds,
                source_type="JSON_ARRAY_FIELD_OPS",
                metadata=self._meta(rule),
            )

        # list of scalar facts
        preds = []
        for index, item in enumerate(items):
            preds.append(
                ConditionPredicate(
                    condition_id=f"C{index + 1:03d}",
                    field=f"facts.{item}",
                    operator="eq",
                    value=True,
                )
            )
        return RuleContract(
            condition_group="AND",
            conditions=preds,
            source_type="JSON_ARRAY_SCALAR",
            metadata=self._meta(rule),
        )

    def _from_json_object_map(
        self,
        mapping: dict[str, Any],
        rule: dict[str, Any],
    ) -> RuleContract:
        preds: list[ConditionPredicate] = []
        for index, (key, value) in enumerate(mapping.items()):
            field, operator = OBJECT_MAP_HINTS.get(
                key,
                (key, "eq"),
            )
            # boolean-ish keys
            if isinstance(value, bool) or (
                isinstance(value, str) and value.lower() in {"true", "false"}
            ):
                operator = "eq"
                if isinstance(value, str):
                    value = value.lower() == "true"
            elif isinstance(value, list):
                operator = "in"
            elif "contains" in key:
                operator = "contains"

            preds.append(
                ConditionPredicate(
                    condition_id=f"C{index + 1:03d}",
                    field=field,
                    operator=operator,
                    value=value,
                )
            )
        return RuleContract(
            condition_group="AND",
            conditions=preds,
            source_type="JSON_OBJECT_MAP",
            metadata=self._meta(rule),
        )

    def _predicate_from_mapping(
        self,
        item: Mapping[str, Any],
        index: int,
        rule: dict[str, Any],
    ) -> ConditionPredicate:
        operator = item.get("operator", item.get("op", "eq"))
        condition_id = str(
            item.get("condition_id", item.get("id", f"C{index + 1:03d}"))
        )
        field = str(item.get("field", "value"))
        return ConditionPredicate(
            condition_id=condition_id,
            field=field,
            operator=str(operator),
            value=item.get("value"),
        )

    # =========================================================
    # Scalar / enum / status / compare
    # =========================================================

    def _from_scalar_condition(
        self,
        raw: Any,
        rule: dict[str, Any],
    ) -> RuleContract:
        if raw is None or (isinstance(raw, float) and str(raw) == "nan"):
            return self._from_implicit_metadata(rule)

        text = str(raw).strip()
        if text == "" or text.lower() in {"nan", "none", "null"}:
            return RuleContract(
                condition_group="AND",
                conditions=[],
                source_type="EMPTY",
                metadata=self._meta(rule),
            )

        # Field compare expression (priority style)
        match = FIELD_COMPARE_RE.match(text)
        if match:
            field, op, expected = match.groups()
            return RuleContract(
                condition_group="AND",
                conditions=[
                    ConditionPredicate(
                        condition_id="C001",
                        field=field,
                        operator=op,
                        value=self._parse_literal(expected),
                    )
                ],
                source_type="FIELD_COMPARE_EXPR",
                metadata=self._meta(rule),
            )

        # ASCII ENUM token
        if ASCII_ENUM_RE.fullmatch(text):
            return self._from_enum_token(text, rule)

        # Boolean fact key (snake_case identifier)
        if re.fullmatch(r"[A-Za-z_][\w]*", text) and "_" in text:
            return RuleContract(
                condition_group="AND",
                conditions=[
                    ConditionPredicate(
                        condition_id="C001",
                        field=f"facts.{text}",
                        operator="eq",
                        value=True,
                    )
                ],
                source_type="BOOLEAN_FACT_KEY",
                metadata=self._meta(rule),
            )

        # STATUS_PHRASE
        return self._from_status_phrase(text, rule)

    def _from_enum_token(self, token: str, rule: dict[str, Any]) -> RuleContract:
        element = rule.get("element")
        if element:
            element_key = str(element).strip().lower()
            field = f"wuxing.{element_key}.status"
        elif rule.get("season"):
            field = "wuxing.season_status"
        else:
            # generic status bucket for the rule domain
            field = self._guess_status_field(rule)

        return RuleContract(
            condition_group="AND",
            conditions=[
                ConditionPredicate(
                    condition_id="C001",
                    field=field,
                    operator="eq",
                    value=token,
                )
            ],
            source_type="ENUM_TOKEN_ASCII",
            metadata=self._meta(rule),
        )

    def _from_status_phrase(self, phrase: str, rule: dict[str, Any]) -> RuleContract:
        key = phrase.strip().lower()
        value = STATUS_VALUE_MAP.get(key)
        if value is None:
            # keep original phrase as value; slug field by domain
            value = phrase.strip()

        field = self._guess_status_field(rule)
        # User example: "Cách thành" → pattern.status == SUCCESS
        if key in {"cách thành", "thành cách", "hợp cách", "hữu chế"}:
            field = "pattern.status"
            value = STATUS_VALUE_MAP.get(key, "SUCCESS")
        elif key == "hiện diện":
            star = rule.get("star_name")
            if star:
                field = f"shensha.{self._slug(str(star))}.status"
            else:
                field = "shensha.status"
            value = "PRESENT"

        return RuleContract(
            condition_group="AND",
            conditions=[
                ConditionPredicate(
                    condition_id="C001",
                    field=field,
                    operator="eq",
                    value=value,
                )
            ],
            source_type="STATUS_PHRASE",
            metadata=self._meta(rule),
        )

    def _from_priority_terms(
        self,
        terms: list[Any],
        rule: dict[str, Any],
    ) -> RuleContract:
        match_type = str(rule.get("match_type", "all")).lower()
        group = "OR" if match_type in {"any", "first"} else "AND"
        preds: list[ConditionPredicate] = []
        for index, term in enumerate(terms):
            text = str(term).strip()
            compare = FIELD_COMPARE_RE.match(text)
            if compare:
                field, op, expected = compare.groups()
                preds.append(
                    ConditionPredicate(
                        condition_id=f"C{index + 1:03d}",
                        field=field,
                        operator=op,
                        value=self._parse_literal(expected),
                    )
                )
            else:
                preds.append(
                    ConditionPredicate(
                        condition_id=f"C{index + 1:03d}",
                        field=f"facts.{text}",
                        operator="eq",
                        value=True,
                    )
                )
        return RuleContract(
            condition_group=group,
            conditions=preds,
            source_type="PRIORITY_TERMS",
            metadata=self._meta(rule),
        )

    def _from_implicit_metadata(self, rule: dict[str, Any]) -> RuleContract:
        preds: list[ConditionPredicate] = []
        index = 1

        # Range schema
        if "min_score" in rule and "max_score" in rule:
            preds.append(
                ConditionPredicate(
                    condition_id=f"C{index:03d}",
                    field="score.total_score",
                    operator="between",
                    value=[
                        self._parse_literal(rule.get("min_score")),
                        self._parse_literal(rule.get("max_score")),
                    ],
                )
            )
            index += 1

        if "min_ratio" in rule and "max_ratio" in rule:
            preds.append(
                ConditionPredicate(
                    condition_id=f"C{index:03d}",
                    field="wuxing.balance_ratio",
                    operator="between",
                    value=[
                        self._parse_literal(rule.get("min_ratio")),
                        self._parse_literal(rule.get("max_ratio")),
                    ],
                )
            )
            index += 1

        if "min_value" in rule and "max_value" in rule:
            preds.append(
                ConditionPredicate(
                    condition_id=f"C{index:03d}",
                    field="score.confidence_value",
                    operator="between",
                    value=[
                        self._parse_literal(rule.get("min_value")),
                        self._parse_literal(rule.get("max_value")),
                    ],
                )
            )
            index += 1

        for column, field in IMPLICIT_FIELD_MAP.items():
            if column not in rule:
                continue
            value = rule.get(column)
            if value is None or (isinstance(value, float) and str(value) == "nan"):
                continue
            text = str(value).strip()
            if text == "" or text.lower() == "nan":
                continue
            preds.append(
                ConditionPredicate(
                    condition_id=f"C{index:03d}",
                    field=field,
                    operator="eq",
                    value=text,
                )
            )
            index += 1

        source = "IMPLICIT_COLUMN_SCHEMA" if preds else "EMPTY"
        return RuleContract(
            condition_group="AND",
            conditions=preds,
            source_type=source,
            metadata=self._meta(rule),
        )

    # =========================================================
    # Helpers
    # =========================================================

    def _guess_status_field(self, rule: dict[str, Any]) -> str:
        if rule.get("pattern_name") or rule.get("follow_type"):
            return "pattern.status"
        if rule.get("star_name"):
            return "shensha.status"
        if rule.get("ten_god"):
            return "ten_gods.status"
        if any(key.startswith("useful") or "Dụng" in str(rule.get("description", "")) for key in rule):
            return "useful_god.status"
        if rule.get("element") or rule.get("season"):
            return "wuxing.status"
        return "rule.status"

    @staticmethod
    def _slug(text: str) -> str:
        cleaned = re.sub(r"\s+", "_", text.strip().lower())
        cleaned = re.sub(r"[^a-z0-9_]+", "", cleaned)
        return cleaned or "item"

    @staticmethod
    def _parse_literal(raw: Any) -> Any:
        if raw is None:
            return None
        text = str(raw).strip().strip('"').strip("'")
        lowered = text.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if lowered in {"none", "null"}:
            return None
        try:
            if "." in text:
                return float(text)
            return int(text)
        except ValueError:
            return text

    @staticmethod
    def _as_dict(rule: Any) -> dict[str, Any]:
        if rule is None:
            return {}
        if isinstance(rule, dict):
            return dict(rule)
        to_dict = getattr(rule, "to_dict", None)
        if callable(to_dict):
            data = to_dict()
            if isinstance(data, dict):
                return dict(data)
        # pandas Series
        if hasattr(rule, "items") and not isinstance(rule, (str, bytes, list)):
            try:
                return dict(rule)  # type: ignore[arg-type]
            except Exception:
                pass
        if hasattr(rule, "__dict__"):
            return {
                key: value
                for key, value in vars(rule).items()
                if not key.startswith("_")
            }
        return {"value": rule}

    @staticmethod
    def _meta(rule: dict[str, Any]) -> dict[str, Any]:
        keys = (
            "id",
            "rule_id",
            "rule_code",
            "pattern",
            "pattern_name",
            "element",
            "description",
        )
        return {key: rule[key] for key in keys if key in rule}
