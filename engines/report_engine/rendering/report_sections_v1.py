"""Shared Report V1 presentation model — HTML/PDF/DOCX consume the same sections."""

from __future__ import annotations

from dataclasses import dataclass, field

from applications.api.services.five_elements_truth import FIVE_ELEMENTS_DISCLAIMER
from engines.bazi_engine.ten_god import branch_element, stem_element
from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportPillarV1,
    ReportTenGodsV1,
    missing_data_message,
)
from engines.report_engine.localization.customer_text import customer_paragraphs
from engines.report_engine.localization.display import display_text
from engines.report_engine.localization.labels_vi import (
    EXECUTIVE_SUMMARY_MISSING,
    FULL_LUCK_CYCLES_GAP_NOTE,
    RUNTIME_GAP_MESSAGE,
)
from engines.report_engine.adapters.commercial_presentation_adapter import (
    COMMERCIAL_PRESENTATION_EMPTY,
    CommercialPresentationAdapter,
)
from engines.report_engine.rendering.customer_facing import (
    shensha_customer_line,
    temperature_customer_evidence,
    ten_gods_prominence,
)
from engines.useful_god_engine.presentation import (
    EMPTY_CUSTOMER_FAVORABLE_DISPLAY,
    KY_SCOPE_NOTE,
)

_DOMAIN_ALIASES: dict[str, tuple[str, ...]] = {
    "career": ("su_nghiep", "career", "nghiep", "nghề"),
    "wealth": ("tai_van", "wealth", "tai", "tài"),
    "marriage": ("hon_nhan", "relationship", "hon", "hôn"),
    "health": ("suc_khoe", "health", "sức"),
    "children": ("tu_tuc", "children", "con"),
}

_RUNTIME_GAP_DOMAINS = frozenset({"wealth", "children"})


@dataclass(slots=True)
class PresentedTable:
    """Simple table for profile/pillars/cycles."""

    headers: list[str]
    rows: list[list[str]]


@dataclass(slots=True)
class PresentedPillar:
    """One pillar card."""

    label: str
    lines: list[tuple[str, str]]


@dataclass(slots=True)
class PresentedSection:
    """One customer-facing report section."""

    id: str
    title: str
    meta_rows: list[tuple[str, str]] = field(default_factory=list)
    pillars: list[PresentedPillar] = field(default_factory=list)
    table: PresentedTable | None = None
    paragraphs: list[str] = field(default_factory=list)
    list_items: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    fallback: str | None = None
    allow_break: bool = False


@dataclass(slots=True)
class PresentedReportV1:
    """Display-ready report shared by all V1 renderers."""

    document_title: str
    heading: str
    subtitle: str
    footer: str
    sections: list[PresentedSection]


def build_presented_report(report_input: ReportInputV1) -> PresentedReportV1:
    """Build the single presentation used by HTML, PDF, and DOCX."""
    profile = report_input.profile
    metadata = report_input.metadata
    name = display_text(profile.full_name)
    document_title = f"Báo cáo Bát Tự — {name}" if name else "Báo cáo Bát Tự"
    subtitle_parts = [
        name or "—",
        display_text(metadata.case_id) or "—",
        display_text(metadata.generated_at),
    ]
    footer_parts = [
        "BTE V1.0",
        f"Report V1 · {display_text(metadata.report_version)}",
    ]
    if metadata.case_id:
        footer_parts.append(f"Mã phân tích {display_text(metadata.case_id)}")
    if metadata.generated_at:
        footer_parts.append(display_text(metadata.generated_at))
    return PresentedReportV1(
        document_title=document_title,
        heading="Báo cáo luận giải Bát Tự",
        subtitle=" · ".join(part for part in subtitle_parts if part),
        footer=" · ".join(footer_parts),
        sections=_build_sections(report_input),
    )


