"""G2-03 narrative consistency probe. Read-only. No engine writes."""

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

HY_INSUFFICIENT = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng"
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}|\$\{[^}]+\}|\bNone\b|\bnull\b|\bundefined\b")
RULE_ID_RE = re.compile(
    r"\b(?:cli|com_san|pat|str|sea|tmp|flo|flw|ctl|sup|spc|spe|cmb|root)_[a-z0-9_]+\b",
    re.I,
)
ABSOLUTE_RE = re.compile(
    r"chắc chắn|duy nhất đúng|100%|không thể khác|định sẵn|tuyệt đối",
    re.I,
)
HY_DEFINITE_RE = re.compile(
    r"Hỷ thần (là|chính là)(?!\s+bổ trợ)(?!\s+Chưa)",
    re.I,
)
SPECIAL_OVERRIDE_RE = re.compile(
    r"chuyên cách hoàn chỉnh|chuyên cách quyết định Dụng|ưu tiên Ấn vì chuyên cách|Giá Sắc tuyệt đối",
    re.I,
)
TONG_TAI_RE = re.compile(r"Tòng Tài")
WEAK_EXTREME_RE = re.compile(r"cực nhược")
STRUCTURAL_STRENGTH_RE = re.compile(r"(Thủy|Hỏa|Kim|Mộc|Thổ) (mạnh nhất|suy|khuyết nên phải bổ)")
MEDICAL_RE = re.compile(r"(?<![Kk]hông )chẩn đoán|kê đơn|điều trị bệnh")
FINANCE_RE = re.compile(r"chắc chắn giàu|bảo đảm lợi nhuận|đảm bảo thu nhập")
MARRIAGE_RE = re.compile(r"chắc chắn ly hôn|nhất định hai đời")

STALE_DUNG = {
    "Ngô Đắc Dũng": ["Thổ · Mậu · Thiên Ấn", "Chuyên cách ưu tiên Ấn", "Hỷ thần Quý"],
    "Vũ Thị Thanh Tuyền": ["Tòng Tài", "Nhật chủ cực nhược theo Tài"],
    "Lưu Hoàng Sơn": [],
}


def _narrative_blob(payload: dict) -> str:
    nr = payload.get("narrative_result") or {}
    parts: list[str] = []
    summary = nr.get("summary") or {}
    if isinstance(summary, dict):
        for key in ("identity", "priority_recommendation", "next_action"):
            if summary.get(key):
                parts.append(str(summary[key]))
        for key in ("strengths", "weaknesses"):
            for item in summary.get(key) or []:
                parts.append(str(item))
    for section in nr.get("sections") or []:
        if not isinstance(section, dict):
            continue
        parts.append(str(section.get("title") or ""))
        for para in section.get("paragraphs") or []:
            if isinstance(para, dict):
                parts.append(str(para.get("text") or ""))
            else:
                parts.append(str(para))
        for rec in section.get("recommendations") or []:
            if isinstance(rec, dict):
                parts.append(str(rec.get("action") or ""))
                parts.append(str(rec.get("reason") or ""))
    for rec in nr.get("recommendations") or []:
        if isinstance(rec, dict):
            parts.append(str(rec.get("action") or ""))
    exec_sum = nr.get("commercial_executive_summary") or {}
    if isinstance(exec_sum, dict):
        for key in ("central_message", "conclusion", "composed_text"):
            if exec_sum.get(key):
                parts.append(str(exec_sum[key]))
        for item in exec_sum.get("supporting_points") or []:
            parts.append(str(item))
    interp = payload.get("interpretation") or {}
    if isinstance(interp, dict):
        for section in interp.get("sections") or []:
            if isinstance(section, dict):
                parts.append(str(section.get("title") or ""))
                parts.append(str(section.get("body") or section.get("text") or ""))
    report = payload.get("report") or {}
    if isinstance(report, dict):
        parts.append(str(report.get("html") or "")[:8000])
        parts.append(str(report.get("markdown") or "")[:8000])
    return "\n".join(p for p in parts if p)


def _section_titles(payload: dict) -> list[str]:
    nr = payload.get("narrative_result") or {}
    return [str(s.get("title") or s.get("id") or "") for s in (nr.get("sections") or []) if isinstance(s, dict)]


