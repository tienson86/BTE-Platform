"""Capture BZ-UI-01 Result Workspace V2 screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "canonical" / "bz_ui_01_workspace"
PORTAL_PORT = 8081

VIEWPORTS = (
    ("01_desktop", 1440, 1100),
    ("02_tablet", 768, 1024),
    ("03_mobile", 390, 844),
)


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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started: subprocess.Popen[bytes] | None = None
    if not _listening(PORTAL_PORT):
        started = _spawn_portal()
        _wait(PORTAL_PORT)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            url = f"http://127.0.0.1:{PORTAL_PORT}/result-workspace"
            for name, width, height in VIEWPORTS:
                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_selector("[data-workspace='bazi-result-v2']")
                page.wait_for_selector("[data-canonical='tu-tru-panel']")
                page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)
                page.screenshot(
                    path=str(OUT / f"{name}_grid.png"),
                    full_page=False,
                    clip={"x": 0, "y": 0, "width": width, "height": min(height, 900)},
                )
                page.close()
            browser.close()
    finally:
        if started is not None:
            started.terminate()
            started.wait(timeout=8)


if __name__ == "__main__":
    main()