def _build_sections(report_input: ReportInputV1) -> list[PresentedSection]:
    sections = [
        _section_profile(report_input),
        _section_pillars(report_input),
        _section_five_elements(report_input),
        _section_strength(report_input),
        _section_ten_gods(report_input),
        _section_pattern(report_input),
        _section_useful_god(report_input),
        _section_shensha(report_input),
        _section_luck(report_input),
        _section_executive_summary(report_input),
    ]
    if _has_pack05_narrative(report_input):
        sections.extend(_pack05_narrative_sections(report_input))
    else:
        sections.extend(
            [
                _domain_section(report_input, "11. Nghề nghiệp", "career"),
                _domain_section(report_input, "12. Tài vận", "wealth"),
                _domain_section(report_input, "13. Hôn nhân", "marriage"),
                _domain_section(report_input, "14. Sức khỏe", "health"),
                _domain_section(report_input, "15. Tử tức", "children"),
            ]
        )
    sections.extend(_commercial_consulting_sections(report_input))
    sections.append(_section_recommendations(report_input))
    sections.append(_section_conclusion(report_input))
    return sections


def _commercial_consulting_sections(report_input: ReportInputV1) -> list[PresentedSection]:
    """Present composed consulting. Omit when the report field is absent."""
    raw = report_input.commercial_consulting
    if raw is None:
        return []
    model = CommercialPresentationAdapter().adapt(raw)
    if not model.visible:
        return [
            PresentedSection(
                id="commercial-consulting",
                title="Tư vấn thương mại",
                fallback=COMMERCIAL_PRESENTATION_EMPTY,
                allow_break=True,
            )
        ]
    presented: list[PresentedSection] = []
    for section in model.sections:
        paragraphs: list[str] = []
        if section.summary:
            paragraphs.append(section.summary)
        paragraphs.extend(section.meaning)
        presented.append(
            PresentedSection(
                id=f"commercial-{section.domain or section.title}",
                title=section.title,
                paragraphs=paragraphs,
                list_items=list(section.recommendations),
                allow_break=True,
            )
        )
    return presented


def _section_profile(report_input: ReportInputV1) -> PresentedSection:
    profile = report_input.profile
    calendar = report_input.calendar
    return PresentedSection(
        id="chart-info",
        title="01. Thông tin lá số",
        meta_rows=_filled_rows(
            [
                ("Họ tên", display_text(profile.full_name)),
                ("Giới tính", display_text(profile.gender, "gender")),
                ("Ngày sinh", display_text(profile.birth_date)),
                ("Giờ sinh", display_text(profile.birth_time)),
                ("Nơi sinh", display_text(profile.birth_place)),
                ("Múi giờ", display_text(profile.timezone)),
                ("Dương lịch", display_text(calendar.solar_date)),
                ("Âm lịch", display_text(calendar.lunar_date)),
                ("Can Chi năm âm", display_text(calendar.lunar_year_can_chi)),
                ("Tiết khí", display_text(calendar.solar_term)),
                ("Tam Nguyên", display_text(calendar.tam_nguyen)),
                ("Cửu Vận", display_text(calendar.cuu_van)),
                ("Cung Phi", display_text(calendar.cung_phi)),
                ("Mệnh Quái", display_text(calendar.menh_quai)),
                ("Hành Cung", display_text(calendar.hanh_cung)),
                ("Nhóm Trạch", display_text(calendar.nhom_trach or calendar.house_group)),
                ("Múi giờ lịch", display_text(calendar.timezone)),
            ]
        ),
    )


_PILLAR_KEYS = {
    "Năm": "year",
    "Tháng": "month",
    "Ngày": "day",
    "Giờ": "hour",
}


def _section_pillars(report_input: ReportInputV1) -> PresentedSection:
    pillars = report_input.pillars
    ten_gods = report_input.ten_gods
    return PresentedSection(
        id="four-pillars",
        title="02. Tứ Trụ",
        pillars=[
            _pillar("Năm", pillars.year, ten_gods),
            _pillar("Tháng", pillars.month, ten_gods),
            _pillar("Ngày", pillars.day, ten_gods),
            _pillar("Giờ", pillars.hour, ten_gods),
        ],
        table=PresentedTable(
            headers=["Trụ", "Can Chi", "Ẩn can", "Nạp âm", "Thập thần", "Trường sinh"],
            rows=[
                _pillar_row("Năm", pillars.year, ten_gods),
                _pillar_row("Tháng", pillars.month, ten_gods),
                _pillar_row("Ngày", pillars.day, ten_gods),
                _pillar_row("Giờ", pillars.hour, ten_gods),
            ],
        ),
    )


