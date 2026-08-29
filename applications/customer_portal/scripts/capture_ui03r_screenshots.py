"""Capture UI-03R canonical layout restoration screenshots."""

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
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui03r"
BEFORE_SRC = (
    REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui10" / "09_full_dashboard_ui10.png"
)
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
API = f"http://127.0.0.1:{API_PORT}"
VIEWPORT = {"width": 1440, "height": 900}


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


def _collapse_bazi(page) -> None:
    toggle = page.locator('[data-card="bazi"] button.bte-bazi__toggle')
    if toggle.count() and toggle.first.get_attribute("aria-expanded") == "true":
        toggle.first.click()
        page.wait_for_timeout(200)


def _shot_element(page, selector: str, path: Path) -> None:
    locator = page.locator(selector).first
    locator.wait_for()
    locator.screenshot(path=str(path))


def _shot_row01(page, path: Path) -> None:
    cards = [
        page.locator('[data-card="overview"]').first.bounding_box(),
        page.locator('[data-card="bazi"]').first.bounding_box(),
    ]
    if any(box is None for box in cards):
        raise RuntimeError("row 01 cards are missing")
    left = min(box["x"] for box in cards if box)
    top = min(box["y"] for box in cards if box)
    right = max(box["x"] + box["width"] for box in cards if box)
    bottom = max(box["y"] + box["height"] for box in cards if box)
    page.screenshot(
        path=str(path),
        clip={"x": left, "y": top, "width": right - left, "height": bottom - top},
    )


def _crop_before_viewport(dest: Path) -> None:
    from PIL import Image

    if not BEFORE_SRC.exists():
        raise FileNotFoundError(str(BEFORE_SRC))
    image = Image.open(BEFORE_SRC).convert("RGB")
    width = min(VIEWPORT["width"], image.width)
    height = min(VIEWPORT["height"], image.height)
    image.crop((0, 0, width, height)).save(dest)


def _compose_before_after(before: Path, after: Path, dest: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    left = Image.open(before).convert("RGB")
    right = Image.open(after).convert("RGB")
    label_h = 36
    gap = 16
    target_h = max(left.height, right.height)
    scale_left = target_h / left.height
    scale_right = target_h / right.height
    left = left.resize((int(left.width * scale_left), target_h))
    right = right.resize((int(right.width * scale_right), target_h))
    canvas = Image.new("RGB", (left.width + right.width + gap, target_h + label_h), (242, 241, 239))
    canvas.paste(left, (0, label_h))
    canvas.paste(right, (left.width + gap, label_h))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((12, 10), "BEFORE (UI-10)", fill=(92, 101, 112), font=font)
    draw.text((left.width + gap + 12, 10), "AFTER (UI-03R)", fill=(154, 27, 27), font=font)
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


def main() -> None:
    """Capture UI-03R first-viewport restoration screenshots."""
    OUT.mkdir(parents=True, exist_ok=True)
    before_viewport = OUT / "_before_first_viewport.png"
    _crop_before_viewport(before_viewport)
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
            page.wait_for_selector('[data-identity-header="true"]')
            page.wait_for_selector('[data-card="overview"][data-implemented="overview"]')
            page.wait_for_selector('[data-card="bazi"][data-implemented="bazi"]')
            page.wait_for_selector("text=Nguyễn Tiến Sơn")
            _collapse_bazi(page)
            page.screenshot(path=str(OUT / "02_first_viewport.png"))
            _shot_element(page, '[data-identity-header="true"]', OUT / "03_identity_header.png")
            _shot_row01(page, OUT / "04_row01_balance.png")
            header_box = page.locator('[data-identity-header="true"]').first.bounding_box()
            if header_box:
                print("identity_header_height_px", round(header_box["height"]))
            status_text = page.locator('[data-region="status"]').first.inner_text()
            print("status_region", status_text.encode("ascii", "replace").decode("ascii").replace("\n", " | "))
            _compose_before_after(before_viewport, OUT / "02_first_viewport.png", OUT / "01_before_after.png")
            browser.close()
    finally:
        before_viewport.unlink(missing_ok=True)
        for proc in (portal_proc, api_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
