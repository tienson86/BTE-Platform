"""Minimal PDF writer without external dependencies."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _escape_pdf_text(text: str) -> str:
    """Escape characters for PDF literal strings (Latin-1 fallback)."""
    cleaned = (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )
    # PDF Helvetica is Latin-1; drop unsupported glyphs safely
    return cleaned.encode("latin-1", errors="replace").decode("latin-1")


def write_simple_pdf(
    lines: list[str],
    output: str | Path,
    *,
    title: str = "BTE Report",
) -> Path:
    """
    Write a minimal single-page-flow PDF (multiple pages) using core PDF ops.

    No third-party dependency (reportlab optional elsewhere).
    """
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    page_width = 595  # A4
    page_height = 842
    margin = 50
    font_size = 11
    leading = 16
    max_chars = 90

    # Wrap lines
    wrapped: list[str] = []
    for raw in lines:
        text = str(raw or "")
        if not text:
            wrapped.append("")
            continue
        while len(text) > max_chars:
            wrapped.append(text[:max_chars])
            text = text[max_chars:]
        wrapped.append(text)

    # Paginate
    usable = page_height - 2 * margin
    rows_per_page = max(1, usable // leading)
    pages: list[list[str]] = []
    for index in range(0, len(wrapped), rows_per_page):
        pages.append(wrapped[index : index + rows_per_page])
    if not pages:
        pages = [[title]]

    objects: list[bytes] = []

    def add_object(payload: bytes) -> int:
        objects.append(payload)
        return len(objects)

    # 1: Catalog, 2: Pages (filled later), then page objects
    font_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    page_ids: list[int] = []
    content_ids: list[int] = []

    for page_lines in pages:
        y = page_height - margin
        content_parts = ["BT", "/F1 {0} Tf".format(font_size)]
        for line in page_lines:
            safe = _escape_pdf_text(line)
            content_parts.append(f"1 0 0 1 {margin} {y} Tm ({safe}) Tj")
            y -= leading
        content_parts.append("ET")
        stream = "\n".join(content_parts).encode("latin-1", errors="replace")
        content_id = add_object(
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"
        )
        content_ids.append(content_id)
        # placeholder page id
        page_ids.append(0)

    pages_id = 2  # reserved conceptually; we rebuild object list carefully
    # Rebuild with known IDs: use sequential construction
    objects = []
    font_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    content_ids = []
    for page_lines in pages:
        y = page_height - margin
        content_parts = ["BT", f"/F1 {font_size} Tf"]
        for line in page_lines:
            safe = _escape_pdf_text(line)
            content_parts.append(f"1 0 0 1 {margin} {y} Tm ({safe}) Tj")
            y -= leading
        content_parts.append("ET")
        stream = "\n".join(content_parts).encode("latin-1", errors="replace")
        content_ids.append(
            add_object(
                b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"
            )
        )

    page_obj_ids: list[int] = []
    # Pages object will be inserted after we know kids — allocate later via rewrite
    # Simpler approach: build page objects pointing to a fixed Pages id after font+contents
    pages_object_number = len(objects) + len(pages) + 1

    for content_id in content_ids:
        page_obj_ids.append(
            add_object(
                (
                    f"<< /Type /Page /Parent {pages_object_number} 0 R "
                    f"/MediaBox [0 0 {page_width} {page_height}] "
                    f"/Contents {content_id} 0 R "
                    f"/Resources << /Font << /F1 {font_id} 0 R >> >> >> >>"
                ).encode("ascii")
            )
        )

    kids = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
    add_object(
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_ids)} >>".encode("ascii")
    )
    # Fix: pages_object_number must equal actual id
    actual_pages_id = len(objects)
    if actual_pages_id != pages_object_number:
        # Rebuild page objects with correct parent — patch in-memory
        for index, content_id in enumerate(content_ids):
            objects[page_obj_ids[index] - 1] = (
                f"<< /Type /Page /Parent {actual_pages_id} 0 R "
                f"/MediaBox [0 0 {page_width} {page_height}] "
                f"/Contents {content_id} 0 R "
                f"/Resources << /Font << /F1 {font_id} 0 R >> >> >> >>"
            ).encode("ascii")

    catalog_id = add_object(
        f"<< /Type /Catalog /Pages {actual_pages_id} 0 R >>".encode("ascii")
    )

    # Write PDF
    buffer = bytearray()
    buffer.extend(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(buffer))
        buffer.extend(f"{index} 0 obj\n".encode("ascii"))
        buffer.extend(obj)
        buffer.extend(b"\nendobj\n")

    xref_pos = len(buffer)
    buffer.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    buffer.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        buffer.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    buffer.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode("ascii")
    )
    output_path.write_bytes(bytes(buffer))
    return output_path


def report_lines_from_model(report: Any) -> list[str]:
    """Flatten Report / ReportModel into text lines for PDF."""
    lines: list[str] = []
    metadata = getattr(report, "metadata", None)
    title = getattr(metadata, "title", None) if metadata is not None else None
    lines.append(str(title or "BTE Report"))
    lines.append("=" * 40)
    summary = getattr(report, "summary", None)
    if summary is not None:
        st = getattr(summary, "title", "") or ""
        sc = getattr(summary, "content", "") or ""
        if st:
            lines.append(str(st))
        if sc:
            lines.extend(str(sc).splitlines())
        lines.append("")
    for section in getattr(report, "sections", []) or []:
        if hasattr(section, "visible") and not section.visible:
            continue
        lines.append(str(getattr(section, "title", "") or ""))
        lines.append("-" * 20)
        content = getattr(section, "content", "") or ""
        lines.extend(str(content).splitlines())
        lines.append("")
    return lines
