from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.rule_context_bridge import (
    build_rule_context,
    enrich_result_from_rule_context,
)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "validation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INPUT = {
    "full_name": "E2E Trace",
    "birth_place": "Ho Chi Minh",
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
    "timezone": "Asia/Ho_Chi_Minh",
}

FIELDS = [
    "than",
    "than_vuong_nhuoc",
    "cach_cuc",
    "tong_cach",
    "dung_than",
    "hy_than",
    "ky_than",
    "dieu_hau",
]


def compute_engine_fields() -> dict[str, Any]:
    calendar = CalendarEngine().build(
        INPUT["year"],
        INPUT["month"],
        INPUT["day"],
        INPUT["hour"],
        INPUT["minute"],
    )
    bazi_chart = BaziEngine().build(calendar, gender=INPUT["gender"])
    pattern_context = PatternContext(
        year_pillar=f"{bazi_chart.year_pillar.stem} {bazi_chart.year_pillar.branch}",
        month_pillar=f"{bazi_chart.month_pillar.stem} {bazi_chart.month_pillar.branch}",
        day_pillar=f"{bazi_chart.day_pillar.stem} {bazi_chart.day_pillar.branch}",
        hour_pillar=f"{bazi_chart.hour_pillar.stem} {bazi_chart.hour_pillar.branch}",
        day_master=bazi_chart.day_master,
        ten_gods={"list": list(bazi_chart.ten_gods or [])},
        shensha=list(bazi_chart.shensha or []),
        calendar=calendar,
        bazi=bazi_chart,
    )
    pattern_result = PatternEngine().calculate(pattern_context)
    rule_context = build_rule_context(
        calendar=calendar,
        bazi=bazi_chart,
        pattern=pattern_result,
    )
    enrich_result_from_rule_context(pattern_result, rule_context)
    return {field: getattr(pattern_result, field, None) for field in FIELDS}


def run_browser_trace() -> dict[str, Any]:
    api_response: dict[str, Any] | None = None
    portal_base_url = os.getenv("BTE_TRACE_PORTAL_URL", "http://127.0.0.1:8081")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def on_response(response) -> None:
            nonlocal api_response
            req = response.request
            if req.method != "POST":
                return
            if not response.url.endswith("/backend/api/v1/analyze"):
                return
            try:
                api_response = response.json()
            except Exception:
                api_response = {"_error": "unable_to_parse_json"}

        page.on("response", on_response)
        page.goto(f"{portal_base_url}/analyze", wait_until="networkidle")
        page.fill("#full_name", str(INPUT["full_name"]))
        page.fill("#birth_place", str(INPUT["birth_place"]))
        page.fill("#year", str(INPUT["year"]))
        page.fill("#month", str(INPUT["month"]))
        page.fill("#day", str(INPUT["day"]))
        page.fill("#hour", str(INPUT["hour"]))
        page.fill("#minute", str(INPUT["minute"]))
        page.select_option("#gender", str(INPUT["gender"]))
        page.fill("#timezone", str(INPUT["timezone"]))
        page.click("#btnAnalyze")
        page.wait_for_url("**/result", timeout=120_000)
        page.wait_for_timeout(800)

        # Hook presenters to capture real props payloads.
        page.evaluate(
            """
            () => {
              window.__trace = window.__trace || {};
              if (window.BtePresenters && window.BtePresenters.pattern && !window.__trace_wrapped_pattern) {
                const orig = window.BtePresenters.pattern;
                window.BtePresenters.pattern = function(payload) {
                  window.__trace.patternPayload = payload;
                  return orig.apply(this, arguments);
                };
                window.__trace_wrapped_pattern = true;
              }
              if (window.BtePresenters && window.BtePresenters.score && !window.__trace_wrapped_score) {
                const orig = window.BtePresenters.score;
                window.BtePresenters.score = function(payload) {
                  window.__trace.scorePayload = payload;
                  return orig.apply(this, arguments);
                };
                window.__trace_wrapped_score = true;
              }
              if (window.BteSummaryBuilder && window.BteSummaryBuilder.build && !window.__trace_wrapped_summary) {
                const orig = window.BteSummaryBuilder.build;
                window.BteSummaryBuilder.build = function(data, options) {
                  window.__trace.summaryInput = data;
                  return orig.apply(this, arguments);
                };
                window.__trace_wrapped_summary = true;
              }
            }
            """
        )

        page.click('button.tab[data-stage="pattern"]')
        page.wait_for_timeout(200)
        pattern_dom = page.evaluate(
            """
            () => {
              const rows = Array.from(document.querySelectorAll('.bte-pattern-card'));
              const out = {};
              rows.forEach((card) => {
                const label = (card.querySelector('.bte-card-label')?.textContent || '').trim();
                const value = (card.querySelector('.bte-card-value')?.textContent || '').trim();
                out[label] = value;
              });
              return out;
            }
            """
        )

        page.click('button.tab[data-stage="score"]')
        page.wait_for_timeout(200)
        page.click('button.tab[data-stage="narrative"]')
        page.wait_for_timeout(200)
        presenter_props = page.evaluate("() => window.__trace || {}")
        store_result = page.evaluate(
            """
            () => {
              if (!window.BtePortal || !window.BtePortal.ResultStore) return null;
              return window.BtePortal.ResultStore.loadForView();
            }
            """
        )
        browser.close()

    return {
        "api_response": api_response,
        "store_result": store_result,
        "presenter_props": presenter_props,
        "pattern_dom": pattern_dom,
    }


