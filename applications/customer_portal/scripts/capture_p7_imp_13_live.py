"""P7-IMP-13 live proof: Life Optimization Action Plan on /result."""

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

FORBIDDEN = (
    "mặc đỏ",
    "wear red",
    "sống gần nước",
    "mua cây",
    "chẩn đoán",
    "điều trị",
    "uống thuốc",
    "mua cổ phiếu",
    "đòn bẩy",
    "chắc chắn giàu",
    "chắc chắn thăng",
)


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
    page.wait_for_selector("[data-ap-opt='true']")


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
    from engines.detailed_interpretation_engine.diagnostics import diagnostics_from_payload
    from engines.detailed_interpretation_engine.domain_interpretation.engine import (
        interpret_and_bind_domain_interpretation,
    )
    from engines.detailed_interpretation_engine.evidence_priority.engine import (
        interpret_and_bind_evidence_priority,
    )
    from engines.detailed_interpretation_engine.life_optimization.engine import (
        interpret_and_bind_life_optimization,
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
    from engines.detailed_interpretation_engine.temporal_activation.engine import (
        interpret_and_bind_temporal_activation,
    )
    from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods

    bound = dict(payload)
    attach_mc01_reference(bound)
    context = interpret_and_bind_life_optimization(
        interpret_and_bind_temporal_activation(
            interpret_and_bind_luck_interaction(
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
            ),
            bound,
        ),
        bound,
    )
    result = context.runtime.optimization
    domains: dict[str, dict[str, object]] = {}
    luck = context.runtime.temporal.luck_activation
    interaction = context.runtime.temporal.luck_interaction
    ep = context.runtime.interpretation.evidence_priority
    by_id = {item.action_id: item for item in result.actions}
    for domain_id in ("authority", "career", "wealth", "relationship", "legacy", "vitality"):
        natal = getattr(context.runtime.domains, domain_id).natal
        plan = result.domain_plans.get(domain_id)
        luck_item = luck.items.get(domain_id)
        domains[domain_id] = {
            "natal_state": natal.state.value,
            "natal_priority": natal.priority,
            "driver": natal.driver_id or natal.driver,
            "bottleneck": natal.bottleneck,
            "leakage": natal.leakage,
            "dimensions": dict(natal.dimensions),
            "luck_state": luck_item.activation_state.value if luck_item is not None else None,
            "recommended": list(plan.recommended_actions) if plan else [],
            "avoid": list(plan.avoid_actions) if plan else [],
            "temporal": list(plan.temporal_adjustments) if plan else [],
            "conditions": list(natal.conditions),
        }
    top3_traces: list[dict[str, object]] = []
    for action_id in result.top_priorities:
        action = by_id.get(action_id)
        if action is None:
            continue
        natal = getattr(context.runtime.domains, action.target_domain).natal
        luck_item = luck.items.get(action.target_domain)
        related = []
        for finding in ep.findings:
            if finding.domain != action.target_domain and finding.finding_id not in action.evidence_ids:
                continue
            related.append(
                {
                    "finding_id": finding.finding_id,
                    "domain": finding.domain,
                    "tier": finding.tier.value,
                    "source_kind": finding.source_kind,
                    "semantic_key": finding.semantic_key,
                    "category": finding.category,
                    "tier_reason": finding.tier_reason,
                }
            )
        top3_traces.append(
            {
                "action_id": action.action_id,
                "recommended_action_key": action.recommended_action_key,
                "target_domain": action.target_domain,
                "mechanism": action.target_mechanism,
                "action_type": action.action_type,
                "priority": action.priority,
                "category": action.category,
                "reason_key": action.reason_key,
                "time_scope": action.time_scope,
                "effect": action.expected_structural_effect,
                "conditions": list(action.conditions),
                "evidence_ids": list(action.evidence_ids),
                "trace_ids": list(action.trace_ids),
                "domain": {
                    "state": natal.state.value,
                    "priority": natal.priority,
                    "driver": natal.driver_id or natal.driver,
                    "bottleneck": natal.bottleneck,
                    "leakage": natal.leakage,
                },
                "luck_activation": luck_item.activation_state.value if luck_item is not None else None,
                "evidence_priority_findings": related[:8],
            }
        )
    diagnostics = diagnostics_from_payload(payload)
    keys = " ".join(item.recommended_action_key for item in result.actions)
    return {
        "state": result.state.value,
        "top_priorities": list(result.top_priorities),
        "top3_traces": top3_traces,
        "natal_action_ids": list(result.natal_plan.action_ids),
        "temporal_action_ids": list(result.temporal_plan.action_ids),
        "conflicts": [item.conflict_id for item in result.conflicts],
        "interaction": {
            "stress_transfers": to_jsonable(interaction.stress_transfers),
            "findings": [
                {
                    "finding_id": item.finding_id,
                    "type": item.interaction_type,
                    "source": item.source_domain,
                    "target": item.target_domain,
                }
                for item in interaction.findings
            ],
        },
        "useful_god": to_jsonable(result.useful_god_plan),
        "elements": to_jsonable(result.element_plan),
        "actions": to_jsonable(result.actions),
        "saturations": to_jsonable(result.saturations),
        "overload_guard": {
            "strengthen_workload": "strengthen_workload" not in keys,
            "increase_output": "increase_output" not in keys,
            "expand_responsibility": "expand_responsibility" not in keys,
            "aggressive_investment": "investment" not in keys.lower(),
        },
        "domains": domains,
        "diagnostics": diagnostics.to_dict(),
    }


def main() -> None:
    """Restart runtime and capture Life Optimization live proof."""
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
        optimization = (
            analyze_data.get("optimization") if isinstance(analyze_data.get("optimization"), dict) else {}
        )
        live_diag_status, live_diag = _post("/api/v1/dev/pack07/diagnostics", CASE)
        diag_body = live_diag.get("data") if isinstance(live_diag, dict) else {}
        if not isinstance(diag_body, dict):
            diag_body = {}
        empty_status, empty_diag = _get("/api/v1/dev/pack07/diagnostics")
        history_code = urllib.request.urlopen(f"{BASE}/history", timeout=20).status
        engine = _engine_slice(analyze_data)
        overview = SHOTS / "p7_imp_13_result_overview.png"
        top = SHOTS / "p7_imp_13_top3.png"
        natal = SHOTS / "p7_imp_13_natal_plan.png"
        temporal = SHOTS / "p7_imp_13_temporal_plan.png"
        wealth = SHOTS / "p7_imp_13_wealth_expanded.png"
        career = SHOTS / "p7_imp_13_career_expanded.png"
        vitality = SHOTS / "p7_imp_13_vitality_expanded.png"
        conflict = SHOTS / "p7_imp_13_career_vitality_conflict.png"
        elements = SHOTS / "p7_imp_13_five_element.png"
        function_plan = SHOTS / "p7_imp_13_useful_god_five_element.png"
        mobile = SHOTS / "p7_imp_13_mobile_optimization.png"
        diag_shot = SHOTS / "p7_imp_13_diagnostics.png"
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            desk = browser.new_context(viewport={"width": 1440, "height": 1400})
            page = desk.new_page()
            _open_result(page)
            content = (page.content() or "").lower()
            if "tr-p7-" in content or "e-di-" in content or "mingju_result_id" in content:
                raise RuntimeError("Pack 07 debug IDs leaked onto customer /result")
            for token in FORBIDDEN:
                if token in content:
                    raise RuntimeError(f"Forbidden copy leaked onto /result: {token}")
            page.screenshot(path=str(overview), full_page=False)
            card = page.locator("[data-card='action-plan']")
            card.scroll_into_view_if_needed()
            page.locator("[data-ap-section='top-priorities']").screenshot(path=str(top))
            page.locator("[data-ap-scope='natal']").screenshot(path=str(natal))
            page.locator("[data-ap-scope='temporal']").screenshot(path=str(temporal))
            for domain_id, dest in (
                ("career", career),
                ("wealth", wealth),
                ("vitality", vitality),
            ):
                btn = page.locator(f"[data-ap-domain='{domain_id}'] .bte-ap__domain-btn")
                if btn.count():
                    btn.click()
                    page.wait_for_timeout(200)
                page.locator(f"[data-ap-domain='{domain_id}']").screenshot(path=str(dest))
            if page.locator("[data-ap-section='conflicts']").count():
                page.locator("[data-ap-section='conflicts']").screenshot(path=str(conflict))
            else:
                page.locator("[data-ap-scope='temporal']").screenshot(path=str(conflict))
            if page.locator("[data-ap-section='function-plan']").count():
                page.locator("[data-ap-section='function-plan']").screenshot(path=str(function_plan))
            elif page.locator("[data-ap-section='elements']").count():
                page.locator("[data-ap-section='elements']").screenshot(path=str(function_plan))
            else:
                page.locator("[data-ap-opt='true']").screenshot(path=str(function_plan))
            if page.locator("[data-ap-section='elements']").count():
                page.locator("[data-ap-section='elements']").screenshot(path=str(elements))
            else:
                page.locator("[data-ap-opt='true']").screenshot(path=str(elements))
            phone = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = phone.new_page()
            _open_result(mobile_page)
            mobile_card = mobile_page.locator("[data-card='action-plan']")
            mobile_card.scroll_into_view_if_needed()
            mobile_toggle = mobile_page.locator(
                "[data-card='action-plan'] [data-mobile-toggle], [data-card='action-plan'] .bte-mobile-toggle"
            )
            if mobile_toggle.count():
                mobile_toggle.first.click()
                mobile_page.wait_for_timeout(300)
            mobile_page.locator("[data-ap-opt='true']").screenshot(path=str(mobile))
            diag_page = desk.new_page()
            diag_page.set_content(_diagnostics_html(diag_body))
            diag_page.screenshot(path=str(diag_shot), full_page=True)
            browser.close()
        dump = json.dumps(analyze_data, ensure_ascii=False)
        if '"mc01"' in dump or "mingju_result_id" in dump or "_mc01_snapshot" in dump:
            raise RuntimeError("MC-01 debug metadata leaked onto public analyze payload")
        if "E-DI-" in dump or "TR-P7-" in dump:
            raise RuntimeError("Optimization traces leaked onto public analyze payload")
        if diag_body.get("optimization") != "PASS":
            raise RuntimeError(f"Optimization diagnostics not PASS: {diag_body.get('optimization')}")
        if not optimization.get("top_priorities"):
            raise RuntimeError("Customer optimization compact missing")
        proof = {
            "health": {"status": health_status, "body": health},
            "analyze": {
                "status": analyze_status,
                "pipeline": analyze_data.get("pipeline"),
                "analysis_id": analyze_data.get("analysis_id"),
                "optimization": optimization,
            },
            "engine": engine,
            "history_portal": history_code,
            "diagnostics_post": {"status": live_diag_status, "body": live_diag},
            "diagnostics_empty": {"status": empty_status, "body": empty_diag},
            "screenshots": {
                "overview": str(overview.relative_to(REPO)).replace("\\", "/"),
                "top3": str(top.relative_to(REPO)).replace("\\", "/"),
                "natal_plan": str(natal.relative_to(REPO)).replace("\\", "/"),
                "temporal_plan": str(temporal.relative_to(REPO)).replace("\\", "/"),
                "wealth_expanded": str(wealth.relative_to(REPO)).replace("\\", "/"),
                "career_expanded": str(career.relative_to(REPO)).replace("\\", "/"),
                "vitality_expanded": str(vitality.relative_to(REPO)).replace("\\", "/"),
                "career_vitality_conflict": str(conflict.relative_to(REPO)).replace("\\", "/"),
                "five_element": str(elements.relative_to(REPO)).replace("\\", "/"),
                "useful_god_five_element": str(function_plan.relative_to(REPO)).replace("\\", "/"),
                "mobile_optimization": str(mobile.relative_to(REPO)).replace("\\", "/"),
                "diagnostics": str(diag_shot.relative_to(REPO)).replace("\\", "/"),
            },
        }
        (OUT / "P7-IMP-13_diagnostics.json").write_text(
            json.dumps(proof, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(proof, ensure_ascii=False, indent=2)[:20000])
        print("Servers left running")
    except Exception:
        api_proc.terminate()
        portal_proc.terminate()
        raise


if __name__ == "__main__":
    main()
