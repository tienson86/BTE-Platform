"""P7-IMP-11 live proof: current Đại Vận Luck Interaction on /result."""

from __future__ import annotations

import html
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


def _diagnostics_html(data: dict[str, object]) -> str:
    rows = "".join(
        f"<tr><th>{html.escape(str(key))}</th><td>{html.escape(str(value))}</td></tr>"
        for key, value in data.items()
        if key not in {"issues", "validation"}
    )
    return (
        "<html><body style='font-family:Segoe UI,sans-serif;padding:24px'>"
        "<h1>Pack 07 diagnostics</h1>"
        f"<table border='1' cellpadding='8'>{rows}</table>"
        "</body></html>"
    )


def _engine_slice(payload: dict[str, object]) -> dict[str, object]:
    from engines.detailed_interpretation_engine.builders import (
        build_canonical_analysis_context_from_payload,
    )
    from engines.detailed_interpretation_engine.domain_interpretation.engine import (
        interpret_and_bind_domain_interpretation,
    )
    from engines.detailed_interpretation_engine.evidence_priority.engine import (
        interpret_and_bind_evidence_priority,
    )
    from engines.detailed_interpretation_engine.luck_activation.engine import (
        interpret_and_bind_luck_activation,
    )
    from engines.detailed_interpretation_engine.luck_interaction.engine import (
        interpret_and_bind_luck_interaction,
    )
    from engines.detailed_interpretation_engine.mc01 import attach_mc01_reference
    from engines.detailed_interpretation_engine.serialization import to_jsonable
    from engines.detailed_interpretation_engine.shen_sha.engine import interpret_and_bind_shen_sha
    from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods

    bound = dict(payload)
    attach_mc01_reference(bound)
    context = interpret_and_bind_luck_interaction(
        interpret_and_bind_luck_activation(
            interpret_and_bind_domain_interpretation(
                interpret_and_bind_evidence_priority(
                    interpret_and_bind_shen_sha(
                        interpret_and_bind_ten_gods(
                            build_canonical_analysis_context_from_payload(bound),
                            bound,
                        ),
                        bound,
                    ),
                    bound,
                ),
                bound,
            ),
            bound,
        )
    )
    interaction = context.runtime.temporal.luck_interaction
    activation = context.runtime.temporal.luck_activation
    return {
        "cycle_id": activation.cycle_id,
        "time_window": activation.time_window,
        "temporal_stem": activation.temporal_stem,
        "temporal_branch": activation.temporal_branch,
        "activation_states": {
            domain_id: item.activation_state.value for domain_id, item in activation.items.items()
        },
        "luck_interaction": to_jsonable(interaction),
        "natal_states": {
            "authority": context.runtime.domains.authority.natal.state.value,
            "career": context.runtime.domains.career.natal.state.value,
            "wealth": context.runtime.domains.wealth.natal.state.value,
            "relationship": context.runtime.domains.relationship.natal.state.value,
            "legacy": context.runtime.domains.legacy.natal.state.value,
            "vitality": context.runtime.domains.vitality.natal.state.value,
        },
    }


