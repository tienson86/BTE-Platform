"""Capture UI-10R1 compact Luck header screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui10r1"
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


def _shot_header(page, path: Path) -> None:
    card = page.locator('[data-card="luck"]').first
    current = page.locator('[data-card="luck"] [data-luck-section="current"]').first
    start = page.locator('[data-card="luck"] [data-luck-section="start"]').first
    card.wait_for()
    boxes = [card.bounding_box(), current.bounding_box(), start.bounding_box()]
    if any(box is None for box in boxes):
        raise RuntimeError("luck header boxes missing")
    card_box, current_box, start_box = boxes
    assert card_box and current_box and start_box
    bottom = max(current_box["y"] + current_box["height"], start_box["y"] + start_box["height"])
    page.screenshot(
        path=str(path),
        clip={
            "x": card_box["x"],
            "y": card_box["y"],
            "width": card_box["width"],
            "height": bottom - card_box["y"] + 8,
        },
    )


def _shot_row03(page, path: Path) -> None:
    cards = [
        page.locator('[data-card="shensha"]').first.bounding_box(),
        page.locator('[data-card="luck"]').first.bounding_box(),
    ]
    if any(box is None for box in cards):
        raise RuntimeError("row 03 cards are missing")
    left = min(box["x"] for box in cards if box)
    top = min(box["y"] for box in cards if box)
    right = max(box["x"] + box["width"] for box in cards if box)
    bottom = max(box["y"] + box["height"] for box in cards if box)
    page.screenshot(
        path=str(path),
        clip={"x": left, "y": top, "width": right - left, "height": bottom - top},
    )


def _collapse(page) -> None:
    toggle = page.locator('[data-card="luck"] button.bte-luck__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") == "true":
        toggle.first.click()
        page.wait_for_timeout(200)


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
            page = browser.new_page(viewport={"width": 1440, "height": 1400})
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.fill("#full_name", "Nguyen Tien Son")
            page.check("#gender_male")
            page.fill("#birth_date", "21/01/1987")
            page.fill("#birth_time", "04:30")
            page.fill("#birth_place", "Ha Tay, Viet Nam")
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-card="luck"][data-implemented="luck"]')
            _collapse(page)
            text = page.locator('[data-card="luck"]').inner_text()
            if "dayun_runtime" in text or "{" in text:
                raise RuntimeError("Luck Card leaked runtime JSON")
            _shot_header(page, OUT / "01_luck_compact_header.png")
            _shot_element(page, '[data-card="luck"]', OUT / "02_luck_compact_full_card.png")
            _shot_row03(page, OUT / "03_row03_compact.png")
            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(400)
            _collapse(page)
            _shot_element(page, '[data-card="luck"]', OUT / "04_luck_compact_mobile.png")
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
