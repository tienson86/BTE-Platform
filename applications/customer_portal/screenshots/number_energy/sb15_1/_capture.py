"""Ephemeral SB15.1 live screenshot capture. Not a product feature."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PORTAL = REPO / "applications" / "customer_portal"
PORTAL_PORT = 8091
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
FORBIDDEN = [
    "fixture_id",
    "presentation_fixture",
    "verified_by_runtime",
    "knowledge_version",
    "DIEN_NIEN",
    "THIEN_Y",
    "HOA_HAI",
    "82%",
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


def _wait(port: int, timeout: float = 25.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


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
            overflow.push({
              testid,
              cls: cls.slice(0, 80),
              scrollWidth: el.scrollWidth,
              clientWidth: el.clientWidth,
              allowed: allowed.has(testid) || cls.includes("ne-pair-strip"),
            });
          });
          const wealthStyle = wealth ? getComputedStyle(wealth) : null;
          return {
            viewport: { innerWidth: window.innerWidth, innerHeight: window.innerHeight },
            documentScrollWidth: document.documentElement.scrollWidth,
            documentClientWidth: document.documentElement.clientWidth,
            pageScrollWidth: pageEl ? pageEl.scrollWidth : null,
            pageClientWidth: pageEl ? pageEl.clientWidth : null,
            pairScrollWidth: pair ? pair.scrollWidth : null,
            pairClientWidth: pair ? pair.clientWidth : null,
            identityScrollWidth: identity ? identity.scrollWidth : null,
            identityClientWidth: identity ? identity.clientWidth : null,
            wealthFlexDirection: wealthStyle ? wealthStyle.flexDirection : null,
            ctaRect: cta ? cta.getBoundingClientRect().toJSON() : null,
            expertHidden: expert ? expert.hasAttribute("hidden") : null,
            expertAriaHidden: expert ? expert.getAttribute("aria-hidden") : null,
            overflow,
          };
        }"""
    )


def _visible_text(page) -> str:
    return page.locator("[data-testid='number-energy-page']").inner_text()


