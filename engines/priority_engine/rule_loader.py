"""Load priority engine JSON data from the BTE Knowledge Base."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar

from .exceptions import PriorityDataNotFoundError, PriorityDataValidationError
from .models import (
    PriorityCondition,
    PriorityData,
    PriorityExample,
    PriorityLabel,
    PriorityOrder,
    PriorityRule,
    unique_ids,
)

T = TypeVar("T")


class PriorityRuleLoader:
    """Load and validate the ``08_priority_rules`` Knowledge Base folder."""

    REQUIRED_FILES = {
        "rules": "priority_rules.json",
        "conditions": "priority_conditions.json",
        "orders": "priority_order.json",
        "labels": "priority_labels.json",
    }
    OPTIONAL_FILES = {
        "examples": "priority_examples.json",
    }

    def __init__(self, priority_dir: str | Path) -> None:
        self.priority_dir = Path(priority_dir)

    @classmethod
    def from_project_root(cls, project_root: str | Path) -> "PriorityRuleLoader":
        """Create a loader by searching common BTE Knowledge Base locations."""

        root = Path(project_root)
        candidates = (
            root
            / "engines"
            / "interpretation_engine"
            / "knowledge"
            / "05_rule_database"
            / "08_priority_rules",
            root / "Knowledge Base" / "05_rule_database" / "08_priority_rules",
            root / "knowledge_base" / "05_rule_database" / "08_priority_rules",
            root / "05_rule_database" / "08_priority_rules",
            root / "08_priority_rules",
        )
        for candidate in candidates:
            if candidate.exists():
                return cls(candidate)
        raise PriorityDataNotFoundError(
            "Could not find 08_priority_rules under the provided project root."
        )

    def load(self) -> PriorityData:
        """Load all priority data and validate cross-file references."""

        self._ensure_required_files()
        rules = self._load_collection("rules", PriorityRule.from_dict)
        conditions = self._load_collection("conditions", PriorityCondition.from_dict)
        orders = self._load_collection("orders", PriorityOrder.from_dict)
        labels = self._load_collection("labels", PriorityLabel.from_dict)
        examples = self._load_optional_collection("examples", PriorityExample.from_dict)

        data = PriorityData(
            source_dir=self.priority_dir,
            rules=tuple(rules),
            conditions=tuple(conditions),
            orders=tuple(orders),
            labels=tuple(labels),
            examples=tuple(examples),
        )
        self._validate(data)
        return data

    def _ensure_required_files(self) -> None:
        if not self.priority_dir.exists():
            raise PriorityDataNotFoundError(
                f"Priority data directory not found: {self.priority_dir}"
            )
        missing = [
            filename
            for filename in self.REQUIRED_FILES.values()
            if not (self.priority_dir / filename).exists()
        ]
        if missing:
            raise PriorityDataNotFoundError(
                f"Missing required priority data files: {', '.join(missing)}"
            )

    def _load_collection(self, key: str, factory: Callable[[dict[str, Any]], T]) -> list[T]:
        path = self.priority_dir / self.REQUIRED_FILES[key]
        return self._read_json_list(path, factory)

    def _load_optional_collection(
        self, key: str, factory: Callable[[dict[str, Any]], T]
    ) -> list[T]:
        path = self.priority_dir / self.OPTIONAL_FILES[key]
        if not path.exists():
            return []
        return self._read_json_list(path, factory)

    @staticmethod
    def _read_json_list(path: Path, factory: Callable[[dict[str, Any]], T]) -> list[T]:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise PriorityDataValidationError(f"Invalid JSON in {path}: {exc}") from exc

        if not isinstance(raw, list):
            raise PriorityDataValidationError(f"{path.name} must contain a JSON array.")

        items: list[T] = []
        for index, item in enumerate(raw):
            if not isinstance(item, dict):
                raise PriorityDataValidationError(
                    f"{path.name}[{index}] must be a JSON object."
                )
            try:
                items.append(factory(item))
            except KeyError as exc:
                raise PriorityDataValidationError(
                    f"{path.name}[{index}] is missing required field {exc!s}."
                ) from exc
        return items

    @staticmethod
    def _validate(data: PriorityData) -> None:
        PriorityRuleLoader._validate_unique("priority_rules.json", data.rules)
        PriorityRuleLoader._validate_unique("priority_conditions.json", data.conditions)
        PriorityRuleLoader._validate_unique("priority_order.json", data.orders)
        PriorityRuleLoader._validate_unique("priority_labels.json", data.labels)

        rule_ids = set(data.rules_by_id)
        order_ids = set(data.orders_by_id)
        condition_ids = set(data.conditions_by_id)
        label_ids = set(data.labels_by_id)

        for condition in data.conditions:
            if condition.priority_rule not in rule_ids:
                raise PriorityDataValidationError(
                    f"{condition.id} references missing rule {condition.priority_rule}."
                )

        for order in data.orders:
            if order.priority_rule not in rule_ids:
                raise PriorityDataValidationError(
                    f"{order.id} references missing rule {order.priority_rule}."
                )

        for example in data.examples:
            missing_rules = set(example.input_rules) - rule_ids
            missing_conditions = set(example.matched_conditions) - condition_ids
            missing_orders = set(example.priority_order) - order_ids
            missing_expected_orders = set(example.expected_execution_order) - order_ids
            missing_labels = {
                item
                for item in (example.expected_label, example.expected_pipeline_status)
                if item is not None and item not in label_ids
            }
            if example.expected_rule is not None and example.expected_rule not in rule_ids:
                missing_rules.add(example.expected_rule)
            if missing_rules or missing_conditions or missing_orders or missing_expected_orders:
                raise PriorityDataValidationError(
                    f"{example.id} contains invalid rule, condition, or order references."
                )
            if missing_labels:
                raise PriorityDataValidationError(
                    f"{example.id} contains invalid label references: {missing_labels}."
                )

    @staticmethod
    def _validate_unique(filename: str, items: Iterable[Any]) -> None:
        duplicates = unique_ids(tuple(items))
        if duplicates:
            raise PriorityDataValidationError(
                f"{filename} contains duplicate IDs: {', '.join(sorted(duplicates))}"
            )
