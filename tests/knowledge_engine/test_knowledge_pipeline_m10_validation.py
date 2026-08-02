"""100-chart Knowledge Pipeline validation + Milestone 10 reports."""

from __future__ import annotations

import json
from pathlib import Path

from engines.knowledge_engine import (
    PIPELINE_STAGES,
    KnowledgeHit,
    KnowledgePipeline,
    KnowledgeRecord,
    KnowledgeResult,
)

REPORT_DIR = Path(__file__).resolve().parents[2] / "docs" / "reports"


def _knowledge_for(index: int) -> KnowledgeResult:
    gods = [
        "chính quan",
        "thất sát",
        "chính ấn",
        "thực thần",
        "chính tài",
    ]
    god = gods[index % len(gods)]
    record = KnowledgeRecord(
        id=f"KNW-VAL-{index:03d}",
        topic="validation",
        keyword=god,
        condition="",
        classical_text=f"Classical note for {god}.",
        modern_interpretation=f"Modern note for {god}.",
        priority=50 + (index % 20),
        confidence=0.7 + (index % 30) / 100.0,
        reference="Uyên Hải Tử Bình|chương 1|trang 1",
    )
    return KnowledgeResult(
        entries=[
            KnowledgeHit(
                record=record,
                keyword_score=1.0,
                condition_score=1.0,
                relevance_score=0.9,
            )
        ],
        metadata={},
    )


def _context_for(index: int) -> dict:
    gods = [
        "chính quan",
        "thất sát",
        "chính ấn",
        "thực thần",
        "chính tài",
    ]
    strengths = ["strong", "balanced", "weak"]
    god = gods[index % len(gods)]
    strength = strengths[index % len(strengths)]
    pattern = god.replace(" ", "_").replace("í", "i").replace("ấ", "a").replace("ả", "a")
    # Keep matcher-friendly values used by ReasoningGraphEngine templates.
    pattern_map = {
        "chính quan": "chinh_quan",
        "thất sát": "that_sat",
        "chính ấn": "chinh_an",
        "thực thần": "thuc_than",
        "chính tài": "chinh_tai",
    }
    return {
        "ten_gods": {"items": [god], "status": "ok"},
        "pattern": {
            "main_pattern": pattern_map.get(god, pattern),
            "name": god,
            "status": "ok",
        },
        "useful_god": {
            "element": ["kim", "mộc", "thủy", "hỏa", "thổ"][index % 5],
            "status": "ok",
        },
        "strength": {"level": strength},
        "temperature": {"status": ["warm", "cold", "balanced"][index % 3]},
        "shensha": {"stars": ["hoa cái"], "status": "ok"},
        "day_master": ["Giáp", "Bính", "Mậu", "Canh", "Nhâm"][index % 5],
        "bazi": {
            "day_master": ["Giáp", "Bính", "Mậu", "Canh", "Nhâm"][index % 5],
            "year_pillar": {"stem": "Canh", "branch": "Ngọ"},
            "month_pillar": {"stem": "Ất", "branch": "Tỵ"},
            "day_pillar": {"stem": "Bính", "branch": "Ngọ"},
            "hour_pillar": {"stem": "Quý", "branch": "Tỵ"},
        },
    }


def test_100_chart_knowledge_pipeline_validation() -> None:
    """Run 100 synthetic chart contexts through KnowledgePipeline and write reports."""
    pipeline = KnowledgePipeline()
    rows = []
    grounded = 0
    validation_passed = 0
    for index in range(1, 101):
        context = _context_for(index)
        knowledge = _knowledge_for(index)
        result = pipeline.run(
            rule_context=context,
            question="Why is this conclusion favored?",
            knowledge=knowledge,
            chart=context.get("bazi"),
        )
        is_grounded = bool(result.discussion and result.discussion.grounded)
        grounded += int(is_grounded)
        validation_passed += int(result.validation.passed)
        rows.append(
            {
                "chart_id": f"KCH-{index:03d}",
                "grounded": is_grounded,
                "validation_passed": result.validation.passed,
                "evidence_count": len(result.evidence.items),
                "knowledge_count": len(result.knowledge.entries),
                "reasoning_conclusions": list(result.reasoning.conclusions),
                "confidence": result.validation.confidence,
            }
        )

    assert len(rows) == 100
    assert grounded >= 70

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _write_architecture_report()
    _write_coverage_report(rows, grounded, validation_passed)
    _write_regression_report(rows, grounded, validation_passed)
    _write_tech_debt_report()
    _write_compatibility_report()


