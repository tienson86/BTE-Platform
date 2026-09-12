"""RB18 Number Energy public runtime visual review. Does not intercept the public bundle."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import Route, sync_playwright

REPO = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PORTAL = REPO / "applications" / "customer_portal"
PORTAL_PORT = 8091
API_PORT = 8000
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
ROUTE = f"{BASE}/number-energy"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
FORBIDDEN = [
    "verified_by_runtime",
    "fixture_id",
    "presentation_fixture",
    "energy_id",
    "source_span",
    "DIEN_NIEN",
    "THIEN_Y",
    "CAT",
    "HUNG",
    "score_axis",
    "copy_key",
    "evidence_id",
]
RUNTIME_SLOTS = [
    ("P-S00", "result-hero"),
    ("P-S01", "energy-map"),
    ("P-S02", "quick-structure"),
    ("P-S03", "wealth-flow"),
    ("P-S04", "triple-story"),
    ("P-S05", "energy-distribution"),
    ("P-S06", "domain-insights"),
    ("P-S07", "strengths-cautions"),
    ("P-S08", "score-breakdown"),
    ("P-S09", "final-assessment"),
    ("P-S10", "basis-of-assessment"),
]


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _kill_port(port: int) -> None:
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
    deadline = time.time() + 5
    while time.time() < deadline and _listening(port):
        time.sleep(0.2)


def _wait(port: int, timeout: float = 40.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _start_proc(args: list[str], env: dict[str, str] | None = None) -> subprocess.Popen:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.Popen(
        args,
        cwd=str(REPO),
        env=merged,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _overflow_report(page) -> dict:
    return page.evaluate(
        """() => {
          const pageEl = document.querySelector('[data-testid="number-energy-page"]');
          const pair = document.querySelector('[data-testid="pair-strip-scroller"]');
          const identity = document.querySelector('[data-testid="hero-identity"]');
          const wealth = document.querySelector('[data-testid="wealth-stages"]');
          const cta = document.querySelector('[data-testid="analysis-submit"]');
          const expert = document.querySelector('[data-testid="expert-details"]');
          const allowed = new Set(["pair-strip-scroller", "hero-identity"]);
          const overflow = [];
          document.querySelectorAll("body *").forEach((el) => {
            if (!(el instanceof HTMLElement)) return;
            if (el.scrollWidth <= el.clientWidth + 1) return;
            const testid = el.getAttribute("data-testid") || "";
            const cls = el.className && typeof el.className === "string" ? el.className : "";
            if (cls.includes("ne-sr-only") || testid === "form-status") return;
            overflow.push({
              testid,
              cls: cls.slice(0, 80),
              scrollWidth: el.scrollWidth,
              clientWidth: el.clientWidth,
              allowed: allowed.has(testid) || cls.includes("ne-pair-strip"),
            });
          });
          const wealthStyle = wealth ? getComputedStyle(wealth) : null;
          const desktopConnector = document.querySelector(".ne-wealth-connector--desktop");
          const mobileConnector = document.querySelector(".ne-wealth-connector--mobile");
          return {
            viewport: { innerWidth: window.innerWidth, innerHeight: window.innerHeight },
            documentScrollWidth: document.documentElement.scrollWidth,
            documentClientWidth: document.documentElement.clientWidth,
            innerWidth: window.innerWidth,
            pageScrollWidth: pageEl ? pageEl.scrollWidth : null,
            pageClientWidth: pageEl ? pageEl.clientWidth : null,
            pairScrollWidth: pair ? pair.scrollWidth : null,
            pairClientWidth: pair ? pair.clientWidth : null,
            identityScrollWidth: identity ? identity.scrollWidth : null,
            identityClientWidth: identity ? identity.clientWidth : null,
            wealthFlexDirection: wealthStyle ? wealthStyle.flexDirection : null,
            desktopConnectorDisplay: desktopConnector ? getComputedStyle(desktopConnector).display : null,
            mobileConnectorDisplay: mobileConnector ? getComputedStyle(mobileConnector).display : null,
            ctaRect: cta ? cta.getBoundingClientRect().toJSON() : null,
            expertHidden: expert ? expert.hasAttribute("hidden") : null,
            expertAriaHidden: expert ? expert.getAttribute("aria-hidden") : null,
            pageScrollLeft: (() => {
              const html = document.documentElement;
              html.scrollLeft = 9999;
              const scrolled = html.scrollLeft;
              html.scrollLeft = 0;
              return scrolled;
            })(),
            overflow,
          };
        }"""
    )


def _slot_sources(page) -> dict:
    return page.evaluate(
        """(slots) => {
          const out = {};
          for (const [sectionId, testId] of slots) {
            const el = document.querySelector(`[data-testid="${testId}"]`);
            out[sectionId] = el ? el.getAttribute("data-slot-source") : null;
          }
          const expert = document.querySelector('[data-testid="expert-details"]');
          out["P-S11"] = {
            hidden: expert ? expert.hasAttribute("hidden") : null,
            ariaHidden: expert ? expert.getAttribute("aria-hidden") : null,
            slotSource: expert ? expert.getAttribute("data-slot-source") : null,
          };
          return out;
        }""",
        RUNTIME_SLOTS,
    )


def _hero(page) -> dict:
    return {
        "identity": page.locator("[data-testid='hero-identity']").inner_text(),
        "score": page.locator("[data-testid='hero-score']").inner_text(),
        "grade": page.locator("[data-testid='hero-grade']").inner_text(),
        "primary": page.locator("[data-testid='hero-primary-energy']").inner_text(),
        "summary": page.locator("[data-testid='hero-summary']").inner_text(),
    }


def _nav_state(page) -> dict:
    return page.evaluate(
        """() => {
          const nav = document.querySelector('[data-customer-nav="primary"]');
          const active = nav ? nav.querySelector(".nav-link.active, [aria-current='page']") : null;
          const labels = nav
            ? Array.from(nav.querySelectorAll("a")).map((el) => el.textContent || "")
            : [];
          return {
            labels,
            navActive: active ? active.getAttribute("data-nav-id") : null,
            navLabel: active ? active.textContent : null,
            href: active ? active.getAttribute("href") : null,
          };
        }"""
    )


def _visible_text(page) -> str:
    return page.locator("[data-testid='number-energy-page']").text_content() or ""


def _token_leaks(blob: str) -> list[str]:
    return [token for token in FORBIDDEN if token in blob]


def _analyze_calls(requests: list[dict]) -> list[dict]:
    calls = []
    for item in requests:
        url = item.get("url") or ""
        if item.get("resource") not in {"fetch", "xhr"}:
            continue
        if "number-energy/analyze" in url:
            calls.append(item)
    return calls


def _fail_analyze(page) -> None:
    def handle(route: Route) -> None:
        if route.request.method == "POST" and "number-energy/analyze" in route.request.url:
            route.fulfill(
                status=500,
                content_type="application/json",
                body=json.dumps(
                    {
                        "success": False,
                        "message": "Traceback (most recent call last): energy_id",
                        "data": None,
                    }
                ),
            )
            return
        route.continue_()

    page.route("**/number-energy/analyze*", handle)


def _goto_number_energy(page) -> None:
    page.goto(ROUTE, wait_until="networkidle")
    page.locator("[data-testid='number-energy-page']").wait_for()


def _submit_golden(page, *, wait_result: bool = True) -> None:
    page.locator("[data-testid='number-input']").fill("0328278786")
    page.locator("[data-testid='analysis-submit']").click()
    if wait_result:
        page.locator("[data-testid='result-hero']").wait_for(state="visible", timeout=20000)
        page.wait_for_timeout(350)


def _unexpected_overflow(block: dict) -> dict:
    items = []
    for row in block.get("overflow") or []:
        if row.get("allowed"):
            continue
        if row["scrollWidth"] - row["clientWidth"] < 8:
            continue
        items.append(row)
    return {
        "documentOverflowPx": block["documentScrollWidth"] - block["innerWidth"],
        "pageScrollLeft": block.get("pageScrollLeft"),
        "nodes": items[:20],
        "wealthFlexDirection": block.get("wealthFlexDirection"),
        "desktopConnectorDisplay": block.get("desktopConnectorDisplay"),
        "mobileConnectorDisplay": block.get("mobileConnectorDisplay"),
        "expertHidden": block.get("expertHidden"),
        "pairInternalScroll": (block.get("pairScrollWidth") or 0) - (block.get("pairClientWidth") or 0),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api = _start_proc(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "applications.api.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(API_PORT),
        ]
    )
    portal = _start_proc(
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
        env={"BTE_API_BASE_URL": f"http://127.0.0.1:{API_PORT}"},
    )
    report: dict = {"screenshots": [], "issues": []}
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()

            requests: list[dict] = []
            page_errors: list[str] = []
            page = browser.new_page(viewport=DESKTOP)
            page.on(
                "request",
                lambda req: requests.append(
                    {"url": req.url, "method": req.method, "resource": req.resource_type}
                ),
            )
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            _goto_number_energy(page)
            analyze_before_submit = _analyze_calls(requests)
            input_hidden = page.locator("[data-testid='result-section']").evaluate("el => el.hidden")
            nav = _nav_state(page)
            runtime_mode = page.locator("[data-testid='number-energy-page']").get_attribute(
                "data-runtime-mode"
            )
            freeze = page.locator("[data-testid='number-energy-page']").get_attribute(
                "data-static-freeze"
            )
            static_note = page.locator("[data-testid='static-sample-note']")
            page.screenshot(path=str(OUT / "01_runtime_input_desktop.png"), full_page=True)
            report["inputDesktop"] = {
                "runtimeMode": runtime_mode,
                "freeze": freeze,
                "resultHidden": input_hidden,
                "navActive": nav["navActive"],
                "navLabel": nav["navLabel"],
                "navLabels": nav["labels"],
                "staticSampleNote": static_note.count(),
                "analyzeBeforeSubmit": analyze_before_submit,
                "text": _visible_text(page),
                "overflow": _overflow_report(page),
            }

            _submit_golden(page)
            page.locator("[data-testid='result-hero']").scroll_into_view_if_needed()
            page.screenshot(path=str(OUT / "02_runtime_result_top_desktop.png"), full_page=False)
            page.screenshot(path=str(OUT / "03_runtime_result_full_desktop.png"), full_page=True)
            analyze_after_submit = _analyze_calls(requests)
            report["successDesktop"] = {
                "runtimeMode": page.locator("[data-testid='number-energy-page']").get_attribute(
                    "data-runtime-mode"
                ),
                "slotSources": _slot_sources(page),
                "hero": _hero(page),
                "overflow": _overflow_report(page),
                "text": _visible_text(page),
                "analyzeCalls": analyze_after_submit,
                "pageErrors": page_errors[-20:],
            }

            page.set_viewport_size(MOBILE)
            _goto_number_energy(page)
            page.screenshot(path=str(OUT / "05_runtime_input_mobile.png"), full_page=True)
            _submit_golden(page)
            page.locator("[data-testid='result-hero']").scroll_into_view_if_needed()
            page.screenshot(path=str(OUT / "06_runtime_result_top_mobile.png"), full_page=False)
            page.screenshot(path=str(OUT / "07_runtime_result_full_mobile.png"), full_page=True)
            report["successMobile"] = {
                "slotSources": _slot_sources(page),
                "hero": _hero(page),
                "overflow": _overflow_report(page),
                "text": _visible_text(page),
                "nav": _nav_state(page),
            }
            page.close()

            error_requests: list[dict] = []
            error_page = browser.new_page(viewport=DESKTOP)
            error_page.on(
                "request",
                lambda req: error_requests.append(
                    {"url": req.url, "method": req.method, "resource": req.resource_type}
                ),
            )
            _fail_analyze(error_page)
            _goto_number_energy(error_page)
            _submit_golden(error_page, wait_result=False)
            error_page.locator("[data-testid='input-error']").wait_for(timeout=15000)
            error_hidden = error_page.locator("[data-testid='result-section']").evaluate(
                "el => el.hidden"
            )
            error_text = error_page.locator("[data-testid='number-energy-page']").text_content() or ""
            error_page.evaluate("window.scrollTo(0, 0)")
            error_page.screenshot(path=str(OUT / "04_runtime_error_desktop.png"), full_page=False)
            error_page.set_viewport_size(MOBILE)
            _goto_number_energy(error_page)
            _submit_golden(error_page, wait_result=False)
            error_page.locator("[data-testid='input-error']").wait_for(timeout=15000)
            error_page.evaluate("window.scrollTo(0, 0)")
            error_page.screenshot(path=str(OUT / "08_runtime_error_mobile.png"), full_page=True)
            report["errorDesktop"] = {
                "resultHidden": error_hidden,
                "message": error_page.locator("[data-testid='input-error']").inner_text(),
                "text": error_text,
                "analyzeCalls": _analyze_calls(error_requests),
            }
            error_page.close()
            browser.close()
    finally:
        for proc in (portal, api):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    leaks = []
    for label in ("inputDesktop", "successDesktop", "successMobile"):
        blob = report[label]["text"]
        for token in _token_leaks(blob):
            leaks.append({"surface": label, "token": token})
    if any(token in report["errorDesktop"]["text"] for token in ("Traceback", "energy_id", "HTTP_ERROR")):
        leaks.append({"surface": "runtimeError", "token": "technical-error"})

    summary = {
        "stage": "RB18",
        "route": "/number-energy",
        "portal": BASE,
        "analyzeBeforeSubmit": report["inputDesktop"]["analyzeBeforeSubmit"],
        "analyzeCalls": report["successDesktop"]["analyzeCalls"],
        "leaks": leaks,
        "inputDesktop": {
            "runtimeMode": report["inputDesktop"]["runtimeMode"],
            "freeze": report["inputDesktop"]["freeze"],
            "resultHidden": report["inputDesktop"]["resultHidden"],
            "navActive": report["inputDesktop"]["navActive"],
            "navLabel": report["inputDesktop"]["navLabel"],
            "navLabels": report["inputDesktop"]["navLabels"],
            "staticSampleNote": report["inputDesktop"]["staticSampleNote"],
            "overflow": _unexpected_overflow(report["inputDesktop"]["overflow"]),
        },
        "successDesktop": {
            "runtimeMode": report["successDesktop"]["runtimeMode"],
            "slotSources": report["successDesktop"]["slotSources"],
            "hero": report["successDesktop"]["hero"],
            "overflow": _unexpected_overflow(report["successDesktop"]["overflow"]),
        },
        "successMobile": {
            "slotSources": report["successMobile"]["slotSources"],
            "hero": report["successMobile"]["hero"],
            "overflow": _unexpected_overflow(report["successMobile"]["overflow"]),
            "nav": report["successMobile"]["nav"],
        },
        "errorDesktop": {
            "resultHidden": report["errorDesktop"]["resultHidden"],
            "message": report["errorDesktop"]["message"],
            "analyzeCalls": len(report["errorDesktop"]["analyzeCalls"]),
        },
        "screenshots": [
            "01_runtime_input_desktop.png",
            "02_runtime_result_top_desktop.png",
            "03_runtime_result_full_desktop.png",
            "04_runtime_error_desktop.png",
            "05_runtime_input_mobile.png",
            "06_runtime_result_top_mobile.png",
            "07_runtime_result_full_mobile.png",
            "08_runtime_error_mobile.png",
        ],
        "pageErrors": report["successDesktop"]["pageErrors"],
    }
    (OUT / "review.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("RB18 capture complete")
    print(
        json.dumps(
            {
                "runtimeMode": summary["inputDesktop"]["runtimeMode"],
                "navActive": summary["inputDesktop"]["navActive"],
                "analyzeBefore": len(summary["analyzeBeforeSubmit"]),
                "analyzeAfter": len(summary["analyzeCalls"]),
                "leaks": leaks,
                "overflow": summary["successDesktop"]["overflow"]["documentOverflowPx"],
                "slots": summary["successDesktop"]["slotSources"],
                "errorHidden": summary["errorDesktop"]["resultHidden"],
                "errorMessage": summary["errorDesktop"]["message"],
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
