"""B1-P0-003: Professional Ten Gods writing product check."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from applications.api.services.narrative_result_truth import build_narrative_result_dict
from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from applications.production.orchestrator import ProductionEndToEndOrchestrator

GLOSSARY: tuple[str, ...] = (
    "là quan hệ nhật chủ",
    "là dụng thần:",
    "là hỷ thần:",
    "là kỵ thần hoặc",
    "thập thần là",
)

SLOT_MARKERS: tuple[str, ...] = (
    "đang đóng vai trò",
    "ảnh hưởng hiện tại của",
    "với cấu trúc lá số này",
    "cơ hội từ",
    "rủi ro của",
    "việc cần làm với",
)


def _cases(export_dir: Path) -> list[tuple[str, ProductionRequest]]:
    """Three golden charts. Birth data is not invented."""
    return [
        (
            "son",
            ProductionRequest(
                case_id="CASE-0001",
                year=CASE_0001_REQUEST.year,
                month=CASE_0001_REQUEST.month,
                day=CASE_0001_REQUEST.day,
                hour=CASE_0001_REQUEST.hour,
                minute=CASE_0001_REQUEST.minute,
                gender=CASE_0001_REQUEST.gender,
                timezone=CASE_0001_REQUEST.timezone,
                full_name=CASE_0001_REQUEST.full_name,
                birth_place=CASE_0001_REQUEST.birth_place,
                export_pdf=True,
                export_dir=export_dir,
                options={"publication_edition": "professional"},
            ),
        ),
        (
            "huynh",
            ProductionRequest(
                case_id="HUYNH",
                year=1966,
                month=9,
                day=24,
                hour=4,
                minute=15,
                gender="male",
                timezone="Asia/Bangkok",
                full_name="Lương Ngọc Huỳnh",
                birth_place="Việt Nam",
                export_pdf=True,
                export_dir=export_dir,
                options={"publication_edition": "professional"},
            ),
        ),
        (
            "tan",
            ProductionRequest(
                case_id="TAN",
                year=2008,
                month=3,
                day=17,
                hour=6,
                minute=20,
                gender="male",
                timezone="Asia/Bangkok",
                full_name="Ngô Đặng Minh Tân",
                birth_place="Hà Nội",
                export_pdf=True,
                export_dir=export_dir,
                options={"publication_edition": "professional"},
            ),
        ),
    ]


def _section_texts(payload: dict[str, Any], section_id: str) -> list[str]:
    """Published paragraph texts for one section."""
    texts: list[str] = []
    for section in payload.get("sections") or []:
        if not isinstance(section, dict):
            continue
        if str(section.get("id") or "") != section_id:
            continue
        for paragraph in section.get("paragraphs") or []:
            if isinstance(paragraph, dict):
                text = str(paragraph.get("text") or "").strip()
            else:
                text = str(paragraph).strip()
            if text:
                texts.append(text)
    return texts


def _blob(texts: list[str]) -> str:
    """Join paragraphs for search."""
    return "\n".join(texts)


def _page_count(path: Path) -> int | None:
    """Estimate PDF page count."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    matches = re.findall(rb"/Type\s*/Page(?![sA-Za-z])", data)
    return len(matches) if matches else None


def _role_names(texts: list[str]) -> list[str]:
    """Ten Gods that received a role slot in this chapter."""
    names: list[str] = []
    pattern = re.compile(r"Trong lá số này, ([^,.]+?) đang đóng vai trò")
    for text in texts:
        match = pattern.search(text)
        if match:
            names.append(match.group(1).strip())
    return names


