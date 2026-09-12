"""RB16 Number Energy runtime visual review capture. Review-only; not a product feature."""

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
HARNESS_JS = OUT / "harness" / "numberEnergyRuntime.js"
PORTAL_PORT = 8091
API_PORT = 8000
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
ROUTE = f"{BASE}/number-energy"
ANALYZE_PATH = "/backend/api/v1/number-energy/analyze"
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


def _build_runtime_harness() -> None:
    result = subprocess.run(
        [
            "npm",
            "run",
            "build:number-energy-screenshots",
        ],
        cwd=str(PORTAL),
        check=False,
        capture_output=True,
        text=True,
        shell=os.name == "nt",
    )
    if result.returncode != 0:
        raise RuntimeError(
            "RB16 harness build failed:\n"
            f"{result.stdout}\n{result.stderr}"
        )
    if not HARNESS_JS.exists():
        raise RuntimeError(f"Missing runtime harness bundle: {HARNESS_JS}")


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


def _slot_sources(page) -> dict[str, str | None]:
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


def _install_runtime_bundle(page) -> None:
    body = HARNESS_JS.read_text(encoding="utf-8")

    def handle(route: Route) -> None:
        if "numberEnergy.js" in route.request.url and "Runtime" not in route.request.url:
            route.fulfill(status=200, content_type="text/javascript", body=body)
            return
        route.continue_()

    page.route("**/static/dist/numberEnergy.js*", handle)


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


