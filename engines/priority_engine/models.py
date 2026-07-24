"""Data models used by the BTE priority engine.

The models intentionally mirror the JSON files in
``05_rule_database/08_priority_rules`` while keeping enough derived metadata
for the resolver, planner, and tests to operate without hard-coded rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


JsonDict = dict[str, Any]


@dataclass(frozen=True)
class PriorityRule:
    """A rule priority definition from ``priority_rules.json``."""

    id: str
    rule_type: str
    rule_code: str
    rule_name: str
    priority: int
    execution_order: int
    override_lower_rules: bool = False
    stop_processing: bool = False
    enabled: bool = True
    description: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PriorityRule":
        return cls(
            id=str(data["id"]),
            rule_type=str(data["rule_type"]),
            rule_code=str(data.get("rule_code", data.get("name", ""))),
            rule_name=str(data.get("rule_name", data.get("name", ""))),
            priority=int(data["priority"]),
            execution_order=int(data.get("execution_order", data.get("order", 0))),
            override_lower_rules=bool(data.get("override_lower_rules", False)),
            stop_processing=bool(data.get("stop_processing", False)),
            enabled=bool(data.get("enabled", True)),
            description=str(data.get("description", "")),
        )


@dataclass(frozen=True)
class PriorityCondition:
    """A condition that activates a priority rule."""

    id: str
    condition_code: str
    condition_name: str
    priority_rule: str
    rule_type: str
    trigger_stage: str
    match_type: str = "all"
    required_conditions: tuple[str, ...] = field(default_factory=tuple)
    enabled: bool = True
    description: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PriorityCondition":
        required = data.get("required_conditions", data.get("conditions", []))
        return cls(
            id=str(data["id"]),
            condition_code=str(data.get("condition_code", data.get("condition", ""))),
            condition_name=str(data.get("condition_name", data.get("condition", ""))),
            priority_rule=str(data["priority_rule"]),
            rule_type=str(data["rule_type"]),
            trigger_stage=str(data.get("trigger_stage", "")),
            match_type=str(data.get("match_type", "all")),
            required_conditions=tuple(str(item) for item in required),
            enabled=bool(data.get("enabled", True)),
            description=str(data.get("description", "")),
        )


@dataclass(frozen=True)
class PriorityOrder:
    """An execution step from ``priority_order.json``."""

    id: str
    stage: int
    priority_rule: str
    rule_type: str
    execution_group: str
    execution_mode: str
    depends_on: tuple[str, ...] = field(default_factory=tuple)
    continue_on_success: bool = True
    continue_on_failure: bool = True
    skip_remaining_same_group: bool = False
    terminate_pipeline: bool = False
    enabled: bool = True
    description: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PriorityOrder":
        return cls(
            id=str(data["id"]),
            stage=int(data.get("stage", data.get("order", 0))),
            priority_rule=str(data.get("priority_rule", data.get("rule_type", ""))),
            rule_type=str(data["rule_type"]),
            execution_group=str(data.get("execution_group", data["rule_type"])),
            execution_mode=str(data.get("execution_mode", "sequential")),
            depends_on=tuple(str(item) for item in data.get("depends_on", [])),
            continue_on_success=bool(data.get("continue_on_success", True)),
            continue_on_failure=bool(data.get("continue_on_failure", True)),
            skip_remaining_same_group=bool(data.get("skip_remaining_same_group", False)),
            terminate_pipeline=bool(data.get("terminate_pipeline", False)),
            enabled=bool(data.get("enabled", True)),
            description=str(data.get("description", "")),
        )


@dataclass(frozen=True)
class PriorityLabel:
    """A reusable label definition from ``priority_labels.json``."""

    id: str
    label_code: str
    label_name: str
    category: str
    sort_order: int
    display_name: str
    severity: str
    color: str
    icon: str
    enabled: bool = True
    priority_value: int | None = None
    status_code: str | None = None
    decision_code: str | None = None
    description: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PriorityLabel":
        priority_value = data.get("priority_value")
        return cls(
            id=str(data["id"]),
            label_code=str(data.get("label_code", data.get("label", ""))),
            label_name=str(data.get("label_name", data.get("label", ""))),
            category=str(data["category"]),
            sort_order=int(data.get("sort_order", 0)),
            display_name=str(data.get("display_name", data.get("label_name", ""))),
            severity=str(data.get("severity", "info")),
            color=str(data.get("color", "")),
            icon=str(data.get("icon", "")),
            enabled=bool(data.get("enabled", True)),
            priority_value=None if priority_value is None else int(priority_value),
            status_code=data.get("status_code"),
            decision_code=data.get("decision_code"),
            description=str(data.get("description", "")),
        )


@dataclass(frozen=True)
class PriorityExample:
    """A golden example from ``priority_examples.json``."""

    id: str
    title: str
    category: str
    description: str
    input_rules: tuple[str, ...]
    matched_conditions: tuple[str, ...]
    priority_order: tuple[str, ...]
    expected_rule: str | None
    expected_label: str | None
    expected_pipeline_status: str | None
    expected_execution_order: tuple[str, ...]
    notes: str = ""
    enabled: bool = True

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PriorityExample":
        return cls(
            id=str(data["id"]),
            title=str(data.get("title", "")),
            category=str(data.get("category", "")),
            description=str(data.get("description", "")),
            input_rules=tuple(str(item) for item in data.get("input_rules", [])),
            matched_conditions=tuple(str(item) for item in data.get("matched_conditions", [])),
            priority_order=tuple(str(item) for item in data.get("priority_order", [])),
            expected_rule=data.get("expected_rule"),
            expected_label=data.get("expected_label"),
            expected_pipeline_status=data.get("expected_pipeline_status"),
            expected_execution_order=tuple(
                str(item) for item in data.get("expected_execution_order", [])
            ),
            notes=str(data.get("notes", "")),
            enabled=bool(data.get("enabled", True)),
        )


@dataclass(frozen=True)
class PriorityData:
    """All priority-engine data loaded from the Knowledge Base."""

    source_dir: Path
    rules: tuple[PriorityRule, ...]
    conditions: tuple[PriorityCondition, ...]
    orders: tuple[PriorityOrder, ...]
    labels: tuple[PriorityLabel, ...]
    examples: tuple[PriorityExample, ...] = field(default_factory=tuple)

    @property
    def rules_by_id(self) -> dict[str, PriorityRule]:
        return {item.id: item for item in self.rules}

    @property
    def conditions_by_id(self) -> dict[str, PriorityCondition]:
        return {item.id: item for item in self.conditions}

    @property
    def orders_by_id(self) -> dict[str, PriorityOrder]:
        return {item.id: item for item in self.orders}

    @property
    def orders_by_rule_id(self) -> dict[str, PriorityOrder]:
        return {item.priority_rule: item for item in self.orders}

    @property
    def labels_by_id(self) -> dict[str, PriorityLabel]:
        return {item.id: item for item in self.labels}


@dataclass(frozen=True)
class ConditionMatch:
    """Result of evaluating one priority condition."""

    condition: PriorityCondition
    matched: bool
    matched_terms: tuple[str, ...] = field(default_factory=tuple)
    failed_terms: tuple[str, ...] = field(default_factory=tuple)

    @property
    def priority_rule(self) -> str:
        return self.condition.priority_rule


@dataclass(frozen=True)
class ExecutionStep:
    """A planned executable priority step."""

    order: PriorityOrder
    rule: PriorityRule
    condition: PriorityCondition | None = None


@dataclass(frozen=True)
class ExecutionPlan:
    """Ordered execution plan produced by the planner."""

    steps: tuple[ExecutionStep, ...]
    skipped: tuple[str, ...] = field(default_factory=tuple)

    @property
    def order_ids(self) -> tuple[str, ...]:
        return tuple(step.order.id for step in self.steps)

    @property
    def rule_ids(self) -> tuple[str, ...]:
        return tuple(step.rule.id for step in self.steps)


@dataclass(frozen=True)
class ResolutionResult:
    """Final result produced by the priority resolver."""

    accepted_rules: tuple[PriorityRule, ...]
    rejected_rules: tuple[PriorityRule, ...]
    conflict_rules: tuple[PriorityRule, ...]
    winner: PriorityRule | None
    decision_label: str
    pipeline_status: str
    terminate_pipeline: bool = False
    reason: str = ""

    @property
    def accepted_rule_ids(self) -> tuple[str, ...]:
        return tuple(rule.id for rule in self.accepted_rules)

    @property
    def rejected_rule_ids(self) -> tuple[str, ...]:
        return tuple(rule.id for rule in self.rejected_rules)

    @property
    def conflict_rule_ids(self) -> tuple[str, ...]:
        return tuple(rule.id for rule in self.conflict_rules)


@dataclass(frozen=True)
class PriorityPipelineResult:
    """Full output of one priority-engine run."""

    matched_conditions: tuple[ConditionMatch, ...]
    execution_plan: ExecutionPlan
    resolution: ResolutionResult

    def to_dict(self) -> JsonDict:
        """Return a compact, API-friendly representation."""

        return {
            "matched_conditions": [
                {
                    "condition_id": item.condition.id,
                    "priority_rule": item.priority_rule,
                    "matched": item.matched,
                    "matched_terms": list(item.matched_terms),
                    "failed_terms": list(item.failed_terms),
                }
                for item in self.matched_conditions
            ],
            "execution_order": list(self.execution_plan.order_ids),
            "accepted_rules": list(self.resolution.accepted_rule_ids),
            "rejected_rules": list(self.resolution.rejected_rule_ids),
            "conflict_rules": list(self.resolution.conflict_rule_ids),
            "winner": None if self.resolution.winner is None else self.resolution.winner.id,
            "decision_label": self.resolution.decision_label,
            "pipeline_status": self.resolution.pipeline_status,
            "terminate_pipeline": self.resolution.terminate_pipeline,
            "reason": self.resolution.reason,
        }


def unique_ids(items: Sequence[Any]) -> set[str]:
    """Return duplicate IDs from any sequence of objects with an ``id`` field."""

    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        item_id = item.id
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    return duplicates
