"""Capture LANG-08A customer Assessment Card refinement.

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
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "lang08a"
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
Q1_FORBIDDEN_VERDICT = "Độ hòa hợp ở mức trung bình."


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
    """Verify refined customer Assessment Cards on live TV-01."""
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
    cards = ((created.get("data") or {}).get("assessment_cards") or [])
    summary = {
        "consultation_id": (created.get("data") or {}).get("consultation_id"),
        "overall_state": (created.get("data") or {}).get("overall_state"),
        "assessment_cards": cards,
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
        page.screenshot(path=str(SHOTS / "01_desktop_six_cards.png"))
        customer_board = page.locator('[data-testid="marriage-assessment"]').inner_text()
        for question_id in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"):
            details = page.locator(f'[data-testid="assessment-card-{question_id}"] details.mc-assessment-card__more')
            if details.count():
                details.first.locator("summary").click()
            page.locator(f'[data-testid="assessment-card-{question_id}"]').screenshot(
                path=str(SHOTS / f"02_{question_id.lower()}_expanded.png")
            )
        page.locator('[data-testid="conclusion"]').scroll_into_view_if_needed()
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "03_report_conclusion.png"))
        page.locator('[data-testid="marriage-assessment"]').screenshot(
            path=str(SHOTS / "04_report_assessment_section.png")
        )
        customer_has_technical = page.locator('[data-testid^="assessment-technical-"]').count()
        page.locator('[data-testid="expert-mode"] summary').click()
        page.get_by_role("button", name="Xem chế độ chuyên gia").click()
        page.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
        q1_tech = page.locator('[data-testid="assessment-card-Q1"] details.mc-assessment-card__technical')
        if q1_tech.count():
            q1_tech.first.locator("summary").click()
        page.locator('[data-testid="assessment-card-Q1"]').screenshot(path=str(SHOTS / "05_expert_q1.png"))
        expert_has_technical = page.locator('[data-testid^="assessment-technical-"]').count()
        page.set_viewport_size({"width": 768, "height": 1024})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "06_tablet.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "07_mobile_six_cards.png"), full_page=True)
        visible = page.locator('[data-testid="marriage-assessment"]').inner_text()
        q1_verdict = next((item.get("verdict") or item.get("headline") for item in cards if item.get("question_id") == "Q1"), "")
        q5_verdict = next((item.get("verdict") or item.get("headline") for item in cards if item.get("question_id") == "Q5"), "")
        checks = {
            "has_six_cards": page.locator('[data-testid^="assessment-card-"]').count() == 6,
            "questions_visible": all(item in visible for item in QUESTIONS),
            "no_generic_wording": all(item not in customer_board for item in GENERIC),
            "q1_not_score_speak": q1_verdict != Q1_FORBIDDEN_VERDICT and "Trung bình." not in str(q1_verdict),
            "q5_no_insufficient": "Insufficient" not in str(q5_verdict),
            "api_semantic_keys": all(str(item.get("semantic_key") or "").startswith("marriage.q") for item in cards),
            "api_has_verdict": all(bool(item.get("verdict")) for item in cards),
            "customer_hides_technical": customer_has_technical == 0,
            "expert_shows_technical": expert_has_technical > 0,
            "no_score_leak": "score-leak" not in page.locator('[data-testid="score-grade-guard"]').inner_text(),
        }
        browser.close()
    report_doc = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "viewports": ["1440x1100", "768x1024", "390x844"],
        "summary": {
            "consultation_id": summary["consultation_id"],
            "overall_state": summary["overall_state"],
            "verdicts": [item.get("verdict") for item in cards],
            "language_keys": [item.get("semantic_key") or item.get("language_key") for item in cards],
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
