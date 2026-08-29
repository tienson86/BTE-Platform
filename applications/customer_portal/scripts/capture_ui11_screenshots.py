"""Capture UI-11 Interpretation Phase A fixture and Phase B live screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui11"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
PORTAL = REPO / "applications" / "customer_portal"


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


def _build_result() -> None:
    npm = "npm.cmd" if os.name == "nt" else "npm"
    subprocess.run([npm, "run", "build:result"], cwd=str(PORTAL), check=True)


def _shot_element(page, selector: str, path: Path) -> None:
    locator = page.locator(selector).first
    locator.wait_for()
    locator.screenshot(path=str(path))


def _expand(page) -> None:
    toggle = page.locator('[data-card="interpretation"] button.bte-int__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") != "true":
        toggle.first.click()
        page.wait_for_timeout(200)


def _collapse(page) -> None:
    toggle = page.locator('[data-card="interpretation"] button.bte-int__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") == "true":
        toggle.first.click()
        page.wait_for_timeout(200)


def _assert_safe(text: str) -> None:
    lowered = text.lower()
    if "dayun_runtime" in lowered or "source_unit_ids" in lowered or "{" in text:
        raise RuntimeError("Interpretation Card leaked technical content")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
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
            page = browser.new_page(viewport={"width": 1440, "height": 1600})
            page.goto(f"{BASE}/result?layout=visual", wait_until="networkidle")
            page.wait_for_selector('[data-card="interpretation"][data-implemented="interpretation"]')
            _collapse(page)
            _shot_element(page, '[data-card="interpretation"]', OUT / "01_interpretation_visual_desktop.png")
            _expand(page)
            _shot_element(page, '[data-card="interpretation"]', OUT / "02_interpretation_visual_expanded.png")
            page.set_viewport_size({"width": 390, "height": 1100})
            page.wait_for_timeout(400)
            _collapse(page)
            _shot_element(page, '[data-card="interpretation"]', OUT / "03_interpretation_visual_mobile.png")

            page.set_viewport_size({"width": 1440, "height": 2200})
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.fill("#full_name", "Nguyen Tien Son")
            page.check("#gender_male")
            page.fill("#birth_date", "21/01/1987")
            page.fill("#birth_time", "04:30")
            page.fill("#birth_place", "Ha Tay, Viet Nam")
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-card="interpretation"][data-implemented="interpretation"]')
            page.wait_for_selector('[data-card="action-plan"][data-skeleton="true"]')
            _collapse(page)
            live = page.locator('[data-card="interpretation"]').inner_text()
            _assert_safe(live)
            if "Chưa đủ dữ liệu để tạo luận giải tổng thể" in live:
                raise RuntimeError("Live CASE-0001 Interpretation is empty")
            _shot_element(page, '[data-card="interpretation"]', OUT / "04_interpretation_live_case0001.png")
            _expand(page)
            _shot_element(page, '[data-card="interpretation"]', OUT / "05_interpretation_live_expanded_case0001.png")
            page.set_viewport_size({"width": 390, "height": 1400})
            page.wait_for_timeout(400)
            _collapse(page)
            _shot_element(page, '[data-card="interpretation"]', OUT / "06_interpretation_live_mobile.png")
            page.set_viewport_size({"width": 1440, "height": 2800})
            page.wait_for_timeout(400)
            _collapse(page)
            page.locator(".bte-cdash").first.screenshot(path=str(OUT / "07_full_dashboard_ui11.png"))
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
