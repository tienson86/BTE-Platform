"""Capture N-IMP-10 production vs Narrative V2 shadow screenshots."""

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
OUT = REPO / "implementation" / "narrative_v2" / "n_imp_10"
PRESENTATION = (
    REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
)
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


def _wait(port: int, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _store_payload() -> dict[str, object]:
    presentation = json.loads(PRESENTATION.read_text(encoding="utf-8"))
    return {
        "analysis_id": "ana-nimp10-0001",
        "input": {
            "year": 1987,
            "month": 1,
            "day": 21,
            "hour": 4,
            "minute": 30,
            "gender": "male",
            "full_name": "Nguyễn Tiến Sơn",
            "timezone": "Asia/Bangkok",
        },
        "data": {
            "analysis_id": "ana-nimp10-0001",
            "identity": {
                "person": {
                    "full_name": "Nguyễn Tiến Sơn",
                    "gender": "male",
                    "solar_birth": "1987-01-21",
                    "lunar_birth": "1986-12-22",
                    "birth_time": "04:30",
                    "birth_place": "Hà Tây, Việt Nam",
                },
                "calendar": {"solar_term": "Đại Hàn"},
                "four_pillars": {
                    "year": {"stem": "Bính", "branch": "Dần", "can_chi": "Bính Dần", "nayin_element": "Hỏa"},
                    "month": {"stem": "Tân", "branch": "Sửu", "can_chi": "Tân Sửu", "nayin_element": "Thổ"},
                    "day": {"stem": "Canh", "branch": "Ngọ", "can_chi": "Canh Ngọ", "nayin_element": "Thổ"},
                    "hour": {"stem": "Mậu", "branch": "Dần", "can_chi": "Mậu Dần", "nayin_element": "Thổ"},
                },
            },
            "bazi": {
                "day_master": "Canh",
                "day_master_element": "Kim",
                "year_pillar": {"stem": "Bính", "branch": "Dần", "nap_am": "Lư Trung Hỏa"},
                "month_pillar": {"stem": "Tân", "branch": "Sửu", "nap_am": "Bích Thượng Thổ"},
                "day_pillar": {"stem": "Canh", "branch": "Ngọ", "nap_am": "Lộ Bàng Thổ"},
                "hour_pillar": {"stem": "Mậu", "branch": "Dần", "nap_am": "Thành Đầu Thổ"},
            },
            "calendar": {
                "solar_term": {"name": "Đại Hàn"},
                "calendar_rule_version": "G1-10C",
            },
            "useful_god_source": {"contract": "analysis_result.UsefulGodView@1.5"},
            "useful_god": {"useful_display": "Thổ · Canh · Tỷ Kiên"},
            "result_meta": {
                "analysis_id": "ana-nimp10-0001",
                "customer_contract": "analysis_result.UsefulGodView@1.5",
                "release_label": "BTE V1.0",
            },
            "score": {"confidence": "high"},
            "narrative_result": {
                "contract": "pack05_narrative_result_v1",
                "status": "ok",
                "summary": {
                    "identity": "Pack05 identity",
                    "priority_recommendation": "Pack05 priority",
                },
            },
            "narrative_v2_shadow": {
                "status": "ok",
                "portal_connection": "true_shadow",
                "replaces_pack05": False,
                "presentation": presentation,
                "error": None,
            },
        },
    }


def _inject_store(page, payload: dict[str, object]) -> None:
    raw = json.dumps(payload, ensure_ascii=False)
    page.add_init_script(
        f"() => {{ sessionStorage.setItem('bte_last_result', {json.dumps(raw)}); }}"
    )


def main() -> None:
    """Capture production /result and Narrative V2 shadow review screenshots."""
    OUT.mkdir(parents=True, exist_ok=True)
    payload = _store_payload()
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            desktop = browser.new_page(viewport={"width": 1440, "height": 1100})
            _inject_store(desktop, payload)

            desktop.goto(f"{BASE}/result", wait_until="networkidle")
            desktop.wait_for_selector('[data-dashboard="commercial-v1"]')
            desktop.screenshot(path=str(OUT / "01_production_result_unchanged.png"), full_page=True)

            desktop.goto(f"{BASE}/result?narrative=v2-shadow", wait_until="networkidle")
            desktop.wait_for_selector("[data-narrative-v2-shadow='true']")
            desktop.screenshot(path=str(OUT / "02_narrative_v2_shadow_full.png"), full_page=True)
            desktop.locator("[data-v2-overview]").screenshot(path=str(OUT / "03_narrative_v2_shadow_overview.png"))
            desktop.locator("[data-v2-structured]").evaluate("node => node.open = true")
            desktop.locator("[data-v2-interpretation]").screenshot(
                path=str(OUT / "04_narrative_v2_shadow_interpretation.png")
            )
            desktop.locator("[data-v2-action]").screenshot(path=str(OUT / "05_narrative_v2_shadow_action.png"))

            desktop.goto(f"{BASE}/result?narrative=v2-compare", wait_until="networkidle")
            desktop.wait_for_selector("[data-v2-compare]")
            desktop.screenshot(path=str(OUT / "06_production_vs_v2_comparison.png"), full_page=True)

            mobile = browser.new_page(viewport={"width": 390, "height": 844})
            _inject_store(mobile, payload)
            mobile.goto(f"{BASE}/result?narrative=v2-shadow", wait_until="networkidle")
            mobile.wait_for_selector("[data-narrative-v2-shadow='true']")
            mobile.screenshot(path=str(OUT / "07_mobile_shadow.png"), full_page=True)
            browser.close()
    finally:
        api_proc.terminate()
        portal_proc.terminate()


if __name__ == "__main__":
    main()
