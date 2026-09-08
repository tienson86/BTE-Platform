"""Capture TV1-R02C commercial presentation on the live PO pair.

Product Owner pair: An 1987-01-21 07:30 / Binh 1990-05-15.
"""

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
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "r02c"
SHOTS = OUT / "screenshots"
PORTAL_ROOT = REPO / "applications" / "customer_portal"
PORTAL = "http://127.0.0.1:8081"
MARRIAGE_API = "http://127.0.0.1:8082"

FORBIDDEN = (
    "timezone_unspecified",
    "birth_time_unknown",
    "Insufficient.",
    "Trung bình.",
    "So sánh hai chiều",
    "A bổ trợ B",
    "B bổ trợ A",
    "semantic_key",
    "language_key",
    "Timezone was not",
    "structural data",
)


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
    deadline = time.time() + 10.0
    while time.time() < deadline and _listen(port):
        time.sleep(0.25)


def _spawn(app: str, port: int, factory: bool = False) -> None:
    args = [sys.executable, "-m", "uvicorn", app, "--host", "127.0.0.1", "--port", str(port)]
    if factory:
        args.append("--factory")
    log_path = OUT / f"uvicorn-{port}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handle = log_path.open("ab")
    subprocess.Popen(args, cwd=str(REPO), stdout=handle, stderr=handle)


def _wait(port: int, timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listen(port):
            try:
                urlopen(f"http://127.0.0.1:{port}/healthz", timeout=2)
                return
            except Exception:
                try:
                    urlopen(f"http://127.0.0.1:{port}/marriage-consulting", timeout=2)
                    return
                except Exception:
                    pass
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
        return json.loads(response.read().decode("utf-8"))


def _npm() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"


def main() -> None:
    """Verify the commercial consulting report on live TV-01."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    subprocess.run([_npm(), "run", "build:result"], cwd=str(PORTAL_ROOT), check=True)
    _kill_port(8082)
    _spawn("consulting.marriage.api.http:create_marriage_api_app", 8082, factory=True)
    _wait(8082, 60.0)
    if _listen(8081):
        _kill_port(8081)
    _spawn("applications.customer_portal.app:app", 8081)
    _wait(8081, 30.0)
    created = _post_live_pair()
    consultation_id = (created.get("data") or {}).get("consultation_id")
    request = Request(
        f"{MARRIAGE_API}/api/v1/consulting/marriage/{consultation_id}/report",
        headers={"Accept": "application/json"},
    )
    with urlopen(request, timeout=60) as response:
        report = json.loads(response.read().decode("utf-8"))
    report_data = report.get("data") or {}
    sections = {item["section_id"]: item for item in report_data.get("sections") or []}
    conclusion_blocks = {
        item["block_id"]: item.get("body") or ""
        for item in (sections.get("conclusion") or {}).get("blocks") or []
    }
    cung_blocks = {
        item["block_id"]: item
        for item in (sections.get("cung_phi") or {}).get("blocks") or []
    }
    (OUT / "live_pair_output.json").write_text(
        json.dumps(
            {
                "consultation_id": consultation_id,
                "section_ids": list(sections),
                "conclusion": conclusion_blocks,
                "cung_phi": {
                    key: {"title": item.get("title"), "body": item.get("body")}
                    for key, item in cung_blocks.items()
                },
                "mutual_title": (sections.get("comparison_a_to_b") or {}).get("title"),
            },
            ensure_ascii=False,
            indent=2,
        ),
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
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "01_desktop_cards.png"))
        page.locator('[data-testid="conclusion"]').scroll_into_view_if_needed()
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "02_desktop_final_opinion.png"))
        page.locator('[data-testid="detailed-analysis"] > summary').click()
        page.locator('[data-testid="mutual-support"]').scroll_into_view_if_needed()
        page.locator('[data-testid="mutual-support"]').screenshot(path=str(SHOTS / "03_desktop_mutual_support.png"))
        page.locator('[data-testid="cung-phi"]').scroll_into_view_if_needed()
        page.locator('[data-testid="cung-phi"]').screenshot(path=str(SHOTS / "04_desktop_cung_phi.png"))
        page.screenshot(path=str(SHOTS / "05_desktop_details_open.png"), full_page=True)
        visible = page.locator('[data-testid="marriage-result"]').inner_text()
        page.set_viewport_size({"width": 768, "height": 1024})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "06_tablet.png"), full_page=True)
        page.locator('[data-testid="conclusion"]').scroll_into_view_if_needed()
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "07_tablet_final_opinion.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "08_mobile_cards.png"), full_page=True)
        page.locator('[data-testid="conclusion"]').scroll_into_view_if_needed()
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "09_mobile_final_opinion.png"))
        checks = {
            "has_six_cards": page.locator('[data-testid^="assessment-card-"]').count() == 6,
            "hero_not_visible": page.locator('[data-testid="compatibility-hero"]').is_hidden(),
            "exec_not_visible": page.locator('[data-testid="executive-summary"]').is_hidden(),
            "has_mutual_support": page.locator('[data-testid="mutual-support"]').count() == 1,
            "no_mirrored_board": page.locator('[data-testid="comparison-board"]').count() == 0,
            "has_cung_phi": page.locator('[data-testid="cung-phi"]').count() == 1,
            "has_final_opinion": "Kết luận cuối" in visible,
            "has_strongest": page.locator('[data-testid="conclusion-strength"]').count() == 1,
            "has_attention": page.locator('[data-testid="conclusion-attention"]').count() == 1,
            "has_recommendation": page.locator('[data-testid="conclusion-recommendation"]').count() == 1,
            "q6_visible": "Có nên tiến tới hôn nhân không?" in visible,
            "no_forbidden": all(item not in visible for item in FORBIDDEN),
            "report_mutual_title": (sections.get("comparison_a_to_b") or {}).get("title") == "Bổ trợ lẫn nhau",
            "report_conclusion_title": (sections.get("conclusion") or {}).get("title") == "Kết luận cuối",
            "report_has_cung_phi": "cung_phi" in sections,
            "ui_matches_report_opinion": page.locator('[data-testid="conclusion-opinion"]').inner_text().endswith(
                str(conclusion_blocks.get("conclusion-opinion") or "")
            )
            or str(conclusion_blocks.get("conclusion-opinion") or "") in page.locator('[data-testid="conclusion-opinion"]').inner_text(),
            "no_score_leak": "score-leak" not in page.locator('[data-testid="score-grade-guard"]').inner_text(),
        }
        browser.close()
    report_doc = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "viewports": ["1440x1100", "768x1024", "390x844"],
        "final_opinion": conclusion_blocks,
        "cung_phi": {
            key: {"title": item.get("title"), "body": item.get("body")}
            for key, item in cung_blocks.items()
        },
    }
    (OUT / "browser_verification.json").write_text(
        json.dumps(report_doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if report_doc["status"] != "PASS":
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))


if __name__ == "__main__":
    main()
