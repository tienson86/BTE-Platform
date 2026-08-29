"""Capture UI-03R1 Tứ Trụ summary vs Bát Tự detail screenshots."""

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
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui03r1"
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


def _compose(left: Path, right: Path, dest: Path, left_label: str, right_label: str) -> None:
    from PIL import Image, ImageDraw, ImageFont

    a = Image.open(left).convert("RGB")
    b = Image.open(right).convert("RGB")
    label_h = 36
    gap = 16
    target_h = max(a.height, b.height)
    a = a.resize((int(a.width * target_h / a.height), target_h))
    b = b.resize((int(b.width * target_h / b.height), target_h))
    canvas = Image.new("RGB", (a.width + b.width + gap, target_h + label_h), (242, 241, 239))
    canvas.paste(a, (0, label_h))
    canvas.paste(b, (a.width + gap, label_h))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((12, 10), left_label, fill=(92, 101, 112), font=font)
    draw.text((a.width + gap + 12, 10), right_label, fill=(154, 27, 27), font=font)
    canvas.save(dest)


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


def _report_cung_phi(payload: dict[str, object]) -> None:
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    identity = data.get("identity") if isinstance(data, dict) else None
    four = identity.get("four_pillars") if isinstance(identity, dict) else None
    four = four if isinstance(four, dict) else {}
    snapshot = {}
    for key in ("year", "month", "day", "hour"):
        cell = four.get(key)
        cell = cell if isinstance(cell, dict) else {}
        snapshot[key] = {
            "can_chi": cell.get("can_chi"),
            "nayin_element": cell.get("nayin_element"),
            "cung_phi": cell.get("cung_phi"),
            "nap_am": None,
        }
    bazi = data.get("bazi") if isinstance(data, dict) else None
    bazi = bazi if isinstance(bazi, dict) else {}
    for key, field in (
        ("year", "year_pillar"),
        ("month", "month_pillar"),
        ("day", "day_pillar"),
        ("hour", "hour_pillar"),
    ):
        pillar = bazi.get(field)
        pillar = pillar if isinstance(pillar, dict) else {}
        snapshot[key]["nap_am"] = pillar.get("nap_am")
        snapshot[key]["bazi_cung_phi"] = pillar.get("cung_phi")
    (OUT / "cung_phi_contract.json").write_text(
        json.dumps(snapshot, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )
    print("cung_phi_contract", json.dumps(snapshot, ensure_ascii=True))


def main() -> None:
    """Capture UI-03R1 Good Date vs Result Tứ Trụ and Bát Tự screenshots."""
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        try:
            _report_cung_phi(_analyze_case_0001())
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            print("analyze_contract_failed")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport=VIEWPORT)

            page.goto(f"{BASE}/good-date", wait_until="networkidle")
            page.wait_for_selector("#dsCalendar .ds-day[data-day]")
            page.wait_for_selector('[data-canonical="tu-tru-panel"]')
            _shot_element(page, '[data-canonical="tu-tru-panel"]', OUT / "_gooddate_tutru.png")

            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            _fill_case_0001(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-region="pillars"] [data-canonical="tu-tru-panel"]')
            page.wait_for_selector('[data-card="bazi"][data-implemented="bazi"]')
            page.wait_for_selector("text=Nguyễn Tiến Sơn")
            page.screenshot(path=str(OUT / "04_first_viewport_corrected.png"))
            _shot_element(page, '[data-region="pillars"]', OUT / "02_result_tutru.png")
            _shot_element(page, '[data-card="bazi"]', OUT / "03_result_bazi_detail.png")
            _shot_clip(
                page,
                ['[data-region="pillars"]', '[data-card="bazi"]'],
                OUT / "05_tutru_bazi_together.png",
            )
            _compose(
                OUT / "_gooddate_tutru.png",
                OUT / "02_result_tutru.png",
                OUT / "01_tutru_reference_comparison.png",
                "GOOD DATE TUTRU",
                "RESULT TUTRU",
            )
            (OUT / "_gooddate_tutru.png").unlink(missing_ok=True)
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
