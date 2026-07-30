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
  .report-section {{
    background: var(--surface);
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    border: 1px solid var(--border);
  }}
  .data-block, .chart-block {{
    border: 1px solid var(--border);
    background: var(--surface);
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
  }}
  table.report-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.5rem 0;
  }}
  table.report-table th {{
    background: var(--table-header-bg);
    text-align: left;
    padding: 0.4rem 0.6rem;
    border: 1px solid var(--border);
  }}
  table.report-table td {{
    padding: 0.4rem 0.6rem;
    border: 1px solid var(--border);
  }}
  .chart-bar-track {{
    background: var(--chart-track);
    height: 0.75rem;
    margin: 0.25rem 0 0.75rem;
  }}
  .chart-bar-fill {{
    background: var(--chart-bar);
    height: 100%;
  }}
  pre {{ white-space: pre-wrap; }}
{print_css}
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

_PRINT_HTML_SHELL = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <style>
{theme_css}
  body {{
    margin: 0;
    padding: 0.6in;
    background: #ffffff;
    color: #000000;
    font-family: {font_family};
    line-height: 1.45;
    font-size: 11pt;
  }}
  h1 {{ color: #000000; font-size: 18pt; }}
  h2 {{
    margin-top: 1rem;
    border-bottom: 1px solid #999999;
    padding-bottom: 0.15rem;
    font-size: 13pt;
  }}
  .muted {{ color: #333333; }}
  .report-section {{ margin: 0.6rem 0; }}
  table.report-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.4rem 0;
  }}
  table.report-table th, table.report-table td {{
    border: 1px solid #999999;
    padding: 0.25rem 0.4rem;
    text-align: left;
  }}
  .no-screen {{ display: none; }}
{print_css}
  </style>
</head>
<body class="print-document">
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


def _layout(
    template_id: str,
    *,
    html_shell: str = _HTML_SHELL,
    markdown_shell: str = _MARKDOWN_SHELL,
    section_order: tuple[str, ...] = (),
    family: str = "default",
) -> LayoutTemplate:
    return LayoutTemplate(
        template_id=template_id,
        html_shell=html_shell,
        markdown_shell=markdown_shell,
        section_order=section_order,
        metadata={"version": "1.0.0", "family": family},
    )


class TemplateLoader:
    """Load presentation layout templates (no interpretive content)."""

    def __init__(self, templates: dict[str, LayoutTemplate] | None = None) -> None:
        self._templates = dict(templates or self._default_templates())

    @staticmethod
    def _default_templates() -> dict[str, LayoutTemplate]:
        return {
            DEFAULT_TEMPLATE_ID: _layout(DEFAULT_TEMPLATE_ID, family="default"),
            "classic": _layout("classic", family="classic"),
            "modern": _layout("modern", family="modern"),
            "professional": _layout("professional", family="professional"),
            "dark": _layout("dark", family="dark"),
            "print": _layout(
                "print",
                html_shell=_PRINT_HTML_SHELL,
                family="print",
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

    def register(self, template: LayoutTemplate) -> None:
        """Register or replace a layout template."""
        self._templates[template.template_id] = template
