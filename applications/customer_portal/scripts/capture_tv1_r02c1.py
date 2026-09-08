"""Capture TV1-R02C1 customer-mode cleanup on the live PO pair.

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
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "r02c1"
SHOTS = OUT / "screenshots"
PORTAL_ROOT = REPO / "applications" / "customer_portal"
PORTAL = "http://127.0.0.1:8081"
MARRIAGE_API = "http://127.0.0.1:8082"

CUSTOMER_FORBIDDEN = (
    "Giải thích kỹ thuật",
    "Độ tin cậy và giới hạn",
    "Phụ lục phương pháp",
    "Chi tiết bổ sung",
    "semantic_key",
    "language_key",
    "timezone_unspecified",
    "birth_time_unknown",
)

CUSTOMER_REPORT_REQUIRED = (
    "identity",
    "executive_summary",
    "strengths",
    "risks",
    "comparison_a_to_b",
    "cung_phi",
    "conclusion",
)

CUSTOMER_REPORT_REMOVED = (
    "confidence_limitations",
    "appendix",
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


def _get_report(consultation_id: str, expert: bool = False) -> dict[str, object]:
    suffix = "?expert=true" if expert else ""
    request = Request(
        f"{MARRIAGE_API}/api/v1/consulting/marriage/{consultation_id}/report{suffix}",
        headers={"Accept": "application/json"},
    )
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _npm() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"


def _section_ids(payload: dict[str, object]) -> list[str]:
    data = payload.get("data") or {}
    return [str(item.get("section_id")) for item in (data.get("sections") or [])]


def main() -> None:
    """Verify customer cleanup and Expert Mode relocation on live TV-01."""
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
    consultation_id = str((created.get("data") or {}).get("consultation_id") or "")
    customer_report = _get_report(consultation_id, expert=False)
    expert_report = _get_report(consultation_id, expert=True)
    customer_ids = _section_ids(customer_report)
    expert_ids = _section_ids(expert_report)
    (OUT / "live_pair_output.json").write_text(
        json.dumps(
            {
                "consultation_id": consultation_id,
                "customer_section_ids": customer_ids,
                "expert_section_ids": expert_ids,
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
        page.locator('[data-testid="assessment-card-Q1"] details.mc-assessment-card__more > summary').click()
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "01_desktop_cards.png"))
        page.locator('[data-testid="detailed-analysis"] > summary').click()
        page.locator('[data-testid="detailed-analysis"]').screenshot(path=str(SHOTS / "02_desktop_detail_analysis.png"))
        page.locator('[data-testid="conclusion"]').scroll_into_view_if_needed()
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "03_desktop_final_opinion.png"))
        page.screenshot(path=str(SHOTS / "04_desktop_customer_full.png"), full_page=True)
        flow = page.evaluate(
            """() => [...document.querySelectorAll('[data-testid="marriage-assessment"], [data-testid="detailed-analysis"], [data-testid="conclusion"], [data-testid="expert-mode"]')].map(el => el.getAttribute('data-testid'))"""
        )
        visible = page.locator('[data-testid="marriage-result"]').inner_text()
        customer_visible = {
            "no_technical_explanation": "Giải thích kỹ thuật" not in visible,
            "no_confidence_section": "Độ tin cậy và giới hạn" not in visible,
            "no_methodology_section": "Phụ lục phương pháp" not in visible,
            "no_old_technical_accordion": "Chi tiết bổ sung" not in visible,
            "has_assessment_basis": "Cơ sở đánh giá" in visible,
            "no_card_chi_tiet_summary": page.locator(".mc-assessment-card__more > summary").first.inner_text().strip()
            == "Cơ sở đánh giá",
            "has_assessment": page.locator('[data-testid="marriage-assessment"]').is_visible(),
            "has_detail_analysis": "Phân tích chi tiết" in visible,
            "has_strengths": page.locator('[data-testid="key-strengths"]').is_visible(),
            "has_risks": page.locator('[data-testid="key-risks"]').is_visible(),
            "has_mutual": page.locator('[data-testid="mutual-support"]').is_visible(),
            "has_cung_phi": page.locator('[data-testid="cung-phi"]').is_visible(),
            "has_conclusion": page.locator('[data-testid="conclusion"]').is_visible(),
            "has_expert_seam": page.locator('[data-testid="expert-mode"]').count() == 1,
            "expert_closed": page.locator('[data-testid="expert-trace"]').count() == 0,
            "no_domain_in_customer": page.locator('[data-testid="domain-analysis"]').count() == 0,
            "no_action_in_customer": page.locator('[data-testid="action-plan"]').count() == 0,
            "no_confidence_testid": page.locator('[data-testid="confidence-limitations"]').count() == 0,
            "no_appendix_testid": page.locator('[data-testid="appendix"]').count() == 0,
            "customer_flow": flow
            == ["marriage-assessment", "detailed-analysis", "conclusion", "expert-mode"],
            "no_forbidden": all(item not in visible for item in CUSTOMER_FORBIDDEN),
        }
        page.set_viewport_size({"width": 768, "height": 1024})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "06_tablet.png"), full_page=True)
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "07_tablet_final_opinion.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator('[data-testid="marriage-assessment"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "08_mobile_cards.png"), full_page=True)
        page.locator('[data-testid="conclusion"]').screenshot(path=str(SHOTS / "09_mobile_final_opinion.png"))
        page.set_viewport_size({"width": 1440, "height": 1100})
        page.locator('[data-testid="expert-toggle"]').click()
        page.locator('[data-testid="assessment-technical-Q1"]').wait_for(timeout=120000)
        page.locator('[data-testid="expert-mode"]').scroll_into_view_if_needed()
        page.locator('[data-testid="expert-mode"]').screenshot(path=str(SHOTS / "05_desktop_expert_mode.png"))
        expert_visible = page.locator('[data-testid="expert-mode"]').inner_text()
        expert_checks = {
            "expert_has_technical": "Giải thích kỹ thuật" in expert_visible,
            "expert_has_confidence": page.locator('[data-testid="confidence-limitations"]').count() == 1,
            "expert_has_appendix": page.locator('[data-testid="appendix"]').count() == 1,
            "expert_has_domains": page.locator('[data-testid="domain-analysis"]').count() == 1,
            "expert_has_actions": page.locator('[data-testid="action-plan"]').count() == 1,
            "expert_trace": page.locator('[data-testid="expert-trace"]').count() == 1,
        }
        report_checks = {
            "customer_has_required": all(item in customer_ids for item in CUSTOMER_REPORT_REQUIRED),
            "customer_omits_confidence": "confidence_limitations" not in customer_ids,
            "customer_omits_appendix": "appendix" not in customer_ids,
            "expert_report_keeps_confidence": "confidence_limitations" in expert_ids,
            "expert_report_keeps_appendix": "appendix" in expert_ids,
            "expert_report_keeps_domains": "domain_analysis" in expert_ids,
            "ui_matches_customer_report_conclusion": page.locator(
                '[data-testid="conclusion"] h2'
            ).inner_text()
            == "Kết luận cuối",
        }
        checks = {**customer_visible, **expert_checks, **report_checks}
        browser.close()
    report_doc = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "customer_section_ids": customer_ids,
        "expert_section_ids": expert_ids,
        "viewports": ["1440x1100", "768x1024", "390x844"],
    }
    (OUT / "browser_verification.json").write_text(
        json.dumps(report_doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if report_doc["status"] != "PASS":
        raise RuntimeError(json.dumps(checks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
