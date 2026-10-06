"""Childbirth reports use the same PDF and DOCX layout as other consultations."""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import re
import unicodedata

from consulting.childbirth.repository import ChildbirthProfile
from consulting.marriage.models.report import ReportBlock, ReportSection
from consulting.marriage.report.export import (
    ConsultationExportDocument, MarriageExportArtifact, MarriageExportFormat,
    MarriagePdfBackend, export_consultation_file,
)

GENDER_LABELS = {"boy": "Ưu tiên con trai", "girl": "Ưu tiên con gái", "either": "Trai/gái đều xét được"}
LEVEL_LABELS = {"very_suitable": "Rất phù hợp", "suitable": "Phù hợp", "consider": "Có thể cân nhắc", "sensitive": "Cần thận trọng"}
HOUR_BRANCHES = ("Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi")


def _timestamp(value: str) -> str:
    return datetime.fromisoformat(value).astimezone(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M")


def build_childbirth_document(profile: ChildbirthProfile) -> ConsultationExportDocument:
    data = profile.result
    father = profile.input["father"]
    mother = profile.input["mother"]
    names = f"{father.get('full_name') or 'Người bố'} và {mother.get('full_name') or 'Người mẹ'}"
    normalized = unicodedata.normalize("NFKD", names.replace("đ", "d").replace("Đ", "D")).encode("ascii", "ignore").decode("ascii")
    identity = re.sub(r"[^A-Za-z0-9]+", "-", normalized).strip("-").lower()[:100]
    rows = [("Mã hồ sơ", profile.consultation_id), ("Ngày lập", _timestamp(profile.created_at))]
    if profile.saved_at:
        rows.append(("Ngày lưu", _timestamp(profile.saved_at)))
    for label, person in (("Người bố", father), ("Người mẹ", mother)):
        time = person.get("birth_time")
        hour = f"Giờ {HOUR_BRANCHES[((int(time[:2]) + 1) // 2) % 12]}" if time else "Không biết"
        rows.append((label, f"{person.get('full_name') or label}; sinh {date.fromisoformat(person['birth_date']).strftime('%d/%m/%Y')}; {hour}"))
        place = person.get("birth_place")
        if place:
            rows.append((f"Nơi sinh {label.lower()}", place.get("display_name") or place.get("province") or place.get("city") or "Chưa rõ"))
    rows.append(("Khoảng năm xét", f"{data['start_year']} - {data['start_year'] + data['years_ahead'] - 1}"))
    sections = [ReportSection(
        section_id="summary", title="Kết luận tư vấn sinh con", summary=data["summary"]["headline"],
        blocks=[ReportBlock(block_id="eligibility", kind="text", body=data["eligibility"]["rule"]),
                ReportBlock(block_id="summary-note", kind="text", body=data["summary"].get("note"))],
    )]
    for role, label in (("father", "Người bố"), ("mother", "Người mẹ")):
        parent = data["parents"][role]
        signals = [
            ("Nhật chủ", f"{parent['day_master']} ({parent['day_master_element']})"),
            ("Mệnh cục", parent.get("pattern") or "Chưa rõ"),
            ("Dụng thần", ", ".join(parent.get("useful_elements", [])) or "Chưa rõ"),
            ("Hỷ thần", ", ".join(parent.get("favorable_elements", [])) or "Chưa rõ"),
            ("Thần sát", ", ".join(parent.get("shen_sha", [])) or "Chưa rõ"),
            ("Thập thần", ", ".join(parent.get("ten_gods", [])) or "Chưa rõ"),
            ("Cung phi", f"{parent.get('cung_phi') or 'Chưa rõ'}; {parent.get('trach_group') or 'Chưa rõ'}"),
        ]
        sections.append(ReportSection(section_id=role, title=f"Lá số {label.lower()}", blocks=[
            ReportBlock(block_id=f"{role}-{index}", kind="text", body=f"{label}: {value}")
            for index, (label, value) in enumerate(signals)
        ]))
    for item in data["recommendations"]:
        year = item["year"]
        details = [
            ("Đánh giá", f"{LEVEL_LABELS[item['level']]}; {GENDER_LABELS[item['recommended_child_gender']]}; điểm {item['score']}/100"),
            ("Tuổi bố mẹ", f"Bố {item['father_age']} tuổi; mẹ {item['mother_age']} tuổi"),
            ("Ngũ hành", f"{item['primary_element']} / {item['branch_element']}"),
            ("Bé trai", f"{item['boy']['cung_phi']}; {item['boy']['trach_group']}"),
            ("Bé gái", f"{item['girl']['cung_phi']}; {item['girl']['trach_group']}"),
            ("Cơ sở đánh giá", "\n".join(item["reasons"])),
            ("Lưu ý", " ".join(item.get("cautions", []))),
        ]
        sections.append(ReportSection(section_id=f"year-{year}", title=f"Năm {year} {item['can_chi']}", blocks=[
            ReportBlock(block_id=f"year-{year}-{index}", kind="text", title=label, body=value)
            for index, (label, value) in enumerate(details) if value
        ]))
    excluded = data["eligibility"].get("ineligible_years", [])
    if excluded:
        sections.append(ReportSection(section_id="excluded", title="Các năm chưa đủ điều kiện tuổi", blocks=[
            ReportBlock(block_id=f"excluded-{item['year']}", kind="text", body=f"{item['year']}: bố {item['father_age']} tuổi; mẹ {item['mother_age']} tuổi. {item['reason']}")
            for item in excluded
        ]))
    return ConsultationExportDocument(
        title=f"Tư vấn sinh con - {names}", heading="BẢN LUẬN GIẢI TƯ VẤN SINH CON", subtitle=names,
        filename_stem=f"BTE_TuVanSinhCon_{identity}_{profile.consultation_id[-8:]}",
        summary_rows=rows, sections=sections,
        notice="Kết quả là luận giải theo Bát Tự và Cung Phi. Đánh giá bé trai/bé gái thể hiện tương hợp theo mô hình, không dự đoán giới tính thực tế.",
    )


def export_childbirth_file(
    profile: ChildbirthProfile, fmt: MarriageExportFormat, *,
    output_root: Path | None = None, pdf_backend: MarriagePdfBackend | None = None,
) -> MarriageExportArtifact:
    return export_consultation_file(
        build_childbirth_document(profile), profile.consultation_id, fmt,
        output_root=output_root, pdf_backend=pdf_backend,
    )