def _pillar(
    label: str,
    pillar: ReportPillarV1,
    ten_gods: ReportTenGodsV1,
) -> PresentedPillar:
    hidden = _format_pillar_hidden(label, pillar, ten_gods)
    stem_line = _stem_with_element(label, pillar, ten_gods)
    return PresentedPillar(
        label=label,
        lines=[
            ("Can Chi", f"{display_text(pillar.stem)} {display_text(pillar.branch)}".strip()),
            ("Thiên can", stem_line),
            ("Ẩn can", hidden),
            ("Nạp âm", display_text(pillar.na_yin) or "—"),
            ("Thập thần", display_text(pillar.ten_god) or "—"),
            ("Trường sinh", display_text(pillar.truong_sinh) or "—"),
        ],
    )


def _pillar_row(
    label: str,
    pillar: ReportPillarV1,
    ten_gods: ReportTenGodsV1,
) -> list[str]:
    hidden = _format_pillar_hidden(label, pillar, ten_gods)
    return [
        label,
        f"{display_text(pillar.stem)} {display_text(pillar.branch)}".strip(),
        hidden,
        display_text(pillar.na_yin) or "—",
        display_text(pillar.ten_god) or "—",
        display_text(pillar.truong_sinh) or "—",
    ]


def _stem_with_element(
    label: str,
    pillar: ReportPillarV1,
    ten_gods: ReportTenGodsV1,
) -> str:
    element = ""
    pillar_key = _PILLAR_KEYS.get(label, "")
    for item in ten_gods.visible_entries:
        if str(item.get("pillar") or "") == pillar_key:
            element = str(item.get("element") or "")
            break
    if not element:
        element = stem_element(pillar.stem)
    stem = display_text(pillar.stem)
    if element:
        return f"{stem} · {element}"
    return stem


def _format_pillar_hidden(
    label: str,
    pillar: ReportPillarV1,
    ten_gods: ReportTenGodsV1,
) -> str:
    pillar_key = _PILLAR_KEYS.get(label, "")
    lines = [
        str(item.get("display") or _hidden_display(item))
        for item in ten_gods.hidden_entries
        if str(item.get("pillar") or "") == pillar_key
    ]
    if lines:
        return " · ".join(lines)
    return ", ".join(display_text(item) for item in pillar.hidden_stems) or "—"


def _five_element_display(value: object) -> str:
    """Format a structural count. Zero is absence in the distribution, not khuyết/Dụng."""
    text = display_text(value)
    if not text:
        return "—"
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return text
    if number == 0:
        return "0 — Không xuất hiện trong phân bố cấu trúc"
    if number.is_integer():
        return str(int(number))
    return text


def _strength_score_display(value: object) -> str:
    """Canonical Strength 0–1 as two decimals. Not Score Engine grade."""
    if value is None or value == "":
        return ""
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return display_text(value)
    if 0 <= number <= 1:
        return f"{number:.2f}"
    return display_text(value)


_PACK05_EXTRA_SECTIONS: tuple[tuple[str, str], ...] = (
    ("sec-observation", "Quan sát"),
    ("sec-reasoning", "Lý giải"),
    ("sec-impact", "Tác động"),
    ("sec-warning", "Lưu ý"),
)


def _has_pack05_narrative(report_input: ReportInputV1) -> bool:
    ids = {section.id for section in report_input.interpretation.sections}
    return "sec-executive_summary" in ids or "sec-observation" in ids


def _pack05_narrative_sections(report_input: ReportInputV1) -> list[PresentedSection]:
    extras: list[PresentedSection] = []
    for section_id, default_title in _PACK05_EXTRA_SECTIONS:
        section = _find_section(report_input.interpretation.sections, section_id, default_title.lower())
        if section is None or not section.content:
            continue
        extras.append(
            PresentedSection(
                id=section_id,
                title=section.title or default_title,
                paragraphs=customer_paragraphs(section.content),
                allow_break=True,
            )
        )
    return extras


