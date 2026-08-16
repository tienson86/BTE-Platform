"""WP-002 audit-only leak probe.

Inspects generated HTML/source text before PDF conversion.
Does not change production behavior, engines, narrative, or layout.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

LEAK_PATTERNS: tuple[str, ...] = (
    "Career:",
    "Health:",
    "Decision:",
    "Loaded",
    "Winner",
    "priority",
    "engine",
    "detector",
    "token",
    "Production phải truyền stems",
    "Knowledge không sửa engine",
)

DISTINCTIVE: tuple[str, ...] = (
    "Loaded 6 candidates from engine",
    "Loaded 7 candidates from engine",
    "Engine chọn Thực Thần",
    "Engine chọn Đinh",
    "Engine chọn Canh",
    "Decision Explanation",
    "Production phải truyền stems",
    "Knowledge không sửa engine",
    "priority 90",
    "priority 80",
    "Winner",
    "detector",
    "engine emit",
)


def count_leaks(text: str) -> dict[str, int]:
    """Count distinctive leak fragments in source text."""
    blob = text or ""
    folded = blob.casefold()
    counts: dict[str, int] = {}
    for pattern in LEAK_PATTERNS:
        if pattern.casefold() == pattern:
            counts[pattern] = folded.count(pattern.casefold())
        else:
            counts[pattern] = blob.count(pattern)
    for pattern in DISTINCTIVE:
        counts[f"exact::{pattern}"] = blob.count(pattern)
        if pattern not in counts:
            counts[f"ci::{pattern}"] = folded.count(pattern.casefold())
    return counts


def blob_from_mapping(value: Any) -> str:
    """Flatten JSON-like payloads to searchable text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except TypeError:
        return str(value)