def _issues(name: str, live: dict, blob: str, payload: dict) -> list[str]:
    issues: list[str] = []
    dung = str(live.get("overall_dung") or "")
    hy = str(live.get("customer_hy") or "")
    pattern = str(live.get("pattern") or "")
    strength = str(live.get("strength_level") or "")
    climate = str(live.get("climate_preference_label") or "")
    reason = str(live.get("short_reason") or "")
    nr = payload.get("narrative_result") or {}

    if not blob.strip():
        issues.append("empty_narrative")
    if PLACEHOLDER_RE.search(blob):
        issues.append("unresolved_placeholder")
    if RULE_ID_RE.search(blob):
        issues.append("rule_id")
    if SPECIAL_OVERRIDE_RE.search(blob) and live.get("ug_override_eligible") is False:
        issues.append("level1_override_overclaim")
    if name == "Vũ Thị Thanh Tuyền" and TONG_TAI_RE.search(blob):
        issues.append("stale_tong_tai")
    if name == "Cao Xuân Trường" and WEAK_EXTREME_RE.search(blob):
        issues.append("extreme_weak_wording")
    if STRUCTURAL_STRENGTH_RE.search(blob):
        issues.append("five_elements_as_strength")
    if MEDICAL_RE.search(blob) and not re.search(r"Không chẩn đoán", blob):
        issues.append("medical_claim")
    if FINANCE_RE.search(blob):
        issues.append("finance_guarantee")
    if MARRIAGE_RE.search(blob):
        issues.append("marriage_deterministic")

    if hy == HY_INSUFFICIENT:
        if HY_DEFINITE_RE.search(blob):
            issues.append("hy_invention")
        if "Hỷ thần (" in blob and HY_INSUFFICIENT not in blob and "Chưa đủ căn cứ" not in blob and "Chưa có Hỷ" not in blob:
            issues.append("hy_parenthetical_invention")

    if strength == "strong" and re.search(
        r"Nhật chủ (suy nhược|cực nhược|thân nhược)|mức lực đang mỏng lực",
        blob,
    ):
        issues.append("strength_contradiction")
    if strength == "weak" and re.search(r"Nhật chủ (thân vượng|rất vượng)", blob) and "không" not in blob.lower():
        issues.append("strength_contradiction")

    if dung:
        stem = dung.split("·")[1].strip() if "·" in dung else ""
        # Contradiction: narrative names a different Overall Dụng as the winner.
        if re.search(r"Dụng thần (chính|tổng thể|Overall).{0,20}Hỏa", blob) and "Thủy" in dung and "Hỏa" not in dung:
            issues.append("dung_contradiction_fire")
        if name == "Ngô Đắc Dũng":
            if "Thổ · Mậu · Thiên Ấn" in blob or re.search(r"Dụng thần chính: Mậu", blob):
                issues.append("dung_stale_earth")
            if "Hỏa chính là Overall" in blob or "Hỏa chính là Dụng" in blob:
                issues.append("climate_as_overall")
        if name == "Lưu Hoàng Sơn" and re.search(r"Dụng thần chính: (Bính|Đinh|Hỏa)", blob):
            issues.append("climate_switched_overall")

    if live.get("ug_override_eligible") is False and "gia_sac" in str(live.get("detected_special_pattern") or ""):
        if re.search(r"ưu tiên Ấn", blob, re.I):
            issues.append("special_an_override")

    for stale in STALE_DUNG.get(name, []):
        if stale and stale in blob:
            issues.append(f"stale:{stale}")

    if ABSOLUTE_RE.search(blob):
        issues.append("absolute_wording")

    analysis_id = payload.get("analysis_id") or payload.get("request_id")
    nr_run = nr.get("run_id")
    if analysis_id and nr_run and str(analysis_id) != str(nr_run):
        issues.append(f"analysis_id_mismatch:{analysis_id}!={nr_run}")

    return issues


def main() -> None:
    frozen_rows = json.loads(FROZEN.read_text(encoding="utf-8"))
    frozen_by = {row["case"]: row for row in frozen_rows}
    orch = OrchestratorService()
    rows = []
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
        blob = _narrative_blob(payload)
        issues = _issues(name, live, blob, payload)
        nr = payload.get("narrative_result") or {}
        status = "PASS"
        if diffs:
            status = "FAIL (analytical)"
        elif issues:
            status = "FAIL"
        excerpt = blob.replace("\n", " ")[:900]
        rows.append(
            {
                "case": name,
                "analytical": "MATCH" if not diffs else "DIFF",
                "status": status,
                "issues": issues,
                "strength": f"{live.get('strength_score')} {live.get('strength_level')}",
                "pattern": live.get("pattern"),
                "override": live.get("ug_override_eligible"),
                "dung": live.get("overall_dung"),
                "hy": live.get("customer_hy"),
                "dieu_hau": live.get("climate_preference_label"),
                "archetype": live.get("reason_archetype"),
                "analysis_id": payload.get("analysis_id") or payload.get("request_id"),
                "narrative_run_id": nr.get("run_id"),
                "narrative_contract": nr.get("contract"),
                "narrative_generator": nr.get("generator"),
                "section_titles": _section_titles(payload),
                "excerpt": excerpt,
                "diffs": diffs,
            }
        )

    dest = ROOT / "G2_03_NARRATIVE_PROBE.json"
    dest.write_text(json.dumps({"rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(
        {
            "fail": [r["case"] for r in rows if r["status"] != "PASS"],
            "rows": [
                {
                    "case": r["case"],
                    "status": r["status"],
                    "issues": r["issues"],
                    "generator": r["narrative_generator"],
                    "run_id": r["narrative_run_id"],
                    "analysis_id": r["analysis_id"],
                }
                for r in rows
            ],
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