def _section_five_elements(report_input: ReportInputV1) -> PresentedSection:
    five = report_input.five_elements
    values = (five.wood, five.fire, five.earth, five.metal, five.water)
    if all(value is None for value in values):
        return PresentedSection(
            id="five-elements",
            title="03. Phân bố Ngũ hành",
            fallback=RUNTIME_GAP_MESSAGE,
        )
    total = sum(float(value) for value in values if isinstance(value, (int, float)))
    notes = [
        "Tính theo Thiên can · bản hành Địa chi · Tàng can",
    ]
    if total > 0:
        notes.append(f"Tổng đơn vị cấu trúc: {int(total)}")
    notes.append(FIVE_ELEMENTS_DISCLAIMER)
    return PresentedSection(
        id="five-elements",
        title="03. Phân bố Ngũ hành",
        table=PresentedTable(
            headers=["Hành", "Số đơn vị"],
            rows=[
                ["Mộc", _five_element_display(five.wood)],
                ["Hỏa", _five_element_display(five.fire)],
                ["Thổ", _five_element_display(five.earth)],
                ["Kim", _five_element_display(five.metal)],
                ["Thủy", _five_element_display(five.water)],
            ],
        ),
        notes=notes,
    )


def _section_strength(report_input: ReportInputV1) -> PresentedSection:
    strength = report_input.strength
    rows = _filled_rows(
            [
                ("Nhật chủ", display_text(strength.day_master)),
                ("Điểm thân", _strength_score_display(strength.score)),
                ("Mức", display_text(strength.level, "strength")),
                ("Phân loại", display_text(strength.classification, "strength")),
                ("Hỗ trợ mùa", display_text(strength.seasonal_support)),
                ("Căn", display_text(strength.root_support)),
            ]
    )
    paragraphs = customer_paragraphs(strength.summary)
    fallback = None
    if not rows and not paragraphs:
        fallback = missing_data_message()
    return PresentedSection(
        id="strength",
        title="04. Thân vượng nhược",
        meta_rows=rows,
        paragraphs=paragraphs,
        fallback=fallback,
    )


def _section_ten_gods(report_input: ReportInputV1) -> PresentedSection:
    ten_gods = report_input.ten_gods
    prominence = ten_gods_prominence(
        ten_gods.visible_entries,
        ten_gods.hidden_entries,
        day_master_stem=report_input.strength.day_master,
    )
    featured_rows = [
        (f"{item['name']} — {item['klass']}", display_text(item["evidence"]))
        for item in prominence["featured"]
    ]
    visible_lines = [
        _visible_display(item)
        for item in (ten_gods.visible_entries or [])
    ] or list(ten_gods.visible)
    hidden_lines = [
        str(item.get("display") or _hidden_display(item))
        for item in (ten_gods.hidden_entries or [])
        if isinstance(item, dict)
    ] or [str(item) for item in ten_gods.hidden if item]
    note = ten_gods.note or "Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ."
    extra_rows: list[tuple[str, str]] = []
    others = str(prominence.get("others_line") or "")
    if others:
        extra_rows.append(("Các thần khác", others.replace("Các thần khác: ", "", 1)))
    extra_rows.append(("Ghi chú", note))
    return PresentedSection(
        id="ten-gods",
        title="05. Thập thần",
        meta_rows=_filled_rows(
            featured_rows
            + [
                ("Lộ can", " · ".join(display_text(item) for item in visible_lines)),
                ("Tàng can", " · ".join(display_text(item) for item in hidden_lines)),
                ("Tóm tắt lộ", display_text(ten_gods.visible_summary or ten_gods.summary)),
                ("Tóm tắt tàng", display_text(ten_gods.hidden_summary)),
            ]
            + extra_rows
        ),
    )


def _visible_display(item: dict[str, object]) -> str:
    stem = str(item.get("stem") or "")
    element = str(item.get("element") or "")
    ten_god = str(item.get("ten_god") or "")
    head = " · ".join(part for part in (stem, element) if part)
    if head and ten_god:
        return f"{head} / {ten_god}"
    return ten_god or head


