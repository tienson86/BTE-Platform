"""Capture BZ-UI-03 canonical binding screenshots from a live Analyze."""

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
OUT = REPO / "docs" / "reports" / "canonical" / "bz_ui_03_binding"
PORTAL_PORT = 8081
API_PORT = 8000
PORTAL = f"http://127.0.0.1:{PORTAL_PORT}"

CASE = {
    "full_name": "Nguyễn Tiến Sơn",
    "birth_place": "Hà Nội",
    "year": "1987",
    "month": "1",
    "day": "21",
    "hour": "4",
    "minute": "30",
    "gender": "male",
}


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _spawn(module: str, port: int) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
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


def _wait(port: int, timeout: float = 40.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started: list[subprocess.Popen[bytes]] = []
    if not _listening(API_PORT):
        started.append(_spawn("applications.api.app:app", API_PORT))
        _wait(API_PORT)
    if not _listening(PORTAL_PORT):
        started.append(_spawn("applications.customer_portal.app:app", PORTAL_PORT))
        _wait(PORTAL_PORT)
    notes: dict[str, object] = {}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 1600})
            errors: list[str] = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.on(
                "console",
                lambda msg: errors.append(msg.text) if msg.type == "error" else None,
            )

            page.goto(f"{PORTAL}/analyze", wait_until="networkidle", timeout=60000)
            for field, value in CASE.items():
                locator = page.locator(f"#{field}")
                if field == "gender":
                    locator.select_option(value)
                else:
                    locator.fill(value)
            page.locator("#btnAnalyze").click()
            page.wait_for_url("**/result", timeout=180000)
            page.wait_for_selector("[data-analysis-id]", timeout=60000)
            result_id = page.locator("[data-analysis-id]").first.get_attribute("data-analysis-id") or ""
            notes["result_analysis_id"] = result_id
            notes["result_url"] = page.url

            page.goto(f"{PORTAL}/result-workspace", wait_until="networkidle", timeout=60000)
            page.wait_for_selector("[data-workspace='bazi-result-v2'][data-binding='canonical']", timeout=30000)
            workspace_id = page.locator("[data-analysis-id]").first.get_attribute("data-analysis-id") or ""
            body = page.inner_text("body") or ""
            notes["workspace_analysis_id"] = workspace_id
            notes["workspace_url"] = page.url
            notes["preview_attr"] = page.locator("[data-workspace]").first.get_attribute("data-preview")
            notes["same_id"] = result_id == workspace_id and bool(result_id)
            notes["has_binh_dan"] = "Bính Dần" in body
            notes["has_preview_binh_ngo"] = "Bính Ngọ" in body
            notes["console_errors"] = errors

            page.set_viewport_size({"width": 1440, "height": 2400})
            page.screenshot(path=str(OUT / "01_desktop.png"), full_page=True)
            _row_shot(page, OUT / "02_header_row1.png", extra="[data-chrome='header']", row="1")
            _row_shot(page, OUT / "03_row2.png", row="2")
            _row_shot(page, OUT / "04_row3.png", row="3")
            _row_shot(page, OUT / "05_row4.png", row="4")

            page.set_viewport_size({"width": 768, "height": 1400})
            page.screenshot(path=str(OUT / "06_tablet.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 1200})
            page.screenshot(path=str(OUT / "07_mobile.png"), full_page=True)

            (OUT / "live_notes.json").write_text(
                json.dumps(notes, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            browser.close()
    finally:
        for proc in started:
            proc.terminate()


def _row_shot(page, path: Path, row: str, extra: str = "") -> None:
    page.evaluate(
        """(row) => {
          const el = document.querySelector(`[data-row='${row}']`);
          if (el) el.scrollIntoView({ block: "start" });
        }""",
        row,
    )
    time.sleep(0.15)
    clip = page.evaluate(
        """({ row, extra }) => {
          const nodes = [];
          if (extra) {
            const found = document.querySelector(extra);
            if (found) nodes.push(found);
          }
          document.querySelectorAll(`[data-row='${row}']`).forEach((el) => nodes.push(el));
          if (!nodes.length) return null;
          const first = nodes[0].getBoundingClientRect();
          let left = first.left, top = first.top, right = first.right, bottom = first.bottom;
          for (const el of nodes) {
            const box = el.getBoundingClientRect();
            left = Math.min(left, box.left);
            top = Math.min(top, box.top);
            right = Math.max(right, box.right);
            bottom = Math.max(bottom, box.bottom);
          }
          return {
            x: Math.max(0, left),
            y: Math.max(0, top),
            width: Math.max(1, right - left),
            height: Math.max(1, bottom - top),
          };
        }""",
        {"row": row, "extra": extra},
    )
    if clip:
        page.screenshot(path=str(path), clip=clip)


if __name__ == "__main__":
    main()
