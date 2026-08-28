"""Capture CP-01 TuTruPanel screenshots on /good-date."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "canonical" / "cp01_tu_tru_panel"
API_PORT = 8000
PORTAL_PORT = 8081


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _spawn(module: str, port: int) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env["BTE_API_BASE_URL"] = f"http://127.0.0.1:{API_PORT}"
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            module,
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=str(REPO),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _wait(port: int, timeout: float = 25.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _wait_panel(page) -> None:
    page.wait_for_selector('[data-canonical="tu-tru-panel"]')
    page.wait_for_function(
        """() => {
          const text = document.querySelector('[data-canonical="tu-tru-panel"]')?.textContent || '';
          return text.includes('TỨ TRỤ') && text.includes('Can Chi') && text.includes('Nạp âm')
            && text.includes('Cung Phi') && text.includes('Năm') && text.includes('Tháng')
            && text.includes('Ngày') && text.includes('Giờ');
        }"""
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started: list[subprocess.Popen[bytes]] = []
    if not _listening(API_PORT):
        started.append(_spawn("applications.api.app:app", API_PORT))
        _wait(API_PORT)
    if not _listening(PORTAL_PORT):
        started.append(_spawn("applications.customer_portal.app:app", PORTAL_PORT))
        _wait(PORTAL_PORT)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1100})
            page.goto("http://127.0.0.1:8081/good-date", wait_until="networkidle")
            page.wait_for_selector("#dsCalendar .ds-day[data-day]")
            _wait_panel(page)
            page.screenshot(path=str(OUT / "01_desktop.png"), full_page=True)
            page.locator('[data-canonical="tu-tru-panel"]').screenshot(path=str(OUT / "02_panel_desktop.png"))
            page.locator(".ds-detail").screenshot(path=str(OUT / "03_day_card_desktop.png"))

            page.set_viewport_size({"width": 768, "height": 1024})
            page.goto("http://127.0.0.1:8081/good-date", wait_until="networkidle")
            page.wait_for_selector("#dsCalendar .ds-day[data-day]")
            _wait_panel(page)
            page.screenshot(path=str(OUT / "04_tablet.png"), full_page=True)
            page.locator('[data-canonical="tu-tru-panel"]').screenshot(path=str(OUT / "05_panel_tablet.png"))

            page.set_viewport_size({"width": 390, "height": 844})
            page.goto("http://127.0.0.1:8081/good-date", wait_until="networkidle")
            page.wait_for_selector("#dsCalendar .ds-day[data-day]")
            _wait_panel(page)
            page.screenshot(path=str(OUT / "06_phone.png"), full_page=True)
            page.locator('[data-canonical="tu-tru-panel"]').screenshot(path=str(OUT / "07_panel_phone.png"))
            browser.close()
    finally:
        for proc in started:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