def _hidden_display(item: dict[str, object]) -> str:
    stem = str(item.get("hidden_stem") or item.get("stem") or "")
    element = str(item.get("element") or "")
    ten_god = str(item.get("ten_god") or "")
    return " · ".join(part for part in (stem, element, ten_god) if part)


def _section_pattern(report_input: ReportInputV1) -> PresentedSection:
    pattern = report_input.pattern
    return PresentedSection(
        id="pattern",
        title="06. Mệnh cục / Cách cục",
        meta_rows=_filled_rows(
            [
                ("Cách chính", display_text(pattern.primary_pattern)),
                ("Cách phụ", ", ".join(display_text(item) for item in pattern.secondary_patterns)),
                ("Theo cách", display_text(pattern.follow_pattern)),
                ("Trạng thái", display_text(pattern.status, "pattern_status")),
                ("Độ tin cậy", display_text(pattern.confidence)),
            ]
        ),
        paragraphs=customer_paragraphs(pattern.explanation),
    )


def _section_useful_god(report_input: ReportInputV1) -> PresentedSection:
    useful = report_input.useful_god
    return PresentedSection(
        id="useful-god",
        title="07. Dụng thần – Hỷ thần – Kỵ thần",
        meta_rows=_filled_rows(
            [
                ("Dụng thần", display_text(useful.useful_display or useful.useful_god)),
                ("Căn cứ chọn Dụng", display_text(useful.short_reason or useful.reasoning)),
                ("Hỷ thần", display_text(
                    useful.favorable_display or EMPTY_CUSTOMER_FAVORABLE_DISPLAY
                )),
                ("Kỵ thần", display_text(
                    useful.unfavorable_display
                    or ", ".join(item for item in useful.unfavorable_gods if item)
                )),
                ("Phạm vi Kỵ", display_text(useful.ky_scope_note or KY_SCOPE_NOTE)),
                ("Trung tính", ", ".join(display_text(item) for item in useful.neutral_gods)),
                ("Điều hậu nhiệt", display_text(useful.temperature_adjustment, "temperature")),
                ("Nhu cầu điều hòa", display_text(useful.balancing_need, "balancing_need")),
                ("Ứng dụng Điều hậu", display_text(useful.climate_display)),
                ("Điều hậu", temperature_customer_evidence(useful.climate_evidence)),
                ("Điều hậu ưu tiên", display_text(useful.climate_preference_label)),
            ]
        ),
        paragraphs=(
            ()
            if useful.short_reason
            else customer_paragraphs(useful.reasoning)
        ),
    )


def _section_shensha(report_input: ReportInputV1) -> PresentedSection:
    if not report_input.shensha:
        return PresentedSection(
            id="shensha",
            title="08. Thần sát",
            fallback=missing_data_message(),
        )
    rows = []
    for item in report_input.shensha:
        name, presence, evidence = shensha_customer_line(item)
        rows.append(
            [
                display_text(name),
                display_text(presence),
                display_text(evidence),
            ]
        )
    return PresentedSection(
        id="shensha",
        title="08. Thần sát",
        table=PresentedTable(
            headers=["Tên", "Hiện diện", "Vị trí"],
            rows=rows,
        ),
    )


