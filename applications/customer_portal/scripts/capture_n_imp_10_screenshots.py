"""Capture N-IMP-10 production vs Narrative V2 shadow screenshots."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "implementation" / "narrative_v2" / "n_imp_10"
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


def _fill_case_0001(page) -> None:
    page.fill("#full_name", "Nguyễn Tiến Sơn")
    page.check("#gender_male")
    page.fill("#birth_date", "1987-01-21")
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", "Hà Tây, Việt Nam")


def main() -> None:
    """Capture production /result and Narrative V2 shadow review screenshots."""
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
            desktop = browser.new_page(viewport={"width": 1440, "height": 1100})

            desktop.goto(f"{BASE}/analyze", wait_until="networkidle")
            desktop.wait_for_selector("#analyzeForm")
            _fill_case_0001(desktop)
            desktop.click("#btnAnalyze")
            desktop.wait_for_url("**/result", timeout=180000)
            desktop.wait_for_selector('[data-dashboard="commercial-v1"]')
            desktop.wait_for_selector('[data-narrative-surface="production"]')
            desktop.wait_for_selector("text=Nguyễn Tiến Sơn")
            desktop.screenshot(path=str(OUT / "01_production_result_unchanged.png"), full_page=True)

            stored = desktop.evaluate("() => sessionStorage.getItem('bte_last_result')")
            if not stored:
                raise RuntimeError("ResultStore did not persist CASE-0001")
            payload = json.loads(stored)
            shadow = (payload.get("data") or {}).get("narrative_v2_shadow") or {}
            if shadow.get("status") != "ok" or not shadow.get("presentation"):
                raise RuntimeError(f"narrative_v2_shadow missing: {shadow!r}")

            desktop.goto(f"{BASE}/result?narrative=v2-shadow", wait_until="networkidle")
            desktop.wait_for_selector("[data-narrative-v2-shadow='true']")
            desktop.wait_for_selector("[data-v2-overview]")
            desktop.screenshot(path=str(OUT / "02_narrative_v2_shadow_full.png"), full_page=True)
            desktop.locator("[data-v2-overview]").screenshot(path=str(OUT / "03_narrative_v2_shadow_overview.png"))
            desktop.locator("[data-v2-structured]").evaluate("node => { node.open = true; }")
            desktop.locator("[data-v2-interpretation]").screenshot(
                path=str(OUT / "04_narrative_v2_shadow_interpretation.png")
            )
            desktop.locator("[data-v2-action]").screenshot(path=str(OUT / "05_narrative_v2_shadow_action.png"))

            desktop.goto(f"{BASE}/result?narrative=v2-compare", wait_until="networkidle")
            desktop.wait_for_selector("[data-v2-compare]")
            desktop.screenshot(path=str(OUT / "06_production_vs_v2_comparison.png"), full_page=True)

            mobile = browser.new_page(viewport={"width": 390, "height": 844})
            mobile.add_init_script(f"sessionStorage.setItem('bte_last_result', {json.dumps(stored)});")
            mobile.goto(f"{BASE}/result?narrative=v2-shadow", wait_until="networkidle")
            mobile.wait_for_selector("[data-narrative-v2-shadow='true']")
            mobile.wait_for_selector("[data-v2-overview]")
            mobile.screenshot(path=str(OUT / "07_mobile_shadow.png"), full_page=True)
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
