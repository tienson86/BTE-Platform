"""Capture BZ-UI-02 canonical panel screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "canonical" / "bz_ui_02_panels"
PORTAL_PORT = 8081


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _spawn_portal() -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "applications.customer_portal.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(PORTAL_PORT),
        ],
        cwd=str(REPO),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _wait(port: int, timeout: float = 25.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _union_clip(page, selector: str) -> dict[str, float]:
    boxes = page.locator(selector).evaluate_all(
        """els => {
          const first = els[0].getBoundingClientRect();
          let left = first.left, top = first.top, right = first.right, bottom = first.bottom;
          for (const el of els) {
            const box = el.getBoundingClientRect();
            left = Math.min(left, box.left);
            top = Math.min(top, box.top);
            right = Math.max(right, box.right);
            bottom = Math.max(bottom, box.bottom);
          }
          return { x: Math.max(0, left), y: Math.max(0, top),
                   width: Math.max(1, right - left), height: Math.max(1, bottom - top) };
        }"""
    )
    return boxes


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started: subprocess.Popen[bytes] | None = None
    if not _listening(PORTAL_PORT):
        started = _spawn_portal()
        _wait(PORTAL_PORT)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            url = f"http://127.0.0.1:{PORTAL_PORT}/result-workspace?preview=1"
            desktop = browser.new_page(viewport={"width": 1440, "height": 1200})
            desktop.goto(url, wait_until="domcontentloaded")
            desktop.wait_for_selector("[data-canonical='tu-tru-panel']")
            desktop.wait_for_selector("[data-shell='overview']")
            desktop.screenshot(path=str(OUT / "01_desktop.png"), full_page=True)
            for row in (1, 2, 3, 4):
                desktop.locator(f"[data-row='{row}']").first.scroll_into_view_if_needed()
                desktop.wait_for_timeout(150)
                clip = _union_clip(desktop, f"[data-row='{row}']")
                viewport = desktop.viewport_size or {"width": 1440, "height": 1200}
                pad = 12
                x = max(0, clip["x"] - pad)
                y = max(0, clip["y"] - pad)
                width = min(clip["width"] + pad * 2, viewport["width"] - x)
                height = min(clip["height"] + pad * 2, viewport["height"] - y)
                desktop.screenshot(
                    path=str(OUT / f"0{row + 1}_row_{row}.png"),
                    clip={"x": x, "y": y, "width": max(1, width), "height": max(1, height)},
                )
            desktop.close()

            tablet = browser.new_page(viewport={"width": 768, "height": 1024})
            tablet.goto(url, wait_until="domcontentloaded")
            tablet.wait_for_selector("[data-shell='overview']")
            tablet.screenshot(path=str(OUT / "06_tablet.png"), full_page=True)
            tablet.close()

            mobile = browser.new_page(viewport={"width": 390, "height": 844})
            mobile.goto(url, wait_until="domcontentloaded")
            mobile.wait_for_selector("[data-shell='overview']")
            mobile.screenshot(path=str(OUT / "07_mobile.png"), full_page=True)
            mobile.close()
            browser.close()
    finally:
        if started is not None:
            started.terminate()
            started.wait(timeout=8)


if __name__ == "__main__":
    main()