def _section_luck(report_input: ReportInputV1) -> PresentedSection:
    luck = report_input.luck_cycles
    if not luck.cycles:
        return PresentedSection(
            id="luck-cycles",
            title="09. Đại vận",
            fallback=RUNTIME_GAP_MESSAGE,
            notes=[FULL_LUCK_CYCLES_GAP_NOTE],
        )
    table = PresentedTable(
        headers=["#", "Can Chi", "Từ năm", "Đến năm", "Tuổi", "Ngũ hành"],
        rows=[
            [
                display_text(cycle.index),
                f"{display_text(cycle.stem)} {display_text(cycle.branch)}".strip(),
                display_text(cycle.start_year) or "—",
                display_text(cycle.end_year) or "—",
                f"{display_text(cycle.age_start) or '—'} – {display_text(cycle.age_end) or '—'}",
                _luck_element_line(cycle.stem, cycle.branch),
            ]
            for cycle in luck.cycles
        ],
    )
    current_years = ""
    if luck.current_year_start is not None and luck.current_year_end is not None:
        current_years = f"{luck.current_year_start}–{luck.current_year_end}"
    current_ages = ""
    if luck.current_age_start is not None and luck.current_age_end is not None:
        current_ages = f"{luck.current_age_start}–{luck.current_age_end}"
    current_display = " · ".join(
        part for part in (luck.current_gan_zhi, current_years, current_ages) if part
    )
    return PresentedSection(
        id="luck-cycles",
        title="09. Đại vận",
        meta_rows=_filled_rows(
            [
                ("Đại vận hiện tại", current_display),
                ("Chiều vận", display_text(luck.direction, "luck_direction")),
                ("Tuổi khởi vận", display_text(luck.start_age)),
                ("Căn cứ", display_text(luck.evidence)),
                ("Phương pháp V1.0", display_text(luck.method_note)),
            ]
        ),
        table=table,
        allow_break=True,
    )


def _luck_element_line(stem: str, branch: str) -> str:
    """Stem/branch elements from canonical metadata, not a renderer table."""
    stem_el = stem_element(stem)
    branch_el = branch_element(branch)
    parts: list[str] = []
    if stem and stem_el:
        parts.append(f"{stem} · {stem_el}")
    if branch and branch_el:
        parts.append(f"{branch} · {branch_el}")
    return " / ".join(parts)


def _section_executive_summary(report_input: ReportInputV1) -> PresentedSection:
    interpretation = report_input.interpretation
    paragraphs = customer_paragraphs(interpretation.executive_summary)
    if not paragraphs:
        summary_section = _find_section(interpretation.sections, "summary", "tổng quan")
        if summary_section is not None:
            paragraphs = customer_paragraphs(summary_section.content)
    if not paragraphs:
        return PresentedSection(
            id="executive-summary",
            title="10. Luận giải tổng thể",
            fallback=EXECUTIVE_SUMMARY_MISSING,
            allow_break=True,
        )
    return PresentedSection(
        id="executive-summary",
        title="10. Luận giải tổng thể",
        paragraphs=paragraphs,
        allow_break=True,
    )


def _domain_section(
    report_input: ReportInputV1,
    title: str,
    key: str,
) -> PresentedSection:
    aliases = _DOMAIN_ALIASES.get(key, (key,))
    section = _find_section(report_input.interpretation.sections, *aliases)
    paragraphs = customer_paragraphs(section.content) if section is not None else []
    if paragraphs:
        return PresentedSection(id=key, title=title, paragraphs=paragraphs, allow_break=True)
    fallback = RUNTIME_GAP_MESSAGE if key in _RUNTIME_GAP_DOMAINS else missing_data_message()
    return PresentedSection(id=key, title=title, fallback=fallback, allow_break=True)


def _section_recommendations(report_input: ReportInputV1) -> PresentedSection:
    items = [
        paragraph
        for raw in report_input.interpretation.recommendations
        for paragraph in customer_paragraphs(raw)
    ]
    if items:
        return PresentedSection(
            id="recommendations",
            title="16. Khuyến nghị",
            list_items=items,
            allow_break=True,
        )
    return PresentedSection(
        id="recommendations",
        title="16. Khuyến nghị",
        fallback=missing_data_message(),
        allow_break=True,
    )


def _section_conclusion(report_input: ReportInputV1) -> PresentedSection:
    interpretation = report_input.interpretation
    paragraphs = customer_paragraphs(interpretation.conclusion)
    if not paragraphs:
        conclusion = _find_section(interpretation.sections, "conclusion", "kết luận")
        if conclusion is not None:
            paragraphs = customer_paragraphs(conclusion.content)
    if not paragraphs:
        return PresentedSection(
            id="conclusion",
            title="17. Tổng kết",
            fallback=missing_data_message(),
            allow_break=True,
        )
    return PresentedSection(
        id="conclusion",
        title="17. Tổng kết",
        paragraphs=paragraphs,
        allow_break=True,
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


def _filled_rows(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(label, value) for label, value in rows if value]
