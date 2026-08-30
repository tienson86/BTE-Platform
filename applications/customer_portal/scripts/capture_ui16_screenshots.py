"""Capture UI-16 CASE-0001 Executive Report Preview screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "implementation" / "commercial_ui_polish" / "ui16" / "screenshots"
PORTAL = REPO / "applications" / "customer_portal"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _kill_port(port: int) -> None:
    if sys.platform == "win32":
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
    env["NARRATIVE_PROVIDER"] = "v2"
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


def _wait(port: int, timeout: float = 45.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _fill_case_0001(page) -> None:
    page.fill("#full_name", "Nguyễn Tiến Sơn")
    page.check("#gender_male")
    page.fill("#birth_date", "1987-01-21")
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", "Hà Tây, Việt Nam")


def _build_result() -> None:
    npm = "npm.cmd" if os.name == "nt" else "npm"
    subprocess.run([npm, "run", "build:result"], cwd=str(PORTAL), check=True)


def _shot(page, selector: str, name: str) -> None:
    locator = page.locator(selector).first
    locator.scroll_into_view_if_needed()
    locator.screenshot(path=str(OUT / name))


def main() -> None:
    """Render CASE-0001 Executive Report Preview."""
    OUT.mkdir(parents=True, exist_ok=True)
    reuse = os.environ.get("BTE_CAPTURE_REUSE") == "1"
    api_proc = None
    portal_proc = None
    if not reuse:
        _build_result()
        _kill_port(API_PORT)
        _kill_port(PORTAL_PORT)
        api_proc = _spawn("applications.api.app:app", API_PORT)
        portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
        try:
            _wait(API_PORT)
            _wait(PORTAL_PORT)
            _capture()
        finally:
            for proc in (portal_proc, api_proc):
                if proc is None:
                    continue
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
        return
    _capture()


def _capture() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto(f"{BASE}/analyze", wait_until="networkidle")
        page.wait_for_selector("#analyzeForm")
        _fill_case_0001(page)
        page.click("#btnAnalyze")
        page.wait_for_url("**/result", timeout=180000)
        page.wait_for_selector('[data-dashboard="commercial-v1"]')
        page.goto(f"{BASE}/report-preview", wait_until="networkidle")
        page.wait_for_selector('[data-ui="executive-report"]')
        page.wait_for_selector('[data-consulting-flow="true"]')

        _shot(page, '[data-report-section="cover"]', "01_cover.png")
        _shot(page, '[data-report-section="executive-summary"]', "02_executive_summary.png")
        _shot(page, '[data-report-section="chart-snapshot"]', "03_core_snapshot.png")
        _shot(page, '[data-report-section="key-findings"]', "04_key_findings.png")
        _shot(page, '[data-report-section="interpretation"]', "05_interpretation.png")
        _shot(page, '[data-report-section="action-plan"]', "06_action_plan.png")
        _shot(page, '[data-report-section="luck"]', "07_luck.png")
        _shot(page, '[data-report-section="supporting"]', "08_supporting_analysis.png")
        page.locator(".bte-er").screenshot(path=str(OUT / "09_full_report_preview.png"))

        page.emulate_media(media="print")
        page.screenshot(path=str(OUT / "10_print_preview.png"), full_page=True)
        page.emulate_media(media="screen")
        browser.close()


if __name__ == "__main__":
    main()
