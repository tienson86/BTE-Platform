"""Capture N-REL-01 Pack05 → V2 → rollback Pack05 screenshots for CASE-0001."""

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
OUT = REPO / "implementation" / "narrative_release" / "n_rel_01" / "screenshots"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
CONSULTING_PREFIX = "Điểm nổi bật ở đây là"


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


def _assert_provider(page, provider: str) -> None:
    page.wait_for_selector('[data-dashboard="commercial-v1"]')
    page.wait_for_selector('[data-narrative-surface="production"]')
    page.wait_for_selector(f'[data-narrative-provider="{provider}"]')
    page.wait_for_selector("text=Nguyễn Tiến Sơn")


def main() -> None:
    """Capture Pack05 production, V2 production, and Pack05 rollback."""
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
            desktop.wait_for_selector("text=Nguyễn Tiến Sơn")

            stored = desktop.evaluate("() => sessionStorage.getItem('bte_last_result')")
            if not stored:
                raise RuntimeError("ResultStore did not persist CASE-0001")
            payload = json.loads(stored)
            data = payload.get("data") or {}
            if (data.get("narrative_result") or {}).get("contract") != "pack05_narrative_result_v1":
                raise RuntimeError("Pack05 layer missing from ResultStore")
            shadow = data.get("narrative_v2_shadow") or {}
            if shadow.get("status") != "ok" or not shadow.get("presentation"):
                raise RuntimeError(f"Narrative V2 layer missing: {shadow!r}")

            desktop.goto(f"{BASE}/result?provider=pack05", wait_until="networkidle")
            _assert_provider(desktop, "pack05")
            body = desktop.inner_text("body")
            if CONSULTING_PREFIX in body:
                raise RuntimeError("Pack05 production rendered Narrative V2 consulting_flow")
            desktop.screenshot(path=str(OUT / "01_pack05_production.png"), full_page=True)

            desktop.goto(f"{BASE}/result?provider=v2", wait_until="networkidle")
            _assert_provider(desktop, "v2")
            desktop.wait_for_selector(f"text={CONSULTING_PREFIX}")
            desktop.screenshot(path=str(OUT / "02_narrative_v2_production.png"), full_page=True)
            desktop.locator('[data-card="overview"]').screenshot(path=str(OUT / "02a_v2_overview.png"))
            desktop.locator('[data-card="interpretation"]').screenshot(
                path=str(OUT / "02b_v2_interpretation.png")
            )
            desktop.locator('[data-card="action-plan"]').screenshot(path=str(OUT / "02c_v2_action.png"))

            desktop.goto(f"{BASE}/result?provider=pack05", wait_until="networkidle")
            _assert_provider(desktop, "pack05")
            body = desktop.inner_text("body")
            if CONSULTING_PREFIX in body:
                raise RuntimeError("Rollback still rendered Narrative V2 consulting_flow")
            layers = desktop.evaluate(
                """() => {
                  const store = window.BtePortal && window.BtePortal.ResultStore;
                  return store && store.selectNarrativeLayers ? store.selectNarrativeLayers() : null;
                }"""
            )
            if not layers or not layers.get("pack05") or not layers.get("narrative_v2"):
                raise RuntimeError(f"Rollback lost ResultStore layers: {layers!r}")
            desktop.screenshot(path=str(OUT / "03_rollback_pack05.png"), full_page=True)
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
