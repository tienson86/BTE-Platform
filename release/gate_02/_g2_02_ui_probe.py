"""G2-02 ten-case UI probe. Presentation copy only. Does not write engines."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(ROOT))

from applications.api.services.orchestrator import OrchestratorService

from _g2_01_binding_probe import CASES, COMPARE_KEYS, FROZEN, fingerprint

ROOT = Path(__file__).resolve().parent
HY_NEUTRAL = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng"
RULE_ID_RE = re.compile(
    r"\b(?:cli|com_san|pat|str|sea|tmp|flo|flw|ctl|sup|spc|spe|cmb|root)_[a-z0-9_]+\b",
    re.I,
)
MACHINE_RE = re.compile(r"\b(?:male|female|preview|mock|fixture|debug)\b", re.I)
CONTRACT_RE = re.compile(r"UsefulGodView@1\.5")

SUPPORTED_HY = {"Đặng Thị Dung", "Cao Xuân Trường"}
LEVEL1_DETECTED = {"Ngô Đắc Dũng", "Lương Văn Mạnh"}


def _ui_copy(live: dict[str, object]) -> dict[str, object]:
    dung = str(live.get("overall_dung") or "").strip()
    hy = str(live.get("customer_hy") or "").strip()
    reason = str(live.get("short_reason") or "").strip()
    climate = " · ".join(
        part
        for part in (
            str(live.get("dieu_hau") or "").strip(),
            str(live.get("climate_preference_label") or "").strip(),
        )
        if part
    )
    pattern = str(live.get("pattern") or "").strip()
    blobs = " | ".join([dung, hy, reason, climate, pattern, str(live.get("ky") or "")])
    return {
        "pillars": live.get("four_pillars"),
        "strength": f"{live.get('strength_score')} {live.get('strength_level')}",
        "pattern": pattern,
        "dieu_hau": climate,
        "dung": dung,
        "reason": reason,
        "hy": hy,
        "ky": live.get("ky"),
        "luck": live.get("current_luck"),
        "hy_duplicates_dung": bool(hy) and hy == dung,
        "hy_neutral": hy == HY_NEUTRAL,
        "reason_visible": bool(reason),
        "climate_separate": bool(climate) and climate != dung,
        "has_rule_id": bool(RULE_ID_RE.search(blobs)),
        "has_machine_token": bool(MACHINE_RE.search(blobs)),
        "exposes_contract": bool(CONTRACT_RE.search(blobs)),
        "absolute_override_wording": bool(
            re.search(r"tuyệt đối|chuyên cách ưu tiên", pattern, re.I)
        ),
    }


def _ui_status(name: str, copy: dict[str, object], analytical_match: bool) -> str:
    if not analytical_match:
        return "FAIL (analytical)"
    required = [
        copy["pillars"],
        copy["strength"],
        copy["pattern"],
        copy["dieu_hau"],
        copy["dung"],
        copy["reason"],
        copy["hy"],
        copy["ky"],
        copy["luck"],
    ]
    if not all(required):
        return "FAIL"
    if copy["has_rule_id"] or copy["has_machine_token"] or copy["exposes_contract"]:
        return "FAIL"
    if copy["absolute_override_wording"]:
        return "FAIL"
    if not copy["climate_separate"] or not copy["reason_visible"]:
        return "FAIL"
    if name in SUPPORTED_HY:
        if copy["hy_neutral"] or copy["hy_duplicates_dung"]:
            return "FAIL"
    else:
        if copy["hy_duplicates_dung"]:
            return "FAIL"
        if not copy["hy_neutral"] and "Chưa đủ căn cứ" not in str(copy["hy"]):
            return "FAIL"
    if name in LEVEL1_DETECTED and "Cấu trúc đặc biệt được nhận diện" not in str(
        copy["pattern"]
    ):
        return "FAIL"
    if name == "Vũ Thị Thanh Tuyền" and "Tòng Tài" in str(copy["pattern"]):
        return "FAIL"
    if name == "Ngô Đắc Dũng" and copy["dung"] != "Thủy · Nhâm · Thực Thần":
        return "FAIL"
    if name == "Vũ Thị Thanh Tuyền" and copy["dung"] != "Mộc · Ất · Chính Quan":
        return "FAIL"
    return "PASS"


def main() -> None:
    frozen_rows = json.loads(FROZEN.read_text(encoding="utf-8"))
    frozen_by = {row["case"]: row for row in frozen_rows}
    orch = OrchestratorService()
    rows: list[dict[str, object]] = []
    for spec in CASES:
        name = str(spec["name"])
        kwargs = {k: v for k, v in spec.items() if k != "name"}
        payload = orch.analyze(**kwargs)
        live = fingerprint(name, payload)
        diffs = {
            key: {"frozen": frozen_by[name].get(key), "live": live.get(key)}
            for key in COMPARE_KEYS
            if frozen_by[name].get(key) != live.get(key)
        }
        copy = _ui_copy(live)
        status = _ui_status(name, copy, not diffs)
        rows.append(
            {
                "case": name,
                "analytical": "MATCH" if not diffs else "DIFF",
                "ui": status,
                "diffs": diffs,
                **copy,
            }
        )

    dest_json = ROOT / "G2_02_CONTROL_CASE_UI_PROBE.json"
    dest_json.write_text(json.dumps({"rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# G2-02 — Control-case UI matrix",
        "",
        "Fresh `OrchestratorService.analyze` → customer copy fields the Result UI binds.",
        "No engine writes. Analytical columns must remain MATCH vs `G1_PREFINAL_CONTROL_CASES.json`.",
        "",
        "| Case | Analytical | UI | Four Pillars | Strength | Pattern | Điều hậu | Dụng | Reason | Hỷ | Kỵ | Luck |",
        "|------|------------|----|--------------|----------|---------|----------|------|--------|-----|-----|------|",
    ]
    for row in rows:
        lines.append(
            "| {case} | {analytical} | {ui} | {pillars} | {strength} | {pattern} | {dieu_hau} | {dung} | {reason_ok} | {hy} | {ky} | {luck} |".format(
                case=row["case"],
                analytical=row["analytical"],
                ui=row["ui"],
                pillars=row["pillars"],
                strength=row["strength"],
                pattern=row["pattern"],
                dieu_hau=row["dieu_hau"],
                dung=row["dung"],
                reason_ok="yes" if row["reason_visible"] else "NO",
                hy=row["hy"],
                ky=row["ky"],
                luck=row["luck"],
            )
        )
    fail = [row["case"] for row in rows if str(row["ui"]) != "PASS"]
    lines.extend(
        [
            "",
            f"**UI failures:** {len(fail)} ({', '.join(fail) or 'none'})",
            f"**Analytical diffs:** {sum(1 for row in rows if row['analytical'] != 'MATCH')}",
            "",
            "Machine dump: `release/gate_02/G2_02_CONTROL_CASE_UI_PROBE.json`.",
        ]
    )
    (ROOT / "G2_02_CONTROL_CASE_UI_MATRIX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"fail": fail, "rows": [{k: r[k] for k in ('case', 'analytical', 'ui')} for r in rows]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
