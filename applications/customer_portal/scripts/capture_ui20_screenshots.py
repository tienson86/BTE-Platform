"""Capture UI-20 Commercial Finish CASE-0001 baseline screenshots."""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "implementation" / "commercial_ui_polish" / "ui20" / "screenshots"
BEFORE_NREL = REPO / "implementation" / "narrative_release" / "n_rel_01" / "screenshots"
BEFORE_UI14 = REPO / "implementation" / "commercial_ui_polish" / "ui14" / "screenshots"
BEFORE_UI16 = REPO / "implementation" / "commercial_ui_polish" / "ui16" / "screenshots"
BEFORE_UI17 = REPO / "implementation" / "commercial_ui_polish" / "ui17" / "screenshots"
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


def _wait(port: int, timeout: float = 20.0) -> None:
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


def _copy_before() -> None:
    mapping = {
        BEFORE_NREL / "02_narrative_v2_production.png": "before_desktop_full.png",
        BEFORE_UI14 / "mobile_full.png": "before_mobile.png",
        BEFORE_UI16 / "09_full_report_preview.png": "before_report.png",
        BEFORE_UI17 / "06_print_preview.png": "before_print.png",
    }
    for src, dest in mapping.items():
        if src.exists():
            shutil.copyfile(src, OUT / dest)


def _shot(page, selector: str, name: str) -> None:
    locator = page.locator(selector).first
    locator.scroll_into_view_if_needed()
    locator.screenshot(path=str(OUT / name))


def main() -> None:
    """Capture the UI-20 freeze baseline for CASE-0001."""
    OUT.mkdir(parents=True, exist_ok=True)
    _copy_before()
    _build_result()
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
            _fill_case_0001(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=180000)
            page.wait_for_selector('[data-finish="v2"]')
            page.goto(f"{BASE}/result?provider=v2", wait_until="networkidle")
            page.wait_for_selector('[data-card="overview"]')
            page.wait_for_timeout(400)

            page.set_viewport_size({"width": 1920, "height": 1100})
            page.screenshot(path=str(OUT / "desktop_1920.png"), full_page=True)
            page.set_viewport_size({"width": 1280, "height": 1100})
            page.screenshot(path=str(OUT / "desktop_1280.png"), full_page=True)
            page.set_viewport_size({"width": 1440, "height": 1100})
            page.screenshot(path=str(OUT / "desktop_full.png"), full_page=True)
            _shot(page, '[data-card="overview"]', "desktop_hero.png")
            _shot(page, '[data-card="interpretation"]', "desktop_interpretation.png")
            _shot(page, '[data-card="action-plan"]', "desktop_action.png")
            _shot(page, '[data-card="five-elements"]', "desktop_visualizations.png")

            page.set_viewport_size({"width": 834, "height": 1112})
            page.reload(wait_until="networkidle")
            page.wait_for_selector('[data-card="overview"]')
            page.screenshot(path=str(OUT / "tablet_full.png"), full_page=True)

            page.set_viewport_size({"width": 390, "height": 844})
            page.reload(wait_until="networkidle")
            page.wait_for_selector('[data-card="overview"]')
            page.wait_for_timeout(400)
            page.screenshot(path=str(OUT / "mobile_full.png"), full_page=True)
            _shot(page, '[data-card="overview"]', "mobile_hero.png")
            _shot(page, '[data-card="action-plan"]', "mobile_action.png")
            _shot(page, '[data-card="interpretation"]', "mobile_interpretation.png")
            _shot(page, '[data-card="five-elements"]', "mobile_evidence.png")

            page.set_viewport_size({"width": 1440, "height": 1100})
            page.goto(f"{BASE}/report-preview", wait_until="networkidle")
            page.wait_for_selector('[data-ui="executive-report"]', timeout=60000)
            _shot(page, '[data-report-section="cover"]', "report_cover.png")
            _shot(page, '[data-report-section="executive-summary"]', "report_executive.png")
            _shot(page, '[data-report-section="interpretation"]', "report_interpretation.png")
            _shot(page, '[data-report-section="action-plan"]', "report_action.png")
            page.locator(".bte-er").screenshot(path=str(OUT / "report_full.png"))

            page.emulate_media(media="print")
            _shot(page, '[data-report-section="cover"]', "print_cover.png")
            _shot(page, '[data-report-section="executive-summary"]', "print_page.png")
            _shot(page, '[data-report-section="appendix"]', "print_appendix.png")
            page.emulate_media(media="screen")
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
