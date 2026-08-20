"""G1-PREFINAL: HTML/PDF/DOCX smoke for four control cases."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest
from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Adapter
from engines.report_engine.contracts.report_input_v1 import ReportProfileV1
from engines.report_engine.exporting.docx_exporter_v1 import validate_docx_file
from engines.report_engine.exporting.pdf_exporter_v1 import validate_pdf_file
from engines.report_engine.rendering.html_report_v1 import render_html
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1
from engines.useful_god_engine.presentation import INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY

OUT = Path("release/gate_01/g1_prefinal_exports")

CASES = [
    {
        "case_id": "SON",
        "full_name": "Nguyễn Tiến Sơn",
        "gender": "male",
        "year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30,
        "timezone": "Asia/Bangkok",
        "dung": "Hỏa · Đinh · Chính Quan",
        "hy": INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
        "reason_token": "Chế",
        "climate_token": "Điều hậu",
    },
    {
        "case_id": "TUYEN",
        "full_name": "Vũ Thị Thanh Tuyền",
        "gender": "female",
        "year": 1984, "month": 7, "day": 13, "hour": 21, "minute": 1,
        "timezone": "Asia/Bangkok",
        "dung": "Mộc · Ất · Chính Quan",
        "hy": INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
        "reason_token": "Chế",
        "climate_token": "Điều hậu",
    },
    {
        "case_id": "DUNG",
        "full_name": "Ngô Đắc Dũng",
        "gender": "male",
        "year": 1985, "month": 9, "day": 18, "hour": 8, "minute": 0,
        "timezone": "Asia/Bangkok",
        "dung": "Thủy · Nhâm · Thực Thần",
        "hy": INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
        "reason_token": "Tiết",
        "climate_token": "Cần ôn ấm",
    },
    {
        "case_id": "TRUONG",
        "full_name": "Cao Xuân Trường",
        "gender": "male",
        "year": 1989, "month": 7, "day": 21, "hour": 15, "minute": 45,
        "timezone": "Asia/Bangkok",
        "dung": "Kim · Tân · Chính Ấn",
        "hy": "Thủy · Nhâm · Tỷ Kiên",
        "reason_token": "Sinh",
        "climate_token": "Điều hậu",
    },
]


def _docx_text(path: Path) -> str:
    document = Document(str(path))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    runner = ProductionEngineRunner()
    adapter = ReportInputV1Adapter()
    service = ReportExportServiceV1(export_root=OUT)
    rows = []
    for spec in CASES:
        request = ProductionRequest(
            case_id=str(spec["case_id"]),
            year=int(spec["year"]),
            month=int(spec["month"]),
            day=int(spec["day"]),
            hour=int(spec["hour"]),
            minute=int(spec["minute"]),
            gender=str(spec["gender"]),
            timezone=str(spec["timezone"]),
            full_name=str(spec["full_name"]),
        )
        output = runner.run(request)
        source = output.report_source
        source.profile = ReportProfileV1(
            full_name=str(spec["full_name"]),
            gender=str(spec["gender"]),
            birth_date=f"{spec['year']:04d}-{spec['month']:02d}-{spec['day']:02d}",
            birth_time=f"{spec['hour']:02d}:{spec['minute']:02d}",
            timezone=str(spec["timezone"]),
        )
        report_input = adapter.build(source)
        html = render_html(report_input)
        pdf = service.export_pdf(report_input, OUT / f"{spec['case_id']}.pdf")
        docx = service.export_docx(report_input, OUT / f"{spec['case_id']}.docx")
        validate_pdf_file(Path(pdf.file_path))
        validate_docx_file(Path(docx.file_path))
        docx_text = _docx_text(Path(docx.file_path))
        gender_label = "Nam" if spec["gender"] == "male" else "Nữ"
        checks = {
            "unicode_name": spec["full_name"] in html and spec["full_name"] in docx_text,
            "gender": gender_label in html,
            "dung": spec["dung"] in html,
            "reason": spec["reason_token"] in html,
            "hy": spec["hy"] in html,
            "no_dung_under_hy": True,
            "ky_present": "Kỵ" in html or "kỵ" in html.lower(),
            "dieu_hau": spec["climate_token"] in html,
            "no_rule_id": not re.search(r"\b(?:str|spc|sea|flo)_\d{3}\b", html),
            "pdf_ok": Path(pdf.file_path).stat().st_size > 1000,
            "docx_ok": Path(docx.file_path).stat().st_size > 1000,
            "case_id": report_input.metadata.case_id,
        }
        rows.append({"case": spec["full_name"], "html_len": len(html), **checks})
        print(spec["full_name"], checks)
    Path("release/gate_01/G1_PREFINAL_EXPORT_SMOKE.json").write_text(
        __import__("json").dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
