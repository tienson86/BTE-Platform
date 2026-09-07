"""Capture TV1-B07A live Customer Portal navigation screenshots.

Verifies localhost:8081 chrome, not the isolated Marriage host.
Leaves the portal process running after success.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT_DIR = REPO / "docs" / "reports" / "tv01_marriage" / "b07a"
SHOTS = OUT_DIR / "screenshots"
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
EXPECTED_LABELS = ["Trang chủ", "Chọn ngày tốt", "Xem lá số", "Tư vấn hôn nhân"]
_LEAVE_RUNNING = True


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


def _spawn_portal() -> subprocess.Popen[bytes]:
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


def _primary_labels(page: Page) -> list[str]:
    return page.locator('[data-customer-nav="primary"] a').all_inner_texts()


def _header_overflow(page: Page) -> bool:
    return bool(
        page.evaluate(
            """() => {
              const header = document.querySelector('.app-header');
              if (!header) return true;
              return header.scrollWidth > header.clientWidth + 1;
            }"""
        )
    )


def _inspect_route(page: Page, path: str) -> dict[str, object]:
    page.goto(f"{BASE}{path}", wait_until="networkidle")
    page.wait_for_selector('[data-customer-nav="primary"]')
    labels = _primary_labels(page)
    marriage = page.locator('[data-customer-nav="primary"] a[href="/marriage-consulting"]')
    return {
        "path": path,
        "labels": labels,
        "has_marriage": marriage.count() > 0,
        "marriage_href": marriage.get_attribute("href") if marriage.count() else None,
        "marriage_active": (
            "active" in (marriage.get_attribute("class") or "")
            and marriage.get_attribute("aria-current") == "page"
        ),
        "header_overflow": _header_overflow(page),
    }


def main() -> None:
    """Verify live 8081 header mount and capture B07A screenshots."""
    SHOTS.mkdir(parents=True, exist_ok=True)
    _kill_port(PORTAL_PORT)
    portal_proc = _spawn_portal()
    report: dict[str, object] = {"base": BASE, "checks": {}, "status": "FAIL"}
    try:
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900})

            good_date = _inspect_route(page, "/good-date")
            page.locator(".app-header").screenshot(path=str(SHOTS / "01_good_date_header.png"))
            page.screenshot(path=str(SHOTS / "01_good_date.png"), full_page=False)

            choose_date = _inspect_route(page, "/choose-date")
            page.locator(".app-header").screenshot(path=str(SHOTS / "02_choose_date_header.png"))

            analyze = _inspect_route(page, "/analyze")
            page.locator(".app-header").screenshot(path=str(SHOTS / "03_analyze_header.png"))

            page.goto(f"{BASE}/good-date", wait_until="networkidle")
            page.wait_for_selector('[data-customer-nav="primary"] a[href="/marriage-consulting"]')
            page.click('[data-customer-nav="primary"] a[href="/marriage-consulting"]')
            page.wait_for_url("**/marriage-consulting")
            page.wait_for_selector("#marriage-consulting-root")
            marriage = _inspect_route(page, "/marriage-consulting")
            page.locator(".app-header").screenshot(path=str(SHOTS / "04_marriage_header_active.png"))
            page.screenshot(path=str(SHOTS / "04_marriage_consulting.png"), full_page=False)

            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(f"{BASE}/good-date", wait_until="networkidle")
            page.wait_for_selector("#btnNavToggle")
            toggle_visible = page.locator("#btnNavToggle").is_visible()
            page.locator("#btnNavToggle").click()
            page.wait_for_selector('[data-customer-nav="primary"] a[href="/marriage-consulting"]')
            mobile_labels = _primary_labels(page)
            page.screenshot(path=str(SHOTS / "05_mobile_nav.png"), full_page=False)

            browser.close()

        checks = {
            "visible_on_good_date": good_date["has_marriage"] and good_date["labels"] == EXPECTED_LABELS,
            "visible_on_choose_date": choose_date["has_marriage"] and choose_date["labels"] == EXPECTED_LABELS,
            "visible_on_analyze": analyze["has_marriage"] and analyze["labels"] == EXPECTED_LABELS,
            "active_on_marriage_consulting": bool(marriage["marriage_active"]),
            "click_opens_marriage_page": True,
            "existing_three_unchanged": all(
                route["labels"][:3] == EXPECTED_LABELS[:3]
                for route in (good_date, choose_date, analyze, marriage)
            ),
            "no_desktop_overflow": not any(
                route["header_overflow"]
                for route in (good_date, choose_date, analyze, marriage)
            ),
            "mobile_header_usable": toggle_visible and mobile_labels == EXPECTED_LABELS,
        }
        report["checks"] = checks
        report["routes"] = {
            "good_date": good_date,
            "choose_date": choose_date,
            "analyze": analyze,
            "marriage_consulting": marriage,
            "mobile_labels": mobile_labels,
        }
        report["status"] = "PASS" if all(checks.values()) else "FAIL"
        if report["status"] != "PASS":
            raise RuntimeError(f"TV1-B07A live verification failed: {json.dumps(checks, ensure_ascii=False)}")
    finally:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "browser_verification.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if not _LEAVE_RUNNING:
            portal_proc.terminate()
            try:
                portal_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                portal_proc.kill()


if __name__ == "__main__":
    main()
