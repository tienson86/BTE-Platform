"""Official customer PDF/DOCX from a selected stored analysis."""

from __future__ import annotations

import logging
import re
import tempfile
import uuid
from html import escape
from pathlib import Path
from typing import Any, Literal, Mapping

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from applications.api.exceptions import CustomerExportError
from applications.api.services.customer_contract import (
    CONTRACT_MISMATCH_MESSAGE,
    EMPTY_RESULT_MESSAGE,
    HISTORY_MISMATCH_MESSAGE,
    RENDERER_FAILURE_MESSAGE,
    customer_contract_message,
    customer_contract_status,
    is_compatible_customer_contract,
)
from applications.api.services.customer_report_input import build_customer_report_input
from engines.report_engine.contracts.report_export_result_v1 import ReportExportResultV1
from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.contracts.report_export_result_v1 import MEDIA_TYPE_DOCX, MEDIA_TYPE_PDF
from engines.report_engine.exporting.docx_exporter_v1 import validate_docx_file
from engines.report_engine.exporting.filename import ascii_slug
from engines.report_engine.exporting.pdf_exporter_v1 import PlaywrightPdfBackend, validate_pdf_file
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1

logger = logging.getLogger(__name__)

ExportFormat = Literal["pdf", "docx"]

_EXPORT_ROOT = Path(tempfile.gettempdir()) / "bte_customer_export"


def prepare_customer_report_input(
    *,
    analysis_id: str,
    source: str,
    data: Mapping[str, Any],
    birth_input: Mapping[str, Any] | None = None,
) -> ReportInputV1:
    """Validate selected analysis and build the canonical presentation model."""
    selected_id = str(analysis_id or "").strip()
    payload = dict(data or {})
    if not selected_id:
        raise CustomerExportError(EMPTY_RESULT_MESSAGE, code="export_missing_analysis")
    if not payload:
        raise CustomerExportError(EMPTY_RESULT_MESSAGE, code="export_missing_result")
    payload_id = str(payload.get("analysis_id") or payload.get("request_id") or "").strip()
    if payload_id and payload_id != selected_id:
        raise CustomerExportError(
            HISTORY_MISMATCH_MESSAGE,
            status_code=409,
            code="export_history_mismatch",
            details={"analysis_id": selected_id, "payload_id": payload_id, "source": source},
        )
    status = customer_contract_status(payload)
    if status != "ok" or not is_compatible_customer_contract(payload):
        raise CustomerExportError(
            customer_contract_message(status) or CONTRACT_MISMATCH_MESSAGE,
            status_code=409,
            code="export_contract_mismatch",
            details={"status": status, "source": source},
        )
    return build_customer_report_input(
        analysis_id=selected_id,
        data=payload,
        birth_input=birth_input,
    )


def build_customer_export_filename(report_input: ReportInputV1, fmt: str) -> str:
    """Customer download name: slug + birth date + report type. Not the analysis id alone."""
    slug = ascii_slug(report_input.profile.full_name or "KhachHang")
    birth = (report_input.profile.birth_date or "").replace("-", "").replace("/", "")[:8]
    date_token = birth if birth.isdigit() and len(birth) >= 8 else ""
    kind = "LuanGiaiBatTu" if _has_modern_report(report_input) else "BaoCao"
    parts = ["BTE", kind, slug]
    if date_token:
        parts.append(date_token)
    parts.append("V1")
    extension = fmt.lower().lstrip(".")
    return f"{'_'.join(parts)}.{extension}"


def export_customer_file(
    *,
    report_input: ReportInputV1,
    fmt: ExportFormat,
    service: ReportExportServiceV1 | None = None,
) -> tuple[Path, str, ReportExportResultV1]:
    """Render official PDF or DOCX into a unique temp file."""
    download_name = build_customer_export_filename(report_input, fmt)
    token = uuid.uuid4().hex[:12]
    analysis_token = ascii_slug(report_input.metadata.case_id)[:16] or "analysis"
    _EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    output_path = _EXPORT_ROOT / f"bte_{analysis_token}_{token}_{download_name}"
    if _has_modern_report(report_input):
        try:
            return _export_modern_customer_file(
                report_input=report_input,
                fmt=fmt,
                output_path=output_path,
                download_name=download_name,
            )
        except CustomerExportError:
            cleanup_export_file(output_path)
            raise
        except Exception:
            logger.exception("customer_modern_export_renderer_failed format=%s", fmt)
            cleanup_export_file(output_path)
            raise CustomerExportError(
                RENDERER_FAILURE_MESSAGE,
                status_code=500,
                code="export_renderer_failed",
            ) from None
    exporter = service or ReportExportServiceV1(export_root=_EXPORT_ROOT)
    try:
        if fmt == "pdf":
            result = exporter.export_pdf(report_input, output_path)
        elif fmt == "docx":
            result = exporter.export_docx(report_input, output_path)
        else:
            raise CustomerExportError(RENDERER_FAILURE_MESSAGE, code="export_unsupported_format")
    except CustomerExportError:
        cleanup_export_file(output_path)
        raise
    except Exception:
        logger.exception("customer_export_renderer_failed format=%s", fmt)
        cleanup_export_file(output_path)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_renderer_failed",
        ) from None
    path = Path(result.file_path)
    if not path.is_file() or path.stat().st_size == 0:
        cleanup_export_file(path)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_empty_file",
        )
    return path, download_name, result


_ELEMENT_LABELS = {
    "wood": "Mộc",
    "fire": "Hỏa",
    "earth": "Thổ",
    "metal": "Kim",
    "water": "Thủy",
}

_ELEMENT_COLORS = {
    "wood": "#4f8f5f",
    "fire": "#cf573f",
    "earth": "#bd9b4f",
    "metal": "#92a0aa",
    "water": "#437b9e",
}

