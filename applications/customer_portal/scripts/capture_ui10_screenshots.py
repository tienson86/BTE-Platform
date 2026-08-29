"""Capture UI-10 Luck visual fixture and live CASE-0001 screenshots."""

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
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui10"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
API = f"http://127.0.0.1:{API_PORT}"


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


def _expand(page) -> None:
    toggle = page.locator('[data-card="luck"] button.bte-luck__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") != "true":
        toggle.first.click()
        page.wait_for_timeout(200)


def _collapse(page) -> None:
    toggle = page.locator('[data-card="luck"] button.bte-luck__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") == "true":
        toggle.first.click()
        page.wait_for_timeout(200)


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


def _report_live_contract(payload: dict[str, object]) -> None:
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    luck = data.get("luck") if isinstance(data, dict) else None
    luck = luck if isinstance(luck, dict) else {}
    current = luck.get("current_cycle") if isinstance(luck.get("current_cycle"), dict) else {}
    cycles = luck.get("cycles") if isinstance(luck.get("cycles"), list) else []
    snapshot = {
        "keys": sorted(str(key) for key in luck.keys()),
        "cycle_count": len(cycles),
        "cycle_names": [
            str(item.get("gan_zhi") or "") for item in cycles if isinstance(item, dict)
        ],
        "current_gan_zhi": current.get("gan_zhi"),
        "current_year_start": current.get("year_start"),
        "current_year_end": current.get("year_end"),
        "current_age_start": current.get("age_start"),
        "current_age_end": current.get("age_end"),
        "direction": luck.get("direction"),
        "direction_label": luck.get("direction_label"),
        "start_age": luck.get("start_age"),
        "has_luck_summary": bool(luck.get("luck_summary")),
        "has_luck_strength": "luck_strength" in luck,
        "sample_cycle_keys": sorted(str(key) for key in (cycles[0].keys() if cycles and isinstance(cycles[0], dict) else [])),
    }
    (OUT / "live_contract.json").write_text(
        json.dumps(snapshot, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )
    print("UI-10 live luck cycles:", snapshot["cycle_count"])


def main() -> None:
    """Capture UI-10 Luck fixture and live screenshots."""
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        try:
            _report_live_contract(_analyze_case_0001())
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            (OUT / "live_contract.json").write_text("analyze failed", encoding="utf-8")
            print("analyze_contract_failed")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1400})

            page.goto(f"{BASE}/result?layout=visual", wait_until="networkidle")
            page.wait_for_selector('[data-card="luck"][data-implemented="luck"]')
            _collapse(page)
            _shot_element(page, '[data-card="luck"]', OUT / "01_luck_visual_desktop.png")
            _expand(page)
            _shot_element(page, '[data-card="luck"]', OUT / "02_luck_visual_expanded.png")
            _collapse(page)
            _shot_row03(page, OUT / "03_row03_visual_complete.png")

            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(400)
            _collapse(page)
            _shot_element(page, '[data-card="luck"]', OUT / "04_luck_visual_mobile.png")

            page.set_viewport_size({"width": 1440, "height": 1400})
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            _fill_case_0001(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-card="luck"][data-implemented="luck"]')
            page.wait_for_selector("text=Nguyễn Tiến Sơn")
            _collapse(page)
            _shot_element(page, '[data-card="luck"]', OUT / "05_luck_live_case0001.png")
            _expand(page)
            _shot_element(page, '[data-card="luck"]', OUT / "06_luck_live_expanded_case0001.png")
            _collapse(page)
            _shot_row03(page, OUT / "07_row03_live_complete.png")
            page.screenshot(path=str(OUT / "09_full_dashboard_ui10.png"), full_page=True)

            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(400)
            _collapse(page)
            _shot_element(page, '[data-card="luck"]', OUT / "08_luck_live_mobile.png")

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
