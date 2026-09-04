"""P-004R live CASE-0001: rebuild result bundle, analyze, screenshot Life Consulting."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
PORTAL = REPO / "applications" / "customer_portal"
OUT = REPO / "docs" / "reports" / "p004r_life_consulting"
SHOTS = OUT / "screenshots"
BUNDLE = PORTAL / "static" / "dist" / "result.js"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _kill_port(port: int) -> None:
    if os.name == "nt":
        lookup = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            check=False,
        )
        pids: set[str] = set()
        for line in lookup.stdout.splitlines():
            if f":{port} " not in line or "LISTENING" not in line.upper():
                continue
            pid = line.split()[-1]
            if pid.isdigit() and pid != "0":
                pids.add(pid)
        for pid in pids:
            subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True, check=False)
    else:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True, check=False)
    deadline = time.time() + 5
    while time.time() < deadline and _listening(port):
        time.sleep(0.2)


def _spawn(module: str, port: int) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env["BTE_API_BASE_URL"] = f"http://127.0.0.1:{API_PORT}"
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            module,
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=str(REPO),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _wait(port: int, timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _build_result() -> dict[str, str]:
    before = BUNDLE.stat().st_mtime if BUNDLE.exists() else 0.0
    npm = "npm.cmd" if os.name == "nt" else "npm"
    subprocess.run([npm, "run", "build:result"], cwd=str(PORTAL), check=True)
    after = BUNDLE.stat().st_mtime
    if after <= before:
        raise RuntimeError("result.js timestamp did not change after build:result")
    return {
        "path": str(BUNDLE),
        "mtime_before": str(before),
        "mtime_after": str(after),
        "size": str(BUNDLE.stat().st_size),
    }


def _shot_element(page, selector: str, path: Path) -> None:
    locator = page.locator(selector).first
    locator.wait_for()
    locator.screenshot(path=str(path))


def _audit_payload(data: dict) -> dict:
    identity = (data.get("identity") or {}).get("person") or {}
    ten = data.get("ten_gods") or {}
    luck = data.get("luck") or {}
    current = luck.get("current_cycle") or {}
    temperature = data.get("temperature") or {}
    five = data.get("five_elements") or {}
    useful = data.get("useful_god") or {}
    bazi = data.get("bazi") or {}
    pattern = data.get("pattern") or {}
    strength = data.get("strength") or {}
    shensha = bazi.get("shensha_matches") or bazi.get("shensha") or data.get("shensha")
    return {
        "gender": identity.get("gender") or bazi.get("gender"),
        "visible_ten_gods": ten.get("visible_labels") or ten.get("visible"),
        "hidden_ten_gods": ten.get("hidden_labels") or ten.get("hidden"),
        "pattern": pattern.get("cach_cuc") or pattern.get("pattern"),
        "strength": strength.get("strength_level"),
        "useful_god": useful.get("useful_display"),
        "current_luck": current.get("gan_zhi"),
        "five_elements_status": five.get("status"),
        "temperature": temperature.get("climate_state_label") or temperature.get("climate_state"),
        "shensha": shensha,
        "calendar_rule_version": (data.get("calendar") or {}).get("calendar_rule_version"),
        "has_life_keys": {
            "identity": "identity" in data,
            "ten_gods": "ten_gods" in data,
            "pattern": "pattern" in data,
            "strength": "strength" in data,
            "useful_god": "useful_god" in data,
            "luck": "luck" in data,
            "five_elements": "five_elements" in data,
            "temperature": "temperature" in data,
        },
    }


def main() -> None:
    """Rebuild production /result bundle and capture live CASE-0001 Life Consulting."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    bundle = _build_result()
    (OUT / "bundle_verify.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1800})
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            page.fill("#full_name", "Nguyễn Tiến Sơn")
            page.check("#gender_male")
            page.fill("#birth_date", "1987-01-21")
            page.fill("#birth_time", "04:30")
            page.fill("#birth_place", "Hà Tây, Việt Nam")
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=180000)
            page.wait_for_selector('[data-dashboard="commercial-v1"]')
            page.wait_for_selector("[data-life-consulting]", timeout=30000)
            stored = page.evaluate(
                """() => {
                  const store = window.BtePortal && window.BtePortal.ResultStore;
                  const rec = store && (store.loadCurrent ? store.loadCurrent() : store.load());
                  return rec && rec.data ? rec.data : null;
                }"""
            )
            audit = _audit_payload(stored if isinstance(stored, dict) else {})
            domains = page.locator("[data-life-domain]").evaluate_all(
                "nodes => nodes.map(node => node.getAttribute('data-life-domain'))"
            )
            audit["rendered_domains"] = domains
            (OUT / "live_payload_audit.json").write_text(
                json.dumps(audit, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            page.screenshot(path=str(SHOTS / "01_live_full.png"), full_page=True)
            _shot_element(page, "[data-life-consulting]", SHOTS / "02_life_consulting_section.png")
            _shot_element(page, '[data-life-domain="marriage"]', SHOTS / "03_marriage.png")
            _shot_element(page, '[data-life-domain="career"]', SHOTS / "04_career.png")
            _shot_element(page, '[data-life-domain="finance"]', SHOTS / "05_finance.png")
            page.set_viewport_size({"width": 390, "height": 1800})
            page.wait_for_timeout(400)
            page.wait_for_selector("[data-life-consulting]", timeout=10000)
            page.screenshot(path=str(SHOTS / "06_mobile.png"), full_page=True)
            browser.close()
    finally:
        for proc in (portal_proc, api_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
