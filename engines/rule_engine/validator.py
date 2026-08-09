"""Rule validation diagnostics."""

from __future__ import annotations

from typing import Any, Mapping

from engines.rule_engine.models import (
    KNOWN_CATEGORIES,
    PRIORITY_LEVEL_RANK,
    RuleRecord,
    ValidationDiagnostic,
)


class RuleValidator:
    """Validate rule records and emit structured diagnostics."""

    def validate_raw(
        self,
        raw: Mapping[str, Any],
        *,
        source_path: str,
        seen_ids: set[str],
    ) -> tuple[list[ValidationDiagnostic], bool]:
        """
        Validate one raw rule mapping.

        Returns diagnostics and whether the rule is recoverable for registration.
        """
        diagnostics: list[ValidationDiagnostic] = []
        rule_id = str(raw.get("id") or "").strip() or None

        if not rule_id:
            diagnostics.append(
                ValidationDiagnostic(
                    code="missing_id",
                    message="Rule is missing required field 'id'.",
                    severity="error",
                    field="id",
                    source_path=source_path,
                )
            )
            return diagnostics, False

        if rule_id in seen_ids:
            diagnostics.append(
                ValidationDiagnostic(
                    code="duplicate_id",
                    message=f"Duplicate rule id '{rule_id}'.",
                    severity="error",
                    rule_id=rule_id,
                    field="id",
                    source_path=source_path,
                )
            )
            return diagnostics, False

        for required in ("code", "name"):
            if not str(raw.get(required) or "").strip():
                diagnostics.append(
                    ValidationDiagnostic(
                        code="missing_field",
                        message=f"Rule is missing required field '{required}'.",
                        severity="error",
                        rule_id=rule_id,
                        field=required,
                        source_path=source_path,
                    )
                )

        classification = raw.get("classification")
        classification_map = classification if isinstance(classification, Mapping) else {}
        category = str(
            classification_map.get("category")
            or classification_map.get("domain")
            or raw.get("category")
            or ""
        ).strip()
        if not category:
            diagnostics.append(
                ValidationDiagnostic(
                    code="missing_category",
                    message="Rule is missing category.",
                    severity="warning",
                    rule_id=rule_id,
                    field="classification.category",
                    source_path=source_path,
                )
            )
        elif category.lower() not in KNOWN_CATEGORIES and category not in KNOWN_CATEGORIES:
            diagnostics.append(
                ValidationDiagnostic(
                    code="invalid_category",
                    message=f"Unknown category '{category}'.",
                    severity="warning",
                    rule_id=rule_id,
                    field="classification.category",
                    source_path=source_path,
                )
            )

        priority = raw.get("priority")
        priority_map = priority if isinstance(priority, Mapping) else {}
        level = str(priority_map.get("level") or raw.get("priority_level") or "").strip().lower()
        if level and level not in PRIORITY_LEVEL_RANK:
            diagnostics.append(
                ValidationDiagnostic(
                    code="invalid_priority",
                    message=f"Unknown priority level '{level}'.",
                    severity="warning",
                    rule_id=rule_id,
                    field="priority.level",
                    source_path=source_path,
                )
            )
        order = priority_map.get("order", raw.get("priority_order"))
        if order is not None:
            try:
                int(order)
            except (TypeError, ValueError):
                diagnostics.append(
                    ValidationDiagnostic(
                        code="invalid_priority",
                        message=f"Priority order is not an integer: {order!r}.",
                        severity="warning",
                        rule_id=rule_id,
                        field="priority.order",
                        source_path=source_path,
                    )
                )

        conditions = raw.get("conditions")
        if conditions is None:
            diagnostics.append(
                ValidationDiagnostic(
                    code="missing_field",
                    message="Rule is missing 'conditions' (empty list allowed).",
                    severity="warning",
                    rule_id=rule_id,
                    field="conditions",
                    source_path=source_path,
                )
            )
        elif not isinstance(conditions, list):
            diagnostics.append(
                ValidationDiagnostic(
                    code="invalid_conditions",
                    message="Rule conditions must be a list.",
                    severity="error",
                    rule_id=rule_id,
                    field="conditions",
                    source_path=source_path,
                )
            )
        else:
            for index, item in enumerate(conditions):
                if not isinstance(item, Mapping):
                    diagnostics.append(
                        ValidationDiagnostic(
                            code="invalid_conditions",
                            message=f"Condition at index {index} must be an object.",
                            severity="error",
                            rule_id=rule_id,
                            field=f"conditions[{index}]",
                            source_path=source_path,
                        )
                    )
                    continue
                if not (item.get("field") or item.get("type") or item.get("path")):
                    diagnostics.append(
                        ValidationDiagnostic(
                            code="invalid_reference",
                            message=(
                                f"Condition at index {index} has no field/type reference."
                            ),
                            severity="warning",
                            rule_id=rule_id,
                            field=f"conditions[{index}]",
                            source_path=source_path,
                        )
                    )

        has_fatal = any(
            item.severity == "error"
            and item.code in {"missing_id", "duplicate_id", "invalid_conditions"}
            for item in diagnostics
        )
        # Missing code/name is recoverable with empty strings but flagged.
        recoverable = not has_fatal and bool(rule_id)
        if any(item.code == "missing_field" and item.field in {"code", "name"} for item in diagnostics):
            # Still loadable, but flagged.
            pass
        return diagnostics, recoverable

    def validate_record(self, record: RuleRecord) -> list[ValidationDiagnostic]:
        """Validate an already-built record."""
        return self.validate_raw(
            dict(record.raw),
            source_path=record.source_path,
            seen_ids=set(),
        )[0]
