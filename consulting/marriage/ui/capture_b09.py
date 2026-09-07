"""Capture TV1-B09 final browser smoke screenshots. Verification only."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import uvicorn
from playwright.sync_api import sync_playwright

from consulting.marriage.ui.host import create_marriage_customer_app

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs" / "reports" / "tv01_marriage" / "b09" / "screenshots"
HOST = "127.0.0.1"
PORT = 8094
_ID_LEAK = r"\b(?:EV|F|RC)-\d{4}\b"


def _serve() -> uvicorn.Server:
    """Start the isolated TV-01 customer host in-process."""
    config = uvicorn.Config(
        create_marriage_customer_app(),
        host=HOST,
        port=PORT,
        log_level="warning",
    )
    return uvicorn.Server(config)


def _fill_person(page, side: str, name: str, gender: str, date: str, time_value: str | None = None) -> None:
    """Fill one person panel using existing birth-input conventions."""
    page.fill(f"#person-{side}-full-name", name)
    page.check(f'input[name="person-{side}-gender"][value="{gender}"]')
    page.fill(f"#person-{side}-birth-date", date)
    if time_value:
        page.fill(f"#person-{side}-birth-time", time_value)


def _assert_customer_result(page) -> dict[str, object]:
    """Inspect the rendered result for B09 browser acceptance checks."""
    page.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
    text = page.locator('[data-testid="marriage-result"]').inner_text()
    overflow = page.evaluate(
        """() => {
          const root = document.querySelector('[data-testid="marriage-result"]');
          if (!root) return true;
          return root.scrollWidth > root.clientWidth + 1;
        }"""
    )
    return {
        "has_result": True,
        "has_hero": page.locator('[data-testid="compatibility-hero"]').count() > 0,
        "semantic_only": page.locator('[data-testid="compatibility-hero"]').get_attribute("data-semantic-only")
        == "true",
        "has_summary": page.locator('[data-testid="executive-summary"]').count() > 0,
        "has_domains": page.locator('[data-testid="domain-analysis"]').count() > 0,
        "has_actions": page.locator('[data-testid="action-plan"]').count() > 0,
        "has_confidence": page.locator('[data-testid="confidence-limitations"]').count() > 0,
        "fake_score": ("/100" in text) or ("82%" in text) or ("Grade A" in text),
        "id_leak": bool(__import__("re").search(_ID_LEAK, text)),
        "overflow": overflow,
        "unavailable_empty_interaction": page.locator('[data-domain="interaction"]').count() > 0,
    }


def main() -> None:
    """Capture required B09 smoke screenshots from a live consultation."""
    OUT.mkdir(parents=True, exist_ok=True)
    server = _serve()
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        thread.join(0.05)
    origin = f"http://{HOST}:{PORT}"
    verification: dict[str, object] = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        desktop = browser.new_page(viewport={"width": 1280, "height": 900})
        desktop.goto(f"{origin}/marriage-consulting", wait_until="networkidle")
        desktop.screenshot(path=str(OUT / "01_input.png"), full_page=True)
        _fill_person(desktop, "a", "Nguyễn An", "male", "21/01/1987", "04:30")
        _fill_person(desktop, "b", "Trần Bình", "female", "15/05/1990", "10:00")
        desktop.click('[data-testid="submit-marriage"]')
        verification["desktop"] = _assert_customer_result(desktop)
        desktop.locator('[data-testid="compatibility-hero"]').screenshot(path=str(OUT / "02_hero_summary.png"))
        desktop.locator('[data-testid="executive-summary"]').screenshot(path=str(OUT / "02b_summary.png"))
        desktop.locator('[data-testid="domain-analysis"]').screenshot(path=str(OUT / "03_domains.png"))
        desktop.locator('[data-testid="action-plan"]').screenshot(path=str(OUT / "04_action_plan.png"))
        desktop.locator('[data-testid="confidence-limitations"]').screenshot(
            path=str(OUT / "05_confidence_limitations.png")
        )
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(f"{origin}/marriage-consulting", wait_until="networkidle")
        _fill_person(mobile, "a", "Nguyễn An", "male", "21/01/1987")
        _fill_person(mobile, "b", "Trần Bình", "female", "15/05/1990")
        mobile.click('[data-testid="submit-marriage"]')
        verification["mobile"] = _assert_customer_result(mobile)
        mobile.screenshot(path=str(OUT / "06_mobile_result.png"), full_page=True)
        browser.close()
    (OUT.parent / "browser_verification.json").write_text(
        json.dumps(verification, indent=2) + "\n",
        encoding="utf-8",
    )
    server.should_exit = True


if __name__ == "__main__":
    main()
