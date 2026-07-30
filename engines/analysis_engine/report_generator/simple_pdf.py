"""Minimal PDF writer without external dependencies."""

from __future__ import annotations


def _escape_pdf_text(text: str) -> str:
    """Escape characters for PDF literal strings (Latin-1 fallback)."""
    cleaned = (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )
    return cleaned.encode("latin-1", errors="replace").decode("latin-1")


def write_simple_pdf_bytes(
    lines: list[str],
    *,
    title: str = "BTE Report",
) -> bytes:
    """Write a minimal multi-page PDF into memory and return bytes."""
    page_width = 595
    page_height = 842
    margin = 50
    font_size = 11
    leading = 16
    max_chars = 90

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

    font_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    content_ids: list[int] = []
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

    pages_object_number = len(objects) + len(pages) + 1
    page_obj_ids: list[int] = []
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
    actual_pages_id = len(objects)
    if actual_pages_id != pages_object_number:
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
    return bytes(buffer)
