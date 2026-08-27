"""Capture DS-06B /choose-date and /good-date localization screenshots."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "date_selection" / "screenshots"
API_PORT = 8000
PORTAL_PORT = 8081


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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    _spawn("applications.api.app:app", API_PORT)
    _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    _wait(API_PORT)
    _wait(PORTAL_PORT)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto("http://127.0.0.1:8081/choose-date", wait_until="networkidle")
        page.wait_for_selector("#dsSearchForm")
        page.screenshot(path=str(OUT / "ds06b_01_choose_date_form.png"), full_page=True)
        page.fill("#dsBirth", "21011987")
        page.locator("#dsSearchForm").screenshot(path=str(OUT / "ds06b_02_birth_date_input.png"))
        page.fill("#dsTargetMonth", "092026")
        page.locator(".ds-month-input").screenshot(path=str(OUT / "ds06b_03_target_month.png"))
        page.fill("#dsFullName", "Nguyễn Tiến Sơn")
        page.select_option("#dsGender", "male")
        page.click("#dsSearchBtn")
        page.wait_for_selector("#dsPerson:not([hidden])")
        page.wait_for_function(
            """() => {
              const text = document.getElementById('dsPersonDl')?.textContent || '';
              return text.includes('Can Chi năm') && text.includes('Nạp âm') && text.includes('Hành Cung');
            }"""
        )
        page.locator("#dsPerson").screenshot(path=str(OUT / "ds06b_04_thong_tin_cua_ban.png"))
        page.wait_for_selector("#dsResults .ds-result")
        page.locator("#dsResults").screenshot(path=str(OUT / "ds06b_05_top5_cards.png"))
        page.goto("http://127.0.0.1:8081/good-date", wait_until="networkidle")
        page.wait_for_function(
            """() => {
              const text = document.getElementById('dsDetail')?.textContent || '';
              return text.includes('Can Chi năm') && text.includes('Can Chi tháng') && text.includes('Nạp âm');
            }"""
        )
        page.locator(".ds-detail").screenshot(path=str(OUT / "ds06b_06_good_date_day_detail.png"))
        browser.close()


if __name__ == "__main__":
    main()
