"""HTML Report V1 renderer — consumes ReportInputV1 only."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportPillarV1,
    missing_data_message,
)

_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates" / "v1"

_DOMAIN_SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "career": ("su_nghiep", "career", "nghiep", "nghề"),
    "wealth": ("tai_van", "wealth", "tai", "tài"),
    "marriage": ("hon_nhan", "relationship", "hon", "hôn"),
    "health": ("suc_khoe", "health", "sức"),
    "children": ("tu_tuc", "children", "con"),
}


class HtmlReportV1Renderer:
    """Render Report V1 HTML from ReportInputV1."""

    def __init__(
        self,
        *,
        template_dir: Path | None = None,
    ) -> None:
        self._template_dir = template_dir or _TEMPLATE_DIR

    def render(self, report_input: ReportInputV1) -> str:
        """Return a complete UTF-8 HTML document."""
        template = (self._template_dir / "report_v1.html").read_text(encoding="utf-8")
        css = (self._template_dir / "report_v1.css").read_text(encoding="utf-8")
        title = self._document_title(report_input)
        content = self._render_content(report_input)
        return (
            template.replace("{{TITLE}}", escape(title))
            .replace("{{CSS}}", css)
            .replace("{{CONTENT}}", content)
        )


def render_html(report_input: ReportInputV1) -> str:
    """Render HTML Report V1 (module-level API)."""
    return HtmlReportV1Renderer().render(report_input)


def _paragraphs(text: str) -> str:
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    if not blocks:
        return f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    return "".join(f"<p>{escape(block)}</p>" for block in blocks)


def _section(title: str, body_html: str, *, section_id: str = "") -> str:
    anchor = f' id="{escape(section_id)}"' if section_id else ""
    return (
        f'<section class="report-v1__section"{anchor}>'
        f'<h2 class="report-v1__section-title">{escape(title)}</h2>'
        f'<div class="report-v1__section-body">{body_html}</div>'
        "</section>"
    )


def _meta_grid(rows: Iterable[tuple[str, str]]) -> str:
    parts = ['<dl class="report-v1__meta-grid">']
    for label, value in rows:
        if not value:
            continue
        parts.append(f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>")
    parts.append("</dl>")
    return "".join(parts)


def _pillar_card(label: str, pillar: ReportPillarV1) -> str:
    hidden = ", ".join(pillar.hidden_stems) if pillar.hidden_stems else "—"
    return (
        f'<article class="report-v1__pillar-card">'
        f"<h3>{escape(label)}</h3>"
        f"<p><strong>Can Chi:</strong> {escape(pillar.stem)} {escape(pillar.branch)}</p>"
        f"<p><strong>Ẩn can:</strong> {escape(hidden)}</p>"
        f"<p><strong>Nạp âm:</strong> {escape(pillar.na_yin or '—')}</p>"
        f"<p><strong>Thập thần:</strong> {escape(pillar.ten_god or '—')}</p>"
        f"<p><strong>Trường sinh:</strong> {escape(pillar.truong_sinh or '—')}</p>"
        "</article>"
    )


def _find_section(
    sections: list[ReportInterpretationSectionV1],
    *aliases: str,
) -> ReportInterpretationSectionV1 | None:
    normalized = {alias.lower() for alias in aliases}
    for section in sections:
        section_id = section.id.lower()
        title = section.title.lower()
        if section_id in normalized or any(alias in title for alias in normalized):
            return section
    return None


def _domain_section(
    report_input: ReportInputV1,
    title: str,
    section_key: str,
) -> str:
    aliases = _DOMAIN_SECTION_ALIASES.get(section_key, (section_key,))
    section = _find_section(report_input.interpretation.sections, *aliases)
    if section is None or not section.content.strip():
        body = f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    else:
        body = _paragraphs(section.content)
    return _section(title, body, section_id=section_key)


# Bind helper methods on renderer class for readability
def _document_title(self: HtmlReportV1Renderer, report_input: ReportInputV1) -> str:
    name = report_input.profile.full_name.strip()
    if name:
        return f"Báo cáo Bát Tự — {name}"
    return "Báo cáo Bát Tự"


def _render_content(self: HtmlReportV1Renderer, report_input: ReportInputV1) -> str:
    parts: list[str] = []
    profile = report_input.profile
    metadata = report_input.metadata

    parts.append(
        '<header class="report-v1__header">'
        f'<h1 class="report-v1__title">Báo cáo luận giải Bát Tự</h1>'
        f'<p class="report-v1__subtitle">'
        f'{escape(profile.full_name or "—")} · '
        f'{escape(metadata.case_id or "—")} · '
        f'{escape(metadata.generated_at)}'
        f"</p></header>"
    )

    parts.append(
        _section(
            "01. Thông tin lá số",
            _meta_grid(
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
                    ("Chế độ lịch", report_input.calendar.calendar_mode),
                ]
            ),
            section_id="chart-info",
        )
    )

    pillars = report_input.pillars
    parts.append(
        _section(
            "02. Tứ Trụ",
            '<div class="report-v1__pillars">'
            + _pillar_card("Năm", pillars.year)
            + _pillar_card("Tháng", pillars.month)
            + _pillar_card("Ngày", pillars.day)
            + _pillar_card("Giờ", pillars.hour)
            + "</div>",
            section_id="four-pillars",
        )
    )

    five = report_input.five_elements
    parts.append(
        _section(
            "03. Ngũ hành",
            (
                "<table class='report-v1__table'><thead><tr>"
                "<th>Hành</th><th>Giá trị</th></tr></thead><tbody>"
                f"<tr><td>Mộc</td><td>{escape(str(five.wood if five.wood is not None else '—'))}</td></tr>"
                f"<tr><td>Hỏa</td><td>{escape(str(five.fire if five.fire is not None else '—'))}</td></tr>"
                f"<tr><td>Thổ</td><td>{escape(str(five.earth if five.earth is not None else '—'))}</td></tr>"
                f"<tr><td>Kim</td><td>{escape(str(five.metal if five.metal is not None else '—'))}</td></tr>"
                f"<tr><td>Thủy</td><td>{escape(str(five.water if five.water is not None else '—'))}</td></tr>"
                "</tbody></table>"
            ),
            section_id="five-elements",
        )
    )

    strength = report_input.strength
    strength_body = _meta_grid(
        [
            ("Nhật chủ", strength.day_master),
            ("Điểm", str(strength.score) if strength.score is not None else ""),
            ("Mức", strength.level),
            ("Phân loại", strength.classification),
            ("Hỗ trợ mùa", str(strength.seasonal_support) if strength.seasonal_support is not None else ""),
            ("Căn", str(strength.root_support) if strength.root_support is not None else ""),
        ]
    )
    if strength.summary:
        strength_body += _paragraphs(strength.summary)
    elif not strength.day_master:
        strength_body += f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    parts.append(_section("04. Thân vượng nhược", strength_body, section_id="strength"))

    ten_gods = report_input.ten_gods
    ten_gods_body = _meta_grid(
        [
            ("Thập thần hiển", ", ".join(ten_gods.visible)),
            ("Ẩn can", ", ".join(ten_gods.hidden)),
            ("Tóm tắt", ten_gods.summary),
        ]
    )
    parts.append(_section("05. Thập thần", ten_gods_body, section_id="ten-gods"))

    pattern = report_input.pattern
    parts.append(
        _section(
            "06. Mệnh cục / Cách cục",
            _meta_grid(
                [
                    ("Cách chính", pattern.primary_pattern),
                    ("Cách phụ", ", ".join(pattern.secondary_patterns)),
                    ("Theo cách", pattern.follow_pattern),
                    ("Trạng thái", pattern.status),
                    ("Độ tin cậy", str(pattern.confidence) if pattern.confidence is not None else ""),
                ]
            )
            + _paragraphs(pattern.explanation),
            section_id="pattern",
        )
    )

    useful = report_input.useful_god
    parts.append(
        _section(
            "07. Dụng thần – Hỷ thần – Kỵ thần",
            _meta_grid(
                [
                    ("Dụng thần", useful.useful_god),
                    ("Hỷ thần", ", ".join(useful.favorable_gods)),
                    ("Kỵ thần", ", ".join(useful.unfavorable_gods)),
                    ("Trung tính", ", ".join(useful.neutral_gods)),
                    ("Điều hậu nhiệt", useful.temperature_adjustment),
                ]
            )
            + _paragraphs(useful.reasoning),
            section_id="useful-god",
        )
    )

    if report_input.shensha:
        rows = "".join(
            "<tr>"
            f"<td>{escape(item.name)}</td>"
            f"<td>{escape(item.category)}</td>"
            f"<td>{'Có' if item.present else 'Không'}</td>"
            f"<td>{escape(item.evidence)}</td>"
            "</tr>"
            for item in report_input.shensha
        )
        shensha_body = (
            "<table class='report-v1__table'><thead><tr>"
            "<th>Tên</th><th>Loại</th><th>Hiện diện</th><th>Bằng chứng</th>"
            f"</tr></thead><tbody>{rows}</tbody></table>"
        )
    else:
        shensha_body = f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    parts.append(_section("08. Thần sát", shensha_body, section_id="shensha"))

    luck = report_input.luck_cycles
    if luck.cycles:
        rows = "".join(
            "<tr>"
            f"<td>{cycle.index}</td>"
            f"<td>{escape(cycle.stem)} {escape(cycle.branch)}</td>"
            f"<td>{cycle.start_year or '—'}</td>"
            f"<td>{cycle.end_year or '—'}</td>"
            f"<td>{cycle.age_start or '—'} – {cycle.age_end or '—'}</td>"
            f"<td>{escape(cycle.summary)}</td>"
            "</tr>"
            for cycle in luck.cycles
        )
        luck_body = _meta_grid(
            [
                ("Hướng", luck.direction),
                ("Tuổi khởi", str(luck.start_age) if luck.start_age is not None else ""),
                ("Ngày bắt đầu", luck.start_date),
            ]
        ) + (
            "<table class='report-v1__table'><thead><tr>"
            "<th>#</th><th>Can Chi</th><th>Từ năm</th><th>Đến năm</th>"
            "<th>Tuổi</th><th>Tóm tắt</th></tr></thead><tbody>"
            f"{rows}</tbody></table>"
        )
    else:
        luck_body = f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    parts.append(_section("09. Đại vận", luck_body, section_id="luck-cycles"))

    interpretation = report_input.interpretation
    exec_text = interpretation.executive_summary.strip()
    if not exec_text and interpretation.sections:
        exec_text = interpretation.sections[0].content
    exec_body = _paragraphs(exec_text) if exec_text else (
        f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    )
    parts.append(_section("10. Luận giải tổng thể", exec_body, section_id="executive-summary"))

    parts.append(_domain_section(report_input, "11. Nghề nghiệp", "career"))
    parts.append(_domain_section(report_input, "12. Tài vận", "wealth"))
    parts.append(_domain_section(report_input, "13. Hôn nhân", "marriage"))
    parts.append(_domain_section(report_input, "14. Sức khỏe", "health"))
    parts.append(_domain_section(report_input, "15. Tử tức", "children"))

    if interpretation.recommendations:
        rec_body = "<ul class='report-v1__list'>" + "".join(
            f"<li>{escape(item)}</li>" for item in interpretation.recommendations
        ) + "</ul>"
    else:
        rec_body = f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    parts.append(_section("16. Khuyến nghị", rec_body, section_id="recommendations"))

    conclusion = interpretation.conclusion.strip()
    if not conclusion and len(interpretation.sections) > 1:
        conclusion = interpretation.sections[-1].content
    conclusion_body = _paragraphs(conclusion) if conclusion else (
        f'<p class="report-v1__fallback">{escape(missing_data_message())}</p>'
    )
    parts.append(_section("17. Tổng kết", conclusion_body, section_id="conclusion"))

    parts.append(
        '<footer class="report-v1__footer">'
        f"BTE Platform · Report V1 · {escape(metadata.report_version)} · "
        f"{escape(metadata.engine_version)}"
        "</footer>"
    )
    return "".join(parts)


HtmlReportV1Renderer._document_title = _document_title  # type: ignore[method-assign]
HtmlReportV1Renderer._render_content = _render_content  # type: ignore[method-assign]
