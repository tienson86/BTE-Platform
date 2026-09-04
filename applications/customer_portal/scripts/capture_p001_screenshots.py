"""Capture P-001 CASE-0001 Overview Hero before/after screenshots."""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
PREVIEW = REPO / "docs" / "reports" / "p001_executive_summary_completion" / "preview.html"
OUT = REPO / "docs" / "reports" / "p001_executive_summary_completion" / "screenshots"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    url = PREVIEW.resolve().as_uri()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(url, wait_until="networkidle")
        page.locator('[data-p001="before"]').screenshot(path=str(OUT / "case0001_before.png"))
        page.locator('[data-p001="after"]').screenshot(path=str(OUT / "case0001_after.png"))
        page.screenshot(path=str(OUT / "case0001_before_after.png"), full_page=True)
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(url, wait_until="networkidle")
        mobile.locator('[data-p001="after"]').screenshot(path=str(OUT / "case0001_after_mobile.png"))
        browser.close()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
