"""P7-IMP-06 live proof: Shen Sha secondary evidence, /result THẦN SÁT, diagnostics."""

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
OUT = REPO / "implementation" / "pack_07"
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
    deadline = time.time() + 8
    while time.time() < deadline and _listening(port):
        time.sleep(0.2)


def _spawn(module: str, port: int) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env["BTE_API_BASE_URL"] = f"http://127.0.0.1:{API_PORT}"
    env.setdefault("BTE_ENV", "development")
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


def _get(path: str) -> tuple[int, object]:
    with urllib.request.urlopen(f"{API}{path}", timeout=20) as response:
        body = response.read().decode("utf-8")
        try:
            return response.status, json.loads(body)
        except json.JSONDecodeError:
            return response.status, body


def _post(path: str, payload: dict[str, object], timeout: float = 120.0) -> tuple[int, dict[str, object]]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{API}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def _fill(page) -> None:
    page.fill("#full_name", CASE["full_name"])
    page.check("#gender_male")
    page.fill("#birth_date", "1987-01-21")
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", CASE["birth_place"])


def _open_result(page) -> None:
    page.goto(f"{BASE}/analyze", wait_until="networkidle")
    page.wait_for_selector("#analyzeForm")
    _fill(page)
    page.click("#btnAnalyze")
    page.wait_for_url("**/result", timeout=120000)
    page.wait_for_selector("[data-dashboard='commercial-v1']")


def _build_result() -> None:
    npm = "npm.cmd" if os.name == "nt" else "npm"
    result = subprocess.run(
        [npm, "run", "build:result"],
        cwd=str(REPO / "applications" / "customer_portal"),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "vite build failed")


def main() -> None:
    """Restart runtime and capture Shen Sha live proof."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    _build_result()
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        health_status, health = _get("/api/v1/health")
        analyze_status, analyzed = _post("/api/v1/analyze", CASE)
        analyze_data = analyzed.get("data") if isinstance(analyzed, dict) else {}
        if not isinstance(analyze_data, dict):
            analyze_data = {}
        bazi = analyze_data.get("bazi") if isinstance(analyze_data.get("bazi"), dict) else {}
        matches = bazi.get("shensha_matches") if isinstance(bazi, dict) else []
        shen_sha = bazi.get("shen_sha") if isinstance(bazi, dict) else {}
        individual = shen_sha.get("individual") if isinstance(shen_sha, dict) else {}
        ecosystem = shen_sha.get("ecosystem") if isinstance(shen_sha, dict) else {}
        live_diag_status, live_diag = _post("/api/v1/dev/pack07/diagnostics", CASE)
        history_code = urllib.request.urlopen(f"{BASE}/history", timeout=20).status
        overview = SHOTS / "p7_imp_06_result_overview.png"
        desktop = SHOTS / "p7_imp_06_shen_sha_desktop.png"
        expanded = SHOTS / "p7_imp_06_shen_sha_expanded.png"
        eco_shot = SHOTS / "p7_imp_06_shen_sha_ecosystem.png"
        cluster_shot = SHOTS / "p7_imp_06_cluster_expanded.png"
        mobile = SHOTS / "p7_imp_06_shen_sha_mobile.png"
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            desk = browser.new_context(viewport={"width": 1440, "height": 1100})
            page = desk.new_page()
            _open_result(page)
            content = page.content() or ""
            if "TR-P7-" in content or "shen_sha_id" in content or "trace_ids" in content:
                raise RuntimeError("Pack 07 debug IDs leaked onto customer /result")
            page.screenshot(path=str(overview), full_page=False)
            card = page.locator("[data-card='shensha']")
            card.scroll_into_view_if_needed()
            page.wait_for_selector("[data-ss-pack07='true']")
            card.screenshot(path=str(desktop))
            star_toggle = page.locator("[data-ss-section='stars'] .bte-ss__star-toggle")
            if star_toggle.count():
                star_toggle.first.click()
                page.wait_for_timeout(400)
            page.locator("[data-ss-section='stars']").screenshot(path=str(expanded))
            page.wait_for_selector("[data-ss-section='ecosystem']")
            page.locator("[data-ss-section='ecosystem']").screenshot(path=str(eco_shot))
            cluster_toggle = page.locator("[data-ss-clusters] .bte-ss__star-toggle")
            if cluster_toggle.count():
                cluster_toggle.first.click()
                page.wait_for_timeout(400)
                page.locator("[data-ss-section='ecosystem']").screenshot(path=str(cluster_shot))
            else:
                page.locator("[data-ss-section='ecosystem']").screenshot(path=str(cluster_shot))
            phone = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = phone.new_page()
            _open_result(mobile_page)
            mobile_card = mobile_page.locator("[data-card='shensha']")
            mobile_card.scroll_into_view_if_needed()
            toggle = mobile_page.locator(
                "[data-card='shensha'] [data-mobile-toggle], [data-card='shensha'] .bte-mobile-toggle"
            )
            if toggle.count():
                toggle.first.click()
                mobile_page.wait_for_timeout(300)
            mobile_card.screenshot(path=str(mobile))
            browser.close()
        if analyze_data.get("pack07_context") is not None:
            raise RuntimeError("Pack 07 leaked onto public analyze payload")
        if not isinstance(individual, dict) or "items" not in individual:
            raise RuntimeError("Analyze payload missing Shen Sha individual projection")
        if not isinstance(ecosystem, dict) or "clusters" not in ecosystem and "dominant" not in ecosystem:
            raise RuntimeError("Analyze payload missing Shen Sha ecosystem projection")
        leak = json.dumps(shen_sha, ensure_ascii=False)
        if "TR-P7-" in leak or "trace_ids" in leak:
            raise RuntimeError("Shen Sha customer projection leaked traces")
        proof = {
            "health": {"status": health_status, "body": health},
            "analyze": {
                "status": analyze_status,
                "pipeline": analyze_data.get("pipeline"),
                "has_pack07_context": "pack07_context" in analyze_data,
                "detected_matches": [
                    item.get("canonical_name") or item.get("id")
                    for item in (matches or [])
                    if isinstance(item, dict)
                ],
                "individual": individual,
                "ecosystem": ecosystem,
            },
            "history_portal": history_code,
            "diagnostics_post": {"status": live_diag_status, "body": live_diag},
            "screenshots": {
                "overview": str(overview.relative_to(REPO)).replace("\\", "/"),
                "shen_sha_desktop": str(desktop.relative_to(REPO)).replace("\\", "/"),
                "star_expanded": str(expanded.relative_to(REPO)).replace("\\", "/"),
                "ecosystem": str(eco_shot.relative_to(REPO)).replace("\\", "/"),
                "cluster_expanded": str(cluster_shot.relative_to(REPO)).replace("\\", "/"),
                "shen_sha_mobile": str(mobile.relative_to(REPO)).replace("\\", "/"),
            },
        }
        (OUT / "P7-IMP-06_diagnostics.json").write_text(
            json.dumps(proof, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(proof, ensure_ascii=False, indent=2)[:8000])
        print("Servers left running")
    except Exception:
        api_proc.terminate()
        portal_proc.terminate()
        raise


if __name__ == "__main__":
    main()
