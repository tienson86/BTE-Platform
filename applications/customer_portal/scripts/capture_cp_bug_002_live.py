"""CP-BUG-002 live /result proof: Tứ Trụ Year Cung Phi and Technical Information."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
PORTAL = REPO / "applications" / "customer_portal"
OUT = REPO / "implementation" / "bugfixes"
SHOTS = OUT / "screenshots"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"
API = f"http://127.0.0.1:{API_PORT}"

CASE = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
    "full_name": "Nguyễn Tiến Sơn",
    "birth_place": "Hà Nội",
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


def _post(path: str, payload: dict[str, object], timeout: float = 120.0) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{API}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _unwrap(payload: dict[str, object]) -> dict[str, object]:
    data = payload.get("data")
    if isinstance(data, dict):
        return data
    return payload


def _fill_case(page) -> None:
    page.fill("#full_name", CASE["full_name"])
    page.check("#gender_male")
    page.fill("#birth_date", "1987-01-21")
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", CASE["birth_place"])


def main() -> None:
    """Rebuild, restart, fresh analyze, screenshot Tứ Trụ + Technical Information."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    _build_result()
    dist_js = PORTAL / "static" / "dist" / "result.js"
    if not dist_js.is_file():
        raise RuntimeError("production result bundle missing after build")
    bundle = dist_js.read_text(encoding="utf-8", errors="ignore")
    if "Hành Cung" not in bundle:
        raise RuntimeError("result.js does not contain Hành Cung")

    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    proof: dict[str, object] = {}
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        analyzed = _unwrap(_post("/api/v1/analyze", CASE))
        calendar = analyzed.get("calendar") if isinstance(analyzed.get("calendar"), dict) else {}
        bazi = analyzed.get("bazi") if isinstance(analyzed.get("bazi"), dict) else {}
        year_pillar = bazi.get("year_pillar") if isinstance(bazi.get("year_pillar"), dict) else {}
        routing = calendar.get("ganzhi_routing") if isinstance(calendar.get("ganzhi_routing"), dict) else {}
        year_route = routing.get("year") if isinstance(routing.get("year"), dict) else {}
        feng = analyzed.get("feng_shui") if isinstance(analyzed.get("feng_shui"), dict) else {}
        search = _unwrap(
            _post(
                "/api/v1/date-selection/search",
                {
                    "full_name": CASE["full_name"],
                    "gender": CASE["gender"],
                    "birth_year": CASE["year"],
                    "birth_month": CASE["month"],
                    "birth_day": CASE["day"],
                    "target_year": 2026,
                    "target_month": 9,
                },
            )
        )
        person = search.get("person") if isinstance(search.get("person"), dict) else {}
        trach = person.get("trach") if isinstance(person.get("trach"), dict) else {}
        proof["api"] = {
            "analysis_id": analyzed.get("analysis_id") or analyzed.get("request_id"),
            "calendar.cung_phi": calendar.get("cung_phi"),
            "calendar.menh_quai": calendar.get("menh_quai"),
            "calendar.hanh_cung": calendar.get("hanh_cung"),
            "calendar.nhom_trach": calendar.get("nhom_trach"),
            "ganzhi_routing.year.cung_phi": year_route.get("cung_phi"),
            "bazi.year_pillar.cung_phi": year_pillar.get("cung_phi"),
            "feng_shui.gua_name": feng.get("gua_name") or feng.get("cung_phi"),
        }
        proof["date_selection"] = {
            "person.trach.cung": trach.get("cung") or person.get("cung_phi"),
            "person.trach.element_label": trach.get("element_label"),
            "person.trach.trach_group_label": trach.get("trach_group_label")
            or person.get("trach_group_label"),
        }
        expected = ("Khôn", "Thổ", "Tây Tứ Trạch")
        if (
            calendar.get("cung_phi"),
            calendar.get("hanh_cung"),
            calendar.get("nhom_trach"),
        ) != expected:
            raise RuntimeError(f"API personal Cung Phi mismatch: {proof['api']}")
        if (trach.get("cung") or person.get("cung_phi")) != "Khôn":
            raise RuntimeError(f"date-selection person mismatch: {proof['date_selection']}")

        shot_path = SHOTS / "CP-BUG-002_result_cung_phi_parity.png"
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(viewport={"width": 1440, "height": 1100})
            page = context.new_page()
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.wait_for_selector("#analyzeForm")
            _fill_case(page)
            page.click("#btnAnalyze")
            page.wait_for_url("**/result", timeout=120000)
            page.wait_for_selector("[data-identity-header='true']")
            page.wait_for_selector("[data-region='pillars']")
            page.wait_for_selector("[data-region='status']")
            header = page.locator("[data-identity-header='true']").first
            header.screenshot(path=str(shot_path))
            live = page.evaluate(
                """() => {
                  const year = document.querySelector('[data-region="pillars"] [data-pillar="year"]');
                  const status = document.querySelector('[data-region="status"]');
                  return {
                    yearText: year ? year.textContent || "" : "",
                    statusText: status ? status.textContent || "" : "",
                  };
                }"""
            )
            browser.close()
        proof["live_dom"] = live
        proof["screenshot"] = str(shot_path.relative_to(REPO)).replace("\\", "/")
        year_text = str(live.get("yearText") or "")
        status_text = str(live.get("statusText") or "")
        if "Khôn" not in year_text:
            raise RuntimeError(f"Tứ Trụ Year missing Khôn: {year_text}")
        if "Khôn" not in status_text or "Tốn" in status_text:
            raise RuntimeError(f"Technical Information mismatch: {status_text}")
        if "Thổ" not in status_text or "Tây Tứ Trạch" not in status_text:
            raise RuntimeError(f"Technical Information missing derived fields: {status_text}")
        (OUT / "CP-BUG-002_live_proof.json").write_text(
            json.dumps(proof, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(proof, ensure_ascii=False, indent=2))
        print("Servers left running at http://127.0.0.1:8081/result")
    except Exception:
        api_proc.terminate()
        portal_proc.terminate()
        raise


if __name__ == "__main__":
    main()
