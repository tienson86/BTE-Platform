"""HTML Builder — render InterpretationResult as HTML."""

from __future__ import annotations

import html

from engines.analysis_engine.interpretation_engine.models import InterpretationResult


class HtmlBuilder:
    """Build deterministic HTML from chapters and sections."""

    def build(self, result: InterpretationResult) -> str:
        """Render HTML narrative for the interpretation."""
        parts: list[str] = [
            "<!DOCTYPE html>",
            '<html lang="vi">',
            "<head>",
            '  <meta charset="utf-8" />',
            "  <title>Luận giải Bát Tự</title>",
            "</head>",
            "<body>",
            "  <article>",
            "    <h1>Luận giải Bát Tự</h1>",
            f"    <p class=\"overview\">{html.escape(result.overview.strip())}</p>",
        ]
        if result.chapters:
            for chapter in result.chapters:
                parts.append(
                    f'    <section class="chapter" id="{html.escape(chapter.chapter_id)}">'
                )
                parts.append(f"      <h2>{html.escape(chapter.title)}</h2>")
                for section in chapter.sections:
                    parts.append(
                        f'      <section class="interp-section" '
                        f'id="{html.escape(section.section_id)}">'
                    )
                    parts.append(f"        <h3>{html.escape(section.title)}</h3>")
                    parts.append(f"        <p>{html.escape(section.body.strip())}</p>")
                    parts.append("      </section>")
                parts.append("    </section>")
        else:
            for section in result.sections:
                parts.append(
                    f'    <section class="interp-section" '
                    f'id="{html.escape(section.section_id)}">'
                )
                parts.append(f"      <h2>{html.escape(section.title)}</h2>")
                parts.append(f"      <p>{html.escape(section.body.strip())}</p>")
                parts.append("    </section>")
        parts.extend(
            [
                "  </article>",
                "</body>",
                "</html>",
                "",
            ]
        )
        return "\n".join(parts)
