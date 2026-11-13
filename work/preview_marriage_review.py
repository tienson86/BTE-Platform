"""Preview with fictional people; in-memory storage only, no live HTTP calls."""
from pathlib import Path
from consulting.marriage.runtime.api_wiring import wire_marriage_api_runtime
from consulting.marriage.api.parse import parse_consultation_request
from consulting.archive_access import identity
from consulting.marriage.report.export import export_marriage_file, ConsultationExportDocument, _printable_sections
from consulting.marriage.report.access import customer_sections

def main():
    # Preview-only catalog override. The running service keeps its original YAML.
    import consulting.language.loader as language_loader
    draft = Path("artifacts/consulting-review-20261113/marriage/language-draft")
    if not draft.is_dir():
        raise RuntimeError("Preview catalog not prepared")
    language_loader.MARRIAGE_CATALOG_DIR = draft
    api = wire_marriage_api_runtime().api_contract
    body = {"person_a": {"full_name": "Nhân vật minh họa A", "gender": "male", "birth_date": "1991-04-12", "birth_time": "08:30", "timezone": "Asia/Ho_Chi_Minh"}, "person_b": {"full_name": "Nhân vật minh họa B", "gender": "female", "birth_date": "1993-09-23", "birth_time": "14:15", "timezone": "Asia/Ho_Chi_Minh"}}
    token = identity.set({"user_id": "synthetic-preview", "role": "MEMBER"})
    try:
        result = api.create_consultation(parse_consultation_request(body))
        if not result.consultation_id or result.error:
            raise RuntimeError(str(result.error))
        stored = api.get_stored(result.consultation_id)
        sections = _printable_sections([s for s in customer_sections(stored.report_model) if s.section_id != "appendix"])
        notice = "Bản minh họa dùng hai nhân vật giả để duyệt lời văn. Các nhận định thuộc mô hình Bát Tự/Cung Phi, không phải xác suất hạnh phúc hoặc lời khuyên quyết định kết hôn/chia tay. Chưa đưa bản sửa lên dịch vụ đang chạy."
        spec = ConsultationExportDocument(title="Bản mẫu hôn nhân để duyệt", heading="BẢN MẪU TƯ VẤN HÔN NHÂN", subtitle="DỮ LIỆU GIẢ ĐỊNH · CHỈ DÙNG DUYỆT NỘI DUNG", filename_stem="Hon_nhan_Ban_mau_duyet", summary_rows=[("Nhân vật A", "Nam, 12/04/1991, 08:30"), ("Nhân vật B", "Nữ, 23/09/1993, 14:15"), ("Múi giờ", "Asia/Ho_Chi_Minh"), ("Trạng thái", "Dự thảo, chưa nạp vào BTE")], sections=sections, notice=notice)
        root = Path("artifacts/consulting-review-20261113/marriage")
        for fmt in ("docx", "pdf"):
            artifact = export_marriage_file(stored, fmt, output_root=root, document=spec)
            print(artifact.path)
        lines = ["# Bản mẫu tư vấn hôn nhân", "DỮ LIỆU GIẢ ĐỊNH: A nam 12/04/1991 08:30; B nữ 23/09/1993 14:15; Asia/Ho_Chi_Minh.", notice]
        for section in sections:
            lines += ["", "## " + section.title, section.summary or ""]
            for block in section.blocks:
                if block.visibility == "customer" and block.kind != "methodology":
                    if block.title and block.title != block.body:
                        lines.append("### " + block.title)
                    if block.body:
                        lines.append(block.body)
        text = "\n\n".join(lines)
        (root / "Hon_nhan_Ban_mau_duyet.md").write_text(text, encoding="utf-8")
        print("Text characters:", len(text))
    finally:
        identity.reset(token)

if __name__ == "__main__":
    main()