def page_count_pdf(path: Path) -> int | None:
    """Estimate PDF page count from /Type /Page markers."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    matches = re.findall(rb"/Type\s*/Page(?![sA-Za-z])", data)
    return len(matches) if matches else None


def extract_pdf_ascii(path: Path) -> str:
    """Best-effort PDF text for leak search (no production change)."""
    data = path.read_bytes()
    latin = data.decode("latin-1", errors="ignore")
    utf16 = data.decode("utf-16-be", errors="ignore")
    return latin + "\n" + utf16


def _nonzero(counts: dict[str, int]) -> dict[str, int]:
    """Drop zero leak counts for compact audit output."""
    return {key: value for key, value in counts.items() if value}


def inspect_existing_pdfs(root: Path) -> list[dict[str, Any]]:
    """Inspect candidate customer PDFs already on disk."""
    rows: list[dict[str, Any]] = []
    patterns = (
        "knowledge/editorial_validation/exports/**/*.pdf",
        "knowledge/report_v1_validation/**/*.pdf",
        "knowledge/editorial_validation/exports/**/*.html",
    )
    seen: set[Path] = set()
    for pattern in patterns:
        for path in root.glob(pattern):
            if path in seen:
                continue
            seen.add(path)
            if path.suffix.lower() == ".pdf":
                text = extract_pdf_ascii(path)
                rows.append(
                    {
                        "path": str(path),
                        "kind": "pdf",
                        "bytes": path.stat().st_size,
                        "pages": page_count_pdf(path),
                        "leaks": _nonzero(count_leaks(text)),
                    }
                )
            else:
                text = path.read_text(encoding="utf-8", errors="ignore")
                rows.append(
                    {
                        "path": str(path),
                        "kind": "html",
                        "bytes": path.stat().st_size,
                        "pages": None,
                        "leaks": _nonzero(count_leaks(text)),
                    }
                )
    return rows


def _narrative_blob(payload: dict[str, Any] | None) -> str:
    """Concatenate customer-visible NarrativeResult sections."""
    if not payload:
        return ""
    parts: list[str] = []
    for section in payload.get("sections") or []:
        if not isinstance(section, dict):
            continue
        parts.append(str(section.get("title") or ""))
        for paragraph in section.get("paragraphs") or []:
            if isinstance(paragraph, dict):
                parts.append(str(paragraph.get("text") or ""))
            else:
                parts.append(str(paragraph))
        for rec in section.get("recommendations") or []:
            if isinstance(rec, dict):
                parts.append(str(rec.get("action") or rec.get("text") or ""))
    summary = payload.get("summary")
    if isinstance(summary, dict):
        parts.extend(str(item) for item in summary.values() if item)
    return "\n".join(parts)


def run_live_cases(root: Path) -> dict[str, Any]:
    """Regenerate the three charts on the current in-process production path."""
    from applications.api.services.orchestrator import OrchestratorService
    from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
    from applications.production.models import ProductionRequest
    from applications.production.orchestrator import ProductionEndToEndOrchestrator
    from engines.report_engine.adapters.report_input_v1_adapter import (
        build_report_input_v1,
    )
    from engines.report_engine.rendering.html_report_v1 import render_html

    export_dir = root / "knowledge" / "editorial_validation" / "exports" / "wp002"
    export_dir.mkdir(parents=True, exist_ok=True)
    cases = [
        ("son", CASE_0001_REQUEST.__class__(**{
            **{field: getattr(CASE_0001_REQUEST, field) for field in (
                "year", "month", "day", "hour", "minute", "gender",
                "timezone", "full_name", "birth_place", "case_id",
            )},
            "export_pdf": True,
            "export_dir": export_dir,
        })),
        ("huynh", ProductionRequest(
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
        )),
        ("tan", ProductionRequest(
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
        )),
    ]
    orchestrator = ProductionEndToEndOrchestrator()
    api = OrchestratorService()
    results: dict[str, Any] = {}
    for key, request in cases:
        production = orchestrator.run(request)
        html_path = export_dir / f"BTE_{request.request_key}_Production_E2E.html"
        pdf_path = export_dir / f"BTE_{request.request_key}_Production_E2E.pdf"
        html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        pdf_text = extract_pdf_ascii(pdf_path) if pdf_path.exists() else ""
        foundation = production.engine_output.interpretation_foundation if hasattr(production, "engine_output") else None
        # ProductionPipelineResult may not expose engine_output; inspect via runner.
        api_payload = api.analyze(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            gender=request.gender,
            timezone=request.timezone,
        )
        narrative = api_payload.get("narrative_result") or {}
        interpretation = api_payload.get("interpretation") or {}
        useful = api_payload.get("useful_god") or {}
        report = api_payload.get("report") or {}
        report_html = str(report.get("html") or "")
        v1_html = ""
        try:
            from applications.production.engine_runner import ProductionEngineRunner

            engine_output = ProductionEngineRunner().run(request)
            v1_html = render_html(build_report_input_v1(engine_output.report_source))
            explanation = None
            interpretation_b1 = None
            if engine_output.interpretation_foundation is not None:
                explanation = engine_output.interpretation_foundation.useful_god_explanation
                interpretation_b1 = engine_output.interpretation_foundation.useful_god_interpretation
            path_blob = ""
            if explanation is not None:
                path_blob = "\n".join(
                    f"{step.step_id}: {step.outcome}"
                    for step in explanation.decision_path
                )
            b1_reasoning = ""
            if interpretation_b1 is not None:
                b1_reasoning = "\n".join(interpretation_b1.reasoning)
        except Exception as exc:  # noqa: BLE001 — audit must continue
            engine_output = None
            path_blob = f"ERROR {type(exc).__name__}: {exc}"
            b1_reasoning = ""
            explanation = None

        results[key] = {
            "name": request.full_name,
            "commercial_html": str(html_path),
            "commercial_pdf": str(pdf_path),
            "commercial_html_pages_proxy_chars": len(html_text),
            "commercial_pdf_pages": page_count_pdf(pdf_path) if pdf_path.exists() else None,
            "commercial_html_leaks": _nonzero(count_leaks(html_text)),
            "commercial_pdf_leaks": _nonzero(count_leaks(pdf_text)),
            "narrative_generator": narrative.get("generator"),
            "narrative_status": narrative.get("status"),
            "narrative_section_count": len(narrative.get("sections") or []),
            "narrative_leaks": _nonzero(count_leaks(_narrative_blob(narrative))),
            "interpretation_section_count": interpretation.get("section_count"),
            "interpretation_leaks": _nonzero(count_leaks(blob_from_mapping(interpretation))),
            "useful_god_reasoning_leaks": _nonzero(count_leaks(str(useful.get("reasoning") or ""))),
            "api_report_html_leaks": _nonzero(count_leaks(report_html)),
            "report_v1_html_chars": len(v1_html),
            "report_v1_html_leaks": _nonzero(count_leaks(v1_html)),
            "decision_path_leaks": _nonzero(count_leaks(path_blob)),
            "b1_reasoning_leaks": _nonzero(count_leaks(b1_reasoning)),
            "b1_reasoning_preview": b1_reasoning[:500],
            "decision_path_preview": path_blob[:800],
            "has_foundation": engine_output is not None
            and getattr(engine_output, "interpretation_foundation", None) is not None,
        }
        if html_path.exists():
            (export_dir / f"{key}_leak_counts.json").write_text(
                json.dumps(results[key], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
    return results


def main() -> None:
    """Run the WP-002 audit probe and write JSON next to this file."""
    root = Path(__file__).resolve().parents[2]
    existing = inspect_existing_pdfs(root)
    live = run_live_cases(root)
    payload = {
        "existing_artifacts": existing,
        "live_reproduction": live,
    }
    out = Path(__file__).with_name("wp002_leak_probe_output.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"wrote": str(out), "existing": len(existing), "live": list(live)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
