"""CD-02 live /choose-date exhaustive discovery screenshots.

Leave the stack running after restore. Do not kill 8081 on success.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "date_selection" / "screenshots" / "cd_02"
PORTAL_BASE = "http://127.0.0.1:8081"

_SPEC = importlib.util.spec_from_file_location(
    "gd_cal_01_capture",
    Path(__file__).with_name("capture_gd_cal_01_screenshots.py"),
)
_CAPTURE = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_CAPTURE)


def _search_payload() -> dict:
    status, _, body = _CAPTURE._http(
        f"{PORTAL_BASE}/backend/api/v1/date-selection/search",
        method="POST",
        body=json.dumps(
            {
                "full_name": "Nguyễn Thanh Bình",
                "gender": "male",
                "birth_year": 1978,
                "birth_month": 10,
                "birth_day": 25,
                "target_year": 2026,
                "target_month": 11,
            }
        ).encode("utf-8"),
    )
    if status != 200:
        raise RuntimeError(f"search HTTP {status}: {body[:400]!r}")
    payload = json.loads(body.decode("utf-8"))
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("search missing data")
    return data


def _fill_choose_date(page: Page) -> None:
    page.goto(f"{PORTAL_BASE}/choose-date", wait_until="networkidle")
    page.wait_for_selector("#dsSearchForm")
    page.fill("#dsFullName", "Nguyễn Thanh Bình")
    page.check('input[name="gender"][value="male"]')
    page.fill("#dsBirth", "25101978")
    page.fill("#dsTargetMonth", "112026")
    page.click("#dsSearchBtn")
    page.wait_for_selector("[data-testid='result-count']")
    page.wait_for_function(
        """() => {
          const count = document.querySelector('[data-testid="result-count"]')?.textContent || '';
          const cards = [...document.querySelectorAll('[data-testid="ranked-card"]')];
          return count.includes('Tìm thấy 7 ngày phù hợp trong tháng 11/2026')
            && cards.length === 7
            && cards.some((card) => (card.textContent || '').includes('07/11/2026'));
        }"""
    )


def verify_and_capture(api_data: dict) -> dict[str, object]:
    OUT.mkdir(parents=True, exist_ok=True)
    dates = api_data.get("dates") if isinstance(api_data.get("dates"), list) else []
    solar = [
        ((item.get("day") or {}).get("calendar") or {}).get("solar_label")
        for item in dates
    ]
    if api_data.get("total_days_scanned") != 30:
        raise RuntimeError(f"total_days_scanned={api_data.get('total_days_scanned')!r}")
    if api_data.get("total_eligible") != 7 or len(dates) != 7:
        raise RuntimeError(f"eligible={api_data.get('total_eligible')!r} dates={len(dates)}")
    if "07/11/2026" not in solar:
        raise RuntimeError(f"07/11/2026 missing from API dates: {solar}")
    shots: dict[str, str] = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1400})
        _fill_choose_date(page)
        page.screenshot(path=str(OUT / "01_choose_date_full.png"), full_page=True)
        page.locator("#dsResults").screenshot(path=str(OUT / "02_choose_date_results.png"))
        card = page.locator('[data-testid="ranked-card"]').filter(has_text="07/11/2026")
        card.first.screenshot(path=str(OUT / "03_card_07_nov.png"))
        shots["choose_full"] = str(OUT / "01_choose_date_full.png")
        shots["choose_results"] = str(OUT / "02_choose_date_results.png")
        shots["card_07_nov"] = str(OUT / "03_card_07_nov.png")
        page.goto(f"{PORTAL_BASE}/good-date", wait_until="networkidle")
        page.wait_for_selector("#dsCalendar .ds-day[data-day]")
        _CAPTURE._goto_month(page, 2026, 11)
        _CAPTURE._select_day(page, 7, 11, 2026, "Mậu Tuất", "Tốc Hỷ")
        page.locator(".ds-detail").screenshot(path=str(OUT / "04_good_date_07_nov.png"))
        shots["good_date_07_nov"] = str(OUT / "04_good_date_07_nov.png")
        browser.close()
    return {
        "requested_month": api_data.get("requested_month"),
        "total_days_scanned": api_data.get("total_days_scanned"),
        "total_eligible": api_data.get("total_eligible"),
        "solar_dates": solar,
        **shots,
    }


def main() -> None:
    started = _CAPTURE.ensure_runtime()
    api_data = _search_payload()
    live = verify_and_capture(api_data)
    proof = {
        "started": started,
        "live": live,
        "left_running": f"{PORTAL_BASE}/choose-date",
    }
    print(json.dumps(proof, ensure_ascii=False, indent=2))
    print(f"Servers left running at {PORTAL_BASE}/choose-date")


if __name__ == "__main__":
    sys.path.insert(0, str(REPO))
    main()
