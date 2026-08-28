"""Capture HTML-section PNG previews for the Date Selection PDF."""

from __future__ import annotations

from pathlib import Path

from engines.date_selection_report.exporting.html_projection import project_render_tree_to_html
from engines.date_selection_report.rendering.nodes import DateSelectionRenderTree

PREVIEW_SHOTS: tuple[tuple[str, str], ...] = (
    ("01_cover", "#ds-header"),
    ("02_executive", "#ds-exec"),
    ("03_person", "#person"),
    ("04_recommendation", "#recommendation-1"),
    ("05_positive_times", "#positive-times-1"),
    ("06_last_page", "#ds-last"),
)


def capture_pdf_previews(tree: DateSelectionRenderTree, output_dir: Path) -> tuple[Path, ...]:
    """Screenshot canonical report regions from the same HTML used for PDF."""
    from playwright.sync_api import sync_playwright

    output_dir.mkdir(parents=True, exist_ok=True)
    html = project_render_tree_to_html(tree)
    paths: list[Path] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 794, "height": 1123})
            page.set_content(html, wait_until="networkidle")
            page.emulate_media(media="print")
            for name, selector in PREVIEW_SHOTS:
                target = output_dir / f"{name}.png"
                page.locator(selector).screenshot(path=str(target))
                paths.append(target)
        finally:
            browser.close()
    return tuple(paths)
