"""Capture TV1-B07 Marriage Consulting screenshots from the isolated legal host."""

from __future__ import annotations

import threading
from pathlib import Path

import uvicorn
from playwright.sync_api import sync_playwright

from consulting.marriage.ui.host import create_marriage_customer_app

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs" / "reports" / "tv01_marriage" / "b07" / "screenshots"
HOST = "127.0.0.1"
PORT = 8092


def _serve() -> uvicorn.Server:
    """Start the isolated TV-01 customer host in-process."""
    config = uvicorn.Config(
        create_marriage_customer_app(),
        host=HOST,
        port=PORT,
        log_level="warning",
    )
    return uvicorn.Server(config)


def _fill_person(page, side: str, name: str, gender: str, date: str) -> None:
    """Fill one person panel using existing birth-input conventions."""
    page.fill(f"#person-{side}-full-name", name)
    page.check(f'input[name="person-{side}-gender"][value="{gender}"]')
    page.fill(f"#person-{side}-birth-date", date)


def main() -> None:
    """Capture required B07 screenshots from a live consultation."""
    OUT.mkdir(parents=True, exist_ok=True)
    server = _serve()
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        thread.join(0.05)
    origin = f"http://{HOST}:{PORT}"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        desktop = browser.new_page(viewport={"width": 1280, "height": 900})
        desktop.goto(f"{origin}/marriage-consulting", wait_until="networkidle")
        desktop.screenshot(path=str(OUT / "01_input_page.png"), full_page=True)
        _fill_person(desktop, "a", "An", "male", "21/01/1987")
        _fill_person(desktop, "b", "Binh", "female", "15/05/1990")
        desktop.click('[data-testid="submit-marriage"]')
        desktop.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
        desktop.locator('[data-testid="compatibility-hero"]').screenshot(
            path=str(OUT / "02_hero_executive.png")
        )
        desktop.locator('[data-testid="executive-summary"]').screenshot(
            path=str(OUT / "02b_executive_summary.png")
        )
        desktop.locator('[data-testid="domain-analysis"]').screenshot(
            path=str(OUT / "03_domain_analysis.png")
        )
        desktop.locator('[data-testid="action-plan"]').screenshot(
            path=str(OUT / "04_action_plan.png")
        )
        desktop.screenshot(path=str(OUT / "02_result_desktop.png"), full_page=True)
        tablet = browser.new_page(viewport={"width": 768, "height": 1024})
        tablet.goto(f"{origin}/marriage-consulting", wait_until="networkidle")
        _fill_person(tablet, "a", "An", "male", "21/01/1987")
        _fill_person(tablet, "b", "Binh", "female", "15/05/1990")
        tablet.click('[data-testid="submit-marriage"]')
        tablet.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
        tablet.screenshot(path=str(OUT / "04b_tablet_result.png"), full_page=True)
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(f"{origin}/marriage-consulting", wait_until="networkidle")
        _fill_person(mobile, "a", "An", "male", "21/01/1987")
        _fill_person(mobile, "b", "Binh", "female", "15/05/1990")
        mobile.click('[data-testid="submit-marriage"]')
        mobile.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
        mobile.screenshot(path=str(OUT / "05_mobile_result.png"), full_page=True)
        browser.close()
    server.should_exit = True


if __name__ == "__main__":
    main()