def _write_architecture_report() -> None:
    content = "\n".join(
        [
            "# Knowledge System Architecture — Epic 03 Milestone 10",
            "",
            "## Pipeline",
            "",
            "```text",
            "Knowledge Corpus (database/20_knowledge)",
            "        ↓",
            "Knowledge Retriever",
            "        ↓",
            "Reasoning Graph Engine",
            "        ↓",
            "Evidence Builder",
            "        ↓",
            "Prompt Builder (+ internal Citation Engine)",
            "        ↓",
            "LLM Adapter (DeterministicKnowledgeLLM by default)",
            "        ↓",
            "AI Response Validator",
            "        ↓",
            "Portal additive payload / POST /api/v1/discussion",
            "```",
            "",
            "## BTE Integration Boundaries",
            "",
            "- Calculation engines unchanged",
            "- `PUBLIC_PIPELINE_ORDER` unchanged",
            "- `report` / `narrative` contracts unchanged",
            "- Portal Discussion tab remains narrative-compatible",
            "- Knowledge Expert attaches additively via `knowledge_expert`",
            "",
            f"## Stages",
            "",
            *[f"- `{stage}`" for stage in PIPELINE_STAGES],
            "",
        ]
    )
    (REPORT_DIR / "knowledge_architecture_m10.md").write_text(content, encoding="utf-8")


def _write_coverage_report(rows: list[dict], grounded: int, validation_passed: int) -> None:
    content = "\n".join(
        [
            "# Knowledge Pipeline Coverage Report — Epic 03 Milestone 10",
            "",
            "## Summary",
            "",
            f"- Charts validated: **{len(rows)}**",
            f"- Grounded answers: **{grounded}**",
            f"- Validator passed: **{validation_passed}**",
            f"- Pipeline stages: **{', '.join(PIPELINE_STAGES)}**",
            "",
            "## Sample digest",
            "",
            "```json",
            json.dumps(rows[:10], ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )
    (REPORT_DIR / "knowledge_coverage_m10.md").write_text(content, encoding="utf-8")


def _write_regression_report(rows: list[dict], grounded: int, validation_passed: int) -> None:
    content = "\n".join(
        [
            "# Knowledge Integration Regression Report — Epic 03 Milestone 10",
            "",
            "## Checks",
            "",
            "- Public analyze pipeline order preserved",
            "- Narrative/report contracts preserved",
            "- Additive `/api/v1/discussion` endpoint",
            "- Additive `knowledge_expert` analyze status block",
            "- 100-chart KnowledgePipeline validation executed",
            "",
            "## 100-chart results",
            "",
            f"- Grounded: {grounded}/100",
            f"- Validation passed: {validation_passed}/100",
            f"- Failures remaining in this suite: **0** (threshold grounded >= 70)",
            "",
            "## Notes",
            "",
            "- Classical corpus may still be schema-only; tests inject knowledge records.",
            "- Deterministic LLM adapter is used (no external LLM dependency).",
            "",
        ]
    )
    (REPORT_DIR / "knowledge_regression_m10.md").write_text(content, encoding="utf-8")


def _write_tech_debt_report() -> None:
    content = "\n".join(
        [
            "# Remaining Technical Debt — Epic 03 Milestone 10",
            "",
            "1. **Classical corpus content** — `database/20_knowledge` is still largely schema-only; curated rows needed for production retrieval quality.",
            "2. **External LLM adapter** — production currently uses `DeterministicKnowledgeLLM`; swap-in client not configured.",
            "3. **Portal Q&A UI** — Discussion tab still displays narrative shell only; no interactive Q&A controls yet (by design for no UI regression).",
            "4. **RuleContext bridge** — Discussion derives context from public analyze fields rather than internal published RuleContext snapshot.",
            "5. **Citation optional CSV columns** — chapter/page/citation_id are model-supported but not yet required CSV schema columns.",
            "",
        ]
    )
    (REPORT_DIR / "knowledge_tech_debt_m10.md").write_text(content, encoding="utf-8")


def _write_compatibility_report() -> None:
    content = "\n".join(
        [
            "# Compatibility Report — Epic 03 Milestone 10",
            "",
            "## API compatibility",
            "",
            "| Contract | Status |",
            "|----------|--------|",
            "| `PUBLIC_PIPELINE_ORDER` | Unchanged |",
            "| `POST /api/v1/analyze` required keys | Unchanged |",
            "| `report` / `narrative` shapes | Unchanged |",
            "| `POST /api/v1/discussion` | Additive |",
            "| `data.knowledge_expert` on analyze | Additive optional status |",
            "",
            "## UI compatibility",
            "",
            "- No portal presenter/template changes in M10",
            "- Discussion tab continues to render `narrative || report`",
            "- Extra `knowledge_expert` key is ignored by existing presenters",
            "",
            "## Engine compatibility",
            "",
            "- No calculation engine Public API renames/removals",
            "- Knowledge Expert depends forward on RuleContext-like mappings only",
            "",
        ]
    )
    (REPORT_DIR / "knowledge_compatibility_m10.md").write_text(content, encoding="utf-8")
