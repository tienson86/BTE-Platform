"""Template Loader — presentation layout templates only."""

from __future__ import annotations

from engines.analysis_engine.report_generator.exceptions import ReportFormatProfileError
from engines.analysis_engine.report_generator.models import LayoutTemplate

DEFAULT_TEMPLATE_ID = "default"

_HTML_SHELL = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <style>
{theme_css}
  body {{
    margin: 0;
    padding: 2rem;
    background: var(--bg);
    color: var(--fg);
    font-family: {font_family};
    line-height: 1.6;
  }}
  h1 {{ color: var(--accent); }}
  h2 {{
    margin-top: var(--section-gap);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.25rem;
  }}
  .muted {{ color: var(--muted); }}
  .data-block {{
    border: 1px solid var(--border);
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
  }}
  pre {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p class="muted">{overview}</p>
  </header>
  <main>
{sections}
{data_blocks}
  </main>
</body>
</html>
"""

_MARKDOWN_SHELL = """# {title}

{overview}

{sections}
{data_blocks}
"""


class TemplateLoader:
    """Load presentation layout templates (no interpretive content)."""

    def __init__(self, templates: dict[str, LayoutTemplate] | None = None) -> None:
        self._templates = dict(templates or self._default_templates())

    @staticmethod
    def _default_templates() -> dict[str, LayoutTemplate]:
        return {
            DEFAULT_TEMPLATE_ID: LayoutTemplate(
                template_id=DEFAULT_TEMPLATE_ID,
                html_shell=_HTML_SHELL,
                markdown_shell=_MARKDOWN_SHELL,
                section_order=(),
                metadata={"version": "1.0.0"},
            ),
        }

    def load(self, template_id: str) -> LayoutTemplate:
        """Return a layout template or raise FormatProfileError."""
        template = self._templates.get(template_id)
        if template is None:
            raise ReportFormatProfileError(
                f"Unknown template_id: {template_id}",
                details={
                    "template_id": template_id,
                    "available": sorted(self._templates),
                },
            )
        return template

    def list_ids(self) -> tuple[str, ...]:
        """Return registered template ids."""
        return tuple(sorted(self._templates))
