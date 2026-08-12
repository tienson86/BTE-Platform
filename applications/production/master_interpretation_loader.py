"""Load frozen Master Interpretation markdown for customer delivery."""

from __future__ import annotations

import re
from pathlib import Path

MASTER_ROOT = (
    Path(__file__).resolve().parents[2]
    / "knowledge"
    / "master_interpretations"
)

PART_FILES: dict[str, str] = {
    "01": "PART_01_STRENGTH_MASTER_INTERPRETATION.md",
    "02": "PART_02_TEN_GODS_MASTER_INTERPRETATION.md",
    "03": "PART_03_DESTINY_STRUCTURE_MASTER_INTERPRETATION.md",
    "04": "PART_04_BALANCE_STRATEGY_MASTER_INTERPRETATION.md",
    "05": "PART_05_EXTERNAL_INFLUENCES_MASTER_INTERPRETATION.md",
    "06": "PART_06_LIFE_TIMELINE_MASTER_INTERPRETATION.md",
    "08": "PART_08_MASTER_CONSULTING_REPORT.md",
}


def _case_dir(case_id: str) -> Path:
    normalized = case_id.upper().replace("-", "_")
    return MASTER_ROOT / normalized


def _extract_customer_body(markdown: str) -> str:
    """Return main interpretation prose; strip appendices and metadata tables."""
    text = markdown.replace("\r\n", "\n")
    appendix_match = re.search(r"\n# Appendix", text)
    if appendix_match:
        text = text[: appendix_match.start()]
    end_match = re.search(r"\n---\n\nEND\s*$", text)
    if end_match:
        text = text[: end_match.start()]
    lines = text.split("\n")
    body_lines: list[str] = []
    skip_table = False
    for line in lines:
        if line.startswith("| Field |"):
            skip_table = True
            continue
        if skip_table:
            if line.strip() == "" or not line.startswith("|"):
                skip_table = False
            else:
                continue
        if line.startswith("> **Lưu ý:**"):
            continue
        body_lines.append(line)
    return "\n".join(body_lines).strip()


def load_master_interpretation_part(case_id: str, part: str) -> str:
    """Load one master interpretation part as customer prose."""
    filename = PART_FILES.get(part)
    if not filename:
        raise FileNotFoundError(f"Unknown master interpretation part: {part}")
    path = _case_dir(case_id) / filename
    if not path.is_file():
        raise FileNotFoundError(f"Master interpretation not found: {path}")
    return _extract_customer_body(path.read_text(encoding="utf-8"))


def load_all_master_parts(case_id: str) -> dict[str, str]:
    """Load Parts 01–06 master interpretation prose."""
    return {
        part: load_master_interpretation_part(case_id, part)
        for part in ("01", "02", "03", "04", "05", "06")
    }


def load_executive_consulting(case_id: str) -> str:
    """Load Part 08 executive consulting report."""
    return load_master_interpretation_part(case_id, "08")


def extract_executive_summary(consulting_markdown: str) -> str:
    """Extract §6 or §10 executive insight from consulting report."""
    match = re.search(
        r"# 6\.[^\n]*\n+(.*?)(?=\n# 7\.|\Z)",
        consulting_markdown,
        re.DOTALL,
    )
    if match:
        block = match.group(1).strip()
        quote = re.search(r"> \*\*(.+?)\*\*", block, re.DOTALL)
        if quote:
            return quote.group(1).strip()
        return block.split("\n\n")[0][:500]
    return consulting_markdown[:500]
