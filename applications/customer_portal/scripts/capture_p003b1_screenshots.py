"""Capture P-003B.1 combination library screenshots."""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
PREVIEW = REPO / "docs" / "reports" / "p003b1_high_value_combinations" / "preview.html"
OUT = REPO / "docs" / "reports" / "p003b1_high_value_combinations" / "screenshots"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    url = PREVIEW.resolve().as_uri()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1800})
        page.goto(url, wait_until="networkidle")
        page.locator('[data-p003b1="case0001"]').screenshot(path=str(OUT / "case0001.png"))
        page.locator('[data-p003b1="case0002"]').screenshot(path=str(OUT / "case0002.png"))
        page.locator('[data-p003b1="fixture003"]').screenshot(path=str(OUT / "fixture_l08_003.png"))
        page.screenshot(path=str(OUT / "library_board.png"), full_page=True)
        mobile = browser.new_page(viewport={"width": 390, "height": 1400})
        mobile.goto(url, wait_until="networkidle")
        mobile.locator('[data-p003b1="case0001"]').screenshot(path=str(OUT / "case0001_mobile.png"))
        mobile.locator('[data-p003b1="case0002"]').screenshot(path=str(OUT / "case0002_mobile.png"))
        browser.close()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
