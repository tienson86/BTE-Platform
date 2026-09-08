"""Customer vs expert projection of the semantic report. No UI runtime."""

from __future__ import annotations

from consulting.marriage.models.report import MarriageReportModel, ReportBlock, ReportSection

CUSTOMER_OMITTED_SECTION_IDS = frozenset(
    {
        "confidence_limitations",
        "appendix",
    }
)


def customer_sections(model: MarriageReportModel) -> list[ReportSection]:
    """Return sections and blocks visible in Customer Mode."""
    return _filter_sections(model, "customer")


def expert_sections(model: MarriageReportModel) -> list[ReportSection]:
    """Return sections including expert trace blocks."""
    return _filter_sections(model, "expert")


def customer_visible_text(model: MarriageReportModel) -> str:
    """Join customer-visible titles and bodies for wording checks."""
    parts: list[str] = []
    for section in customer_sections(model):
        parts.append(section.title)
        if section.summary:
            parts.append(section.summary)
        for block in section.blocks:
            if block.title:
                parts.append(block.title)
            if block.body:
                parts.append(block.body)
    return "\n".join(parts)


def expert_visible_text(model: MarriageReportModel) -> str:
    """Join expert-visible titles and bodies."""
    parts: list[str] = []
    for section in expert_sections(model):
        for block in section.blocks:
            if block.body:
                parts.append(block.body)
    return "\n".join(parts)


def _filter_sections(model: MarriageReportModel, mode: str) -> list[ReportSection]:
    """Filter sections and blocks by visibility. Expert mode includes customer blocks."""
    sections: list[ReportSection] = []
    for section in model.sections:
        if mode == "customer" and _expert_only_section(section):
            continue
        blocks = [item for item in section.blocks if _visible(item, mode)]
        if not blocks:
            continue
        sections.append(
            ReportSection(
                section_id=section.section_id,
                title=section.title,
                summary=section.summary,
                blocks=blocks,
                visibility=section.visibility,
            )
        )
    return sections


def _expert_only_section(section: ReportSection) -> bool:
    """Technical, confidence, and methodology sections belong in Expert Mode."""
    return section.visibility == "expert" or section.section_id in CUSTOMER_OMITTED_SECTION_IDS


def _visible(block: ReportBlock, mode: str) -> bool:
    """Customer hides expert-only blocks. Expert sees both."""
    if mode == "expert":
        return True
    return block.visibility != "expert"
