"""B1-P0-001: Professional Current Da Yun consultation for three golden charts."""

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

EXPECTED = {
    "son": "Ất Tỵ 2022–2031",
    "huynh": "Quý Mão 2021–2030",
    "tan": "Đinh Tỵ 2024–2033",
}

GLOSSARY = (
    "đại vận là",
    "mười đại vận được tính",
    "lý thuyết đại vận",
    "cách tính đại vận",
)

ENGINE_LEAKS = (
    "trục Dụng output",
    "trục Dụng visibility",
    "trục Dụng discipline",
    "trục Dụng growth",
    "trục Dụng peer",
    "sang peer",
    "sang discipline",
    "sang growth",
    "sang visibility",
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


def _section_paragraphs(payload: dict[str, Any], section_id: str) -> list[str]:
    """Paragraph texts of one published section."""
    for section in payload.get("sections") or []:
        if not isinstance(section, dict) or str(section.get("id") or "") != section_id:
            continue
        texts: list[str] = []
        for paragraph in section.get("paragraphs") or []:
            if isinstance(paragraph, dict):
                text = str(paragraph.get("text") or "").strip()
            else:
                text = str(paragraph).strip()
            if text:
                texts.append(text)
        return texts
    return []


def _overlap(left: str, right: str) -> float:
    """Token Jaccard."""
    a = set(left.casefold().split())
    b = set(right.casefold().split())
    if not a or not b:
        return 0.0
    return round(len(a & b) / len(a | b), 3)


def _page_count(path: Path) -> int | None:
    """Estimate PDF page count."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    matches = re.findall(rb"/Type\s*/Page(?![sA-Za-z])", data)
    return len(matches) if matches else None


def _validate(key: str, paragraphs: list[str]) -> list[str]:
    """Reject timestamp-only, glossary, or generic luck pages."""
    expected = EXPECTED[key]
    blob = "\n".join(paragraphs)
    failures: list[str] = []
    if not paragraphs:
        return ["missing_sec_luck"]
    if len(paragraphs) < 5:
        failures.append(f"too_few_paragraphs:{len(paragraphs)}")
    if expected not in blob:
        failures.append("missing_current_label")
    if len(blob.split()) < 80:
        failures.append("too_short")
    if all(_is_timestamp(item, expected) for item in paragraphs):
        failures.append("timestamp_only")
    lowered = blob.casefold()
    if any(marker in lowered for marker in GLOSSARY):
        failures.append("glossary")
    if any(marker.casefold() in lowered for marker in ENGINE_LEAKS):
        failures.append("engine_language")
    if "cơ hội chính" not in lowered:
        failures.append("missing_opportunity")
    if "áp lực chính" not in lowered:
        failures.append("missing_risk")
    if "hướng vận hành" not in lowered:
        failures.append("missing_direction")
    return failures


def _is_timestamp(text: str, current: str) -> bool:
    """True when the paragraph only names the cycle."""
    return current in text and len(text.split()) <= 14


def run() -> dict[str, Any]:
    """Generate Professional PDFs and score the Current Da Yun section."""
    export_dir = (
        ROOT / "knowledge" / "editorial_validation" / "exports" / "b1_p0_001" / "professional"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    runner = ProductionEngineRunner()
    orchestrator = ProductionEndToEndOrchestrator()
    results: dict[str, Any] = {}
    luck_blobs: dict[str, str] = {}
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
        orchestrator.run(request)
        luck = _section_paragraphs(payload, "sec-luck")
        luck_blobs[key] = "\n".join(luck)
        html_path = export_dir / f"BTE_{request.request_key}_Production_E2E.html"
        pdf_path = export_dir / f"BTE_{request.request_key}_Production_E2E.pdf"
        results[key] = {
            "name": request.full_name,
            "expected_current": EXPECTED[key],
            "luck_frame": (payload.get("metadata") or {}).get("luck_frame") or {},
            "paragraph_count": len(luck),
            "paragraphs": luck,
            "word_count": len(luck_blobs[key].split()),
            "failures": _validate(key, luck),
            "html_path": str(html_path) if html_path.exists() else "",
            "pdf_path": str(pdf_path) if pdf_path.exists() else "",
            "pdf_pages": _page_count(pdf_path) if pdf_path.exists() else None,
        }
    pairs = [("son", "huynh"), ("son", "tan"), ("huynh", "tan")]
    comparison = {
        f"{left}_vs_{right}": {
            "token_overlap": _overlap(luck_blobs[left], luck_blobs[right]),
            "identical_paragraphs": sorted(
                set(results[left]["paragraphs"]) & set(results[right]["paragraphs"])
            ),
        }
        for left, right in pairs
    }
    payload = {
        "results": results,
        "comparison": comparison,
        "pass": all(not item["failures"] for item in results.values())
        and all(
            item["token_overlap"] < 0.62 and not item["identical_paragraphs"]
            for item in comparison.values()
        ),
    }
    out_path = export_dir.parent / "_metrics.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = run()
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
