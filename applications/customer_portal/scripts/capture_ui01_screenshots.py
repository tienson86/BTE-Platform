"""Capture UI-01 Customer Portal shell & navigation screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui01"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"


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
    """Capture UI-01 / UI-01A Customer Portal shell screenshots."""
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

            page.goto(f"{BASE}/", wait_until="networkidle")
            page.wait_for_selector('[data-customer-nav="primary"]')
            page.wait_for_selector('[data-screen="lookup"]')
            page.screenshot(path=str(OUT / "01_home_good_date.png"), full_page=True)

            page.goto(f"{BASE}/choose-date", wait_until="networkidle")
            page.wait_for_selector('[data-screen="search"]')
            page.screenshot(path=str(OUT / "02_good_date_selection.png"), full_page=True)

            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            page.wait_for_selector("h1")
            page.screenshot(path=str(OUT / "03_view_chart_current.png"), full_page=True)

            header = page.locator(".app-header")
            header.screenshot(path=str(OUT / "04_customer_nav_full.png"))

            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(f"{BASE}/", wait_until="networkidle")
            page.wait_for_selector("#btnNavToggle")
            page.locator("#btnNavToggle").click()
            page.wait_for_selector('[data-customer-nav="primary"] a')
            page.screenshot(path=str(OUT / "05_mobile_nav.png"), full_page=True)

            page.set_viewport_size({"width": 1440, "height": 1100})
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            page.fill("#full_name", "Nguyễn Văn A")
            page.fill("#birth_place", "Hà Nội")
            page.fill("#year", "1990")
            page.fill("#month", "5")
            page.fill("#day", "15")
            page.fill("#hour", "10")
            page.fill("#minute", "30")
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-customer-nav="primary"]')
            page.wait_for_selector("#canonical-desktop-root")
            page.wait_for_selector(".cd-root")
            page.screenshot(path=str(OUT / "07_flow_analyze_to_result.png"), full_page=True)
            page.screenshot(path=str(OUT / "06_result_new_shell.png"), full_page=True)

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
