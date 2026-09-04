"""UI-05A live /result information architecture screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
PORTAL = REPO / "applications" / "customer_portal"
OUT = REPO / "docs" / "reports" / "ui05a_result_ia" / "screenshots"
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


def _shot(page, path: Path, full: bool = False) -> None:
    if full:
        page.screenshot(path=str(path), full_page=True)
        return
    page.screenshot(path=str(path))


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
        page.wait_for_selector("[data-ia='ui05a']")
        page.wait_for_selector('[data-card="bazi"]')
        page.wait_for_selector('[data-card="overview"]')
        _shot(page, OUT / "01_identity_primary_chart.png")
        page.locator('[data-card="bazi"]').first.scroll_into_view_if_needed()
        _shot(page, OUT / "02_bazi_below_tutru.png")
        page.locator('[data-card="five-elements"]').first.scroll_into_view_if_needed()
        _shot(page, OUT / "03_five_elements_pattern.png")
        page.locator('[data-card="overview"]').first.scroll_into_view_if_needed()
        _shot(page, OUT / "04_overview_after_dna.png")
        page.locator("[data-life-consulting]").first.scroll_into_view_if_needed()
        _shot(page, OUT / "05_consulting_after_summary.png")
        page.locator('[data-card="ten-gods"]').first.scroll_into_view_if_needed()
        _shot(page, OUT / "06_detailed_sections.png")
        _shot(page, OUT / "00_full_page.png", full=True)
        proof = page.evaluate(
            """() => {
              const root = document.querySelector('[data-ia="ui05a"]');
              const grid = root?.querySelector('.bte-cdash__grid');
              const cards = [...(grid?.querySelectorAll('[data-card], [data-life-consulting]') || [])];
              const visual = cards
                .map((node) => {
                  const style = getComputedStyle(node);
                  return {
                    id: node.getAttribute('data-card') || 'life-consulting',
                    order: Number(style.order || 0),
                  };
                })
                .sort((a, b) => a.order - b.order)
                .map((item) => item.id);
              const identity = root?.querySelector('[data-identity-header="true"]');
              return {
                ia: root?.getAttribute('data-ia'),
                visual,
                hasIdentity: Boolean(identity),
                hasPillars: Boolean(identity?.querySelector('[data-region="pillars"]')),
                hasCanXuong: Boolean(identity?.querySelector('[data-region="foundation"]')),
                hasCungPhi: Boolean(identity?.querySelector('[data-region="status"]')),
                overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
              };
            }"""
        )
        expected = [
            "bazi",
            "five-elements",
            "pattern",
            "overview",
            "life-consulting",
            "interpretation",
            "action-plan",
            "ten-gods",
            "shensha",
            "luck",
        ]
        if proof["visual"] != expected:
            raise RuntimeError(f"visual order mismatch: {proof}")
        if proof["overflow"] or not proof["hasIdentity"] or not proof["hasPillars"]:
            raise RuntimeError(f"live IA layout failed: {proof}")
        browser.close()


if __name__ == "__main__":
    main()
