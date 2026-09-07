"""Capture TV1-R01 live comparison consultation on the Customer Portal."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

from playwright.sync_api import Page, sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "r01"
SHOTS = OUT / "screenshots"
PORTAL = "http://127.0.0.1:8081"
MARRIAGE_API = "http://127.0.0.1:8082"


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
    return subprocess.Popen(cmd, cwd=str(REPO), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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


def _post_live_pair() -> dict[str, object]:
    body = {
        "person_a": {
            "full_name": "An",
            "gender": "male",
            "birth_date": "1987-01-21",
            "birth_time": "07:30",
            "birth_place": "Hà Nội",
        },
        "person_b": {
            "full_name": "Binh",
            "gender": "female",
            "birth_date": "1990-05-15",
            "birth_place": "Hà Nội",
        },
        "options": {"language": "vi", "audience": "customer"},
    }
    request = Request(
        f"{MARRIAGE_API}/api/v1/consulting/marriage",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        created = json.loads(response.read().decode("utf-8"))
    consultation_id = created["data"]["consultation_id"]
    report_req = Request(
        f"{MARRIAGE_API}/api/v1/consulting/marriage/{consultation_id}/report",
        headers={"Accept": "application/json"},
    )
    with urlopen(report_req, timeout=60) as response:
        report = json.loads(response.read().decode("utf-8"))
    return {"created": created, "report": report}


def _section_bodies(report: dict[str, object], section_id: str) -> list[str]:
    sections = ((report.get("data") or {}).get("sections") or []) if isinstance(report, dict) else []
    for section in sections:
        if section.get("section_id") != section_id:
            continue
        return [block.get("body") or block.get("title") or "" for block in section.get("blocks") or []]
    return []


def main() -> None:
    """Verify live comparison cards for the Product Owner pair."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    _kill_port(8082)
    _spawn("consulting.marriage.api.http:create_marriage_api_app", 8082, factory=True)
    started_marriage = True
    _wait(8082, 60.0)
    started_portal = False
    if not _listen(8081):
        _spawn("applications.customer_portal.app:app", 8081)
        started_portal = True
        _wait(8081, 30.0)
    live = _post_live_pair()
    created = live["created"]
    report = live["report"]
    summary = {
        "consultation_id": (created.get("data") or {}).get("consultation_id"),
        "overall_state": (created.get("data") or {}).get("overall_state"),
        "headline": (created.get("data") or {}).get("headline"),
        "a_to_b": _section_bodies(report, "comparison_a_to_b"),
        "b_to_a": _section_bodies(report, "comparison_b_to_a"),
        "harmony": _section_bodies(report, "comparison_harmony"),
        "conflict": _section_bodies(report, "comparison_conflict"),
        "rescue": _section_bodies(report, "comparison_rescue"),
        "executive": _section_bodies(report, "executive_summary"),
        "conclusion": _section_bodies(report, "conclusion"),
        "generic_labels_absent": True,
    }
    blob = " ".join(
        summary["a_to_b"]
        + summary["b_to_a"]
        + summary["harmony"]
        + summary["conflict"]
        + summary["rescue"]
        + summary["executive"]
    )
    forbidden = (
        "Điểm hỗ trợ nền tảng",
        "Điểm bổ trợ vai trò",
        "Điểm cần lưu ý ở nền tảng",
        "Điểm ma sát Can Chi",
        "Điểm bổ trợ tài chính",
    )
    summary["generic_labels_absent"] = not any(item in blob for item in forbidden)
    summary["has_directional_support"] = bool(summary["a_to_b"] or summary["b_to_a"])
    summary["has_conflict_facts"] = bool(summary["conflict"])
    (OUT / "live_pair_output.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto(f"{PORTAL}/marriage-consulting", wait_until="networkidle")
        page.wait_for_selector("#person-a-full-name")
        _fill_pair(page)
        page.click('[data-testid="submit-marriage"]')
        page.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
        page.locator('[data-testid="compatibility-hero"]').screenshot(path=str(SHOTS / "01_hero.png"))
        page.locator('[data-testid="executive-summary"]').screenshot(path=str(SHOTS / "02_executive.png"))
        if page.locator('[data-testid="comparison-board"]').count():
            page.locator('[data-testid="comparison-board"]').screenshot(path=str(SHOTS / "03_comparison.png"))
        if page.locator('[data-testid="comparison_a_to_b"]').count():
            page.locator('[data-testid="comparison_a_to_b"]').screenshot(path=str(SHOTS / "04_a_to_b.png"))
        if page.locator('[data-testid="comparison_b_to_a"]').count():
            page.locator('[data-testid="comparison_b_to_a"]').screenshot(path=str(SHOTS / "05_b_to_a.png"))
        if page.locator('[data-testid="comparison_conflict"]').count():
            page.locator('[data-testid="comparison_conflict"]').screenshot(path=str(SHOTS / "06_conflict.png"))
        if page.locator('[data-testid="comparison_rescue"]').count():
            page.locator('[data-testid="comparison_rescue"]').screenshot(path=str(SHOTS / "07_rescue.png"))
        page.locator('[data-testid="domain-analysis"]').screenshot(path=str(SHOTS / "08_domains.png"))
        page.locator('[data-testid="action-plan"]').screenshot(path=str(SHOTS / "09_actions.png"))
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "10_conclusion.png"))
        page.screenshot(path=str(SHOTS / "11_full.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.screenshot(path=str(SHOTS / "12_mobile.png"), full_page=True)
        checks = {
            "has_result": page.locator('[data-testid="marriage-result"]').count() > 0,
            "has_comparison_board": page.locator('[data-testid="comparison-board"]').count() > 0,
            "has_a_to_b": page.locator('[data-testid="comparison_a_to_b"]').count() > 0,
            "has_b_to_a": page.locator('[data-testid="comparison_b_to_a"]').count() > 0,
            "has_conflict": page.locator('[data-testid="comparison_conflict"]').count() > 0,
            "generic_labels_absent": bool(summary["generic_labels_absent"]),
            "has_directional_support": bool(summary["has_directional_support"]),
            "no_score_leak": "score-leak" not in page.locator('[data-testid="score-grade-guard"]').inner_text(),
        }
        browser.close()
    report_doc = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "summary": summary,
        "started_marriage": started_marriage,
        "started_portal": started_portal,
        "portal_left_running": True,
        "marriage_left_running": True,
    }
    (OUT / "browser_verification.json").write_text(
        json.dumps(report_doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if report_doc["status"] != "PASS":
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))


if __name__ == "__main__":
    main()
