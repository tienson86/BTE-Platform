"""Capture the current live Ten Gods module before P-003C layout work."""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "p003c_ten_gods_layout" / "screenshots"
BASE = "http://127.0.0.1:8081"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto(f"{BASE}/analyze", wait_until="networkidle")
        page.wait_for_selector("#analyzeForm")
        page.fill("#full_name", "Nguyễn Tiến Sơn")
        page.check("#gender_male")
        page.fill("#birth_date", "1987-01-21")
        page.fill("#birth_time", "04:30")
        page.fill("#birth_place", "Hà Tây, Việt Nam")
        page.click("#btnAnalyze")
        page.wait_for_url("**/result", timeout=120000)
        page.wait_for_selector('[data-card="ten-gods"]')
        page.locator('[data-card="ten-gods"]').first.scroll_into_view_if_needed()
        page.locator('[data-card="ten-gods"]').first.screenshot(path=str(OUT / "01_before_ten_gods.png"))
        browser.close()


if __name__ == "__main__":
    main()
