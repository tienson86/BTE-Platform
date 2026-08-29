"""Capture UI-03R2 Tứ Trụ short Nạp âm screenshots."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui03r2"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
API = f"http://127.0.0.1:{API_PORT}"
VIEWPORT = {"width": 1440, "height": 1100}


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


def _shot_element(page, selector: str, path: Path) -> None:
    locator = page.locator(selector).first
    locator.wait_for()
    locator.screenshot(path=str(path))


def _shot_clip(page, selectors: list[str], path: Path) -> None:
    boxes = [page.locator(selector).first.bounding_box() for selector in selectors]
    if any(box is None for box in boxes):
        raise RuntimeError("clip selectors missing")
    left = min(box["x"] for box in boxes if box)
    top = min(box["y"] for box in boxes if box)
    right = max(box["x"] + box["width"] for box in boxes if box)
    bottom = max(box["y"] + box["height"] for box in boxes if box)
    page.screenshot(
        path=str(path),
        clip={"x": left, "y": top, "width": right - left, "height": bottom - top},
    )


def _analyze_case_0001() -> dict[str, object]:
    body = json.dumps(
        {
            "year": 1987,
            "month": 1,
            "day": 21,
            "hour": 4,
            "minute": 30,
            "gender": "male",
            "full_name": "Nguyen Tien Son",
            "birth_place": "Ha Tay, Viet Nam",
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{API}/api/v1/analyze",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    """Capture UI-03R2 short Nạp âm screenshots."""
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        try:
            _analyze_case_0001()
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            print("analyze_warmup_failed")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport=VIEWPORT)
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            _fill_case_0001(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-region="pillars"] [data-kind="nap-am"]')
            page.wait_for_selector('[data-card="bazi"] [data-bazi-field="nap-am"]')
            page.wait_for_selector("text=Nguyễn Tiến Sơn")
            nap_am = page.locator('[data-region="pillars"] [data-kind="nap-am"]').all_inner_texts()
            print("tutru_napam", [item.encode("ascii", "replace").decode("ascii") for item in nap_am])
            _shot_element(page, '[data-region="pillars"]', OUT / "01_tutru_short_napam.png")
            _shot_clip(
                page,
                ['[data-region="pillars"]', '[data-card="bazi"]'],
                OUT / "02_tutru_vs_bazi_napam.png",
            )
            page.screenshot(path=str(OUT / "03_first_viewport_polished.png"))
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
