"""GD-CAL-01 live /good-date screenshots, runtime restore, and health check.

Canonical runtime:
  uvicorn applications.api.app:app --host 127.0.0.1 --port 8000
  uvicorn applications.customer_portal.app:app --host 127.0.0.1 --port 8081

Leave the stack running after restore. Do not kill 8081 on success.
"""

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

from playwright.sync_api import Page, sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "date_selection" / "screenshots" / "gd_cal_01b"
LOG_DIR = REPO / "runtime" / "logs"
API_PORT = 8000
PORTAL_PORT = 8081
API_BASE = f"http://127.0.0.1:{API_PORT}"
PORTAL_BASE = f"http://127.0.0.1:{PORTAL_PORT}"
JS_MARKERS = (
    "date_selection.lunar_month_ganzhi",
    "Can Chi tháng âm",
    "date_selection.can_chi_day_title",
    "CAN CHI NGÀY",
    "good_date_identity",
)
FORBIDDEN_JS = (
    "date_selection.tu_tru_month_note",
    "Trụ tháng theo tiết khí",
)
VENV_PY = REPO / ".venv" / "Scripts" / "python.exe"


def _python() -> str:
    return str(VENV_PY) if VENV_PY.exists() else sys.executable


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _http(url: str, method: str = "GET", body: bytes | None = None, timeout: float = 20.0):
    headers = {"Accept": "application/json, text/html;q=0.9,*/*;q=0.8"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


def _spawn(module: str, port: int, log_name: str) -> subprocess.Popen[bytes] | None:
    """Start uvicorn as an independent OS process that survives this script."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stdout_path = LOG_DIR / log_name
    stderr_path = LOG_DIR / log_name.replace(".log", ".err.log")
    for path in (stdout_path, stderr_path):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            pass
    python = _python()
    args = f"-m uvicorn {module} --host 127.0.0.1 --port {port} --log-level info"
    if os.name == "nt":
        command = (
            "$env:BTE_API_BASE_URL = "
            + json.dumps(API_BASE)
            + "; Start-Process -FilePath "
            + json.dumps(python)
            + " -ArgumentList "
            + json.dumps(args)
            + " -WorkingDirectory "
            + json.dumps(str(REPO))
            + " -WindowStyle Hidden"
            + " -RedirectStandardOutput "
            + json.dumps(str(stdout_path))
            + " -RedirectStandardError "
            + json.dumps(str(stderr_path))
        )
        env = os.environ.copy()
        env["BTE_API_BASE_URL"] = API_BASE
        return subprocess.Popen(
            ["powershell", "-NoProfile", "-Command", command],
            cwd=str(REPO),
            env=env,
        )
    log_handle = stdout_path.open("ab")
    env = os.environ.copy()
    env["BTE_API_BASE_URL"] = API_BASE
    return subprocess.Popen(
        [python, "-m", "uvicorn", module, "--host", "127.0.0.1", "--port", str(port), "--log-level", "info"],
        cwd=str(REPO),
        env=env,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


def _wait(port: int, timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def ensure_runtime() -> dict[str, object]:
    """Start API then Customer Portal if they are not already listening."""
    started = {"api": False, "portal": False}
    if not _listening(API_PORT):
        _spawn("applications.api.app:app", API_PORT, "api.log")
        started["api"] = True
    _wait(API_PORT)
    if not _listening(PORTAL_PORT):
        _spawn("applications.customer_portal.app:app", PORTAL_PORT, "customer_portal.log")
        started["portal"] = True
    _wait(PORTAL_PORT)
    return started


def health_check() -> dict[str, object]:
    """Lightweight proof that 8081 serves the GD-CAL-01 portal + API."""
    report: dict[str, object] = {
        "tcp_8000": _listening(API_PORT),
        "tcp_8081": _listening(PORTAL_PORT),
    }
    if not report["tcp_8081"]:
        raise RuntimeError("TCP 8081 is not listening")
    root_status, _, _ = _http(f"{PORTAL_BASE}/")
    good_status, good_headers, good_body = _http(f"{PORTAL_BASE}/good-date")
    js_status, js_headers, js_body = _http(f"{PORTAL_BASE}/static/js/date_selection.js")
    html = good_body.decode("utf-8", errors="replace")
    js = js_body.decode("utf-8", errors="replace")
    missing = [marker for marker in JS_MARKERS if marker not in js]
    leftover = [marker for marker in FORBIDDEN_JS if marker in js]
    if good_status != 200:
        raise RuntimeError(f"/good-date HTTP {good_status}")
    if js_status != 200:
        raise RuntimeError(f"date_selection.js HTTP {js_status}")
    if "/static/js/date_selection.js" not in html:
        raise RuntimeError("good-date HTML does not load /static/js/date_selection.js")
    if "dsTuTruNote" in html:
        raise RuntimeError("good-date HTML still has dsTuTruNote caption")
    if 'id="dsTuTru"' not in html:
        raise RuntimeError("good-date HTML missing dsTuTru")
    if missing:
        raise RuntimeError(f"served JS missing GD-CAL-01B markers: {missing}")
    if leftover:
        raise RuntimeError(f"served JS still has removed caption: {leftover}")
    day_status, _, day_body = _http(
        f"{PORTAL_BASE}/backend/api/v1/date-selection/day",
        method="POST",
        body=json.dumps({"year": 2026, "month": 9, "day": 7}).encode("utf-8"),
    )
    if day_status != 200:
        raise RuntimeError(f"date-selection/day HTTP {day_status}: {day_body[:400]!r}")
    payload = json.loads(day_body.decode("utf-8"))
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        raise RuntimeError("date-selection/day missing data")
    calendar = data.get("calendar") if isinstance(data.get("calendar"), dict) else {}
    identity = data.get("good_date_identity") if isinstance(data.get("good_date_identity"), dict) else {}
    if calendar.get("lunar_month_can_chi") != "Bính Thân":
        raise RuntimeError(f"live API lunar month Can Chi: {calendar.get('lunar_month_can_chi')!r}")
    if identity.get("month_can_chi") != calendar.get("lunar_month_can_chi"):
        raise RuntimeError("live API good_date_identity.month_can_chi != lunar_month_can_chi")
    report.update(
        {
            "get_root_status": root_status,
            "get_good_date_status": good_status,
            "js_status": js_status,
            "js_cache_control": js_headers.get("Cache-Control") or js_headers.get("cache-control"),
            "js_last_modified": js_headers.get("Last-Modified") or js_headers.get("last-modified"),
            "js_content_length": js_headers.get("Content-Length") or js_headers.get("content-length"),
            "js_markers": list(JS_MARKERS),
            "html_static_js": "/static/js/date_selection.js",
            "day_api_status": day_status,
            "day_lunar_month_can_chi": calendar.get("lunar_month_can_chi"),
            "day_visible_month_can_chi": identity.get("month_can_chi"),
            "day_lunar_label": calendar.get("lunar_label"),
            "day_bazi_month_pillar": (data.get("bazi") or {}).get("month_pillar"),
            "day_six_state": (data.get("six_state") or {}).get("label"),
        }
    )
    return report


def _goto_month(page: Page, year: int, month: int) -> None:
    target = f"Tháng {month}/{year}"
    for _ in range(24):
        title = page.locator("#dsCalTitle").inner_text().strip()
        if title == target:
            return
        current_month = int(title.split()[1].split("/")[0])
        current_year = int(title.split("/")[1])
        current = current_year * 12 + current_month
        wanted = year * 12 + month
        page.click("#dsNext" if wanted > current else "#dsPrev")
        page.wait_for_function(
            """(expected) => document.getElementById('dsCalTitle')?.textContent?.trim() !== expected""",
            arg=title,
        )
    raise RuntimeError(f"could not reach {target}")


def _select_day(page: Page, day: int, month: int, year: int, lunar_month: str, result: str | None = None) -> None:
    solar = f"{day:02d}/{month:02d}/{year:04d}"
    page.locator(f'#dsCalendar [data-day="{day}"]').click()
    page.wait_for_function(
        """({solar, lunar, result}) => {
          const text = document.getElementById('dsDetail')?.textContent || '';
          if (!text.includes(solar) || !text.includes('Can Chi tháng âm') || !text.includes(lunar)) {
            return false;
          }
          return !result || text.includes(result);
        }""",
        arg={"solar": solar, "lunar": lunar_month, "result": result or ""},
    )


def _panel(page: Page) -> dict[str, str]:
    def kv(label: str) -> str:
        return page.evaluate(
            """(label) => {
              const dts = [...document.querySelectorAll('#dsDetail dt')];
              const dt = dts.find((el) => (el.textContent || '').trim() === label);
              return dt && dt.nextElementSibling ? (dt.nextElementSibling.textContent || '').trim() : '';
            }""",
            label,
        )

    caption = ""
    if page.locator("#dsTuTruNote").count():
        caption = page.locator("#dsTuTruNote").inner_text().strip()
    return {
        "solar": kv("Ngày dương"),
        "lunar": kv("Ngày âm"),
        "lunar_year": kv("Can Chi năm âm"),
        "lunar_month": kv("Can Chi tháng âm"),
        "day_ganzhi": kv("Can Chi ngày"),
        "result": kv("Kết quả ngày"),
        "title": page.locator('[data-testid="tu-tru-panel"] .bte-tu-tru__title').inner_text().strip(),
        "tu_tru_month": page.locator('[data-testid="tu-tru-panel"] [data-pillar="month"] .bte-tu-tru__can-chi').inner_text().strip(),
        "caption": caption,
    }


def _assert_case(got: dict[str, str], expected: dict[str, str], label: str) -> None:
    for key, value in expected.items():
        actual = got.get(key, "")
        if value.casefold() not in actual.casefold():
            raise RuntimeError(f"{label} {key}: expected {value!r} in {actual!r}")
    if got.get("caption"):
        raise RuntimeError(f"{label} caption must be hidden, got {got['caption']!r}")
    if got["tu_tru_month"].casefold() != got["lunar_month"].casefold():
        raise RuntimeError(
            f"{label} UI inequality: Tháng {got['tu_tru_month']!r} != Can Chi tháng âm {got['lunar_month']!r}"
        )


CASES = (
    {
        "year": 2026,
        "month": 9,
        "day": 6,
        "lunar": "25/07/2026",
        "lunar_month": "Bính Thân",
        "stem": "sep6",
        "files": ("01_sep_06_2026_full.png", "02_sep_06_2026_detail.png"),
    },
    {
        "year": 2026,
        "month": 9,
        "day": 7,
        "lunar": "26/07/2026",
        "lunar_month": "Bính Thân",
        "stem": "sep7",
        "files": ("03_sep_07_2026_full.png", "04_sep_07_2026_detail.png"),
    },
    {
        "year": 2026,
        "month": 10,
        "day": 7,
        "lunar": "27/08/2026",
        "lunar_month": "Đinh Dậu",
        "result": "Không Vong",
        "stem": "oct7",
        "files": ("05_oct_07_2026_full.png", "06_oct_07_2026_detail.png"),
    },
    {
        "year": 2026,
        "month": 10,
        "day": 8,
        "lunar": "28/08/2026",
        "lunar_month": "Đinh Dậu",
        "result": "Đại An",
        "stem": "oct8",
        "files": ("07_oct_08_2026_full.png", "08_oct_08_2026_detail.png"),
    },
    {
        "year": 2026,
        "month": 11,
        "day": 6,
        "lunar": "28/09/2026",
        "lunar_month": "Mậu Tuất",
        "result": "Lưu Niên",
        "stem": "nov6",
        "files": ("09_nov_06_2026_full.png", "10_nov_06_2026_detail.png"),
    },
    {
        "year": 2026,
        "month": 11,
        "day": 7,
        "lunar": "29/09/2026",
        "lunar_month": "Mậu Tuất",
        "result": "Tốc Hỷ",
        "stem": "nov7",
        "files": ("11_nov_07_2026_full.png", "12_nov_07_2026_detail.png"),
    },
)


def verify_and_capture() -> dict[str, str]:
    OUT.mkdir(parents=True, exist_ok=True)
    shots: dict[str, str] = {}
    live: dict[str, str] = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto(f"{PORTAL_BASE}/good-date", wait_until="networkidle")
        page.wait_for_selector("#dsCalendar .ds-day[data-day]")
        current_month = None
        for case in CASES:
            year, month, day = case["year"], case["month"], case["day"]
            if current_month != (year, month):
                _goto_month(page, year, month)
                current_month = (year, month)
            _select_day(page, day, month, year, case["lunar_month"], case.get("result"))
            got = _panel(page)
            expected = {
                "solar": f"{day:02d}/{month:02d}/{year:04d}",
                "lunar": case["lunar"],
                "lunar_month": case["lunar_month"],
                "tu_tru_month": case["lunar_month"],
                "title": "CAN CHI NGÀY",
            }
            if case.get("result"):
                expected["result"] = case["result"]
            _assert_case(got, expected, f"{day:02d}/{month:02d}/{year:04d}")
            full_name, detail_name = case["files"]
            page.screenshot(path=str(OUT / full_name), full_page=True)
            page.locator(".ds-detail").screenshot(path=str(OUT / detail_name))
            shots[f"{case['stem']}_full"] = str(OUT / full_name)
            shots[f"{case['stem']}_detail"] = str(OUT / detail_name)
            live[case["stem"]] = json.dumps(got, ensure_ascii=False)
        browser.close()
    return {**live, **shots}


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "restore"
    if mode == "--health":
        report = health_check()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    started = ensure_runtime()
    health = health_check()
    live = verify_and_capture()
    proof = {
        "started": started,
        "health": health,
        "live": live,
        "left_running": f"{PORTAL_BASE}/good-date",
    }
    print(json.dumps(proof, ensure_ascii=False, indent=2))
    print(f"Servers left running at {PORTAL_BASE}/good-date")


if __name__ == "__main__":
    main()
