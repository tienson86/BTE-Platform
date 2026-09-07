"""Capture TV1-B07B live consultation request repair evidence.

Starts Marriage API 8082 and restarts Portal 8081. Leaves both running.
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
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "b07b"
SHOTS = OUT / "screenshots"
PORTAL = "http://127.0.0.1:8081"
MARRIAGE_HEALTH = "http://127.0.0.1:8082/healthz"


def _listen(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _kill_port(port: int) -> None:
    if os.name == "nt":
        lookup = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, check=False)
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
    deadline = time.time() + 8
    while time.time() < deadline and _listen(port):
        time.sleep(0.2)


def _spawn(module: str, port: int, *, factory: bool = False) -> subprocess.Popen[bytes]:
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        module,
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--log-level",
        "info",
    ]
    if factory:
        cmd.append("--factory")
    return subprocess.Popen(
        cmd,
        cwd=str(REPO),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _wait(port: int, timeout: float = 45.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listen(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _fill_pair(page: Page) -> None:
    page.fill("#person-a-full-name", "An")
    page.check('input[name="person-a-gender"][value="male"]')
    page.fill("#person-a-birth-date", "21011987")
    page.fill("#person-a-birth-time", "0730")
    page.fill("#person-a-birth-place", "Hà Nội")
    page.fill("#person-b-full-name", "Binh")
    page.check('input[name="person-b-gender"][value="female"]')
    page.fill("#person-b-birth-date", "15051990")
    page.fill("#person-b-birth-place", "Hà Nội")


def main() -> None:
    """Verify success and API-unavailable paths on live 8081."""
    SHOTS.mkdir(parents=True, exist_ok=True)
    _kill_port(8082)
    _kill_port(8081)
    marriage_proc = _spawn(
        "consulting.marriage.api.http:create_marriage_api_app",
        8082,
        factory=True,
    )
    portal_proc = _spawn("applications.customer_portal.app:app", 8081)
    report: dict[str, object] = {"status": "FAIL"}
    try:
        _wait(8082, 60.0)
        _wait(8081, 30.0)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1100})
            network: list[dict[str, object]] = []

            def on_request(request) -> None:
                if "consulting/marriage" in request.url:
                    network.append(
                        {
                            "phase": "request",
                            "url": request.url,
                            "method": request.method,
                            "post_data": request.post_data,
                        }
                    )

            def on_response(response) -> None:
                if "consulting/marriage" in response.url:
                    network.append(
                        {
                            "phase": "response",
                            "url": response.url,
                            "status": response.status,
                        }
                    )

            page.on("request", on_request)
            page.on("response", on_response)

            page.goto(f"{PORTAL}/marriage-consulting", wait_until="networkidle")
            page.wait_for_selector("#person-a-full-name")
            _fill_pair(page)
            page.click('[data-testid="submit-marriage"]')
            page.locator('[data-testid="loading-state"]').wait_for(timeout=5000)
            page.screenshot(path=str(SHOTS / "01_loading.png"), full_page=False)
            page.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
            page.locator('[data-testid="compatibility-hero"]').screenshot(
                path=str(SHOTS / "03_hero.png")
            )
            page.locator('[data-testid="domain-analysis"]').screenshot(
                path=str(SHOTS / "04_domains.png")
            )
            page.locator('[data-testid="action-plan"]').screenshot(
                path=str(SHOTS / "05_action_plan.png")
            )
            notes = page.locator('[data-testid="warning-note"]')
            if notes.count():
                notes.first.screenshot(path=str(SHOTS / "06_birth_time_limitation.png"))
            page.screenshot(path=str(SHOTS / "02_result.png"), full_page=True)

            success = {
                "post_url": next(
                    (
                        item["url"]
                        for item in network
                        if item.get("phase") == "request" and item.get("method") == "POST"
                    ),
                    None,
                ),
                "post_status": next(
                    (
                        item["status"]
                        for item in network
                        if item.get("phase") == "response" and item.get("status") in {200, 201}
                    ),
                    None,
                ),
                "has_result": page.locator('[data-testid="marriage-result"]').count() > 0,
                "has_hero": page.locator('[data-testid="compatibility-hero"]').count() > 0,
                "has_domains": page.locator('[data-testid="domain-analysis"]').count() > 0,
                "has_actions": page.locator('[data-testid="action-plan"]').count() > 0,
                "has_birth_time_note": page.locator('[data-testid="warning-note"]').count() > 0,
                "loading_cleared": page.locator('[data-testid="loading-state"]').count() == 0,
                "payload_omits_person_b_time": True,
            }
            post_body = next(
                (
                    item.get("post_data")
                    for item in network
                    if item.get("phase") == "request" and item.get("method") == "POST"
                ),
                "",
            )
            parsed = json.loads(str(post_body or "{}"))
            success["payload_omits_person_b_time"] = "birth_time" not in parsed.get("person_b", {})
            success["person_a_has_time"] = bool(parsed.get("person_a", {}).get("birth_time"))
            success["person_a_iso"] = parsed.get("person_a", {}).get("birth_date") == "1987-01-21"

            _kill_port(8082)
            page.goto(f"{PORTAL}/marriage-consulting", wait_until="networkidle")
            page.wait_for_selector("#person-a-full-name")
            _fill_pair(page)
            page.click('[data-testid="submit-marriage"]')
            page.locator('[data-testid="error-state"]').wait_for(timeout=20000)
            page.screenshot(path=str(SHOTS / "07_api_unavailable_error.png"), full_page=False)
            failure = {
                "error_shown": page.locator('[data-testid="error-state"]').count() > 0,
                "error_text": page.locator('[data-testid="error-state"]').inner_text(),
                "loading_cleared": page.locator('[data-testid="loading-state"]').count() == 0,
                "has_retry": page.locator('[data-testid="retry-analysis"]').count() > 0,
            }
            browser.close()

        marriage_proc = _spawn(
            "consulting.marriage.api.http:create_marriage_api_app",
            8082,
            factory=True,
        )
        _wait(8082, 60.0)
        checks = {
            "success_url_uses_8081": str(success["post_url"]).startswith(
                "http://127.0.0.1:8081/backend/api/v1/consulting/marriage"
            ),
            "success_result": bool(success["has_result"] and success["has_hero"]),
            "success_loading_cleared": bool(success["loading_cleared"]),
            "blank_b_time_omitted": bool(success["payload_omits_person_b_time"]),
            "iso_dates": bool(success["person_a_iso"]),
            "failure_error": bool(failure["error_shown"] and failure["loading_cleared"]),
            "failure_retry": bool(failure["has_retry"]),
            "controlled_message": "Không thể hoàn tất phân tích lúc này" in str(failure["error_text"]),
        }
        report = {
            "status": "PASS" if all(checks.values()) else "FAIL",
            "checks": checks,
            "success": success,
            "failure": failure,
            "network": network,
            "marriage_health": MARRIAGE_HEALTH,
            "portal_left_running": True,
            "marriage_left_running": True,
        }
        if report["status"] != "PASS":
            raise RuntimeError(json.dumps(checks, ensure_ascii=False))
    finally:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "browser_verification.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        _ = (marriage_proc, portal_proc)


if __name__ == "__main__":
    main()