def main() -> None:
    """Restart runtime and capture Luck Interaction live proof."""
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
        luck = analyze_data.get("luck") if isinstance(analyze_data.get("luck"), dict) else {}
        activation = luck.get("activation") if isinstance(luck.get("activation"), dict) else {}
        interaction = luck.get("interaction") if isinstance(luck.get("interaction"), dict) else {}
        live_diag_status, live_diag = _post("/api/v1/dev/pack07/diagnostics", CASE)
        diag_body = live_diag.get("data") if isinstance(live_diag, dict) else {}
        if not isinstance(diag_body, dict):
            diag_body = {}
        history_code = urllib.request.urlopen(f"{BASE}/history", timeout=20).status
        engine = _engine_slice(analyze_data)
        overview = SHOTS / "p7_imp_11_result_overview.png"
        current = SHOTS / "p7_imp_11_luck_current.png"
        activation_shot = SHOTS / "p7_imp_11_luck_activation.png"
        interaction_shot = SHOTS / "p7_imp_11_luck_interaction.png"
        expanded = SHOTS / "p7_imp_11_luck_interaction_expanded.png"
        mobile = SHOTS / "p7_imp_11_mobile_luck_interaction.png"
        diag_shot = SHOTS / "p7_imp_11_diagnostics.png"
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            desk = browser.new_context(viewport={"width": 1440, "height": 1100})
            page = desk.new_page()
            _open_result(page)
            content = page.content() or ""
            if "TR-P7-" in content or "E-DI-" in content or "mingju_result_id" in content:
                raise RuntimeError("Pack 07 debug IDs leaked onto customer /result")
            if "thăng chức" in content or "phát tài" in content or "chia tay" in content:
                raise RuntimeError("Forbidden event prediction leaked onto /result")
            page.screenshot(path=str(overview), full_page=False)
            luck_card = page.locator("[data-card='luck']")
            luck_card.scroll_into_view_if_needed()
            page.locator("[data-luck-section='current']").screenshot(path=str(current))
            page.locator("[data-luck-section='activation']").scroll_into_view_if_needed()
            page.locator("[data-luck-section='activation']").screenshot(path=str(activation_shot))
            interaction_el = page.locator("[data-luck-section='interaction']")
            interaction_el.scroll_into_view_if_needed()
            interaction_el.screenshot(path=str(interaction_shot))
            toggle = page.locator("[data-luck-interaction-toggle]")
            if toggle.count():
                toggle.first.click()
                page.wait_for_timeout(200)
                first = page.locator("[data-luck-interaction-edge]").first
                first.locator(".bte-luck__interaction-row-btn").click()
                page.wait_for_timeout(200)
                first.screenshot(path=str(expanded))
            else:
                interaction_el.screenshot(path=str(expanded))
            phone = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = phone.new_page()
            _open_result(mobile_page)
            mobile_luck = mobile_page.locator("[data-card='luck']")
            mobile_luck.scroll_into_view_if_needed()
            mobile_toggle = mobile_page.locator(
                "[data-card='luck'] [data-mobile-toggle], [data-card='luck'] .bte-mobile-toggle"
            )
            if mobile_toggle.count():
                mobile_toggle.first.click()
                mobile_page.wait_for_timeout(300)
            mobile_page.locator("[data-luck-section='interaction']").scroll_into_view_if_needed()
            mobile_page.locator("[data-luck-section='interaction']").screenshot(path=str(mobile))
            diag_page = desk.new_page()
            diag_page.set_content(_diagnostics_html(diag_body))
            diag_page.screenshot(path=str(diag_shot), full_page=True)
            browser.close()
        dump = json.dumps(analyze_data, ensure_ascii=False)
        if '"mc01"' in dump or "mingju_result_id" in dump or "_mc01_snapshot" in dump:
            raise RuntimeError("MC-01 debug metadata leaked onto public analyze payload")
        if "E-DI-" in dump or "TR-P7-" in dump:
            raise RuntimeError("Luck traces leaked onto public analyze payload")
        if diag_body.get("luck") != "PASS":
            raise RuntimeError(f"Luck diagnostics not PASS: {diag_body.get('luck')}")
        if diag_body.get("luck_interaction") != "PASS":
            raise RuntimeError(f"Luck Interaction diagnostics not PASS: {diag_body.get('luck_interaction')}")
        if not interaction:
            raise RuntimeError("Customer luck interaction summary missing")
        proof = {
            "health": {"status": health_status, "body": health},
            "analyze": {
                "status": analyze_status,
                "pipeline": analyze_data.get("pipeline"),
                "analysis_id": analyze_data.get("analysis_id"),
                "current_cycle": luck.get("current_cycle"),
                "activation": activation,
                "interaction": interaction,
                "structural_grade": (analyze_data.get("pattern") or {}).get("structural_grade")
                if isinstance(analyze_data.get("pattern"), dict)
                else None,
            },
            "engine": engine,
            "history_portal": history_code,
            "diagnostics_post": {"status": live_diag_status, "body": live_diag},
            "screenshots": {
                "overview": str(overview.relative_to(REPO)).replace("\\", "/"),
                "luck_current": str(current.relative_to(REPO)).replace("\\", "/"),
                "luck_activation": str(activation_shot.relative_to(REPO)).replace("\\", "/"),
                "luck_interaction": str(interaction_shot.relative_to(REPO)).replace("\\", "/"),
                "luck_interaction_expanded": str(expanded.relative_to(REPO)).replace("\\", "/"),
                "mobile_luck_interaction": str(mobile.relative_to(REPO)).replace("\\", "/"),
                "diagnostics": str(diag_shot.relative_to(REPO)).replace("\\", "/"),
            },
        }
        (OUT / "P7-IMP-11_diagnostics.json").write_text(
            json.dumps(proof, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(proof, ensure_ascii=False, indent=2)[:16000])
        print("Servers left running")
    except Exception:
        api_proc.terminate()
        portal_proc.terminate()
        raise


if __name__ == "__main__":
    main()
