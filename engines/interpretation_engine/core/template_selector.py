"""
Template Selector

Lựa chọn Template phù hợp.
"""

from __future__ import annotations

from typing import Any

from ..loader import InterpretationLoader


class TemplateSelector:

    def __init__(
        self,
        loader: InterpretationLoader,
    ) -> None:

        self.loader = loader

    def select(
        self,
        matched_rules: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        templates = self.loader.load_templates()

        selected = []

        for rule in matched_rules:

            template_code = rule.get(
                "template"
            )

            if template_code is None:
                continue

            template = templates.get(
                template_code
            )

            if template:

                selected.append(
                    template
                )

        return selected
