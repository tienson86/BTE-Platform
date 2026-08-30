"""Capture UI-17 CASE-0001 print-ready Executive Report screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "implementation" / "commercial_ui_polish" / "ui17" / "screenshots"
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


def _preflight() -> None:
    """Fail fast if the preview route is missing from the running portal."""
    import urllib.request

    deadline = time.time() + 20
    last_error = ""
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{BASE}/report-preview", timeout=3) as response:
                if response.status == 200:
                    return
                last_error = f"status {response.status}"
        except Exception as exc:
            last_error = str(exc)
        time.sleep(0.4)
    raise RuntimeError(f"/report-preview not ready: {last_error}")


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
    """Render CASE-0001 print preview."""
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
            _preflight()
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
        page.wait_for_selector('[data-print-ready="true"]', timeout=60000)
        page.wait_for_selector('[data-consulting-flow="true"]')
        page.emulate_media(media="print")

        _shot(page, '[data-print="cover"]', "01_cover.png")
        _shot(page, '[data-report-section="executive-summary"]', "02_executive.png")
        _shot(page, '[data-report-section="interpretation"]', "03_interpretation.png")
        _shot(page, '[data-report-section="action-plan"]', "04_action.png")
        _shot(page, '[data-report-section="appendix"]', "05_appendix.png")
        page.screenshot(path=str(OUT / "06_print_preview.png"), full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
