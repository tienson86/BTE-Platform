"""Capture DS-06C /choose-date evidence screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "date_selection" / "screenshots"
API_PORT = 8000
PORTAL_PORT = 8081


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _kill_port(port: int) -> None:
    if os.name == "nt":
        lookup = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            check=False,
        )
        pids: set[str] = set()
        for line in lookup.stdout.splitlines():
            if f":{port} " not in line or "LISTENING" not in line.upper():
                continue
            pid = line.split()[-1]
            if pid.isdigit() and pid != "0":
                pids.add(pid)
        for pid in pids:
            subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True, check=False)
    deadline = time.time() + 5
    while time.time() < deadline and _listening(port):
        time.sleep(0.2)


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


def _wait(port: int, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _search(page) -> None:
    page.goto("http://127.0.0.1:8081/choose-date", wait_until="networkidle")
    page.wait_for_selector("#dsSearchForm")
    page.fill("#dsFullName", "Nguyễn Tiến Sơn")
    page.select_option("#dsGender", "male")
    page.fill("#dsBirth", "21011987")
    page.fill("#dsTargetMonth", "092026")
    page.click("#dsSearchBtn")
    page.wait_for_selector("[data-testid='ranked-card']")
    page.wait_for_selector("[data-testid='recommended-hour']")
    page.wait_for_selector("[data-testid='trach-match']")
    page.wait_for_selector("[data-testid='other-ke-list']")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api = _spawn("applications.api.app:app", API_PORT)
    portal = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1600})
            _search(page)
            page.locator("#dsResults").screenshot(path=str(OUT / "ds06c_01_choose_date_top5_desktop.png"))
            page.locator("[data-testid='ranked-card']").first.screenshot(
                path=str(OUT / "ds06c_02_complete_date_card.png")
            )
            page.locator("[data-testid='recommended-hour']").first.screenshot(
                path=str(OUT / "ds06c_03_recommended_hour_detail.png")
            )
            page.locator("[data-testid='trach-match']").first.screenshot(
                path=str(OUT / "ds06c_04_trach_match.png")
            )
            other = page.locator("[data-testid='other-ke-list']")
            if other.count():
                other.first.screenshot(path=str(OUT / "ds06c_05_other_ke.png"))
            else:
                page.locator("[data-testid='recommended-hour']").first.screenshot(
                    path=str(OUT / "ds06c_05_other_ke.png")
                )
            mobile = browser.new_page(viewport={"width": 375, "height": 900})
            _search(mobile)
            mobile.locator("#dsResults").screenshot(path=str(OUT / "ds06c_06_choose_date_mobile.png"))
            browser.close()
    finally:
        api.terminate()
        portal.terminate()


if __name__ == "__main__":
    main()
