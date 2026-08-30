"""Capture UI-14 CASE-0001 Commercial Dashboard screenshots."""

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
OUT = REPO / "implementation" / "commercial_ui_polish" / "ui14" / "screenshots"
BEFORE_SRC = REPO / "implementation" / "narrative_release" / "n_rel_01" / "screenshots"
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


def _copy_before() -> None:
    mapping = {
        "02_narrative_v2_production.png": "before_desktop_full.png",
        "02a_v2_overview.png": "before_overview.png",
        "02b_v2_interpretation.png": "before_interpretation.png",
        "02c_v2_action.png": "before_action.png",
    }
    for src_name, dest_name in mapping.items():
        src = BEFORE_SRC / src_name
        if src.exists():
            shutil.copyfile(src, OUT / dest_name)


def _build_result() -> None:
    npm = "npm.cmd" if os.name == "nt" else "npm"
    subprocess.run([npm, "run", "build:result"], cwd=str(PORTAL), check=True)


def main() -> None:
    """Render CASE-0001 Narrative V2 Presentation and capture UI-14 viewports."""
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
            desktop = browser.new_page(viewport={"width": 1440, "height": 1100})
            desktop.goto(f"{BASE}/analyze", wait_until="networkidle")
            desktop.wait_for_selector("#analyzeForm")
            _fill_case_0001(desktop)
            desktop.click("#btnAnalyze")
            desktop.wait_for_url("**/result", timeout=180000)
            desktop.wait_for_selector('[data-dashboard="commercial-v1"]')
            desktop.wait_for_selector('[data-visual="v2"]')
            desktop.wait_for_selector("text=Nguyễn Tiến Sơn")

            desktop.goto(f"{BASE}/result?provider=v2", wait_until="networkidle")
            desktop.wait_for_selector('[data-narrative-provider="v2"]')
            desktop.wait_for_selector('[data-card="overview"]')
            desktop.screenshot(path=str(OUT / "desktop_full.png"), full_page=True)
            desktop.locator('[data-card="overview"]').screenshot(path=str(OUT / "hero_overview.png"))
            desktop.locator('[data-overview-section="insight"]').screenshot(
                path=str(OUT / "overview_insight.png")
            )
            desktop.locator('[data-card="interpretation"]').screenshot(
                path=str(OUT / "interpretation.png")
            )
            desktop.locator('[data-card="action-plan"]').screenshot(path=str(OUT / "action.png"))

            desktop.set_viewport_size({"width": 834, "height": 1112})
            desktop.reload(wait_until="networkidle")
            desktop.wait_for_selector('[data-card="overview"]')
            desktop.screenshot(path=str(OUT / "tablet_full.png"), full_page=True)
            desktop.locator('[data-card="overview"]').screenshot(path=str(OUT / "tablet_hero.png"))

            desktop.set_viewport_size({"width": 390, "height": 844})
            desktop.reload(wait_until="networkidle")
            desktop.wait_for_selector('[data-card="overview"]')
            desktop.screenshot(path=str(OUT / "mobile_full.png"), full_page=True)
            desktop.locator('[data-card="overview"]').screenshot(path=str(OUT / "mobile_hero.png"))
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
