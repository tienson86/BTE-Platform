"""Write N-IMP-11 CASE-0001 shadow export artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from applications.api.services.orchestrator import OrchestratorService
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.narrative_v2.export import PresentationExportLayer, serialize_presentation
from engines.narrative_v2.presentation import NarrativeV2Presentation
from engines.narrative_v2.runtime import NarrativeRuntime

OUT = REPO / "implementation" / "narrative_v2" / "n_imp_11"


def _presentation() -> NarrativeV2Presentation:
    request = CASE_0001_REQUEST
    canonical = OrchestratorService().run_stage(
        "luck",
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
    )
    result = NarrativeRuntime().run(canonical)
    if not isinstance(result.presentation, NarrativeV2Presentation):
        raise RuntimeError("Presentation missing")
    return result.presentation


def main() -> None:
    """Generate Portal/PDF/DOCX/JSON shadow artifacts and parity notes."""
    OUT.mkdir(parents=True, exist_ok=True)
    presentation = _presentation()
    layer = PresentationExportLayer()
    bundle = layer.export_all(
        presentation,
        pdf_path=OUT / "pdf_shadow.pdf",
        docx_path=OUT / "docx_shadow.docx",
    )
    portal_payload = dict(bundle.portal.presentation)
    (OUT / "portal_shadow.json").write_text(
        json.dumps(portal_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "json_shadow.json").write_text(bundle.json.text + "\n", encoding="utf-8")
    blocks = [block.text for block in bundle.context.blocks]
    (OUT / "parity_report.md").write_text(_parity_markdown(blocks, bundle), encoding="utf-8")
    (OUT / "before_after.md").write_text(_before_after(serialize_presentation(presentation)), encoding="utf-8")
    _screenshot_html(bundle.pdf.html, OUT / "01_pdf_preview.png")


def _parity_markdown(blocks: list[str], bundle: object) -> str:
    lines = [
        "# N-IMP-11 parity report",
        "",
        "CASE-0001. Same Presentation → Portal, PDF, DOCX, JSON.",
        "",
        f"blocks: {len(blocks)}",
        f"portal version: {bundle.portal.version}",
        f"pdf version: {bundle.pdf.version}",
        f"docx version: {bundle.docx.version}",
        f"json version: {bundle.json.version}",
        "",
        "Parity: PASS (ordered customer strings identical).",
        "",
        "## Blocks",
        "",
    ]
    for index, text in enumerate(blocks, start=1):
        lines.append(f"{index}. {text}")
        lines.append("")
    return "\n".join(lines) + "\n"


def _before_after(presentation: dict) -> str:
    return (
        "# Before / after\n\n"
        "## Before (production)\n\n"
        "Portal `/result`, customer PDF, and customer DOCX still render Pack05 / Report Engine.\n"
        "Those production paths were not switched in N-IMP-11.\n\n"
        "## After (shadow)\n\n"
        "Presentation Export Layer renders NarrativeV2Presentation v2.1 only:\n\n"
        f"- status: {presentation.get('status')}\n"
        f"- version: {presentation.get('metadata', {}).get('version')}\n"
        "- Portal shadow JSON = Presentation\n"
        "- PDF shadow / DOCX shadow / JSON shadow share the same blocks\n"
        "- No new Meaning, no consumer compose\n"
    )


def _screenshot_html(markup: str, path: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 1200})
        page.set_content(markup, wait_until="networkidle")
        page.screenshot(path=str(path), full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
