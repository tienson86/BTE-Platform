"""P-003C live /result Ten Gods layout screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
PORTAL = REPO / "applications" / "customer_portal"
OUT = REPO / "docs" / "reports" / "p003c_ten_gods_layout" / "screenshots"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _build_result() -> None:
    npm = "npm.cmd" if os.name == "nt" else "npm"
    result = subprocess.run(
        [npm, "run", "build:result"],
        cwd=str(PORTAL),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "vite build failed")


def _fill_case_0001(page) -> None:
    page.fill("#full_name", "Nguyễn Tiến Sơn")
    page.check("#gender_male")
    page.fill("#birth_date", "1987-01-21")
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", "Hà Tây, Việt Nam")


def _shot(page, selector: str, path: Path) -> None:
    locator = page.locator(selector).first
    locator.wait_for()
    locator.scroll_into_view_if_needed()
    locator.screenshot(path=str(path))


def _wait_portal() -> None:
    deadline = time.time() + 20
    while time.time() < deadline:
        if _listening(PORTAL_PORT) and _listening(API_PORT):
            return
        time.sleep(0.25)
    raise RuntimeError("portal/api not listening")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _build_result()
    _wait_portal()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto(f"{BASE}/analyze", wait_until="networkidle")
        page.wait_for_selector("#analyzeForm")
        _fill_case_0001(page)
        page.click("#btnAnalyze")
        page.wait_for_url("**/result", timeout=120000)
        page.wait_for_selector('[data-card="ten-gods"][data-tg-layout="consulting-v1"]')
        page.wait_for_selector("[data-tg-combination]")
        page.wait_for_selector('.bte-tg__consult-list[data-tg-count="3"]')
        _shot(page, '[data-card="ten-gods"]', OUT / "02_after_full_module.png")
        _shot(page, "[data-tg-combination]", OUT / "03_combination_hero.png")
        _shot(page, '[data-tg-section="commercial"]', OUT / "04_single_cards_compact.png")
        page.locator('[data-tg-commercial="Thất Sát"] button.bte-tg__more').first.click()
        page.wait_for_timeout(200)
        _shot(page, '[data-tg-commercial="Thất Sát"]', OUT / "05_single_card_expanded.png")
        page.locator('[data-tg-commercial="Thất Sát"] button.bte-tg__more').first.click()
        page.wait_for_timeout(200)
        page.set_viewport_size({"width": 900, "height": 1100})
        page.wait_for_timeout(400)
        _shot(page, '[data-card="ten-gods"]', OUT / "06_tablet.png")
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(400)
        toggle = page.locator('[data-card="ten-gods"] .bte-mobile-toggle').first
        if toggle.count() and toggle.get_attribute("aria-expanded") != "true":
            toggle.click()
            page.wait_for_timeout(200)
        _shot(page, '[data-card="ten-gods"]', OUT / "07_mobile.png")
        proof = page.evaluate(
            """() => {
              const card = document.querySelector('[data-card="ten-gods"]');
              const width = card ? card.getBoundingClientRect().width : 0;
              const parent = card?.parentElement?.getBoundingClientRect().width || 0;
              return {
                layout: card?.getAttribute('data-tg-layout'),
                count: card?.querySelector('.bte-tg__consult-list')?.getAttribute('data-tg-count'),
                combo: Boolean(card?.querySelector('[data-tg-combination]')),
                overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
                fullWidth: parent > 0 ? width / parent > 0.9 : false,
              };
            }"""
        )
        if proof["layout"] != "consulting-v1" or proof["count"] != "3" or not proof["combo"]:
            raise RuntimeError(f"live Ten Gods layout failed: {proof}")
        if proof["overflow"]:
            raise RuntimeError("mobile horizontal overflow")
        browser.close()


if __name__ == "__main__":
    main()
