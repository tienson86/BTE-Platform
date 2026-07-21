"""
Template Renderer
=================

Chịu trách nhiệm render template thành câu hoàn chỉnh.

TemplateRenderer KHÔNG đọc file.

TemplateRenderer KHÔNG biết Rule.

Chỉ nhận:

    template
    +
    metadata

↓

sentence
"""

from __future__ import annotations

from typing import Any


class TemplateRenderer:

    """
    Render template bằng metadata.
    """

    def render(
        self,
        template: str,
        metadata: dict[str, Any],
    ) -> str:

        if not template:

            return ""

        try:

            return template.format(
                **metadata
            )

        except KeyError:

            return template

    # -------------------------------------------------

    def render_list(
        self,
        templates: list[str],
        metadata: dict[str, Any],
    ) -> list[str]:

        return [

            self.render(
                template,
                metadata,
            )

            for template in templates

        ]
