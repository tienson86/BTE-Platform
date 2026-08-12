"""DOCX Export V1 — editable Word report from ReportInputV1."""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Cm, Pt

from engines.report_engine.contracts.report_export_result_v1 import (
    EXPORT_FORMAT_DOCX,
    MEDIA_TYPE_DOCX,
    ReportExportResultV1,
)
from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportPillarV1,
    missing_data_message,
)
from engines.report_engine.exporting.filename import build_export_filename

logger = logging.getLogger(__name__)

DOCX_MIN_BYTES = 2048

_DOMAIN_ALIASES: dict[str, tuple[str, ...]] = {
    "career": ("su_nghiep", "career", "nghiep", "nghề"),
    "wealth": ("tai_van", "wealth", "tai", "tài"),
    "marriage": ("hon_nhan", "relationship", "hon", "hôn"),
    "health": ("suc_khoe", "health", "sức"),
    "children": ("tu_tuc", "children", "con"),
}


class DocxExporterV1:
    """Export ReportInputV1 to a real OpenXML DOCX document."""

    def export(
        self,
        report_input: ReportInputV1,
        output_path: Path,
    ) -> ReportExportResultV1:
        """Build and save DOCX to output_path."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        document = Document()
        self._configure_page(document)
        self._apply_styles(document)
        self._render(document, report_input)
        document.save(str(output_path))
        validate_docx_file(output_path)
        logger.info(
            "report_export_docx case_id=%s path=%s size=%s",
            report_input.metadata.case_id,
            output_path,
            output_path.stat().st_size,
        )
        return ReportExportResultV1(
            format=EXPORT_FORMAT_DOCX,
            file_path=str(output_path.resolve()),
            file_name=output_path.name,
            media_type=MEDIA_TYPE_DOCX,
            size_bytes=output_path.stat().st_size,
            report_version=report_input.metadata.report_version,
            case_id=report_input.metadata.case_id,
            generated_at=report_input.metadata.generated_at,
            page_count=None,
        )

    def _configure_page(self, document: Document) -> None:
        section = document.sections[0]
        section.page_height = Cm(29.7)
        section.page_width = Cm(21.0)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)

    def _apply_styles(self, document: Document) -> None:
        normal = document.styles["Normal"]
        normal.font.name = "Arial"
        normal.font.size = Pt(11)

    def _render(self, document: Document, report_input: ReportInputV1) -> None:
        profile = report_input.profile
        document.add_heading("BÁO CÁO LUẬN GIẢI BÁT TỰ", level=0)
        document.add_paragraph(profile.full_name or "—")
        document.add_paragraph(
            f"{report_input.metadata.case_id} · {report_input.metadata.generated_at}"
        )
        document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

        self._heading(document, "01. Thông tin lá số")
        self._key_value_table(
            document,
            [
                ("Họ tên", profile.full_name),
                ("Giới tính", profile.gender),
                ("Ngày sinh", profile.birth_date),
                ("Giờ sinh", profile.birth_time),
                ("Nơi sinh", profile.birth_place),
                ("Múi giờ", profile.timezone),
                ("Dương lịch", report_input.calendar.solar_date),
                ("Âm lịch", report_input.calendar.lunar_date),
                ("Tiết khí", report_input.calendar.solar_term),
            ],
        )

        self._heading(document, "02. Tứ Trụ")
        self._pillars_table(document, report_input)

        self._heading(document, "03. Ngũ hành")
        five = report_input.five_elements
        self._key_value_table(
            document,
            [
                ("Mộc", _fmt_optional(five.wood)),
                ("Hỏa", _fmt_optional(five.fire)),
                ("Thổ", _fmt_optional(five.earth)),
                ("Kim", _fmt_optional(five.metal)),
                ("Thủy", _fmt_optional(five.water)),
            ],
        )

        self._heading(document, "04. Thân vượng nhược")
        strength = report_input.strength
        self._key_value_table(
            document,
            [
                ("Nhật chủ", strength.day_master),
                ("Điểm", _fmt_optional(strength.score)),
                ("Mức", strength.level),
                ("Phân loại", strength.classification),
            ],
        )
        if strength.summary:
            document.add_paragraph(strength.summary)

        self._heading(document, "05. Thập thần")
        ten_gods = report_input.ten_gods
        self._key_value_table(
            document,
            [
                ("Hiển", ", ".join(ten_gods.visible)),
                ("Ẩn can", ", ".join(ten_gods.hidden)),
                ("Tóm tắt", ten_gods.summary),
            ],
        )

        self._heading(document, "06. Mệnh cục / Cách cục")
        pattern = report_input.pattern
        self._key_value_table(
            document,
            [
                ("Cách chính", pattern.primary_pattern),
                ("Cách phụ", ", ".join(pattern.secondary_patterns)),
                ("Theo cách", pattern.follow_pattern),
                ("Trạng thái", pattern.status),
            ],
        )
        if pattern.explanation:
            document.add_paragraph(pattern.explanation)

        self._heading(document, "07. Dụng thần – Hỷ thần – Kỵ thần")
        useful = report_input.useful_god
        self._key_value_table(
            document,
            [
                ("Dụng thần", useful.useful_god),
                ("Hỷ thần", ", ".join(useful.favorable_gods)),
                ("Kỵ thần", ", ".join(useful.unfavorable_gods)),
                ("Trung tính", ", ".join(useful.neutral_gods)),
            ],
        )
        if useful.reasoning:
            document.add_paragraph(useful.reasoning)

        self._heading(document, "08. Thần sát")
        if report_input.shensha:
            table = document.add_table(rows=1, cols=4)
            table.style = "Table Grid"
            headers = table.rows[0].cells
            headers[0].text = "Tên"
            headers[1].text = "Loại"
            headers[2].text = "Hiện diện"
            headers[3].text = "Bằng chứng"
            for item in report_input.shensha:
                row = table.add_row().cells
                row[0].text = item.name
                row[1].text = item.category
                row[2].text = "Có" if item.present else "Không"
                row[3].text = item.evidence
        else:
            document.add_paragraph(missing_data_message())

        self._heading(document, "09. Đại vận")
        luck = report_input.luck_cycles
        if luck.cycles:
            table = document.add_table(rows=1, cols=6)
            table.style = "Table Grid"
            hdr = table.rows[0].cells
            for index, label in enumerate(
                ("#", "Can Chi", "Từ năm", "Đến năm", "Tuổi", "Tóm tắt")
            ):
                hdr[index].text = label
            for cycle in luck.cycles:
                row = table.add_row().cells
                row[0].text = str(cycle.index)
                row[1].text = f"{cycle.stem} {cycle.branch}".strip()
                row[2].text = str(cycle.start_year or "—")
                row[3].text = str(cycle.end_year or "—")
                row[4].text = f"{cycle.age_start or '—'} – {cycle.age_end or '—'}"
                row[5].text = cycle.summary
        else:
            document.add_paragraph(missing_data_message())

        interpretation = report_input.interpretation
        self._heading(document, "10. Luận giải tổng thể")
        self._paragraphs(
            document,
            interpretation.executive_summary
            or _first_section_content(interpretation.sections),
        )

        self._domain_section(document, report_input, "11. Nghề nghiệp", "career")
        self._domain_section(document, report_input, "12. Tài vận", "wealth")
        self._domain_section(document, report_input, "13. Hôn nhân", "marriage")
        self._domain_section(document, report_input, "14. Sức khỏe", "health")
        self._domain_section(document, report_input, "15. Tử tức", "children")

        self._heading(document, "16. Khuyến nghị")
        if interpretation.recommendations:
            for item in interpretation.recommendations:
                document.add_paragraph(item, style="List Bullet")
        else:
            document.add_paragraph(missing_data_message())

        self._heading(document, "17. Tổng kết")
        conclusion = interpretation.conclusion or _last_section_content(
            interpretation.sections
        )
        self._paragraphs(document, conclusion)

        document.add_paragraph()
        document.add_paragraph(
            f"BTE Platform · Report V1 · {report_input.metadata.report_version}",
            style="Caption",
        )

    def _heading(self, document: Document, title: str) -> None:
        document.add_heading(title, level=1)

    def _key_value_table(
        self,
        document: Document,
        rows: list[tuple[str, str]],
    ) -> None:
        populated = [(label, value) for label, value in rows if value]
        if not populated:
            document.add_paragraph(missing_data_message())
            return
        table = document.add_table(rows=0, cols=2)
        table.style = "Table Grid"
        for label, value in populated:
            cells = table.add_row().cells
            cells[0].text = label
            cells[1].text = value

    def _pillars_table(self, document: Document, report_input: ReportInputV1) -> None:
        table = document.add_table(rows=1, cols=5)
        table.style = "Table Grid"
        header = table.rows[0].cells
        for index, label in enumerate(("Trụ", "Can Chi", "Ẩn can", "Nạp âm", "Thập thần")):
            header[index].text = label
        pillars = report_input.pillars
        for label, pillar in (
            ("Năm", pillars.year),
            ("Tháng", pillars.month),
            ("Ngày", pillars.day),
            ("Giờ", pillars.hour),
        ):
            row = table.add_row().cells
            row[0].text = label
            row[1].text = f"{pillar.stem} {pillar.branch}".strip()
            row[2].text = ", ".join(pillar.hidden_stems) if pillar.hidden_stems else "—"
            row[3].text = pillar.na_yin or "—"
            row[4].text = pillar.ten_god or "—"

    def _domain_section(
        self,
        document: Document,
        report_input: ReportInputV1,
        title: str,
        key: str,
    ) -> None:
        self._heading(document, title)
        section = _find_section(report_input.interpretation.sections, key)
        if section is None or not section.content.strip():
            document.add_paragraph(missing_data_message())
            return
        self._paragraphs(document, section.content)

    def _paragraphs(self, document: Document, text: str) -> None:
        if not text or not text.strip():
            document.add_paragraph(missing_data_message())
            return
        for block in text.split("\n\n"):
            paragraph = block.strip()
            if paragraph:
                document.add_paragraph(paragraph)


def export_docx(report_input: ReportInputV1, output_path: Path) -> ReportExportResultV1:
    """Module-level DOCX export helper."""
    return DocxExporterV1().export(report_input, output_path)


def validate_docx_file(output_path: Path) -> None:
    """Validate DOCX is a non-empty OpenXML zip archive."""
    if not output_path.is_file():
        raise FileNotFoundError(f"DOCX not created: {output_path}")
    if not zipfile.is_zipfile(output_path):
        raise ValueError(f"Invalid DOCX zip archive: {output_path}")
    size = output_path.stat().st_size
    if size < DOCX_MIN_BYTES:
        raise ValueError(f"DOCX too small ({size} bytes): {output_path}")
    with zipfile.ZipFile(output_path, "r") as archive:
        if "[Content_Types].xml" not in archive.namelist():
            raise ValueError(f"Invalid DOCX content types: {output_path}")


def _fmt_optional(value: object) -> str:
    if value is None or value == "":
        return ""
    return str(value)


def _find_section(
    sections: list[ReportInterpretationSectionV1],
    key: str,
) -> ReportInterpretationSectionV1 | None:
    aliases = _DOMAIN_ALIASES.get(key, (key,))
    normalized = {alias.lower() for alias in aliases}
    for section in sections:
        section_id = section.id.lower()
        title = section.title.lower()
        if section_id in normalized or any(alias in title for alias in normalized):
            return section
    return None


def _first_section_content(sections: list[ReportInterpretationSectionV1]) -> str:
    for section in sections:
        if section.content.strip():
            return section.content
    return ""


def _last_section_content(sections: list[ReportInterpretationSectionV1]) -> str:
    for section in reversed(sections):
        if section.content.strip():
            return section.content
    return ""