def _submit_golden(page) -> None:
    page.locator("[data-testid='number-input']").fill("0328278786")
    page.locator("[data-testid='analysis-submit']").click()
    page.locator("[data-testid='result-hero']").wait_for(state="visible")
    page.wait_for_timeout(250)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    requests: list[dict] = []
    _kill_port(PORTAL_PORT)
    env = os.environ.copy()
    env["BTE_API_BASE_URL"] = "http://127.0.0.1:9"
    proc = subprocess.Popen(
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
        cwd=str(REPO),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    report: dict = {}
    try:
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport=DESKTOP)
            page.on(
                "request",
                lambda req: requests.append({"url": req.url, "method": req.method, "resource": req.resource_type}),
            )
            page.goto(f"{BASE}/number-energy", wait_until="networkidle")
            page.locator("[data-testid='number-energy-page']").wait_for()
            page.screenshot(path=str(OUT / "01_input_desktop.png"), full_page=True)
            _submit_golden(page)
            page.locator("[data-testid='result-hero']").scroll_into_view_if_needed()
            page.screenshot(path=str(OUT / "02_result_top_desktop.png"), full_page=False)
            page.screenshot(path=str(OUT / "03_result_full_desktop.png"), full_page=True)
            report["desktop"] = {
                "overflow": _overflow_report(page),
                "hero": {
                    "identity": page.locator("[data-testid='hero-identity']").inner_text(),
                    "score": page.locator("[data-testid='hero-score']").inner_text(),
                    "grade": page.locator("[data-testid='hero-grade']").inner_text(),
                },
                "scoreTotal": page.locator("[data-testid='score-total']").inner_text(),
                "text": _visible_text(page),
            }

            page.set_viewport_size(MOBILE)
            page.goto(f"{BASE}/number-energy", wait_until="networkidle")
            page.locator("[data-testid='number-energy-page']").wait_for()
            page.screenshot(path=str(OUT / "04_input_mobile.png"), full_page=True)
            _submit_golden(page)
            page.locator("[data-testid='result-hero']").scroll_into_view_if_needed()
            page.screenshot(path=str(OUT / "05_result_top_mobile.png"), full_page=False)
            page.screenshot(path=str(OUT / "06_result_full_mobile.png"), full_page=True)
            report["mobile"] = {
                "overflow": _overflow_report(page),
                "widest": page.evaluate(
                    """() => {
                      const rows = [];
                      document.querySelectorAll("body *").forEach((el) => {
                        if (!(el instanceof HTMLElement)) return;
                        if ((el.className || "").includes("ne-sr-only")) return;
                        const rect = el.getBoundingClientRect();
                        const w = Math.max(el.scrollWidth, rect.width);
                        if (w < 400) return;
                        rows.push({
                          tag: el.tagName,
                          testid: el.getAttribute("data-testid") || "",
                          cls: String(el.className || "").slice(0, 90),
                          scrollWidth: el.scrollWidth,
                          offsetWidth: el.offsetWidth,
                          rectWidth: Math.round(rect.width),
                        });
                      });
                      rows.sort((a, b) => b.scrollWidth - a.scrollWidth);
                      return {
                        html: document.documentElement.scrollWidth,
                        body: document.body.scrollWidth,
                        htmlOverflowX: getComputedStyle(document.documentElement).overflowX,
                        bodyOverflowX: getComputedStyle(document.body).overflowX,
                        pageScrollLeft: (() => {
                          const html = document.documentElement;
                          html.scrollLeft = 9999;
                          const scrolled = html.scrollLeft;
                          html.scrollLeft = 0;
                          return scrolled;
                        })(),
                        rows: rows.slice(0, 15),
                      };
                    }"""
                ),
                "hero": {
                    "identity": page.locator("[data-testid='hero-identity']").inner_text(),
                    "score": page.locator("[data-testid='hero-score']").inner_text(),
                    "grade": page.locator("[data-testid='hero-grade']").inner_text(),
                },
                "scoreTotal": page.locator("[data-testid='score-total']").inner_text(),
                "text": _visible_text(page),
            }
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    analyze_calls = [
        item
        for item in requests
        if "analyze" in item["url"] or "number-energy" in item["url"] and item["resource"] in {"fetch", "xhr"}
    ]
    leaks = []
    for label, blob in (("desktop", report["desktop"]["text"]), ("mobile", report["mobile"]["text"])):
        for token in FORBIDDEN:
            if token in blob:
                leaks.append({"surface": label, "token": token})

    def unexpected_overflow(block: dict) -> list[dict]:
        items = []
        for row in block["overflow"]["overflow"]:
            if row.get("allowed"):
                continue
            if row["scrollWidth"] - row["clientWidth"] < 8:
                continue
            items.append(row)
        doc_overflow = block["overflow"]["documentScrollWidth"] - block["overflow"]["documentClientWidth"]
        return {
            "documentOverflowPx": doc_overflow,
            "nodes": items[:20],
            "wealthFlexDirection": block["overflow"]["wealthFlexDirection"],
            "expertHidden": block["overflow"]["expertHidden"],
        }

    summary = {
        "route": "/number-energy",
        "portal": BASE,
        "analyzeOrXhrCalls": analyze_calls,
        "leaks": leaks,
        "desktopHero": report["desktop"]["hero"],
        "desktopScore": report["desktop"]["scoreTotal"],
        "mobileHero": report["mobile"]["hero"],
        "mobileScore": report["mobile"]["scoreTotal"],
        "desktopOverflow": unexpected_overflow(report["desktop"]),
        "mobileOverflow": unexpected_overflow(report["mobile"]),
        "mobileWidest": report["mobile"].get("widest"),
        "requestHosts": sorted({item["url"].split("/")[2] for item in requests if "://" in item["url"]}),
        "requestCount": len(requests),
    }
    (OUT / "review.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SB15.1 capture complete")


if __name__ == "__main__":
    main()