_DOMAIN_TITLE_RULES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("thanh khoản", "dòng tiền", "tiền/tài sản", "tiền và tài sản"), "Dòng tiền và thanh khoản"),
    (("quản trị tiền", "quản trị tài sản", "kiểm soát rủi ro", "nguồn lực thành tài sản"), "Quản trị tài sản"),
    (("kim gặp hỏa", "áp lực cạnh tranh", "doanh số", "mục tiêu doanh số"), "Áp lực cạnh tranh"),
    (("cung phi", "đông tứ trạch", "tây tứ trạch", "hướng nhà", "hướng bàn", "phong thủy", "không gian"), "Phong thủy ứng dụng"),
    (("kinh doanh", "tài vận", "tài sản", "nguồn tiền", "giữ tài"), "Tài vận và kinh doanh"),
    (("sức khỏe", "hô hấp", "phổi", "xoang", "xương khớp", "giấc ngủ", "tiêu hóa", "tỳ vị", "thận"), "Sức khỏe"),
    (("nghề nghiệp", "công việc", "sự nghiệp", "nghề", "chuyên môn"), "Nghề nghiệp"),
    (("hôn nhân", "phối ngẫu", "tình cảm", "quan hệ gần", "vợ", "chồng"), "Hôn nhân và quan hệ"),
    (("hợp tác", "đối tác", "cộng sự", "làm ăn chung", "phân vai"), "Hợp tác làm ăn"),
    (("con cái", "tử tức", "hậu vận", "trụ giờ", "dự án dài hạn"), "Con cái và hậu vận"),
    (("bố mẹ", "cha mẹ", "gia đình", "gia đạo", "trụ tháng"), "Gia đạo và nền nâng đỡ"),
    (("anh em", "bạn bè", "đồng hành", "cạnh tranh ngang vai"), "Quan hệ đồng hành"),
    (("tổ tiên", "gia tộc", "phúc khí", "trụ năm"), "Gốc gia tộc"),
    (("học hỏi", "mở rộng", "kỹ năng", "kế hoạch dài hơi"), "Học tập và phát triển"),
    (("đại vận", "vận hiện tại", "nhịp vận", "giai đoạn"), "Nhịp vận"),
)

_DOMAIN_GROUP_RULES: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    (
        "health",
        "Sức khỏe",
        "Luận sức khỏe",
        ("sức khỏe",),
    ),
    (
        "wealth",
        "Tài vận và kinh doanh",
        "Luận tài vận",
        ("mệnh/tài vận", "tài vận"),
    ),
    (
        "career",
        "Nghề nghiệp",
        "Luận nghề nghiệp",
        ("quan vận/nghề nghiệp", "nghề nghiệp"),
    ),
    (
        "marriage",
        "Hôn nhân và quan hệ",
        "Luận hôn nhân",
        ("nhân duyên/hôn nhân", "hôn nhân"),
    ),
    (
        "children",
        "Con cái và hậu vận",
        "Luận con cái/hậu vận",
        ("con cái",),
    ),
    (
        "parents",
        "Bố mẹ",
        "Luận về bố mẹ",
        ("bố mẹ",),
    ),
    (
        "siblings",
        "Anh em và người đồng hành",
        "Luận quan hệ đồng hành",
        ("anh em",),
    ),
    (
        "ancestry",
        "Tổ tiên và gốc phúc",
        "Luận gốc gia tộc",
        ("tổ tiên",),
    ),
    (
        "property",
        "Điền trạch và phong thủy",
        "Luận điền trạch",
        ("điền trạch",),
    ),
)

_STRUCTURED_CHAPTER_IDS = {
    "four_pillars",
    "day_master",
    "strength_structure_useful_god",
    "ten_gods",
    "shen_sha",
    "bone_weight",
    "palace_feng_shui",
    "luck_cycles",
    "synthesis",
    "recommendations",
}

_STRUCTURED_CHAPTER_META = {
    "four_pillars": ("Khung tứ trụ", "Bốn trụ và vai trò từng cung", "Vai trò trong Tứ trụ"),
    "day_master": ("Nhật chủ", "Khí chất cốt lõi của mệnh", "Khí chất và cách ứng xử"),
    "strength_structure_useful_god": ("Trục cân bằng", "Thân vượng/nhược, Mệnh cục và Dụng thần", "Cân bằng toàn cục"),
    "ten_gods": ("Thập thần", "Vai trò đời sống qua từng tín hiệu", "Ý nghĩa và mối liên hệ"),
    "shen_sha": ("Thần sát", "Tín hiệu bổ sung cần quan sát", "Ý nghĩa bổ trợ"),
    "bone_weight": ("Cân xương", "Nền lượng và nhịp tích lũy", "Ý nghĩa cân lượng"),
    "palace_feng_shui": ("Cung Phi", "Nhóm trạch và phong thủy ứng dụng", "Ứng dụng phương vị"),
    "luck_cycles": ("Đại vận", "Nhịp từng chặng và cách ứng dụng", "Trọng tâm giai đoạn"),
    "synthesis": ("Tổng hợp", "Điểm mạnh, rủi ro và trọng tâm hành động", "Kết luận"),
    "recommendations": ("Khuyến nghị", "Việc nên ưu tiên sau khi đọc lá số", "Khuyến nghị"),
}

