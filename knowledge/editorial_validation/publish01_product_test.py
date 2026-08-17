"""PUBLISH-01 product test: Executive vs Professional editions for three charts."""

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


def _word_count(text: str) -> int:
    """Whitespace-separated tokens."""
    return len((text or "").split())


def _overlap_ratio(left: str, right: str) -> float:
    """Token Jaccard between two edition bodies. 1.0 means identical."""
    left_tokens = set(left.casefold().split())
    right_tokens = set(right.casefold().split())
    if not left_tokens or not right_tokens:
        return 0.0
    return round(len(left_tokens & right_tokens) / len(left_tokens | right_tokens), 3)


def _edition_snapshot(
    *,
    key: str,
    request: ProductionRequest,
    edition: str,
    payload: dict[str, Any],
    html_path: Path,
    pdf_path: Path,
) -> dict[str, Any]:
    """Collect edition metrics for the product report."""
    publication = (payload.get("metadata") or {}).get("publication") or {}
    blob = _section_blob(payload)
    html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    return {
        "name": request.full_name,
        "case_id": request.case_id,
        "edition": edition,
        "publication_edition": publication.get("edition") or edition,
        "metrics": publication.get("metrics") or {},
        "edition_metrics": publication.get("edition_metrics") or {},
        "section_ids": [
            str(section.get("id") or "")
            for section in payload.get("sections") or []
            if isinstance(section, dict)
        ],
        "section_paragraphs": {
            str(section.get("id") or ""): len(section.get("paragraphs") or [])
            for section in payload.get("sections") or []
            if isinstance(section, dict)
        },
        "word_count": _word_count(blob),
        "leaks_narrative": _leak_hits(blob),
        "leaks_html": _leak_hits(html_text),
        "html_path": str(html_path) if html_path.exists() else "",
        "pdf_path": str(pdf_path) if pdf_path.exists() else "",
        "pdf_pages": _page_count(pdf_path) if pdf_path.exists() else None,
        "thesis_title": ((payload.get("metadata") or {}).get("case_thesis") or {}).get(
            "title"
        ),
        "blob": blob,
    }


def _with_edition(request: ProductionRequest, export_dir: Path, edition: str) -> ProductionRequest:
    """Copy a request into an edition export folder."""
    options = dict(request.options or {})
    options["publication_edition"] = edition
    return ProductionRequest(
        case_id=request.case_id,
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
        full_name=request.full_name,
        birth_place=request.birth_place,
        export_pdf=True,
        export_dir=export_dir,
        options=options,
    )


def run() -> dict[str, Any]:
    """Generate Executive and Professional PDFs and compare them."""
    root = ROOT / "knowledge" / "editorial_validation" / "exports" / "publish01"
    exec_dir = root / "executive"
    pro_dir = root / "professional"
    exec_dir.mkdir(parents=True, exist_ok=True)
    pro_dir.mkdir(parents=True, exist_ok=True)
    runner = ProductionEngineRunner()
    orchestrator = ProductionEndToEndOrchestrator()
    results: dict[str, Any] = {}
    for key, base in _cases(root):
        engine_output = runner.run(base)
        analysis = {
            "bazi": engine_output.analysis.bazi_dict(),
            "pattern": engine_output.analysis.pattern_dict(),
            "strength": engine_output.analysis.strength_dict(),
            "useful_god": engine_output.analysis.useful_god_dict(),
            "score": engine_output.analysis.score_dict(),
        }
        interpretation = engine_output.analysis.interpretation_dict()
        executive_payload = build_narrative_result_dict(
            analysis=analysis,
            interpretation=interpretation,
            run_id=base.case_id or base.request_key,
            engine_output=engine_output,
            publication_edition="executive",
        )
        professional_payload = build_narrative_result_dict(
            analysis=analysis,
            interpretation=interpretation,
            run_id=base.case_id or base.request_key,
            engine_output=engine_output,
            publication_edition="professional",
        )
        exec_request = _with_edition(base, exec_dir, "executive")
        pro_request = _with_edition(base, pro_dir, "professional")
        orchestrator.run(exec_request)
        orchestrator.run(pro_request)
        exec_html = exec_dir / f"BTE_{base.request_key}_Production_E2E.html"
        exec_pdf = exec_dir / f"BTE_{base.request_key}_Production_E2E.pdf"
        pro_html = pro_dir / f"BTE_{base.request_key}_Production_E2E.html"
        pro_pdf = pro_dir / f"BTE_{base.request_key}_Production_E2E.pdf"
        executive = _edition_snapshot(
            key=key,
            request=base,
            edition="executive",
            payload=executive_payload,
            html_path=exec_html,
            pdf_path=exec_pdf,
        )
        professional = _edition_snapshot(
            key=key,
            request=base,
            edition="professional",
            payload=professional_payload,
            html_path=pro_html,
            pdf_path=pro_pdf,
        )
        exec_blob = str(executive.pop("blob"))
        pro_blob = str(professional.pop("blob"))
        results[key] = {
            "name": base.full_name,
            "executive": executive,
            "professional": professional,
            "comparison": {
                "executive_words": executive["word_count"],
                "professional_words": professional["word_count"],
                "added_words": professional["word_count"] - executive["word_count"],
                "executive_pages": executive["pdf_pages"],
                "professional_pages": professional["pdf_pages"],
                "token_overlap": _overlap_ratio(exec_blob, pro_blob),
                "professional_has_more_sections": len(professional["section_ids"])
                > len(executive["section_ids"]),
                "copied_executive_summary_into_core": _copied_summary(
                    executive_payload, professional_payload
                ),
            },
        }
    out_path = root / "_metrics.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results


def _copied_summary(executive: dict[str, Any], professional: dict[str, Any]) -> bool:
    """True when core interpretation reprints the executive briefing."""
    exec_summary = _section_text(executive, "sec-executive_summary")
    core = _section_text(professional, "sec-core_interpretation")
    if not exec_summary or not core:
        return False
    return _overlap_ratio(exec_summary, core) >= 0.72


def _section_text(payload: dict[str, Any], section_id: str) -> str:
    """Join one section's paragraphs."""
    for section in payload.get("sections") or []:
        if not isinstance(section, dict) or str(section.get("id") or "") != section_id:
            continue
        parts = []
        for paragraph in section.get("paragraphs") or []:
            if isinstance(paragraph, dict):
                parts.append(str(paragraph.get("text") or ""))
            else:
                parts.append(str(paragraph))
        return "\n".join(parts)
    return ""


if __name__ == "__main__":
    payload = run()
    summary = {
        key: {
            "name": item["name"],
            "comparison": item["comparison"],
            "executive_sections": item["executive"]["section_ids"],
            "professional_sections": item["professional"]["section_ids"],
        }
        for key, item in payload.items()
    }
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
