"""Customer PDF opening pages use the same published fields as Result."""

from docx import Document

from applications.api.services.customer_export import _render_modern_report_html, _render_modern_report_docx
from applications.api.services.customer_report_input import build_customer_report_input
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.result_identity import stamp_customer_result_identity


def test_opening_pages_preserve_published_result_fields() -> None:
    birth = {
        "full_name": "Nguyễn Tiến Sơn", "birth_place": "Hà Nội",
        "year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 31,
        "gender": "male", "timezone": "Asia/Bangkok",
    }
    payload = OrchestratorService().analyze(**{
        key: birth[key] for key in ("year", "month", "day", "hour", "minute", "gender", "timezone")
    })
    payload = stamp_customer_result_identity(payload, "case-opening-0431")
    report = build_customer_report_input(
        analysis_id="case-opening-0431", data=payload, birth_input=birth,
    )
    html = _render_modern_report_html(report)
    opening = report.modern_report["opening"]

    assert opening["person"]["birth_time"] == "04:31"
    assert opening["person"]["birth_place"] == "Hà Nội"
    assert opening["pillars"]["day"]["cung_phi"] == payload["bazi"]["day_pillar"]["cung_phi"]
    assert opening["pillars"]["month"]["shen_sha"] == ["Thiên Ất Quý Nhân", "Hồng Loan"]
    assert opening["pillars"]["year"]["tam_hop"] == "Dần - Ngọ - Tuất"
    assert opening["bone_weight"]["display_weight"] == "2 lượng 7 chỉ"
    assert html.index("Tứ Trụ</h2>") < html.index("Bát Tự</h2>") < html.index("Phân bổ Ngũ hành</h2>")
    assert html.index("Phân bổ Ngũ hành</h2>") < html.index('class="chapter"')


def test_word_opening_uses_same_published_chart_and_editable_tables(tmp_path) -> None:
    birth = {
        "full_name": "Nguyễn Tiến Sơn", "birth_place": "Hà Nội", "year": 1987,
        "month": 1, "day": 21, "hour": 4, "minute": 31,
        "gender": "male", "timezone": "Asia/Bangkok",
    }
    payload = OrchestratorService().analyze(**{
        key: birth[key] for key in ("year", "month", "day", "hour", "minute", "gender", "timezone")
    })
    payload = stamp_customer_result_identity(payload, "case-word-0431")
    report = build_customer_report_input(analysis_id="case-word-0431", data=payload, birth_input=birth)
    path = tmp_path / "editable.docx"
    _render_modern_report_docx(report, path)
    document = Document(path)
    text = "\n".join(p.text for p in document.paragraphs)
    assert [p.text for p in document.paragraphs if p.style.name == "Heading 1"][:3] == [
        "Tứ Trụ", "Bát Tự", "Nhật chủ"
    ]
    assert "2 lượng 7 chỉ" in text and "Phân bổ Ngũ hành" in text
    assert "Canh thuộc Dương Kim" in text
    assert document.tables[0].cell(3, 1).text == "Canh Ngọ"
    assert "Thiên Đức Quý Nhân" in document.tables[2].cell(8, 3).text