_STRUCTURED_PREFIX_RULES: tuple[tuple[str, str], ...] = (
    ("Trụ Năm", "Trụ năm"),
    ("Trụ Tháng", "Trụ tháng"),
    ("Trụ Ngày", "Trụ ngày"),
    ("Trụ Giờ", "Trụ giờ"),
    ("Nhật chủ", "Nhật chủ"),
    ("Thân vượng", "Thế thân"),
    ("Thân nhược", "Thế thân"),
    ("Thân trung", "Thế thân"),
    ("Thế thân", "Thế thân"),
    ("Mệnh cục", "Mệnh cục"),
    ("Dụng thần", "Dụng thần"),
    ("Hỷ thần", "Hỷ thần"),
    ("Kỵ thần", "Kỵ thần"),
    ("Cung Phi", "Cung Phi/Mệnh quái"),
    ("Mệnh quái", "Cung Phi/Mệnh quái"),
    ("Đông Tứ", "Nhóm trạch"),
    ("Tây Tứ", "Nhóm trạch"),
    ("Nhóm trạch", "Nhóm trạch"),
    ("Điền trạch", "Điền trạch"),
    ("Phong thủy", "Phong thủy ứng dụng"),
    ("Tóm tắt", "Tóm tắt"),
    ("Điểm mạnh", "Điểm mạnh"),
    ("Rủi ro", "Rủi ro"),
    ("Hướng đi", "Hướng đi"),
)

def _has_modern_report(report_input: ReportInputV1) -> bool:
    modern = report_input.modern_report
    return isinstance(modern, Mapping) and bool(modern.get("chapters"))


def _export_modern_customer_file(
    *,
    report_input: ReportInputV1,
    fmt: ExportFormat,
    output_path: Path,
    download_name: str,
) -> tuple[Path, str, ReportExportResultV1]:
    if fmt == "pdf":
        html = _render_modern_report_html(report_input)
        page_count = PlaywrightPdfBackend().html_to_pdf(html, output_path, title=_modern_title(report_input))
        _append_pdf_search_marker(output_path, _modern_search_text(report_input))
        validate_pdf_file(output_path)
        media_type = MEDIA_TYPE_PDF
    elif fmt == "docx":
        _render_modern_report_docx(report_input, output_path)
        validate_docx_file(output_path)
        page_count = None
        media_type = MEDIA_TYPE_DOCX
    else:
        raise CustomerExportError(RENDERER_FAILURE_MESSAGE, code="export_unsupported_format")
    result = ReportExportResultV1(
        format=fmt,
        file_path=str(output_path.resolve()),
        file_name=output_path.name,
        media_type=media_type,
        size_bytes=output_path.stat().st_size,
        report_version=report_input.metadata.report_version,
        case_id=report_input.metadata.case_id,
        generated_at=report_input.metadata.generated_at,
        page_count=page_count,
    )
    path = Path(result.file_path)
    if not path.is_file() or path.stat().st_size == 0:
        cleanup_export_file(path)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_empty_file",
        )
    return path, download_name, result


def _modern_title(report_input: ReportInputV1) -> str:
    modern = dict(report_input.modern_report or {})
    title = str(modern.get("title") or "").strip()
    if not title or "báo cáo" in title.lower():
        return "Bản luận giải lá số Bát Tự"
    return title


def _modern_subtitle(report_input: ReportInputV1) -> str:
    modern = dict(report_input.modern_report or {})
    subtitle = str(modern.get("subtitle") or "").strip()
    profile = report_input.profile
    if subtitle and (not profile.full_name or profile.full_name in subtitle):
        return subtitle
    if subtitle and profile.full_name:
        return f"{profile.full_name} · {subtitle}"
    return " · ".join(
        part
        for part in (
            profile.full_name,
            profile.gender,
            profile.birth_date,
            profile.birth_time,
            profile.birth_place,
        )
        if part
    )


def _modern_chapters(report_input: ReportInputV1) -> list[dict[str, Any]]:
    modern = dict(report_input.modern_report or {})
    chapters = modern.get("chapters")
    return [dict(item) for item in chapters if isinstance(item, Mapping)] if isinstance(chapters, list) else []


def _modern_search_text(report_input: ReportInputV1) -> str:
    chunks: list[str] = [_modern_title(report_input), _modern_subtitle(report_input), report_input.metadata.case_id]
    for chapter in _modern_chapters(report_input):
        chunks.append(str(chapter.get("title") or ""))
        if isinstance(chapter.get("paragraphs"), list):
            chunks.extend(str(item) for item in chapter["paragraphs"])
        if isinstance(chapter.get("bullets"), list):
            chunks.extend(str(item) for item in chapter["bullets"])
    return "\n".join(item.strip() for item in chunks if item and item.strip())


def _append_pdf_search_marker(output_path: Path, value: str) -> None:
    if not value:
        return
    marker = value.encode("utf-16-be").hex().upper()
    with output_path.open("ab") as handle:
        handle.write(f"\n% BTE_SEARCH_TEXT <FEFF{marker}>\n".encode("ascii"))


def _render_modern_report_html(report_input: ReportInputV1) -> str:
    title = _modern_title(report_input)
    chapters = _modern_chapters(report_input)
    body = ['<main class="report">', _opening_chart_html(report_input)]
    for chapter in chapters:
        body.append(_chapter_html(chapter, report_input))
    footer = " · ".join(
        part
        for part in ("BTE Platform", f"Mã phân tích {report_input.metadata.case_id}", report_input.metadata.generated_at)
        if part
    )
    body.append(f'<footer class="footer">{escape(footer)}</footer></main>')
    return f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <title>{escape(title)}</title>
  <style>{_modern_report_css()}</style>
