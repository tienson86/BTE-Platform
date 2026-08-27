"""Capture DS-06A /good-date screenshots.

Starts the Applications API and Customer Portal if they are not already
listening, then writes PNGs under docs/reports/date_selection/screenshots/.
"""

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
    """Stop whatever currently owns the screenshot ports so captures use this tree."""
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
    else:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True, check=False)
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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1100})
            page.goto("http://127.0.0.1:8081/good-date", wait_until="networkidle")
            page.wait_for_selector("#dsCalendar .ds-day[data-day]")
            page.wait_for_function(
                """() => {
                  const text = document.getElementById('dsDetail')?.textContent || '';
                  return text.includes('Can Chi tháng') && text.includes('Nạp âm') && text.includes('Quý Dậu');
                }"""
            )
            page.screenshot(path=str(OUT / "01_good_date_desktop_full.png"), full_page=True)
            page.locator(".ds-detail").screenshot(path=str(OUT / "03_compact_ket_qua_ngay.png"))
            page.locator(".ds-hour").screenshot(path=str(OUT / "04_compact_chon_gio.png"))
            page.locator(".ds-left").screenshot(path=str(OUT / "05_calendar_clock_left.png"))
            page.locator(".ds-ke").screenshot(path=str(OUT / "06_six_khac_panel.png"))
            page.set_viewport_size({"width": 390, "height": 844})
            page.goto("http://127.0.0.1:8081/good-date", wait_until="networkidle")
            page.wait_for_selector("#dsCalendar .ds-day[data-day]")
            page.screenshot(path=str(OUT / "02_good_date_mobile.png"), full_page=True)
            browser.close()
    finally:
        for proc in (portal_proc, api_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