def _validate(texts: list[str], stamped: dict[str, Any]) -> list[str]:
    """Reject dictionary, catalogue, and detached writing."""
    failures: list[str] = []
    blob = _blob(texts)
    lowered = blob.casefold()
    if not texts:
        failures.append("ten_gods_section_empty")
        return failures
    if "trong lá số này" not in lowered:
        failures.append("missing_chart_opening")
    for marker in GLOSSARY:
        if marker in lowered:
            failures.append(f"glossary:{marker}")
    if "nhật chủ đang đóng vai trò" in lowered:
        failures.append("day_master_treated_as_ten_god")
    roles = _role_names(texts)
    if len(roles) < 2 or len(roles) > 3:
        failures.append(f"important_role_count:{len(roles)}")
    if len(set(roles)) != len(roles):
        failures.append("repeated_role_block")
    for marker in SLOT_MARKERS:
        count = lowered.count(marker)
        if count != len(roles):
            failures.append(f"slot_count:{marker}:{count}:expected:{len(roles)}")
    unique_paragraphs = set(texts)
    if len(unique_paragraphs) != len(texts):
        failures.append("duplicate_paragraph_in_chapter")
    pattern = str(stamped.get("pattern_label") or "").strip()
    useful = str(stamped.get("useful_god") or "").strip()
    dayun = str(stamped.get("current_dayun") or "").strip()
    if pattern and pattern not in blob:
        failures.append(f"missing_pattern:{pattern}")
    if useful and useful not in blob:
        failures.append(f"missing_useful_god:{useful}")
    if dayun and dayun not in blob:
        failures.append(f"missing_dayun:{dayun}")
    for role in roles:
        if not any(role in text and "đang đóng vai trò" in text for text in texts):
            failures.append(f"role_missing_chart_seat:{role}")
    return failures


def run() -> dict[str, Any]:
    """Generate Professional PDFs and score Ten Gods professional writing."""
    export_dir = (
        ROOT
        / "knowledge"
        / "editorial_validation"
        / "exports"
        / "b1_p0_003_ten_gods"
        / "professional"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    runner = ProductionEngineRunner()
    orchestrator = ProductionEndToEndOrchestrator()
    results: dict[str, Any] = {}
    chapters: dict[str, str] = {}
    role_sets: dict[str, str] = {}
    for key, request in _cases(export_dir):
        engine_output = runner.run(request)
        analysis = {
            "bazi": engine_output.analysis.bazi_dict(),
            "pattern": engine_output.analysis.pattern_dict(),
            "strength": engine_output.analysis.strength_dict(),
            "useful_god": engine_output.analysis.useful_god_dict(),
            "score": engine_output.analysis.score_dict(),
        }
        payload = build_narrative_result_dict(
            analysis=analysis,
            interpretation=engine_output.analysis.interpretation_dict(),
            run_id=request.case_id or request.request_key,
            engine_output=engine_output,
            publication_edition="professional",
        )
        stamped = (payload.get("metadata") or {}).get("ten_gods_consultation") or {}
        texts = _section_texts(payload, "sec-ten_gods")
        orchestrator.run(request)
        html_path = export_dir / f"BTE_{request.request_key}_Production_E2E.html"
        pdf_path = export_dir / f"BTE_{request.request_key}_Production_E2E.pdf"
        html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        failures = _validate(texts, stamped if isinstance(stamped, dict) else {})
        if html_text:
            lowered = html_text.casefold()
            if "trong lá số này, " not in lowered:
                failures.append("html_missing_chart_opening")
            if "đang đóng vai trò" not in lowered:
                failures.append("html_missing_role_slot")
        roles = _role_names(texts)
        chapters[key] = _blob(texts)
        role_sets[key] = "|".join(roles)
        results[key] = {
            "name": request.full_name,
            "pattern": stamped.get("pattern_label") if isinstance(stamped, dict) else "",
            "strength": stamped.get("strength_level") if isinstance(stamped, dict) else "",
            "useful_god": stamped.get("useful_god") if isinstance(stamped, dict) else "",
            "dayun": stamped.get("current_dayun") if isinstance(stamped, dict) else "",
            "dayun_ten_god": stamped.get("dayun_ten_god") if isinstance(stamped, dict) else "",
            "important_roles": roles,
            "paragraphs": texts,
            "paragraph_count": len(texts),
            "failures": failures,
            "html_path": str(html_path) if html_path.exists() else "",
            "pdf_path": str(pdf_path) if pdf_path.exists() else "",
            "pdf_pages": _page_count(pdf_path) if pdf_path.exists() else None,
        }
    comparison_failures: list[str] = []
    if len(set(chapters.values())) < 3:
        comparison_failures.append("chapters_not_meaning_differentiated")
    if len(set(role_sets.values())) < 2:
        comparison_failures.append("important_roles_not_chart_differentiated")
    payload = {
        "results": results,
        "comparison_failures": comparison_failures,
        "pass": all(not item["failures"] for item in results.values())
        and not comparison_failures,
    }
    out_path = export_dir.parent / "_metrics.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = run()
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
