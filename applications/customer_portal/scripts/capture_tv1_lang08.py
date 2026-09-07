"""Capture LANG-08 Marriage Language Pack live verification.

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
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "lang08"
SHOTS = OUT / "screenshots"
PORTAL_ROOT = REPO / "applications" / "customer_portal"
PORTAL = "http://127.0.0.1:8081"
MARRIAGE_API = "http://127.0.0.1:8082"

QUESTIONS = (
    "Hai người có hợp nhau không?",
    "Ai bổ trợ cho ai?",
    "Hai người có hợp tính cách không?",
    "Cuộc hôn nhân có ổn định không?",
    "Khả năng nuôi dạy con chung thế nào?",
    "Có nên tiến tới hôn nhân không?",
)
GENERIC = (
    "Trung bình.",
    "Khá hợp.",
    "Rất hợp.",
    "Áp lực cao.",
    "Insufficient.",
    "__PRODUCT_OWNER_WORDING_REQUIRED__",
)
EXPECTED_KEYS = {
    "Q1": "compatibility.yaml",
    "Q2": "support.yaml",
    "Q3": "personality.yaml",
    "Q4": "stability.yaml",
    "Q5": "children.yaml",
    "Q6": "overall.yaml",
}


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
        created = json.loads(response.read().decode("utf-8"))
    return created


def _npm() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"


def _build_portal() -> None:
    subprocess.run([_npm(), "run", "build:result"], cwd=str(PORTAL_ROOT), check=True)


def main() -> None:
    """Verify six Language Pack cards on live TV-01 for the Product Owner pair."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    _build_portal()
    _kill_port(8082)
    _spawn("consulting.marriage.api.http:create_marriage_api_app", 8082, factory=True)
    started_marriage = True
    _wait(8082, 60.0)
    started_portal = False
    if _listen(8081):
        _kill_port(8081)
    _spawn("applications.customer_portal.app:app", 8081)
    started_portal = True
    _wait(8081, 30.0)
    created = _post_live_pair()
    cards = ((created.get("data") or {}).get("assessment_cards") or [])
    summary = {
        "consultation_id": (created.get("data") or {}).get("consultation_id"),
        "overall_state": (created.get("data") or {}).get("overall_state"),
        "assessment_cards": [
            {
                "question_id": item.get("question_id"),
                "question": item.get("question"),
                "headline": item.get("headline") or item.get("answer"),
                "meaning": item.get("meaning"),
                "language_key": item.get("language_key"),
                "catalog_file": EXPECTED_KEYS.get(str(item.get("question_id"))),
            }
            for item in cards
        ],
    }
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
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "00_desktop_first_screen.png"))
        page.locator('[data-testid="marriage-assessment"]').screenshot(
            path=str(SHOTS / "01_desktop_assessment_board.png")
        )
        for index, question_id in enumerate(("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"), start=2):
            locator = page.locator(f'[data-testid="assessment-card-{question_id}"]')
            if locator.count():
                locator.screenshot(path=str(SHOTS / f"{index:02d}_desktop_{question_id.lower()}.png"))
        page.locator('[data-testid="assessment-card-Q1"] details.mc-assessment-card__more').first.click()
        page.locator('[data-testid="assessment-card-Q1"]').screenshot(
            path=str(SHOTS / "08_desktop_q1_facts.png")
        )
        page.locator('[data-testid="detailed-analysis"]').screenshot(
            path=str(SHOTS / "09_desktop_detailed_collapsed.png")
        )
        page.locator('[data-testid="detailed-analysis"] summary').click()
        detailed_expanded = page.locator('[data-testid="detailed-analysis"]').get_attribute("open") is not None
        page.locator('[data-testid="detailed-analysis"]').screenshot(
            path=str(SHOTS / "10_desktop_detailed_expanded.png")
        )
        page.locator('[data-testid="conclusion"]').scroll_into_view_if_needed()
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "11_desktop_report_conclusion.png"))
        page.locator('[data-testid="action-plan"]').screenshot(path=str(SHOTS / "12_desktop_report_actions.png"))
        page.screenshot(path=str(SHOTS / "13_desktop_full.png"), full_page=True)
        customer_assessment = page.locator('[data-testid="marriage-assessment"]').inner_text()
        customer_has_technical = page.locator('[data-testid^="assessment-technical-"]').count()
        page.locator('[data-testid="expert-mode"] summary').click()
        page.get_by_role("button", name="Xem chế độ chuyên gia").click()
        page.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
        page.locator('[data-testid="assessment-card-Q1"]').screenshot(
            path=str(SHOTS / "14_desktop_expert_q1.png")
        )
        expert_has_technical = page.locator('[data-testid^="assessment-technical-"]').count()
        page.set_viewport_size({"width": 768, "height": 1024})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "15_tablet_assessment.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "16_mobile_assessment.png"), full_page=True)
        page.screenshot(path=str(SHOTS / "17_mobile_full.png"), full_page=True)
        visible = page.locator('[data-testid="marriage-assessment"]').inner_text()
        checks = {
            "has_result": page.locator('[data-testid="marriage-result"]').count() > 0,
            "has_six_cards": page.locator('[data-testid^="assessment-card-"]').count() == 6,
            "questions_visible": all(item in visible for item in QUESTIONS),
            "no_generic_wording": all(item not in customer_assessment for item in GENERIC),
            "api_language_keys": all(
                str(item.get("language_key") or "").startswith(f"marriage.q{index}.")
                for index, item in enumerate(cards, start=1)
            ),
            "api_no_generic": all(
                phrase not in json.dumps(cards, ensure_ascii=False) for phrase in GENERIC
            ),
            "api_has_meaning": all(bool(item.get("meaning")) for item in cards),
            "customer_hides_technical": customer_has_technical == 0,
            "expert_shows_technical": expert_has_technical > 0,
            "detailed_present": page.locator('[data-testid="detailed-analysis"]').count() == 1,
            "report_conclusion": page.locator('[data-testid="conclusion"]').count() == 1,
            "no_score_leak": "score-leak" not in page.locator('[data-testid="score-grade-guard"]').inner_text(),
            "api_has_six_cards": len(cards) == 6,
            "detailed_can_expand": detailed_expanded,
        }
        browser.close()
    report_doc = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "viewports": ["1440x1100", "768x1024", "390x844"],
        "summary": summary,
        "started_marriage": started_marriage,
        "started_portal": started_portal,
    }
    (OUT / "browser_verification.json").write_text(
        json.dumps(report_doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if report_doc["status"] != "PASS":
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))


if __name__ == "__main__":
    main()
