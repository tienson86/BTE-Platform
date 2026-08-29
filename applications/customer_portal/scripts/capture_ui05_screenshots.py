"""Capture UI-05 BaZi visual fixture and live CASE-0001 screenshots."""

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
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui05"
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


def _shot_row01(page, path: Path) -> None:
    overview = page.locator('[data-card="overview"]').first.bounding_box()
    bazi = page.locator('[data-card="bazi"]').first.bounding_box()
    if overview is None or bazi is None:
        raise RuntimeError("row 01 cards are missing")
    left = min(overview["x"], bazi["x"])
    top = min(overview["y"], bazi["y"])
    right = max(overview["x"] + overview["width"], bazi["x"] + bazi["width"])
    bottom = max(overview["y"] + overview["height"], bazi["y"] + bazi["height"])
    page.screenshot(
        path=str(path),
        clip={"x": left, "y": top, "width": right - left, "height": bottom - top},
    )


def _expand_bazi(page) -> None:
    toggle = page.locator('[data-card="bazi"] button.bte-bazi__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") != "true":
        toggle.first.click()
        page.wait_for_timeout(200)


def _collapse_bazi(page) -> None:
    toggle = page.locator('[data-card="bazi"] button.bte-bazi__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") == "true":
        toggle.first.click()
        page.wait_for_timeout(200)


def _pillar_payload(raw: object) -> dict[str, object]:
    return raw if isinstance(raw, dict) else {}


def _report_live_contract(payload: dict[str, object]) -> None:
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    bazi = data.get("bazi") if isinstance(data, dict) and isinstance(data.get("bazi"), dict) else {}
    keys = ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
    snapshot: list[dict[str, object]] = []
    gaps: list[str] = []
    for key in keys:
        pillar = _pillar_payload(bazi.get(key))
        snapshot.append(
            {
                "pillar": key,
                "stem": pillar.get("stem"),
                "branch": pillar.get("branch"),
                "nap_am": pillar.get("nap_am"),
                "hidden_stems": pillar.get("hidden_stems"),
                "ten_god": pillar.get("ten_god"),
                "truong_sinh": pillar.get("truong_sinh"),
                "element": pillar.get("element"),
            }
        )
        if not pillar.get("stem") or not pillar.get("branch"):
            gaps.append(f"{key}: missing stem/branch")
        if not pillar.get("nap_am"):
            gaps.append(f"{key}: missing nap_am")
        if not pillar.get("hidden_stems"):
            gaps.append(f"{key}: missing hidden_stems")
        if key != "day_pillar" and not pillar.get("ten_god"):
            gaps.append(f"{key}: missing ten_god")
        if not pillar.get("truong_sinh"):
            gaps.append(f"{key}: missing truong_sinh")
        if not pillar.get("element"):
            gaps.append(f"{key}: missing stem element (PillarView contract)")
    ten_gods = data.get("ten_gods") if isinstance(data, dict) else None
    if not ten_gods:
        gaps.append("data.ten_gods missing")
    (OUT / "live_contract.json").write_text(
        json.dumps(
            {"pillars": snapshot, "ten_gods_present": bool(ten_gods), "gaps": gaps},
            ensure_ascii=True,
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "live_contract_gaps.txt").write_text("\n".join(gaps) if gaps else "none", encoding="utf-8")
    print("UI-05 live CASE-0001 contract gaps:", len(gaps))


def _analyze_case_0001() -> dict[str, object]:
    body = json.dumps(
        {
            "year": 1987,
            "month": 1,
            "day": 21,
            "hour": 4,
            "minute": 30,
            "gender": "male",
            "full_name": "Nguyễn Tiến Sơn",
            "birth_place": "Hà Tây, Việt Nam",
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
    """Capture UI-05 BaZi fixture and live screenshots."""
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
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            (OUT / "live_contract_gaps.txt").write_text(f"analyze failed: {exc}", encoding="utf-8")
            print("analyze_contract_failed", exc)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1100})

            page.goto(f"{BASE}/result?layout=visual", wait_until="networkidle")
            page.wait_for_selector('[data-card="bazi"][data-implemented="bazi"]')
            _collapse_bazi(page)
            _shot_element(page, '[data-card="bazi"]', OUT / "01_bazi_visual_default_desktop.png")
            _expand_bazi(page)
            _shot_element(page, '[data-card="bazi"]', OUT / "02_bazi_visual_expanded_desktop.png")
            _collapse_bazi(page)
            _shot_row01(page, OUT / "03_row01_visual_overview_bazi.png")

            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(400)
            _collapse_bazi(page)
            _shot_element(page, '[data-card="bazi"]', OUT / "04_bazi_visual_mobile_default.png")
            _expand_bazi(page)
            _shot_element(page, '[data-card="bazi"]', OUT / "05_bazi_visual_mobile_expanded.png")

            page.set_viewport_size({"width": 1440, "height": 1100})
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            _fill_case_0001(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-card="bazi"][data-implemented="bazi"]')
            page.wait_for_selector("text=Nguyễn Tiến Sơn")
            _collapse_bazi(page)
            _shot_element(page, '[data-card="bazi"]', OUT / "06_bazi_live_case0001_default.png")
            _expand_bazi(page)
            _shot_element(page, '[data-card="bazi"]', OUT / "07_bazi_live_case0001_expanded.png")
            _collapse_bazi(page)
            _shot_row01(page, OUT / "08_row01_live_case0001.png")
            page.screenshot(path=str(OUT / "10_full_dashboard_ui05.png"), full_page=True)

            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(400)
            _collapse_bazi(page)
            _shot_element(page, '[data-card="bazi"]', OUT / "09_bazi_live_mobile.png")

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