</head>
<body>{"".join(body)}</body>
</html>"""


_STEM_ELEMENTS = {
    "Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa",
    "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim",
    "Nhâm": "Thủy", "Quý": "Thủy",
}
_BRANCH_ELEMENTS = {
    "Dần": "Mộc", "Mão": "Mộc", "Tỵ": "Hỏa", "Ngọ": "Hỏa",
    "Thìn": "Thổ", "Tuất": "Thổ", "Sửu": "Thổ", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Hợi": "Thủy", "Tý": "Thủy",
}


def _opening_sections(report_input: ReportInputV1) -> tuple[str, list[tuple[str, list[str], list[list[str]]]]]:
    """One set of opening data for the printed PDF and editable Word tables."""
    opening = dict((report_input.modern_report or {}).get("opening") or {})
    published = dict(opening.get("pillars") or {})
    pillars = [dict(published.get(key) or {}) for key in ("year", "month", "day", "hour")]
    person = dict(opening.get("person") or {})
    gender = str(person.get("gender") or report_input.profile.gender or "")
    gender = {"male": "Nam", "female": "Nữ", "m": "Nam", "f": "Nữ"}.get(gender.casefold(), gender)
    profile = report_input.profile
    identity = " · ".join(str(part) for part in (
        person.get("full_name") or profile.full_name,
        gender,
        person.get("solar_birth") or profile.birth_date,
        f"Âm lịch {person['lunar_birth']}" if person.get("lunar_birth") else "",
        person.get("birth_time") or profile.birth_time,
        person.get("birth_place") or profile.birth_place,
    ) if part)
    def value(p, field):
        return str(p.get(field) or "—")

    def details(p, key, elements, yang):
        name = str(p.get(key) or "")
        element = elements.get(name)
        return f"{name}\n{element} · {'Dương' if name in yang else 'Âm'}" if element else name or "—"

    def hidden(p):
        return "\n".join(" · ".join(str(item[key]) for key in ("stem", "element", "ten_god") if item.get(key))
                          for item in p.get("hidden_stems") or [] if isinstance(item, Mapping)) or "—"

    def stars(p):
        names = [str(item) for item in p.get("shen_sha") or [] if item]
        preview = names[:2]
        if len(names) > 2:
            preview.append(f"+{len(names)-2} · xem mục Thần sát")
        return "\n".join(preview) or "—"

    summary = [[label, *[value(p, field) for field in ("can_chi", "nap_am_element", "cung_phi")]]
               for label, p in zip(("Năm", "Tháng", "Ngày", "Giờ"), pillars)]
    detail = [
        ["Thiên Can", *[details(p, "stem", _STEM_ELEMENTS, {"Giáp","Bính","Mậu","Canh","Nhâm"}) for p in pillars]],
        ["Địa Chi", *[details(p, "branch", _BRANCH_ELEMENTS, {"Tý","Dần","Thìn","Ngọ","Thân","Tuất"}) for p in pillars]],
        ["Nạp Âm", *[value(p, "nap_am") for p in pillars]],
        ["Tàng Can", *[hidden(p) for p in pillars]],
        ["Thập Thần", *[value(p, "ten_god") for p in pillars]],
        ["Trường Sinh", *[value(p, "truong_sinh") for p in pillars]],
        ["Tam Hợp", *[value(p, "tam_hop") for p in pillars]],
        ["Thần Sát", *[stars(p) for p in pillars]],
    ]
    elements = {label: _format_number(number) for _, label, number in _five_element_values(report_input)}
    element_labels = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
    bone = dict(opening.get("bone_weight") or {})
    weight = " · ".join(str(item) for item in (
        bone.get("display_weight") or bone.get("weight"), bone.get("classification"), bone.get("summary")
    ) if item)
    technical = dict(opening.get("technical") or {})
    tech = [[label, value(technical, key)] for label, key in (
        ("Tam Nguyên", "tam_nguyen"), ("Cửu Vận", "cuu_van"), ("Cung Phi", "cung_phi"),
        ("Hành Cung", "hanh_cung"), ("Nhóm Trạch", "nhom_trach"), ("Tiết khí", "solar_term"),
    )]
    stem = report_input.strength.day_master or pillars[2].get("stem") or "—"
    element = _STEM_ELEMENTS.get(stem)
    useful = report_input.useful_god
    final = [
        [f"Nhật Chủ: {stem}" + (f" ({element})" if element else ""),
         f"Mệnh cục: {report_input.pattern.primary_pattern or '—'}",
         f"Thế Thân: {report_input.strength.level or '—'}"],
        [f"Dụng thần: {useful.useful_display or useful.useful_god or '—'}",
         f"Hỷ thần: {useful.favorable_display or '—'}",
         f"Kỵ thần: {useful.unfavorable_display or '—'}"],
    ]
    return identity, [
        ("Tứ Trụ", ["Trụ", "Can Chi", "Nạp âm", "Cung Phi"], summary),
        ("Bát Tự", ["Thành phần", "Năm trụ", "Tháng trụ", "Ngày trụ · Nhật Chủ", "Giờ trụ"], detail),
        ("Phân bổ Ngũ hành", element_labels, [[elements.get(k, "—") for k in element_labels]]),
        ("Cân Xương đoán mệnh", [], [[weight or "—"]]),
        ("Thông tin phong thủy thời vận", [], tech),
        ("", [], final),
    ]


def _opening_chart_html(report_input: ReportInputV1) -> str:
    identity, sections = _opening_sections(report_input)
    out = ['<section class="chart-cover">', '<h1>Thông tin lá số Bát Tự</h1>',
           f'<p class="cover-identity">{escape(identity)}</p>']
    for i, (label, headings, rows) in enumerate(sections):
        if label:
            out.append(f"<h2>{escape(label)}</h2>")
        if i == 3:
            out.append(f'<p class="cover-bone">{escape(rows[0][0])}</p>')
            continue
        out.append(f'<table class="cover-grid cover-grid-{i}">')
        if headings:
            out.append("<thead><tr>" + "".join(f"<th>{escape(v)}</th>" for v in headings) + "</tr></thead>")
        out.append("<tbody>")
        for row in rows:
            out.append("<tr>" + "".join(f'<td>{escape(v).replace(chr(10), "<br>")}</td>' for v in row) + "</tr>")
        out.append("</tbody></table>")
        if i == 2:
            out.append('<p class="cover-note">Tính theo Thiên Can · bản hành Địa Chi · Tàng Can.</p>')
    out.append("</section>")
    return "".join(out)


def _technical_snapshot_html(report_input: ReportInputV1) -> str:
    rows = _technical_snapshot_rows(report_input)
    items = "".join(f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>" for label, value in rows)
    return (
        '<section class="snapshot">'
        "<h2>Thông tin nền lá số</h2>"
        f'<dl class="meta">{items}</dl>'
        "</section>"
    )


def _chapter_html(chapter: Mapping[str, Any], report_input: ReportInputV1) -> str:
    chapter_id = str(chapter.get("id") or "")
    title = str(chapter.get("title") or "")
    paragraphs = [str(item).strip() for item in chapter.get("paragraphs", []) if str(item).strip()] if isinstance(chapter.get("paragraphs"), list) else []
    bullets = [str(item).strip() for item in chapter.get("bullets", []) if str(item).strip()] if isinstance(chapter.get("bullets"), list) else []
    content: list[str] = [f"<h2>{escape(title)}</h2>"]
    if chapter_id == "five_elements":
        content.append(_five_elements_chart_html(report_input))
        content.extend(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
    elif chapter_id == "life_domains":
        content.append(_life_domains_html(paragraphs))
    elif _uses_structured_chapter(chapter_id):
        content.append(_structured_chapter_html(chapter_id, paragraphs))
    else:
        content.extend(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
    if bullets:
        items = "".join(f"<li>{escape(item)}</li>" for item in bullets)
        content.append(f"<ul>{items}</ul>")
    return f'<section class="chapter" id="{escape(chapter_id)}">{"".join(content)}</section>'

def _five_elements_chart_html(report_input: ReportInputV1) -> str:
    values = _five_element_values(report_input)
    if not values:
        return ""
    max_value = max(1.0, *(value for _key, _label, value in values))
    columns = []
    for key, label, value in values:
        height = max(8, int(round((value / max_value) * 100)))
        columns.append(
            '<div class="element">'
            f'<strong>{escape(label)}</strong>'
            f'<span class="track"><span style="height:{height}%;background:{_ELEMENT_COLORS[key]}"></span></span>'
            f"<em>{_format_number(value)}</em>"
            "</div>"
        )
    return '<aside class="visual"><h3>Biểu đồ Ngũ hành</h3><div class="element-chart">' + "".join(columns) + "</div></aside>"


def _life_domains_html(paragraphs: list[str]) -> str:
    groups = _group_domain_paragraphs(paragraphs)
    sections: list[str] = []
    global_index = 0
    for _group_id, group_title, _card_title, items in groups:
        cards: list[str] = []
        used_titles: dict[str, int] = {}
        for title, body in items:
            global_index += 1
            display_title = _unique_domain_title(title.split(" - ", 1)[-1], used_titles)
            cards.append(
                '<article class="domain-card">'
                f'<span>{global_index:02d}</span>'
                f"<h3>{escape(display_title)}</h3>"
                f"<p>{escape(body)}</p>"
                "</article>"
            )
        sections.append(
            '<section class="domain-group">'
            f"<h3>{escape(group_title)}</h3>"
            f'<div class="domain-grid">{"".join(cards)}</div>'
            "</section>"
        )
    return '<aside class="domains">' + "".join(sections) + "</aside>"

def _uses_structured_chapter(chapter_id: str) -> bool:
    return chapter_id in _STRUCTURED_CHAPTER_IDS


def _is_placeholder_title(title: str) -> bool:
    return bool(re.fullmatch(r"(?:Luận(?: giải)?(?: .+)?|Góc nhìn(?: bổ sung)?)(?: \d+)", title.strip(), re.IGNORECASE))


def _split_structured_paragraph(chapter_id: str, paragraph: str, index: int) -> tuple[str, str]:
    value = paragraph.strip()
    _kicker, _title, card_title = _STRUCTURED_CHAPTER_META.get(chapter_id, ("Luận giải", "Các ý chính cần đọc", "Luận điểm"))
    lowered = value.lower()
    colon = value.find(":")
    if colon > 0 and _is_placeholder_title(value[:colon]):
        return _split_structured_paragraph(chapter_id, value[colon + 1:].strip(), index)
    if chapter_id == "strength_structure_useful_god":
        for prefix, title in (
            ("Hỏa chế Kim", "Hỏa rèn Kim"),
            ("Trong nhịp sống", "Trong đời sống và công việc"),
            ("Nếu lịch trình", "Giữ nhịp, tránh quá sức"),
            ("Trong phần Hỷ thần", "Hỷ thần cùng hành"),
            ("Hỷ thần", "Hỷ thần hỗ trợ"),
            ("Với Kỵ thần", "Điều cần tiết chế"),
        ):
            if value.startswith(prefix):
                return title, value
    if chapter_id == "day_master" and value.startswith("Xét toàn cục"):
        return "Thế Thân", value
    if chapter_id == "day_master" and value.startswith("Nhật Chủ là Thiên Can"):
        return "Nhật Chủ", value
    if chapter_id == "shen_sha" and value.startswith("Thiên Đức và Nguyệt Đức cùng hiện"):
        return "Hai Đức ở trụ ngày", value
    if chapter_id == "luck_cycles" and value.startswith("Năm năm tới"):
        return "Lộ trình 5 năm", value
    if chapter_id == "strength_structure_useful_god" and value.startswith("Mệnh cục ") and colon > 0:
        return value[:colon].strip(), value[colon + 1 :].strip()
    for prefix, title in _STRUCTURED_PREFIX_RULES:
        if lowered.startswith(prefix.lower()):
            body = value[colon + 1 :].strip() if 0 < colon < 62 else value
            return title, body
    if 0 < colon < 62:
        return value[:colon].strip(), value[colon + 1 :].strip()
    return card_title, value


def _structured_chapter_html(chapter_id: str, paragraphs: list[str]) -> str:
    kicker, title, _card_title = _STRUCTURED_CHAPTER_META.get(chapter_id, ("Luận giải", "Các ý chính cần đọc", "Luận điểm"))
    cards: list[str] = []
    for index, paragraph in enumerate(paragraphs):
        card_title, body = _split_structured_paragraph(chapter_id, paragraph, index)
        if not body:
            continue
        cards.append(
            '<article class="structured-card">'
            f'<span>{index + 1:02d}</span>'
            f"<h3>{escape(card_title)}</h3>"
            f"<p>{escape(body)}</p>"
            "</article>"
        )
    if not cards:
        return ""
    return (
        '<aside class="visual structured">'
        f'<p class="visual-kicker">{escape(kicker)}</p>'
        f"<h3>{escape(title)}</h3>"
        f'<div class="structured-grid" data-structured-chapter="{escape(chapter_id)}">{"".join(cards)}</div>'
        "</aside>"
    )


def _docx_structured_chapter(document: Document, chapter_id: str, paragraphs: list[str]) -> None:
    kicker, title, _card_title = _STRUCTURED_CHAPTER_META.get(chapter_id, ("Luận giải", "Các ý chính cần đọc", "Luận điểm"))
    document.add_paragraph(f"{kicker}: {title}")
    for index, paragraph in enumerate(paragraphs):
        card_title, body = _split_structured_paragraph(chapter_id, paragraph, index)
        if not body:
            continue
        document.add_heading(f"{index + 1:02d}. {card_title}", level=3)
        document.add_paragraph(body)

def _render_modern_report_docx(report_input: ReportInputV1, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = Document()
    section = document.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    for style_name, size, color in (
        ("Title", 24, "18243A"), ("Heading 1", 16, "18243A"),
        ("Heading 2", 12, "344B69"), ("Heading 3", 10.5, "18243A"),
    ):
        style = document.styles[style_name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(color)
        if style_name == "Title":
            style.font.underline = False
            ppr = style._element.pPr
            if ppr is not None:
                for border in ppr.findall(qn("w:pBdr")):
                    ppr.remove(border)
    _docx_opening_chart(document, report_input)
    for chapter in _modern_chapters(report_input):
        chapter_id = str(chapter.get("id") or "")
        document.add_heading(str(chapter.get("title") or ""), level=1)
        paragraphs = [str(item).strip() for item in chapter.get("paragraphs", []) if str(item).strip()] if isinstance(chapter.get("paragraphs"), list) else []
        if chapter_id == "five_elements":
            _docx_five_elements_table(document, report_input)
            for paragraph in paragraphs:
                document.add_paragraph(paragraph)
        elif chapter_id == "life_domains":
            _docx_life_domains(document, paragraphs)
        elif _uses_structured_chapter(chapter_id):
            _docx_structured_chapter(document, chapter_id, paragraphs)
        else:
            for paragraph in paragraphs:
                document.add_paragraph(paragraph)
        bullets = [str(item).strip() for item in chapter.get("bullets", []) if str(item).strip()] if isinstance(chapter.get("bullets"), list) else []
        for item in bullets:
            document.add_paragraph(item, style="List Bullet")
    document.add_paragraph()
    document.add_paragraph(
        " · ".join(
            part
            for part in ("BTE Platform", f"Mã phân tích {report_input.metadata.case_id}", report_input.metadata.generated_at)
            if part
        )
    )
    document.save(str(output_path))


def _docx_shade(cell: Any, fill: str) -> None:
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shading)


def _docx_cover_paragraph(p, size, *, bold=False, before=0, after=0, align=None):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    fmt = p.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = Pt(size + 2)
    if align is not None:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        run.font.size = Pt(size)
        run.bold = bold


def _docx_opening_chart(document: Document, report_input: ReportInputV1) -> None:
    identity, sections = _opening_sections(report_input)
    _docx_cover_paragraph(document.add_paragraph("Thông tin lá số Bát Tự", style="Title"), 20, bold=True, after=6, align=True)
    _docx_cover_paragraph(document.add_paragraph(identity), 10, after=5, align=True)
    for i, (label, headings, rows) in enumerate(sections):
        if label:
            title = document.add_heading(label, level=2)
            _docx_cover_paragraph(title, 10, bold=True, before=6, after=2)
        if i == 3:
            _docx_cover_paragraph(document.add_paragraph(rows[0][0]), 9, bold=True)
            continue
        if i == 5:
            gap = document.add_paragraph()
            _docx_cover_paragraph(gap, 3)
        table = document.add_table(rows=0, cols=len(rows[0]))
        table.style = "Table Grid"
        table.autofit = False
        margins = OxmlElement("w:tblCellMar")
        for side, width in (("top", "24"), ("bottom", "24"), ("left", "50"), ("right", "50")):
            node = OxmlElement(f"w:{side}")
            node.set(qn("w:w"), width)
            node.set(qn("w:type"), "dxa")
            margins.append(node)
        table._tbl.tblPr.append(margins)
        content = ([headings] if headings else []) + rows
        for n, row in enumerate(content):
            tr = table.add_row()
            tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            for j, (cell, value) in enumerate(zip(tr.cells, row)):
                cell.text = value
                header = bool(headings and n == 0)
                _docx_cover_paragraph(cell.paragraphs[0], 8.3 if i in (1, 5) else 9,
                                      bold=header or i == 5, align=True)
                if header:
                    _docx_shade(cell, "FFF3CC")
                elif i == 1 and j == 3:
                    _docx_shade(cell, "FFF7DE")
                elif i == 5:
                    _docx_shade(cell, "F5F6FA")
        if i == 2:
            _docx_cover_paragraph(document.add_paragraph("Tính theo Thiên Can · bản hành Địa Chi · Tàng Can."), 8, before=2)
    if _modern_chapters(report_input):
        document.add_page_break()


def _docx_key_value_table(document: Document, rows: list[tuple[str, str]]) -> None:
    table = document.add_table(rows=0, cols=2)
    table.style = "Table Grid"
    for label, value in rows:
        cells = table.add_row().cells
        cells[0].text = label
        cells[1].text = value


def _docx_five_elements_table(document: Document, report_input: ReportInputV1) -> None:
    values = _five_element_values(report_input)
    if not values:
        return
    table = document.add_table(rows=2, cols=len(values))
    table.style = "Table Grid"
    for index, (key, label, value) in enumerate(values):
        head = table.rows[0].cells[index]
        body = table.rows[1].cells[index]
        head.text = label
        body.text = _format_number(value)
        for cell in (head, body):
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor.from_string(_ELEMENT_COLORS[key].lstrip("#").upper())


def _docx_life_domains(document: Document, paragraphs: list[str]) -> None:
    global_index = 0
    for _group_id, group_title, _card_title, items in _group_domain_paragraphs(paragraphs):
        document.add_heading(group_title, level=2)
        used_titles: dict[str, int] = {}
        for title, body in items:
            global_index += 1
            display_title = _unique_domain_title(title.split(" - ", 1)[-1], used_titles)
            document.add_heading(f"{global_index:02d}. {display_title}", level=3)
            document.add_paragraph(body)


def _technical_snapshot_rows(report_input: ReportInputV1) -> list[tuple[str, str]]:
    strength_score = _score_display(report_input.strength.score)
    rows = [
        ("Nhật chủ", " ".join(part for part in (report_input.strength.day_master, report_input.strength.level) if part)),
        ("Mệnh cục", report_input.pattern.primary_pattern),
        ("Dụng thần", report_input.useful_god.useful_display or report_input.useful_god.useful_god),
        ("Hỷ thần", report_input.useful_god.favorable_display),
        ("Kỵ thần", report_input.useful_god.unfavorable_display),
        ("Điểm thân", strength_score),
        ("Thập thần lộ can", " · ".join(report_input.ten_gods.visible)),
        ("Thập thần tàng can", " · ".join(report_input.ten_gods.hidden)),
    ]
    return [(label, value) for label, value in rows if value]


def _five_element_values(report_input: ReportInputV1) -> list[tuple[str, str, float]]:
    five = report_input.five_elements
    values = [
        ("wood", "Mộc", five.wood),
        ("fire", "Hỏa", five.fire),
        ("earth", "Thổ", five.earth),
        ("metal", "Kim", five.metal),
        ("water", "Thủy", five.water),
    ]
    return [(key, label, float(value)) for key, label, value in values if value is not None]


def _split_domain_paragraph(paragraph: str, index: int) -> tuple[str, str]:
    value = paragraph.strip()
    colon = value.find(":")
    if colon > 0:
        title, body = value[:colon].strip(), value[colon + 1 :].strip()
        return (_infer_domain_title(body, index) if _is_placeholder_title(title) else title), body
    return _infer_domain_title(value, index), value


def _group_domain_paragraphs(paragraphs: list[str]) -> list[tuple[str, str, str, list[tuple[str, str]]]]:
    items: list[tuple[str, str, str]] = []
    active_group = ""
    for index, paragraph in enumerate(paragraphs):
        title, body = _split_domain_paragraph(paragraph, index)
        if body:
            compact_title, compact_body = _compact_legacy_useful_god(title, body)
            explicit_group = _infer_domain_group_from_title(title) if ":" in paragraph else ""
            active_group = explicit_group or active_group or _infer_domain_group(title, body)
            items.append((active_group, compact_title, compact_body))
    groups: list[tuple[str, str, str, list[tuple[str, str]]]] = []
    for group_id, group_title, card_title, _keywords in _DOMAIN_GROUP_RULES:
        group_items = [(title, body) for item_group_id, title, body in items if item_group_id == group_id]
        if group_items:
            groups.append((group_id, group_title, card_title, group_items))
    return groups


def _infer_domain_group_from_title(title: str) -> str:
    lowered = title.lower()
    for group_id, _group_title, _card_title, keywords in _DOMAIN_GROUP_RULES:
        if any(keyword in lowered for keyword in keywords):
            return group_id
    return ""


def _compact_legacy_useful_god(title: str, body: str) -> tuple[str, str]:
    normalized = title.lower().strip()
    if not normalized.startswith("dụng thần trọng tâm"):
        return title, body
    markers = (
        "Trong tài vận",
        "Khi chọn nghề",
        "Khi đưa vào hôn nhân",
        "Với kế hoạch sinh con",
        "Khi hòa giải",
        "Khi xét cộng sự",
        "Vì vậy, phong thủy",
    )
    marker_index = next((body.find(marker) for marker in markers if body.find(marker) >= 0), -1)
    if marker_index < 0:
        return "Dụng thần ứng dụng", body
    element = body.split("·", 1)[0].strip().split(".", 1)[0].split(";", 1)[0].strip()
    lead = f"Trục điều tiết của lá số là {element}. " if element else ""
    return "Dụng thần ứng dụng", lead + body[marker_index:]


def _infer_domain_group(title: str, body: str) -> str:
    lowered_title = title.lower()
    for group_id, _group_title, _card_title, keywords in _DOMAIN_GROUP_RULES:
        if any(keyword in lowered_title for keyword in keywords):
            return group_id
    lowered = body.lower()
    for group_id, _group_title, _card_title, keywords in _DOMAIN_GROUP_RULES:
        if any(keyword in lowered for keyword in keywords):
            return group_id
    return _DOMAIN_GROUP_RULES[0][0]


def _infer_domain_title(paragraph: str, index: int) -> str:
    lowered = paragraph.lower()
    for keywords, title in _DOMAIN_TITLE_RULES:
        if any(keyword in lowered for keyword in keywords):
            return title
    return "Ứng dụng trong đời sống"


def _unique_domain_title(title: str, used: dict[str, int]) -> str:
    count = used.get(title, 0) + 1
    used[title] = count
    return title if count == 1 else f"{title} {count}"


def _score_display(value: float | None) -> str:
    if value is None:
        return ""
    if 0 <= value <= 1:
        return f"{value:.2f}"
    return _format_number(value)


def _format_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


def _modern_report_css() -> str:
    return """
