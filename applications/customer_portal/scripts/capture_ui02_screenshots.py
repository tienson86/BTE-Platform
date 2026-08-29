"""Capture UI-02 Screen 01 (Xem lá số) screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import Route, sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui02"
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


def _fill_form(page) -> None:
    page.fill("#full_name", "Nguyễn Văn A")
    page.check("#gender_male")
    page.fill("#birth_date", "1990-05-15")
    page.fill("#birth_time", "10:30")
    page.fill("#birth_place", "Hà Nội")


def main() -> None:
    """Capture UI-02 View Chart screenshots from a live Customer Portal."""
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

            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            page.wait_for_selector("h1")
            page.screenshot(path=str(OUT / "01_view_chart_desktop.png"), full_page=True)

            _fill_form(page)
            page.screenshot(path=str(OUT / "02_view_chart_filled.png"), full_page=True)

            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            page.click("#btnAnalyze")
            page.wait_for_selector("#err_gender:not([hidden])")
            page.screenshot(path=str(OUT / "03_view_chart_validation.png"), full_page=True)

            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            _fill_form(page)

            def delay_analyze(route: Route) -> None:
                if "/api/v1/analyze" in route.request.url and route.request.method == "POST":
                    time.sleep(1.6)
                route.continue_()

            page.route("**/backend/**", delay_analyze)
            page.click("#btnAnalyze")
            page.wait_for_selector("#analyzeStatus:not([hidden])")
            page.screenshot(path=str(OUT / "04_view_chart_loading.png"), full_page=True)
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector(".cd-root")
            page.screenshot(path=str(OUT / "06_result_after_submit.png"), full_page=True)
            page.unroute("**/backend/**")

            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            page.screenshot(path=str(OUT / "05_view_chart_mobile.png"), full_page=True)

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
