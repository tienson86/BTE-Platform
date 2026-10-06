"""Business PDF and DOCX use the existing consultation document renderer."""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import re
import unicodedata

from consulting.business.presentation import BUSINESS_SCOPE, resolve_business_profile, business_context
from consulting.marriage.dto.history import MarriageStoredResult
from consulting.marriage.report.export import ConsultationExportDocument, MarriageExportArtifact, MarriageExportFormat, MarriagePdfBackend, export_marriage_file


def _display_timestamp(value: str) -> str:
    try:
        return datetime.fromisoformat(value).astimezone(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value


def export_business_file(stored: MarriageStoredResult, fmt: MarriageExportFormat, *, output_root: Path | None = None, pdf_backend: MarriagePdfBackend | None = None) -> MarriageExportArtifact:
    context = business_context(stored)
    if context is None:
        raise ValueError("business_report_missing")
    profile = resolve_business_profile(stored)
    name_a = stored.result.person_a.display_name or "Đối tác A"
    name_b = stored.result.person_b.display_name or "Đối tác B"
    normalized = unicodedata.normalize("NFKD", f"{name_a}-{name_b}".replace("đ", "d").replace("Đ", "D")).encode("ascii", "ignore").decode("ascii")
    identity = re.sub(r"[^A-Za-z0-9]+", "-", normalized).strip("-").lower()[:100] or "doi-tac"
    rows = [("Mã hồ sơ", stored.history.consultation_id), ("Ngày lập (giờ Việt Nam)", _display_timestamp(stored.history.created_at)), ("Ngành/nghề hợp tác", context["occupation_label"])]
    for label, person in (("Đối tác A", stored.request.person_a), ("Đối tác B", stored.request.person_b)):
        gender = "Nam" if person.gender.value == "male" else "Nữ"
        birth_date = date.fromisoformat(person.birth_date).strftime("%d/%m/%Y")
        rows.append((label, f"{person.full_name or label} - {gender}; sinh {birth_date}; giờ sinh {person.birth_time or 'chưa rõ'}"))
        if person.birth_place and person.birth_place.display_name:
            rows.append((f"Nơi sinh {label}", person.birth_place.display_name))
    if stored.business_profile:
        rows.append(("Ngày lưu (giờ Việt Nam)", _display_timestamp(stored.business_profile.saved_at)))
    document = ConsultationExportDocument(
        title=f"Tư vấn hợp tác - {name_a} và {name_b}",
        heading="BẢN LUẬN GIẢI TƯ VẤN HỢP TÁC",
        subtitle=f"{name_a} và {name_b}",
        filename_stem=f"BTE_TuVanHopTac_{identity}",
        summary_rows=rows,
        sections=profile.report_model.sections,
        notice=BUSINESS_SCOPE,
    )
    return export_marriage_file(stored, fmt, output_root=output_root, pdf_backend=pdf_backend, document=document)