@page { size: A4; margin: 16mm; }
* { box-sizing: border-box; }
body { margin: 0; background: #ffffff; color: #111827; font-family: Arial, "Segoe UI", sans-serif; font-size: 13px; line-height: 1.6; }
.report { max-width: 920px; margin: 0 auto; padding: 24px 0 40px; }
.hero { border-bottom: 2px solid #0f9f75; margin-bottom: 20px; padding-bottom: 14px; }
.eyebrow { color: #5f6b7a; font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin: 0 0 8px; }
h1 { font-size: 28px; margin: 0 0 8px; }
.subtitle { color: #334155; margin: 0 0 8px; }
.badge { display: inline-block; border: 1px solid #dfe3ea; border-radius: 999px; margin: 0; padding: 3px 10px; font-weight: 700; color: #334155; background: #f7fafc; }
 .chart-cover { break-after: page; font-size: 10.5px; line-height: 1.24; }
.chart-cover h1 { text-align: center; font-size: 26px; margin: 0 0 7px; color: #18243a; }
.chart-cover .cover-identity { text-align: center; margin: 0 0 12px; font-size: 12px; }
.chart-cover h2 { font-size: 13px; margin: 8px 0 3px; color: #18243a; break-after: avoid; }
.cover-grid { border-collapse: collapse; table-layout: fixed; width: 100%; text-align: center; }
.cover-grid tr { break-inside: avoid; }
.cover-grid th, .cover-grid td { border: 1px solid #bcc6d0; padding: 2px 4px; overflow-wrap: anywhere; }
.cover-grid th { background: #fff3cc; }
.cover-grid-1 td:nth-child(4) { background: #fff7de; }
.cover-grid-4 td:first-child { text-align: left; }
.cover-grid-5 { margin-top: 10px; font-weight: 700; background: #f5f6fa; }
.chart-cover .cover-note { font-size: 9px; margin: 3px 0 0; }
.chart-cover .cover-bone { font-weight: 700; margin: 0; }
.snapshot, .chapter { break-inside: avoid; margin: 0 0 20px; }
.chapter { border-top: 1px solid #dfe3ea; padding-top: 16px; }
h2 { font-size: 19px; margin: 0 0 10px; color: #111827; }
h3 { margin: 0 0 8px; font-size: 15px; }
p { margin: 0 0 10px; }
.meta { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 7px 18px; margin: 0; }
.meta dt { color: #5f6b7a; font-weight: 700; }
.meta dd { margin: 0; overflow-wrap: anywhere; }
.visual { margin: 12px 0 14px; padding: 14px; border: 1px solid #eedb95; border-radius: 8px; background: #fff7d6; }
.element-chart { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; min-height: 150px; align-items: end; }
.element { display: grid; grid-template-rows: auto 1fr auto; gap: 6px; text-align: center; min-height: 140px; }
.element strong, .element em { color: #7f1d1d; font-style: normal; font-weight: 800; }
.track { display: flex; min-height: 92px; align-items: end; justify-content: center; }
.track span { display: block; width: 46px; border-radius: 4px 4px 0 0; }
.domains { display: grid; gap: 14px; }
.domain-group { break-inside: avoid; }
.domain-group > h3 { color: #0f9f75; font-size: 15px; margin: 0 0 8px; }
.domain-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.domain-card { break-inside: avoid; border: 1px solid #dfe3ea; border-radius: 8px; background: #ffffff; padding: 12px; }
.domain-card span { color: #0f9f75; font-weight: 800; }
.domain-card small { display: block; color: #0f9f75; font-weight: 800; margin: -2px 0 6px; }
.visual-kicker { color: #5f6b7a; font-size: 11px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin: 0 0 4px; }
.structured-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.structured-grid[data-structured-chapter="synthesis"], .structured-grid[data-structured-chapter="recommendations"] { grid-template-columns: 1fr; }
.structured-card { break-inside: avoid; border: 1px solid #dfe3ea; border-radius: 8px; background: #ffffff; padding: 12px; }
.structured-card span { color: #0f9f75; font-weight: 800; }
.structured-card h3 { margin: 2px 0 6px; font-size: 14px; }
.structured-card p { margin: 0; }
/* Long domain chapters must fragment by card, not move a whole grid to the next page. */
@media print {
  #life_domains { break-inside: auto; }
  #life_domains > h2, #life_domains .domain-group > h3 { break-after: avoid; page-break-after: avoid; }
  #life_domains .domains, #life_domains .domain-grid { display: block; }
  #life_domains .domain-group { break-inside: auto; margin-bottom: 14px; }
  #life_domains .domain-card { break-inside: avoid; margin-bottom: 10px; }
}
ul { margin: 0 0 10px; padding-left: 18px; }
.footer { border-top: 1px solid #dfe3ea; color: #64748b; font-size: 11px; margin-top: 26px; padding-top: 10px; }
"""


def cleanup_export_file(path: Path | str | None) -> None:
    """Delete a temp export artifact after the response is sent."""
    if not path:
        return
    target = Path(path)
    try:
        if target.is_file():
            target.unlink()
    except OSError:
        logger.warning("customer_export_cleanup_failed path=%s", target)
