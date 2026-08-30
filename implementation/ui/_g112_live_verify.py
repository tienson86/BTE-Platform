"""G1-12 live: Analyze 1966 and screenshot Tổng Quan with Kỵ Thần."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
LOCAL = "http://localhost:8081"


def main() -> None:
    body = json.dumps(
        {
            "year": 1966,
            "month": 9,
            "day": 24,
            "hour": 4,
            "minute": 15,
            "gender": "male",
            "full_name": "G1-12 live",
            "birth_place": "Ha Noi",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{LOCAL}/backend/api/v1/analyze",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as res:
        payload = json.loads(res.read().decode("utf-8"))
    data = payload.get("data") or {}
    useful = data.get("useful_god") or {}
    lines = [
        "useful_display=" + str(useful.get("useful_display")),
        "unfavorable_display=" + str(useful.get("unfavorable_display")),
        "unfavorable_gods=" + json.dumps(useful.get("unfavorable_gods"), ensure_ascii=False),
        "strength=" + json.dumps(data.get("strength"), ensure_ascii=False)[:300],
        "temperature=" + str((data.get("temperature") or {}).get("balancing_need_label")),
        "pattern=" + str((data.get("pattern") or {}).get("cach_cuc")),
        "day_master=" + str((data.get("bazi") or {}).get("day_master")),
        "day_master_element=" + str((data.get("bazi") or {}).get("day_master_element")),
    ]
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1648, "height": 928}).new_page()
        page.goto(f"{LOCAL}/result", wait_until="domcontentloaded", timeout=60000)
        page.evaluate(
            """() => {
              ['bte_last_result','bte_current_analysis_id','bte_view_result'].forEach((key) => {
                localStorage.removeItem(key);
                sessionStorage.removeItem(key);
              });
            }"""
        )
        page.goto(f"{LOCAL}/analyze", wait_until="networkidle", timeout=60000)
        page.fill("#full_name", "G1-12 live")
        page.check("#gender_male")
        page.fill("#birth_date", "24/09/1966")
        page.fill("#birth_time", "04:15")
        page.fill("#birth_place", "Hà Nội")
        page.click("#btnAnalyze")
        page.wait_for_url("**/result", timeout=120000)
        page.wait_for_selector('[data-card="overview"]', timeout=30000)
        page.wait_for_timeout(500)
        snap = page.evaluate(
            """() => {
              const ov = document.querySelector('[data-card=overview]');
              const pat = document.querySelector('[data-card=pattern]');
              return {
                href: location.href,
                scripts: [...document.querySelectorAll('script[src]')].map((el) => el.src),
                overview: ov ? ov.innerText : '',
                labels: [...(ov?.querySelectorAll('[data-evidence]') || [])].map((n) => n.getAttribute('data-evidence') + ':' + n.innerText.replace(/\\s+/g,' ').trim()),
                hasMenhCucInOverview: !!(ov && /Mệnh Cục/i.test(ov.innerText)),
                patternTitle: pat?.querySelector('.bte-cdash__card-title')?.textContent || '',
                conclusion: ov?.querySelector('[data-overview-section=conclusion]')?.innerText || '',
              };
            }"""
        )
        lines.append("DOM=" + json.dumps(snap, ensure_ascii=False))
        page.locator('[data-card="overview"]').screenshot(path=str(OUT / "G1_12_localhost_overview.png"))
        page.screenshot(path=str(OUT / "G1_12_localhost_result.png"), full_page=False)
        browser.close()
    (OUT / "_g112_live.txt").write_text("\n".join(lines), encoding="utf-8")
    print("WROTE", OUT / "_g112_live.txt")


if __name__ == "__main__":
    main()
