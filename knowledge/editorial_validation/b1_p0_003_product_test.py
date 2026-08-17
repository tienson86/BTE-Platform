"""B1-P0-003: Interaction Truth integration product check."""

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

CHART_FORBIDDEN: tuple[str, ...] = (
    "danh tính đại vận",
    "trùng hỗ trợ",
    "trùng áp lực",
    "không lặp luận giải gốc",
)


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


def _factor_names(factors: list[Any]) -> list[str]:
    """Natal identities from overlap factors."""
    names: list[str] = []
    for item in factors:
        if isinstance(item, dict):
            name = str(item.get("natal_identity") or "").strip()
            if name:
                names.append(name)
    return names


def _validate(
    *,
    interaction: dict[str, Any],
    luck: list[str],
    chart: list[str],
    career: list[str],
    life_areas: list[str],
    recommendations: list[str],
    conclusion: list[str],
    html_text: str,
) -> list[str]:
    """Score Interaction Truth consumption. Do not invent expected overlap."""
    failures: list[str] = []
    if not interaction:
        failures.append("interaction_truth_not_stamped")
        return failures
    required = (
        "current_period_identity",
        "interaction_summary",
        "helpful_factors",
        "pressure_factors",
        "supported_direction",
        "restricted_direction",
        "confidence",
        "evidence",
        "diagnostics",
    )
    for field in required:
        if field not in interaction:
            failures.append(f"missing_field:{field}")
    period = interaction.get("current_period_identity") or {}
    label = str(period.get("label") or "").strip()
    luck_blob = _blob(luck).casefold()
    if not luck:
        failures.append("luck_section_empty")
    if label and label.casefold() not in luck_blob:
        failures.append("luck_missing_period_label")
    for marker in THESIS_MARKERS:
        if marker in luck_blob:
            failures.append(f"luck_thesis_copy:{marker}")
    empty = bool((interaction.get("interaction_summary") or {}).get("empty_overlap"))
    helpful = _factor_names(list(interaction.get("helpful_factors") or []))
    pressure = _factor_names(list(interaction.get("pressure_factors") or []))
    if empty:
        if "không trùng" not in luck_blob and "chưa có danh tính" not in luck_blob:
            failures.append("empty_overlap_not_stated")
        if helpful or pressure:
            failures.append("empty_overlap_but_factors_present")
    else:
        for name in helpful:
            if name.casefold() not in luck_blob:
                failures.append(f"helpful_missing_in_luck:{name}")
        for name in pressure:
            if name.casefold() not in luck_blob:
                failures.append(f"pressure_missing_in_luck:{name}")
    chart_blob = _blob(chart).casefold()
    for marker in CHART_FORBIDDEN:
        if marker in chart_blob:
            failures.append(f"chart_has_interaction:{marker}")
    overlay_blob = _blob(career + life_areas + recommendations + conclusion).casefold()
    if label and label.casefold() not in overlay_blob:
        failures.append("overlays_missing_period_label")
    if "không lặp luận giải gốc" not in overlay_blob and "không đổi" not in overlay_blob:
        failures.append("overlays_missing_honest_qualifier")
    if html_text and label and label not in html_text:
        failures.append("html_missing_period_label")
    return failures


def run() -> dict[str, Any]:
    """Generate Professional PDFs and score Interaction Truth integration."""
    export_dir = (
        ROOT
        / "knowledge"
        / "editorial_validation"
        / "exports"
        / "b1_p0_003"
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
        interaction = foundation.interaction_truth.to_dict()
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
        stamped = (payload.get("metadata") or {}).get("interaction_truth") or {}
        luck = _section_texts(payload, "sec-luck")
        chart = _section_texts(payload, "sec-chart")
        career = _section_texts(payload, "sec-career")
        life_areas = _section_texts(payload, "sec-life_areas")
        recommendations = _section_texts(payload, "sec-professional_recommendation")
        conclusion = _section_texts(payload, "sec-professional_conclusion")
        orchestrator.run(request)
        html_path = export_dir / f"BTE_{request.request_key}_Production_E2E.html"
        pdf_path = export_dir / f"BTE_{request.request_key}_Production_E2E.pdf"
        html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        failures = _validate(
            interaction=stamped or interaction,
            luck=luck,
            chart=chart,
            career=career,
            life_areas=life_areas,
            recommendations=recommendations,
            conclusion=conclusion,
            html_text=html_text,
        )
        helpful = _factor_names(list(interaction.get("helpful_factors") or []))
        pressure = _factor_names(list(interaction.get("pressure_factors") or []))
        period = interaction.get("current_period_identity") or {}
        summary = interaction.get("interaction_summary") or {}
        signature = "|".join(
            [
                str(period.get("gan_zhi") or ""),
                str(summary.get("empty_overlap")),
                ",".join(helpful),
                ",".join(pressure),
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
            "hidden_stems": period.get("hidden_stems"),
            "ten_god": period.get("ten_god"),
            "useful_god": summary.get("useful_god"),
            "status": interaction.get("status"),
            "confidence": interaction.get("confidence"),
            "empty_overlap": summary.get("empty_overlap"),
            "overlap_count": summary.get("overlap_count"),
            "helpful": helpful,
            "pressure": pressure,
            "diagnostics": list(interaction.get("diagnostics") or []),
            "luck": luck,
            "career_overlay": career[:1],
            "conclusion": conclusion,
            "failures": failures,
            "html_path": str(html_path) if html_path.exists() else "",
            "pdf_path": str(pdf_path) if pdf_path.exists() else "",
            "pdf_pages": _page_count(pdf_path) if pdf_path.exists() else None,
            "signature": signature,
        }
    unique_signatures = set(signatures.values())
    unique_luck = set(luck_texts.values())
    comparison_failures: list[str] = []
    if len(unique_signatures) < 2:
        comparison_failures.append("cases_share_same_interaction_signature")
    if len(unique_luck) < 2:
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
