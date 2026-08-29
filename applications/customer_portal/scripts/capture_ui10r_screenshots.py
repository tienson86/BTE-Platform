"""Capture UI-10R Luck Card after runtime JSON leak is removed."""

from __future__ import annotations

import base64
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "ui10r"
BEFORE = (
    REPO
    / "knowledge"
    / "commercial_dashboard"
    / "implementation"
    / "ui10"
    / "05_luck_live_case0001.png"
)
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
    subprocess.run(
        [npm, "run", "build:result"],
        cwd=str(PORTAL),
        check=True,
    )


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


def _fill_case_0001(page) -> None:
    page.fill("#full_name", "Nguyen Tien Son")
    page.check("#gender_male")
    page.fill("#birth_date", "21/01/1987")
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", "Ha Tay, Viet Nam")


def _assert_clean(page) -> dict[str, object]:
    text = page.locator('[data-card="luck"]').inner_text()
    leaks = [
        "dayun_runtime",
        "runtime_metadata",
        "attack_elements",
        "support_elements",
        "luck_strength",
        "{",
        "}",
    ]
    found = [token for token in leaks if token in text]
    proof = {
        "has_current": "Ất Tỵ" in text,
        "has_next": "Bính Ngọ" in text,
        "has_timeline": "Timeline Đại Vận" in text,
        "leaks": found,
        "ends_with_next": "Đại Vận kế tiếp" in text,
    }
    (OUT / "dom_proof.json").write_text(json.dumps(proof, ensure_ascii=True, indent=2), encoding="utf-8")
    if found:
        raise RuntimeError("Luck Card still leaks: " + ", ".join(found))
    return proof


def _compose_before_after(page, after_path: Path, out_path: Path) -> None:
    after_b64 = base64.b64encode(after_path.read_bytes()).decode("ascii")
    before_b64 = base64.b64encode(BEFORE.read_bytes()).decode("ascii") if BEFORE.exists() else after_b64
    page.set_viewport_size({"width": 1280, "height": 1600})
    page.set_content(
        """
<!DOCTYPE html>
<html>
<body style="margin:0;background:#f4f1ea;font-family:Segoe UI,sans-serif;color:#1f1b16;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:16px;">
    <figure style="margin:0;background:#fff;border:1px solid #d7cfc4;border-radius:8px;padding:12px;">
      <figcaption style="font-weight:700;margin-bottom:8px;">BEFORE — raw runtime dump</figcaption>
      <img src="data:image/png;base64,__BEFORE__" style="width:100%;height:auto;" />
    </figure>
    <figure style="margin:0;background:#fff;border:1px solid #d7cfc4;border-radius:8px;padding:12px;">
      <figcaption style="font-weight:700;margin-bottom:8px;">AFTER — customer fields only</figcaption>
      <img src="data:image/png;base64,__AFTER__" style="width:100%;height:auto;" />
    </figure>
  </div>
</body>
</html>
        """.replace("__BEFORE__", before_b64).replace("__AFTER__", after_b64)
    )
    page.wait_for_timeout(200)
    page.screenshot(path=str(out_path), full_page=True)


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
            page.wait_for_selector("#analyzeForm")
            _fill_case_0001(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector('[data-card="luck"][data-implemented="luck"]')
            _collapse(page)
            _assert_clean(page)
            _shot_element(page, '[data-card="luck"]', OUT / "02_luck_clean_customer_view.png")
            _expand(page)
            _assert_clean(page)
            _shot_element(page, '[data-card="luck"]', OUT / "03_luck_expanded_clean.png")
            _collapse(page)
            _shot_row03(page, OUT / "04_row03_clean.png")
            _compose_before_after(page, OUT / "02_luck_clean_customer_view.png", OUT / "01_luck_before_after.png")
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
