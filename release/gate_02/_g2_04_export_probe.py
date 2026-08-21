"""G2-04 export probe: frozen truth vs presentation, PDF/DOCX samples, screenshots."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(ROOT))

from applications.api.services.customer_export import (  # noqa: E402
    build_customer_export_filename,
    export_customer_file,
    prepare_customer_report_input,
)
from applications.api.services.orchestrator import OrchestratorService  # noqa: E402
from applications.api.services.result_identity import stamp_customer_result_identity  # noqa: E402
from engines.report_engine.rendering.html_report_v1 import render_html  # noqa: E402
from engines.report_engine.rendering.report_sections_v1 import build_presented_report  # noqa: E402
from _g2_01_binding_probe import CASES, COMPARE_KEYS, FROZEN, fingerprint  # noqa: E402

SHOT = ROOT / "screenshots" / "g2_04"
HY_NEUTRAL = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng"
VISUAL = {
    "Ngô Đắc Dũng": "dung",
    "Vũ Thị Thanh Tuyền": "tuyen",
    "Cao Xuân Trường": "truong",
    "Đặng Thị Dung": "dungthi",
}


def _pdf_contains(raw: bytes, needle: str) -> bool:
    return (
        needle.encode("utf-8") in raw
        or needle.encode("utf-16-be") in raw
        or needle.encode("utf-16-le") in raw
    )


def _screenshot_html(html_path: Path, png_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 1280})
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.screenshot(path=str(png_path), full_page=True)
        browser.close()


def main() -> None:
    SHOT.mkdir(parents=True, exist_ok=True)
    frozen_rows = json.loads(FROZEN.read_text(encoding="utf-8"))
    frozen_by = {row["case"]: row for row in frozen_rows}
    orch = OrchestratorService()
    rows: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []
    timings: dict[str, float] = {}

    for index, spec in enumerate(CASES):
        name = str(spec["name"])
        kwargs = {k: v for k, v in spec.items() if k != "name"}
        payload = stamp_customer_result_identity(orch.analyze(**kwargs), f"g2-04-probe-{index}")
        live = fingerprint(name, payload)
        frozen = frozen_by[name]
        diffs = {}
        for key in COMPARE_KEYS:
            if frozen.get(key) != live.get(key):
                diffs[key] = {"frozen": frozen.get(key), "live": live.get(key)}
        report_input = prepare_customer_report_input(
            analysis_id=str(payload.get("analysis_id")),
            source="current",
            data=payload,
            birth_input=spec,
        )
        presented = build_presented_report(report_input)
        useful_rows = {
            label: value
            for section in presented.sections
            if section.id == "useful-god"
            for label, value in section.meta_rows
        }
        slug = VISUAL.get(name)
        artifacts: dict[str, object] = {}
        if slug:
            html = render_html(report_input)
            html_path = SHOT / f"{slug}_official.html"
            html_path.write_text(html, encoding="utf-8")
            png_path = SHOT / f"{slug}_official.png"
            try:
                _screenshot_html(html_path, png_path)
                artifacts["png"] = png_path.name
            except Exception as exc:  # noqa: BLE001
                artifacts["png_error"] = str(exc)
            started = time.perf_counter()
            pdf_path, pdf_name, _pdf = export_customer_file(report_input=report_input, fmt="pdf")
            timings[f"{slug}_pdf_s"] = round(time.perf_counter() - started, 2)
            dest_pdf = SHOT / pdf_name
            dest_pdf.write_bytes(Path(pdf_path).read_bytes())
            Path(pdf_path).unlink(missing_ok=True)
            raw = dest_pdf.read_bytes()
            artifacts["pdf"] = dest_pdf.name
            artifacts["pdf_searchable"] = _pdf_contains(raw, str(useful_rows.get("Dụng thần") or "Thủy"))
            started = time.perf_counter()
            docx_path, docx_name, _docx = export_customer_file(report_input=report_input, fmt="docx")
            timings[f"{slug}_docx_s"] = round(time.perf_counter() - started, 2)
            dest_docx = SHOT / docx_name
            dest_docx.write_bytes(Path(docx_path).read_bytes())
            Path(docx_path).unlink(missing_ok=True)
            artifacts["docx"] = dest_docx.name
            artifacts["filename_pdf"] = pdf_name
        row = {
            "case": name,
            "analytical": "MATCH" if not diffs else "DIFF",
            "analysis_id": payload.get("analysis_id"),
            "filename": build_customer_export_filename(report_input, "pdf"),
            "dung": useful_rows.get("Dụng thần"),
            "hy": useful_rows.get("Hỷ thần"),
            "ky": useful_rows.get("Kỵ thần"),
            "reason": bool(useful_rows.get("Căn cứ chọn Dụng")),
            "dieu_hau": useful_rows.get("Điều hậu ưu tiên"),
            "hy_neutral_ok": useful_rows.get("Hỷ thần") == live.get("customer_hy"),
            "diffs": diffs,
            "artifacts": artifacts,
        }
        rows.append(row)
        if diffs:
            mismatches.append({"case": name, "diffs": diffs})

    out = {
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "timings": timings,
        "hy_copy": HY_NEUTRAL,
        "rows": rows,
    }
    dest = ROOT / "G2_04_EXPORT_PROBE.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"mismatch_count": len(mismatches), "timings": timings, "mismatches": mismatches}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
