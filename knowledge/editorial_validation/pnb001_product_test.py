"""PNB-001 product test: publish three charts and export customer PDFs."""

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

LEAK_FRAGMENTS = (
    "Career:",
    "Health:",
    "Decision:",
    "Loaded",
    "Winner",
    "priority 90",
    "priority 80",
    "candidates from engine",
    "Engine chọn",
    "detector",
    "Production phải truyền stems",
    "Knowledge không sửa engine",
    "Decision Explanation",
    "engine emit",
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
            ),
        ),
    ]


def _section_blob(payload: dict[str, Any]) -> str:
    """Customer-visible published section text."""
    parts: list[str] = []
    for section in payload.get("sections") or []:
        if not isinstance(section, dict):
            continue
        for paragraph in section.get("paragraphs") or []:
            if isinstance(paragraph, dict):
                parts.append(str(paragraph.get("text") or ""))
            else:
                parts.append(str(paragraph))
    summary = payload.get("summary")
    if isinstance(summary, dict):
        identity = summary.get("identity")
        if identity:
            parts.append(str(identity))
    return "\n".join(parts)


def _leak_hits(text: str) -> dict[str, int]:
    """Count distinctive leak fragments."""
    blob = text or ""
    return {item: blob.count(item) for item in LEAK_FRAGMENTS if blob.count(item)}


def _page_count(path: Path) -> int | None:
    """Estimate PDF page count."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    matches = re.findall(rb"/Type\s*/Page(?![sA-Za-z])", data)
    return len(matches) if matches else None


def run() -> dict[str, Any]:
    """Generate published PDFs and collect editorial metrics."""
    export_dir = ROOT / "knowledge" / "editorial_validation" / "exports" / "pnb001"
    export_dir.mkdir(parents=True, exist_ok=True)
    runner = ProductionEngineRunner()
    orchestrator = ProductionEndToEndOrchestrator()
    results: dict[str, Any] = {}
    for key, request in _cases(export_dir):
        engine_output = runner.run(request)
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
        )
        publication = (payload.get("metadata") or {}).get("publication") or {}
        metrics = publication.get("metrics") or {}
        decisions = publication.get("decisions") or []
        blob = _section_blob(payload)
        orchestrator.run(request)
        html_path = export_dir / f"BTE_{request.request_key}_Production_E2E.html"
        pdf_path = export_dir / f"BTE_{request.request_key}_Production_E2E.pdf"
        html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        results[key] = {
            "name": request.full_name,
            "case_id": request.case_id,
            "generator": payload.get("generator"),
            "publication_applied": publication.get("applied"),
            "metrics": metrics,
            "decision_counts": _count_decisions(decisions),
            "section_paragraphs": {
                str(section.get("id") or ""): len(section.get("paragraphs") or [])
                for section in payload.get("sections") or []
            },
            "leaks_narrative": _leak_hits(blob),
            "leaks_html": _leak_hits(html_text),
            "html_path": str(html_path) if html_path.exists() else "",
            "pdf_path": str(pdf_path) if pdf_path.exists() else "",
            "pdf_pages": _page_count(pdf_path) if pdf_path.exists() else None,
            "thesis_title": ((payload.get("metadata") or {}).get("case_thesis") or {}).get(
                "title"
            ),
        }
    out_path = ROOT / "knowledge" / "editorial_validation" / "exports" / "pnb001" / "_metrics.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results


def _count_decisions(decisions: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Published / dropped / appendix counts by section."""
    counts: dict[str, dict[str, int]] = {}
    for item in decisions:
        section_id = str(item.get("section_id") or "")
        decision = str(item.get("decision") or "")
        bucket = counts.setdefault(
            section_id, {"PUBLISH": 0, "DROP": 0, "APPENDIX": 0}
        )
        if decision in bucket:
            bucket[decision] += 1
    return counts


if __name__ == "__main__":
    payload = run()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