def map_dom_value(dom: dict[str, Any], field: str) -> Any:
    label_map = {
        "than": "Thân",
        "than_vuong_nhuoc": "Thân vượng/nhược",
        "cach_cuc": "Cách cục",
        "tong_cach": "Tòng cách",
        "dung_than": "Dụng thần",
        "hy_than": "Hỷ thần",
        "ky_than": "Kỵ thần",
        "dieu_hau": "Điều hậu",
    }
    return (dom or {}).get(label_map[field])


def main() -> None:
    engine_fields = compute_engine_fields()
    orchestrator_payload = OrchestratorService().analyze(
        year=INPUT["year"],
        month=INPUT["month"],
        day=INPUT["day"],
        hour=INPUT["hour"],
        minute=INPUT["minute"],
        gender=INPUT["gender"],
        timezone=INPUT["timezone"],
    )
    browser = run_browser_trace()
    api_response = browser.get("api_response") or {}
    store_result = browser.get("store_result") or {}
    presenter_props = browser.get("presenter_props") or {}
    pattern_dom = browser.get("pattern_dom") or {}

    response_path = OUT_DIR / "live_analyze_response.json"
    response_path.write_text(
        json.dumps(api_response, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    trace_rows: list[dict[str, Any]] = []
    for field in FIELDS:
        engine_v = engine_fields.get(field)
        orchestrator_v = (orchestrator_payload.get("pattern") or {}).get(field)
        api_v = (((api_response or {}).get("data") or {}).get("pattern") or {}).get(field)
        store_v = ((((store_result or {}).get("data") or {}).get("pattern") or {}).get(field))
        presenter_v = ((presenter_props.get("patternPayload") or {}).get(field))
        dom_v = map_dom_value(pattern_dom, field)
        status = "OK"
        if not api_v:
            status = "MISSING_AT_API"
        elif not store_v:
            status = "MISSING_AT_STORE"
        elif not presenter_v:
            status = "MISSING_AT_PRESENTER"
        elif dom_v in {None, "", "--"}:
            status = "MISSING_AT_UI"
        trace_rows.append(
            {
                "field": field,
                "engine": engine_v,
                "orchestrator": orchestrator_v,
                "api": api_v,
                "store": store_v,
                "presenter": presenter_v,
                "dom": dom_v,
                "status": status,
            }
        )

    out = {
        "input": INPUT,
        "response_json_path": str(response_path),
        "console_log_result_equivalent": store_result,
        "presenter_props": presenter_props,
        "pattern_dom": pattern_dom,
        "trace_rows": trace_rows,
    }
    out_path = OUT_DIR / "live_e2e_trace.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