def _fallback_analyze(page) -> None:
    def handle(route: Route) -> None:
        if route.request.method != "POST" or "number-energy/analyze" not in route.request.url:
            route.continue_()
            return
        response = route.fetch()
        try:
            payload = response.json()
        except Exception:
            route.fulfill(status=response.status, body=response.body(), headers=response.headers)
            return
        data = payload.get("data") if isinstance(payload, dict) else None
        if isinstance(data, dict):
            data.pop("metadata", None)
            data.pop("input_raw", None)
            data.pop("identity", None)
            payload["data"] = data
        route.fulfill(
            status=response.status,
            content_type="application/json",
            body=json.dumps(payload),
        )

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
    _build_runtime_harness()
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

            static_requests: list[dict] = []
            static_page = browser.new_page(viewport=DESKTOP)
            static_page.on(
                "request",
                lambda req: static_requests.append(
                    {"url": req.url, "method": req.method, "resource": req.resource_type}
                ),
            )
            _goto_number_energy(static_page)
            static_input_hidden = static_page.locator("[data-testid='result-section']").evaluate(
                "el => el.hidden"
            )
            static_page.screenshot(path=str(OUT / "01_static_input_desktop.png"), full_page=True)
            _submit_golden(static_page)
            static_page.screenshot(path=str(OUT / "02_static_result_desktop.png"), full_page=True)
            report["staticDesktop"] = {
                "runtimeMode": static_page.locator("[data-testid='number-energy-page']").get_attribute(
                    "data-runtime-mode"
                ),
                "freeze": static_page.locator("[data-testid='number-energy-page']").get_attribute(
                    "data-static-freeze"
                ),
                "resultHiddenBeforeSubmit": static_input_hidden,
                "slotSources": _slot_sources(static_page),
                "hero": _hero(static_page),
                "overflow": _overflow_report(static_page),
                "text": _visible_text(static_page),
                "triples": static_page.locator("[data-testid^='triple-card-']").count(),
                "triple787": static_page.locator("[data-testid='triple-digits-4']").inner_text(),
                "triple878": static_page.locator("[data-testid='triple-digits-5']").inner_text(),
                "scoreText": static_page.locator("[data-testid='score-breakdown']").inner_text(),
            }

            static_page.set_viewport_size(MOBILE)
            _goto_number_energy(static_page)
            static_page.screenshot(path=str(OUT / "07_static_input_mobile.png"), full_page=True)
            _submit_golden(static_page)
            static_page.screenshot(path=str(OUT / "08_static_result_mobile.png"), full_page=True)
            report["staticMobile"] = {
                "overflow": _overflow_report(static_page),
                "slotSources": _slot_sources(static_page),
                "hero": _hero(static_page),
                "text": _visible_text(static_page),
            }
            static_page.close()

            runtime_requests: list[dict] = []
            runtime_errors: list[str] = []
            runtime_page = browser.new_page(viewport=DESKTOP)
            runtime_page.on(
                "request",
                lambda req: runtime_requests.append(
                    {"url": req.url, "method": req.method, "resource": req.resource_type}
                ),
            )
            runtime_page.on("pageerror", lambda err: runtime_errors.append(str(err)))
            runtime_page.on("console", lambda msg: runtime_errors.append(f"console:{msg.type}:{msg.text}"))
            _install_runtime_bundle(runtime_page)
            try:
                _goto_number_energy(runtime_page)
            except Exception:
                print("RB16 runtime mount failed")
                print("\n".join(runtime_errors[-30:]))
                raise
            runtime_input_hidden = runtime_page.locator("[data-testid='result-section']").evaluate(
                "el => el.hidden"
            )
            runtime_mode = runtime_page.locator("[data-testid='number-energy-page']").get_attribute(
                "data-runtime-mode"
            )
            analyze_before_submit = _analyze_calls(runtime_requests)
            runtime_page.screenshot(path=str(OUT / "03_runtime_input_desktop.png"), full_page=True)
            _submit_golden(runtime_page)
            runtime_page.locator("[data-testid='result-hero']").scroll_into_view_if_needed()
            runtime_page.screenshot(path=str(OUT / "04_runtime_result_top_desktop.png"), full_page=False)
            runtime_page.screenshot(path=str(OUT / "05_runtime_result_full_desktop.png"), full_page=True)
            report["runtimeDesktop"] = {
                "runtimeMode": runtime_mode,
                "resultHiddenBeforeSubmit": runtime_input_hidden,
                "analyzeBeforeSubmit": analyze_before_submit,
                "pageErrors": runtime_errors[-20:],
                "slotSources": _slot_sources(runtime_page),
                "hero": _hero(runtime_page),
                "overflow": _overflow_report(runtime_page),
                "text": _visible_text(runtime_page),
                "triples": runtime_page.locator("[data-testid^='triple-card-']").count(),
                "triple787": runtime_page.locator("[data-testid='triple-digits-4']").inner_text(),
                "triple878": runtime_page.locator("[data-testid='triple-digits-5']").inner_text(),
                "scoreText": runtime_page.locator("[data-testid='score-breakdown']").inner_text(),
            }

            runtime_page.set_viewport_size(MOBILE)
            _goto_number_energy(runtime_page)
            runtime_page.screenshot(path=str(OUT / "09_runtime_input_mobile.png"), full_page=True)
            _submit_golden(runtime_page)
            runtime_page.locator("[data-testid='result-hero']").scroll_into_view_if_needed()
            runtime_page.screenshot(path=str(OUT / "10_runtime_result_top_mobile.png"), full_page=False)
            runtime_page.screenshot(path=str(OUT / "11_runtime_result_full_mobile.png"), full_page=True)
            report["runtimeMobile"] = {
                "overflow": _overflow_report(runtime_page),
                "slotSources": _slot_sources(runtime_page),
                "hero": _hero(runtime_page),
                "text": _visible_text(runtime_page),
            }
            runtime_page.close()

            error_requests: list[dict] = []
            error_page = browser.new_page(viewport=DESKTOP)
            error_page.on(
                "request",
                lambda req: error_requests.append(
                    {"url": req.url, "method": req.method, "resource": req.resource_type}
                ),
            )
            _install_runtime_bundle(error_page)
            _fail_analyze(error_page)
            _goto_number_energy(error_page)
            _submit_golden(error_page, wait_result=False)
            error_page.locator("[data-testid='input-error']").wait_for(timeout=15000)
            error_hidden = error_page.locator("[data-testid='result-section']").evaluate("el => el.hidden")
            error_text = error_page.locator("[data-testid='number-energy-page']").text_content() or ""
            error_page.evaluate("window.scrollTo(0, 0)")
            error_page.screenshot(path=str(OUT / "06_runtime_error_desktop.png"), full_page=False)
            error_page.set_viewport_size(MOBILE)
            _goto_number_energy(error_page)
            _submit_golden(error_page, wait_result=False)
            error_page.locator("[data-testid='input-error']").wait_for(timeout=15000)
            error_page.evaluate("window.scrollTo(0, 0)")
            error_page.screenshot(path=str(OUT / "12_runtime_error_mobile.png"), full_page=True)
            report["runtimeError"] = {
                "resultHidden": error_hidden,
                "message": error_page.locator("[data-testid='input-error']").inner_text(),
                "text": error_text,
                "analyzeCalls": _analyze_calls(error_requests),
            }

            fallback_page = browser.new_page(viewport=DESKTOP)
            _install_runtime_bundle(fallback_page)
            _fallback_analyze(fallback_page)
            _goto_number_energy(fallback_page)
            _submit_golden(fallback_page)
            fallback_page.screenshot(path=str(OUT / "13_runtime_fallback_ps00_desktop.png"), full_page=False)
            report["runtimeFallback"] = {
                "slotSources": _slot_sources(fallback_page),
                "hero": _hero(fallback_page),
            }
            fallback_page.close()
            error_page.close()
            browser.close()
    finally:
        for proc in (portal, api):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    static_analyze = _analyze_calls(static_requests)
    runtime_analyze = _analyze_calls(runtime_requests)
    leaks = []
    for label in ("staticDesktop", "staticMobile", "runtimeDesktop", "runtimeMobile"):
        blob = report[label]["text"]
        for token in _token_leaks(blob):
            leaks.append({"surface": label, "token": token})
    if any(token in report["runtimeError"]["text"] for token in ("Traceback", "energy_id", "HTTP_ERROR")):
        leaks.append({"surface": "runtimeError", "token": "technical-error"})

    summary = {
        "stage": "RB16",
        "route": "/number-energy",
        "portal": BASE,
        "staticAnalyzeCalls": static_analyze,
        "runtimeAnalyzeCalls": runtime_analyze,
        "runtimeAnalyzeBeforeSubmit": report["runtimeDesktop"]["analyzeBeforeSubmit"],
        "leaks": leaks,
        "staticDesktop": {
            "runtimeMode": report["staticDesktop"]["runtimeMode"],
            "freeze": report["staticDesktop"]["freeze"],
            "resultHiddenBeforeSubmit": report["staticDesktop"]["resultHiddenBeforeSubmit"],
            "slotSources": report["staticDesktop"]["slotSources"],
            "hero": report["staticDesktop"]["hero"],
            "overflow": _unexpected_overflow(report["staticDesktop"]["overflow"]),
            "triples": report["staticDesktop"]["triples"],
            "triple787": report["staticDesktop"]["triple787"],
            "triple878": report["staticDesktop"]["triple878"],
            "scoreHasPercent": "%" in report["staticDesktop"]["scoreText"],
        },
        "staticMobile": {
            "slotSources": report["staticMobile"]["slotSources"],
            "hero": report["staticMobile"]["hero"],
            "overflow": _unexpected_overflow(report["staticMobile"]["overflow"]),
        },
        "runtimeDesktop": {
            "runtimeMode": report["runtimeDesktop"]["runtimeMode"],
            "resultHiddenBeforeSubmit": report["runtimeDesktop"]["resultHiddenBeforeSubmit"],
            "slotSources": report["runtimeDesktop"]["slotSources"],
            "hero": report["runtimeDesktop"]["hero"],
            "overflow": _unexpected_overflow(report["runtimeDesktop"]["overflow"]),
            "triples": report["runtimeDesktop"]["triples"],
            "triple787": report["runtimeDesktop"]["triple787"],
            "triple878": report["runtimeDesktop"]["triple878"],
            "scoreHasPercent": "%" in report["runtimeDesktop"]["scoreText"],
        },
        "runtimeMobile": {
            "slotSources": report["runtimeMobile"]["slotSources"],
            "hero": report["runtimeMobile"]["hero"],
            "overflow": _unexpected_overflow(report["runtimeMobile"]["overflow"]),
        },
        "runtimeError": {
            "resultHidden": report["runtimeError"]["resultHidden"],
            "message": report["runtimeError"]["message"],
            "analyzeCalls": len(report["runtimeError"]["analyzeCalls"]),
        },
        "runtimeFallback": report["runtimeFallback"],
        "screenshots": [
            "01_static_input_desktop.png",
            "02_static_result_desktop.png",
            "03_runtime_input_desktop.png",
            "04_runtime_result_top_desktop.png",
            "05_runtime_result_full_desktop.png",
            "06_runtime_error_desktop.png",
            "07_static_input_mobile.png",
            "08_static_result_mobile.png",
            "09_runtime_input_mobile.png",
            "10_runtime_result_top_mobile.png",
            "11_runtime_result_full_mobile.png",
            "12_runtime_error_mobile.png",
            "13_runtime_fallback_ps00_desktop.png",
        ],
    }
    (OUT / "review.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("RB16 capture complete")
    print(json.dumps({
        "staticAnalyze": len(static_analyze),
        "runtimeAnalyze": len(runtime_analyze),
        "runtimeMode": summary["runtimeDesktop"]["runtimeMode"],
        "leaks": leaks,
        "runtimeOverflow": summary["runtimeDesktop"]["overflow"]["documentOverflowPx"],
        "runtimeSlots": summary["runtimeDesktop"]["slotSources"],
        "errorHidden": summary["runtimeError"]["resultHidden"],
        "fallbackHero": summary["runtimeFallback"]["slotSources"].get("P-S00"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
