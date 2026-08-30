"""Capture N-IMP-10A Narrative Studio screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "implementation" / "narrative_v2" / "n_imp_10a"
PORT = 8090
BASE = f"http://127.0.0.1:{PORT}"


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


def main() -> None:
    """Capture Overview, Consulting, Trace, Compare, and Approval panels."""
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(PORT)
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "applications.narrative_studio.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(PORT),
        ],
        cwd=str(REPO),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 20
        while time.time() < deadline and not _listening(PORT):
            time.sleep(0.25)
        if not _listening(PORT):
            raise RuntimeError("Narrative Studio did not start")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1100})
            page.goto(f"{BASE}/studio?case=CASE-0001&panel=overview", wait_until="networkidle", timeout=180000)
            page.wait_for_selector('[data-studio-panel="overview"]')
            page.screenshot(path=str(OUT / "01_overview.png"), full_page=True)
            page.goto(f"{BASE}/studio?case=CASE-0001&panel=consulting", wait_until="networkidle")
            page.wait_for_selector("[data-studio-consulting-flow]")
            page.screenshot(path=str(OUT / "02_consulting.png"), full_page=True)
            page.goto(f"{BASE}/studio?case=CASE-0001&panel=trace", wait_until="networkidle")
            page.wait_for_selector('[data-studio-trace="evidence"]')
            page.locator('[data-studio-trace="evidence"]').evaluate("node => { node.open = true; }")
            page.screenshot(path=str(OUT / "03_trace.png"), full_page=True)
            page.goto(f"{BASE}/studio?case=CASE-0001&panel=compare", wait_until="networkidle")
            page.wait_for_selector('[data-studio-panel="compare"]')
            page.screenshot(path=str(OUT / "04_compare.png"), full_page=True)
            page.goto(f"{BASE}/studio?case=CASE-0001&panel=approval", wait_until="networkidle")
            page.wait_for_selector("[data-studio-approval]")
            page.screenshot(path=str(OUT / "05_approval.png"), full_page=True)
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
