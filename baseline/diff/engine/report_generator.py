"""Diff report generators (Markdown, JSON, HTML)."""

from __future__ import annotations

import html
from typing import Any

from baseline.io_utils import canonical_json_dumps


def generate_diff_json(diff_result: dict[str, Any]) -> str:
    """Serialize diff result as deterministic JSON text."""
    return canonical_json_dumps(diff_result)


def generate_diff_markdown(diff_result: dict[str, Any]) -> str:
    """Generate a Markdown diff report."""
    lines = [
        "# Baseline Diff Report",
        "",
        f"- Old: `{diff_result.get('old_version')}`",
        f"- New: `{diff_result.get('new_version')}`",
        f"- Timestamp: `{diff_result.get('timestamp')}`",
        "",
        "## Summary",
        "",
        f"- Breaking changes: `{diff_result.get('summary', {}).get('breaking', False)}`",
        f"- Changed domains: `{', '.join(diff_result.get('summary', {}).get('changed_domains', [])) or 'none'}`",
        "",
    ]
    for domain, payload in sorted(diff_result.get("domains", {}).items()):
        lines.append(f"## {domain}")
        lines.append("")
        lines.append("```json")
        lines.append(canonical_json_dumps(payload).rstrip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines) + "\n"


def generate_diff_html(diff_result: dict[str, Any]) -> str:
    """Generate a simple HTML diff report."""
    title = "Baseline Diff Report"
    body_rows = []
    for domain, payload in sorted(diff_result.get("domains", {}).items()):
        body_rows.append(
            "<section><h2>{domain}</h2><pre>{payload}</pre></section>".format(
                domain=html.escape(domain),
                payload=html.escape(canonical_json_dumps(payload)),
            )
        )
    changed = ", ".join(
        diff_result.get("summary", {}).get("changed_domains", [])
    ) or "none"
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head><meta charset=\"utf-8\"/>"
        f"<title>{html.escape(title)}</title></head>\n"
        "<body>\n"
        f"<h1>{html.escape(title)}</h1>\n"
        f"<p>Old: {html.escape(str(diff_result.get('old_version')))}<br/>"
        f"New: {html.escape(str(diff_result.get('new_version')))}</p>\n"
        f"<p>Changed domains: {html.escape(changed)}</p>\n"
        + "\n".join(body_rows)
        + "\n</body>\n</html>\n"
    )
