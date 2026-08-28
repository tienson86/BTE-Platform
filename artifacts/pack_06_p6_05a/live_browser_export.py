"""Live /choose-date PDF and DOCX download against the running Portal."""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

PORTAL = "http://127.0.0.1:8081"
OUT = Path("artifacts/pack_06_p6_05a/browser")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        console: list[str] = []
        page.on("console", lambda msg: console.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: console.append(f"pageerror: {err}"))
        page.goto(f"{PORTAL}/choose-date", wait_until="networkidle", timeout=60000)
        page.fill("#dsFullName", "Nguyễn Tiến Sơn")
        page.check("input[name=gender][value=male]")
        page.fill("#dsBirth", "21/01/1987")
        page.fill("#dsTargetMonth", "09/2026")
        page.click("#dsSearchBtn")
        page.wait_for_selector("[data-testid=ranked-card]", timeout=30000)
        page.wait_for_selector("#dsExport:not([hidden])", timeout=5000)
        export = page.locator("#dsExport")
        assert export.is_visible()
        with page.expect_download(timeout=120000) as pdf_info:
            page.click("#dsExportPdf")
        pdf = pdf_info.value
        pdf_path = OUT / (pdf.suggested_filename or "export.pdf")
        pdf.save_as(str(pdf_path))
        page.wait_for_function(
            "() => !document.getElementById('dsExportPdf')?.disabled",
            timeout=10000,
        )
        with page.expect_download(timeout=120000) as docx_info:
            page.click("#dsExportDocx")
        docx = docx_info.value
        docx_path = OUT / (docx.suggested_filename or "export.docx")
        docx.save_as(str(docx_path))
        status = page.locator("#dsExportStatus")
        visible_error = status.is_visible() and (status.inner_text() or "").strip()
        print("pdf_name", pdf.suggested_filename)
        print("pdf_path", pdf_path, "size", pdf_path.stat().st_size)
        print("pdf_magic", pdf_path.read_bytes()[:5])
        print("docx_name", docx.suggested_filename)
        print("docx_path", docx_path, "size", docx_path.stat().st_size)
        print("docx_magic", docx_path.read_bytes()[:2])
        print("status_error", visible_error)
        print("console", "\n".join(console[-20:]))
        browser.close()
        if visible_error:
            raise SystemExit(f"export status error: {visible_error}")
        if pdf_path.read_bytes()[:5] != b"%PDF-":
            raise SystemExit("PDF magic mismatch")
        if docx_path.read_bytes()[:2] != b"PK":
            raise SystemExit("DOCX magic mismatch")


if __name__ == "__main__":
    main()
