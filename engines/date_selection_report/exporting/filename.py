"""Canonical Date Selection PDF/DOCX filename. Reuses PACK 05 ascii_slug."""

from __future__ import annotations

from engines.date_selection_report.rendering.nodes import DateSelectionRenderTree
from engines.report_engine.exporting.filename import ascii_slug

FILENAME_PREFIX = "bao-cao-chon-ngay-tot"


def person_full_name(tree: DateSelectionRenderTree) -> str:
    """Return the person display name from the render tree."""
    for row in tree.person.rows:
        if row.key == "full_name":
            return row.value
    return "khach"


def period_filename_token(tree: DateSelectionRenderTree) -> str:
    """Return MM-YYYY from the search-period display."""
    display = tree.search_period.month_display.replace("/", "-")
    return display


def build_pdf_filename(tree: DateSelectionRenderTree) -> str:
    """Return `bao-cao-chon-ngay-tot_<customer>_<MM-YYYY>.pdf`."""
    return _stem(tree) + ".pdf"


def build_docx_filename(tree: DateSelectionRenderTree) -> str:
    """Return `bao-cao-chon-ngay-tot_<customer>_<MM-YYYY>.docx`."""
    return _stem(tree) + ".docx"


def _stem(tree: DateSelectionRenderTree) -> str:
    customer = ascii_slug(person_full_name(tree)).lower().replace("_", "-")
    period = period_filename_token(tree)
    return f"{FILENAME_PREFIX}_{customer}_{period}"
