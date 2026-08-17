"""B1-P0-003: Production Luck Analysis Bridge product check."""

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

THESIS_MARKERS: tuple[str, ...] = (
    "quan trọng vì đây là thập niên",
    "cơ hội chính trong",
    "áp lực chính trong",
    "hướng vận hành nên giữ trong",
)
OVERLAP_MARKERS: tuple[str, ...] = (
    "trùng hỗ trợ",
    "trùng áp lực",
    "qua tàng can",
    "danh tính đại vận trùng",
)
INSUFFICIENT = "chưa xác định thêm tương tác ngoài luận giải gốc"


def _cases(export_dir: Path) -> list[tuple[str, ProductionRequest]]:
    """Three product-test charts. Birth data is not invented."""
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


def _validate(
    *,
    analysis: dict[str, Any],
    luck: list[str],
    chart: list[str],
    html_text: str,
) -> list[str]:
    """Score Luck Analysis consumption. Do not invent expected relations."""
    failures: list[str] = []
    if not analysis:
        failures.append("luck_analysis_not_stamped")
        return failures
    for field in (
        "current_period_identity",
        "governing_roles",
        "helpful_relations",
        "pressure_relations",
        "supported_direction",
        "restricted_direction",
        "confidence",
        "evidence",
        "diagnostics",
        "status",
    ):
        if field not in analysis:
            failures.append(f"missing_field:{field}")
    period = analysis.get("current_period_identity") or {}
    label = str(period.get("label") or "").strip()
    ten_god = str(period.get("ten_god") or "").strip()
    luck_blob = _blob(luck).casefold()
    if not luck:
        failures.append("luck_section_empty")
    if label and label.casefold() not in luck_blob:
        failures.append("luck_missing_period_label")
    if ten_god and ten_god.casefold() not in luck_blob:
        failures.append("luck_missing_period_ten_god")
    for marker in THESIS_MARKERS:
        if marker in luck_blob:
            failures.append(f"luck_thesis_copy:{marker}")
    for marker in OVERLAP_MARKERS:
        if marker in luck_blob:
            failures.append(f"luck_token_overlap:{marker}")
    helpful = list(analysis.get("helpful_relations") or [])
    pressure = list(analysis.get("pressure_relations") or [])
    if not helpful and not pressure:
        if INSUFFICIENT not in luck_blob:
            failures.append("missing_honest_insufficient")
        if "insufficient_luck_analysis" not in list(analysis.get("diagnostics") or []):
            failures.append("missing_insufficient_diagnostic")
        if str(analysis.get("status") or "") not in {"partial", "missing"}:
            failures.append("expected_partial_when_no_relations")
    chart_blob = _blob(chart).casefold()
    if INSUFFICIENT in chart_blob:
        failures.append("chart_has_luck_analysis")
    if html_text and label and label not in html_text:
        failures.append("html_missing_period_label")
    if html_text and ten_god and ten_god not in html_text:
        failures.append("html_missing_period_ten_god")
    return failures


def run() -> dict[str, Any]:
    """Generate Professional PDFs and score the Luck Analysis Bridge."""
    export_dir = (
        ROOT
        / "knowledge"
        / "editorial_validation"
        / "exports"
        / "b1_p0_003_luck_bridge"
        / "professional"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    runner = ProductionEngineRunner()
    orchestrator = ProductionEndToEndOrchestrator()
    results: dict[str, Any] = {}
    luck_texts: dict[str, str] = {}
    signatures: dict[str, str] = {}
    for key, request in _cases(export_dir):
        engine_output = runner.run(request)
        foundation = engine_output.interpretation_foundation
        assert foundation is not None
        analysis = foundation.luck_analysis.to_dict()
        payload = build_narrative_result_dict(
            analysis={
                "bazi": engine_output.analysis.bazi_dict(),
                "pattern": engine_output.analysis.pattern_dict(),
                "strength": engine_output.analysis.strength_dict(),
                "useful_god": engine_output.analysis.useful_god_dict(),
                "score": engine_output.analysis.score_dict(),
            },
            interpretation=engine_output.analysis.interpretation_dict(),
            run_id=request.case_id or request.request_key,
            engine_output=engine_output,
            publication_edition="professional",
        )
        stamped = (payload.get("metadata") or {}).get("luck_analysis") or {}
        luck = _section_texts(payload, "sec-luck")
        chart = _section_texts(payload, "sec-chart")
        orchestrator.run(request)
        html_path = export_dir / f"BTE_{request.request_key}_Production_E2E.html"
        pdf_path = export_dir / f"BTE_{request.request_key}_Production_E2E.pdf"
        html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        failures = _validate(
            analysis=stamped or analysis,
            luck=luck,
            chart=chart,
            html_text=html_text,
        )
        period = analysis.get("current_period_identity") or {}
        signature = "|".join(
            [
                str(period.get("gan_zhi") or ""),
                str(period.get("ten_god") or ""),
                ",".join(period.get("hidden_stems") or []),
                str(analysis.get("status") or ""),
            ]
        )
        signatures[key] = signature
        luck_texts[key] = _blob(luck)
        results[key] = {
            "name": request.full_name,
            "period": period.get("label"),
            "gan_zhi": period.get("gan_zhi"),
            "stem": period.get("stem"),
            "branch": period.get("branch"),
            "element": period.get("element"),
            "yin_yang": period.get("yin_yang"),
            "ten_god": period.get("ten_god"),
            "hidden_stems": period.get("hidden_stems"),
            "support_level": period.get("support_level"),
            "attack_level": period.get("attack_level"),
            "status": analysis.get("status"),
            "confidence": analysis.get("confidence"),
            "helpful": analysis.get("helpful_relations"),
            "pressure": analysis.get("pressure_relations"),
            "diagnostics": list(analysis.get("diagnostics") or []),
            "luck": luck,
            "failures": failures,
            "html_path": str(html_path) if html_path.exists() else "",
            "pdf_path": str(pdf_path) if pdf_path.exists() else "",
            "pdf_pages": _page_count(pdf_path) if pdf_path.exists() else None,
            "signature": signature,
        }
    comparison_failures: list[str] = []
    if len(set(signatures.values())) < 2:
        comparison_failures.append("cases_share_same_luck_analysis_signature")
    if len(set(luck_texts.values())) < 2:
        comparison_failures.append("luck_sections_not_fact_differentiated")
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
