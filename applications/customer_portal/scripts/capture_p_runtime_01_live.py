"""P-RUNTIME-01 live /result proof: Analyze → ResultStore → browser DOM + screenshots."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
PORTAL = REPO / "applications" / "customer_portal"
OUT = REPO / "docs" / "reports" / "p_runtime_01"
SHOTS = OUT / "screenshots"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
API = f"http://127.0.0.1:{API_PORT}"
CACHE = "PRUNTIME01"

CASE_0001 = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
    "full_name": "Nguyễn Tiến Sơn",
    "birth_place": "Hà Tây, Việt Nam",
    "timezone": "Asia/Ho_Chi_Minh",
}


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
    deadline = time.time() + 8
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


def _build_result() -> None:
    npm = "npm.cmd" if os.name == "nt" else "npm"
    result = subprocess.run(
        [npm, "run", "build:result"],
        cwd=str(PORTAL),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "vite build failed")


def _analyze_case_0001() -> dict[str, object]:
    body = json.dumps(CASE_0001).encode("utf-8")
    request = urllib.request.Request(
        f"{API}/api/v1/analyze",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def _unwrap(payload: dict[str, object]) -> dict[str, object]:
    data = payload.get("data")
    if isinstance(data, dict):
        return data
    return payload


def _http_headers(path: str) -> dict[str, str]:
    request = urllib.request.Request(f"{BASE}{path}", method="HEAD")
    with urllib.request.urlopen(request, timeout=20) as response:
        return {key.lower(): value for key, value in response.headers.items()}


def _shot(page, selector: str, path: Path) -> None:
    locator = page.locator(selector).first
    locator.wait_for()
    locator.screenshot(path=str(path))


def _fill_case_0001(page) -> None:
    page.fill("#full_name", CASE_0001["full_name"])
    page.check("#gender_male")
    page.fill("#birth_date", "1987-01-21")
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", CASE_0001["birth_place"])


def _payload_matrix(data: dict[str, object]) -> dict[str, object]:
    bazi = data.get("bazi") if isinstance(data.get("bazi"), dict) else {}
    strength = data.get("strength") if isinstance(data.get("strength"), dict) else {}
    pattern = data.get("pattern") if isinstance(data.get("pattern"), dict) else {}
    useful = data.get("useful_god") if isinstance(data.get("useful_god"), dict) else {}
    ten_gods = data.get("ten_gods") if isinstance(data.get("ten_gods"), dict) else {}
    luck = data.get("luck") if isinstance(data.get("luck"), dict) else {}
    five = data.get("five_elements") if isinstance(data.get("five_elements"), dict) else {}
    temp = data.get("temperature") if isinstance(data.get("temperature"), dict) else {}
    calendar = data.get("calendar") if isinstance(data.get("calendar"), dict) else {}
    return {
        "bazi.day_master": bazi.get("day_master"),
        "bazi.day_master_element": bazi.get("day_master_element"),
        "strength.strength_level": strength.get("strength_level"),
        "pattern.cach_cuc": pattern.get("cach_cuc"),
        "useful_god.useful_display": useful.get("useful_display"),
        "useful_god.favorable_display": useful.get("favorable_display"),
        "useful_god.unfavorable_display": useful.get("unfavorable_display"),
        "ten_gods.visible": bool(ten_gods.get("visible") or ten_gods.get("visible_labels")),
        "ten_gods.hidden": bool(ten_gods.get("hidden") or ten_gods.get("hidden_labels")),
        "shensha": bool(data.get("shensha") or data.get("shen_sha")),
        "luck": bool(luck),
        "five_elements": bool(five),
        "temperature": bool(temp),
        "NarrativeV2Presentation": bool(data.get("narrative_v2_shadow")),
        "calendar.calendar_rule_version": calendar.get("calendar_rule_version"),
        "useful_god_source.contract": (data.get("useful_god_source") or {}).get("contract")
        if isinstance(data.get("useful_god_source"), dict)
        else None,
    }


def main() -> None:
    """Rebuild, restart, Analyze CASE-0001, prove live /result DOM, capture screenshots."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    _build_result()
    dist_js = PORTAL / "static" / "dist" / "result.js"
    dist_css = PORTAL / "static" / "dist" / "result.css"
    if not dist_js.is_file() or not dist_css.is_file():
        raise RuntimeError("production result bundle missing after build")
    bundle_js = dist_js.read_text(encoding="utf-8", errors="ignore")
    if "data-life-consulting" not in bundle_js or "data-overview-section" not in bundle_js:
        raise RuntimeError("result.js does not contain P-001/P-004 production markers")
    if "data-tg-combination" not in bundle_js:
        raise RuntimeError("result.js does not contain P-003B production markers")

    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        payload = _analyze_case_0001()
        data = _unwrap(payload)
        matrix = _payload_matrix(data)
        (OUT / "live_payload_matrix.json").write_text(
            json.dumps(matrix, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        js_stat = dist_js.stat()
        css_stat = dist_css.stat()
        js_headers = _http_headers(f"/static/dist/result.js?v={CACHE}")
        css_headers = _http_headers(f"/static/dist/result.css?v={CACHE}")
        html = urllib.request.urlopen(f"{BASE}/result", timeout=20).read().decode("utf-8")
        bundle_audit = {
            "result_js_mtime": js_stat.st_mtime,
            "result_css_mtime": css_stat.st_mtime,
            "result_js_size": js_stat.st_size,
            "result_css_size": css_stat.st_size,
            "result_js_last_modified": js_headers.get("last-modified"),
            "result_css_last_modified": css_headers.get("last-modified"),
            "cache_bust": CACHE,
            "html_js_src": f"/static/dist/result.js?v={CACHE}" in html,
            "html_css_href": f"/static/dist/result.css?v={CACHE}" in html,
            "bundle_has_p001": "data-overview-section" in bundle_js and "Dụng Thần" in bundle_js,
            "bundle_has_p003": "data-tg-commercial" in bundle_js,
            "bundle_has_p003b": "data-tg-combination" in bundle_js,
            "bundle_has_p004": "data-life-consulting" in bundle_js,
        }
        (OUT / "bundle_audit.json").write_text(
            json.dumps(bundle_audit, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(viewport={"width": 1440, "height": 1100})
            page = context.new_page()
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            _fill_case_0001(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector("[data-dashboard='commercial-v1']")
            page.wait_for_selector('[data-card="overview"]')
            page.wait_for_selector("[data-life-consulting]")
            page.wait_for_selector("[data-tg-combination]")
            page.wait_for_selector('[data-evidence="useful-god"]')

            proof = page.evaluate(
                """() => {
                  const overview = document.querySelector('[data-card="overview"]');
                  const titles = [...document.querySelectorAll('.bte-id__region-label, .bte-id__cx-detail-title')]
                    .map((node) => (node.textContent || '').trim())
                    .filter((text) => text === 'Cân Xương Đoán Mệnh');
                  const asset = [...document.querySelectorAll('script[src], link[href]')]
                    .map((node) => node.getAttribute('src') || node.getAttribute('href') || '')
                    .filter((value) => value.includes('/static/dist/result.'));
                  const stored = sessionStorage.getItem('bte_last_result');
                  return {
                    facts: [...(overview?.querySelectorAll('[data-evidence]') || [])].map((node) => ({
                      key: node.getAttribute('data-evidence'),
                      text: (node.textContent || '').trim(),
                    })),
                    insight: overview?.querySelector('[data-overview-section="insight"]')?.textContent || '',
                    commercial: [...document.querySelectorAll('[data-tg-commercial]')].map((node) => node.getAttribute('data-tg-commercial')),
                    combination: document.querySelector('[data-tg-combination]')?.textContent?.slice(0, 240) || '',
                    lifeDomains: [...document.querySelectorAll('[data-life-domain]')].map((node) => node.getAttribute('data-life-domain')),
                    canXuongTitles: titles,
                    canXuongDetailModules: document.querySelectorAll('[data-module="bone-weight-detail"]').length,
                    bottomCanXuong: Boolean(document.querySelector('.bte-cdash > .bte-id__cx-detail')),
                    assets: asset,
                    stored: Boolean(stored),
                    pack05: document.querySelector('[data-narrative-provider="pack05"]') != null,
                    provider: document.querySelector('[data-narrative-surface]')?.getAttribute('data-narrative-provider') || '',
                  };
                }"""
            )
            if not proof["facts"]:
                raise RuntimeError("P-001 executive facts missing on live /result")
            if not any(item["key"] == "useful-god" for item in proof["facts"]):
                raise RuntimeError("P-001 Dụng Thần missing on live /result")
            if not proof["commercial"]:
                raise RuntimeError("P-003 commercial cards missing on live /result")
            if not proof["combination"]:
                raise RuntimeError("P-003B combination missing on live /result")
            if not proof["lifeDomains"]:
                raise RuntimeError("P-004 Life Consulting missing on live /result")
            if proof["canXuongTitles"] != ["Cân Xương Đoán Mệnh"] or proof["bottomCanXuong"]:
                raise RuntimeError("P-002 duplicate Cân Xương still present")
            if proof["pack05"]:
                raise RuntimeError("Pack05 leaked onto production /result")
            (OUT / "live_dom_proof.json").write_text(
                json.dumps(proof, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            page.screenshot(path=str(SHOTS / "01_live_result_top.png"), full_page=False)
            _shot(page, '[data-card="overview"]', SHOTS / "02_p001_executive_summary.png")
            page.locator('[data-card="ten-gods"]').first.scroll_into_view_if_needed()
            _shot(page, '[data-card="ten-gods"]', SHOTS / "03_p003_ten_gods_commercial.png")
            _shot(page, "[data-tg-combination]", SHOTS / "04_p003b_combination.png")
            page.locator("[data-life-consulting]").first.scroll_into_view_if_needed()
            _shot(page, "[data-life-consulting]", SHOTS / "05_p004_life_consulting.png")
            page.locator("[data-identity-header='true']").first.scroll_into_view_if_needed()
            page.screenshot(path=str(SHOTS / "06_can_xuong_no_duplicate.png"), full_page=True)
            page.screenshot(path=str(SHOTS / "07_live_result_full.png"), full_page=True)

            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(400)
            page.locator('[data-card="overview"]').first.scroll_into_view_if_needed()
            page.screenshot(path=str(SHOTS / "08_mobile_live_result.png"), full_page=True)
            mobile = page.evaluate(
                """() => ({
                  facts: Boolean(document.querySelector('[data-overview-section="facts"]')),
                  commercial: Boolean(document.querySelector('[data-tg-section="commercial"]')),
                  combination: Boolean(document.querySelector('[data-tg-combination]')),
                  life: Boolean(document.querySelector('[data-life-consulting]')),
                })"""
            )
            if not all(mobile.values()):
                raise RuntimeError(f"mobile is missing Product Ticket surfaces: {mobile}")
            browser.close()
    finally:
        for proc in (portal_proc, api_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
