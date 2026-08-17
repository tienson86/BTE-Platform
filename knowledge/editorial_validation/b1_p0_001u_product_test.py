"""B1-P0-001U: Useful God type preservation and customer display repair."""

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
from engines.interpretation_engine.foundation.knowledge import build_useful_god_knowledge_bundle

EXPECTED = {
    "son": {
        "selected": "Thực Thần",
        "entity_type": "role",
        "favorable": ("Thực Thần", "Thương Quan"),
        "unfavorable": ("Tỷ Kiên", "Kiếp Tài"),
        "display": "Dụng thần chính: Thực Thần",
        "forbidden": "Thực Thần (Kim)",
        "stem_ok": "",
    },
    "huynh": {
        "selected": "Đinh",
        "entity_type": "stem",
        "favorable": ("Đinh", "Bính", "Ất"),
        "unfavorable": ("Canh", "Tân"),
        "display": "Dụng thần chính: Đinh (Hỏa)",
        "forbidden": "",
        "stem_ok": "Đinh (Hỏa)",
    },
    "tan": {
        "selected": "Canh",
        "entity_type": "stem",
        "favorable": None,
        "unfavorable": None,
        "display": "Dụng thần chính: Canh (Kim)",
        "forbidden": "",
        "stem_ok": "Canh (Kim)",
    },
}


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


def _blob(payload: dict[str, Any]) -> str:
    """Flatten published customer text."""
    parts: list[str] = []
    for section in payload.get("sections") or []:
        if not isinstance(section, dict):
            continue
        for paragraph in section.get("paragraphs") or []:
            if isinstance(paragraph, dict):
                text = str(paragraph.get("text") or "").strip()
            else:
                text = str(paragraph).strip()
            if text:
                parts.append(text)
    return "\n".join(parts)


def _page_count(path: Path) -> int | None:
    """Estimate PDF page count."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    matches = re.findall(rb"/Type\s*/Page(?![sA-Za-z])", data)
    return len(matches) if matches else None


def _validate(
    key: str,
    *,
    engine_selected: str,
    facts_selected: str,
    facts_type: str,
    favorable: tuple[str, ...],
    unfavorable: tuple[str, ...],
    favorable_types: tuple[str, ...],
    unfavorable_types: tuple[str, ...],
    engine_favorable: tuple[str, ...],
    engine_unfavorable: tuple[str, ...],
    meaning: tuple[str, ...],
    published: str,
    html_text: str,
    knowledge_type: str,
) -> list[str]:
    """Check type preservation and customer display contract."""
    expected = EXPECTED[key]
    failures: list[str] = []
    if engine_selected != expected["selected"]:
        failures.append(f"engine_selected:{engine_selected}")
    if facts_selected != expected["selected"]:
        failures.append(f"facts_selected:{facts_selected}")
    if facts_type != expected["entity_type"]:
        failures.append(f"facts_type:{facts_type}")
    if knowledge_type != expected["entity_type"]:
        failures.append(f"knowledge_type:{knowledge_type}")
    if tuple(favorable) != tuple(engine_favorable):
        failures.append(f"hy_changed:{list(favorable)}")
    if tuple(unfavorable) != tuple(engine_unfavorable):
        failures.append(f"ky_changed:{list(unfavorable)}")
    expected_hy = expected["favorable"]
    expected_ky = expected["unfavorable"]
    if expected_hy is not None and tuple(favorable) != expected_hy:
        failures.append(f"hy:{list(favorable)}")
    if expected_ky is not None and tuple(unfavorable) != expected_ky:
        failures.append(f"ky:{list(unfavorable)}")
    if expected["entity_type"] == "role":
        if any(item != "role" for item in (*favorable_types, *unfavorable_types)):
            failures.append(f"hy_ky_types:{list(favorable_types)}/{list(unfavorable_types)}")
    meaning_blob = " ".join(meaning)
    if expected["display"] not in meaning_blob:
        failures.append("missing_display_in_explanation")
    if expected["forbidden"] and expected["forbidden"] in meaning_blob:
        failures.append("forbidden_in_explanation")
    if expected["display"] not in published and expected["display"] not in html_text:
        failures.append("missing_display_in_report")
    if expected["forbidden"] and (
        expected["forbidden"] in published or expected["forbidden"] in html_text
    ):
        failures.append("forbidden_in_report")
    if expected["stem_ok"] and expected["stem_ok"] not in published and expected["stem_ok"] not in html_text:
        failures.append("missing_stem_display")
    return failures


def run() -> dict[str, Any]:
    """Generate Professional PDFs and score Useful God type display."""
    export_dir = (
        ROOT
        / "knowledge"
        / "editorial_validation"
        / "exports"
        / "b1_p0_001u"
        / "professional"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    runner = ProductionEngineRunner()
    orchestrator = ProductionEndToEndOrchestrator()
    results: dict[str, Any] = {}
    for key, request in _cases(export_dir):
        engine_output = runner.run(request)
        foundation = engine_output.interpretation_foundation
        assert foundation is not None
        ug_facts = foundation.facts.useful_god
        explanation = foundation.useful_god_explanation
        assert explanation is not None
        knowledge = build_useful_god_knowledge_bundle(explanation)
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
        html_path = export_dir / f"BTE_{request.request_key}_Production_E2E.html"
        pdf_path = export_dir / f"BTE_{request.request_key}_Production_E2E.pdf"
        html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        meaning = tuple(item.statement for item in explanation.domain_meaning)
        published = _blob(payload)
        ug_view = engine_output.analysis.useful_god
        engine_selected = str(ug_view.useful_god or "") if ug_view is not None else ""
        engine_hy = tuple(str(item) for item in (ug_view.favorable_gods if ug_view else []))
        engine_ky = tuple(str(item) for item in (ug_view.unfavorable_gods if ug_view else []))
        failures = _validate(
            key,
            engine_selected=engine_selected,
            facts_selected=ug_facts.selected,
            facts_type=ug_facts.selected_entity_type,
            favorable=ug_facts.favorable_gods,
            unfavorable=ug_facts.unfavorable_gods,
            favorable_types=ug_facts.favorable_entity_types,
            unfavorable_types=ug_facts.unfavorable_entity_types,
            engine_favorable=engine_hy,
            engine_unfavorable=engine_ky,
            meaning=meaning,
            published=published,
            html_text=html_text,
            knowledge_type=knowledge.coverage.selected_entity_type,
        )
        results[key] = {
            "name": request.full_name,
            "engine_selected": engine_selected,
            "facts_selected": ug_facts.selected,
            "facts_entity_type": ug_facts.selected_entity_type,
            "knowledge_entity_type": knowledge.coverage.selected_entity_type,
            "explanation_entity_type": (
                explanation.decision.selected_entity_type if explanation.decision else ""
            ),
            "favorable": list(ug_facts.favorable_gods),
            "unfavorable": list(ug_facts.unfavorable_gods),
            "favorable_entity_types": list(ug_facts.favorable_entity_types),
            "unfavorable_entity_types": list(ug_facts.unfavorable_entity_types),
            "domain_meaning": list(meaning),
            "failures": failures,
            "html_path": str(html_path) if html_path.exists() else "",
            "pdf_path": str(pdf_path) if pdf_path.exists() else "",
            "pdf_pages": _page_count(pdf_path) if pdf_path.exists() else None,
        }
    payload = {
        "results": results,
        "pass": all(not item["failures"] for item in results.values()),
    }
    out_path = export_dir.parent / "_metrics.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = run()
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
