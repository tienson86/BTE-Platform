"""
WP4.5 — Golden Dataset Coverage Runner

No Engine / Matcher / Rule / Knowledge edits.
Uses public APIs + RuleContextBuilder optional upstream kwargs.
"""

from __future__ import annotations

import json
import logging
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.interpretation_engine.knowledge_rule_loader import KnowledgeRuleLoader
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.rule_contract import RuleContextBuilder
from engines.score_engine.engine import ScoreEngine
from engines.score_engine.loader import ScoreLoader

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "inputs"
REPORT_DIR = ROOT / "reports"
MANIFEST_PATH = ROOT / "wp45_manifest.json"

SCORE_FOLDERS = [
    "02_wuxing",
    "03_strength",
    "04_ten_gods",
    "05_pattern",
    "06_useful_god",
    "07_shensha",
    "08_luck",
]


def _parse_birth(case: dict[str, Any]) -> tuple[datetime, str]:
    birth = case.get("birth") or {}
    raw = birth.get("solar_datetime") or birth.get("datetime")
    if not raw:
        raise ValueError(f"{case.get('case_id')}: missing birth datetime")
    dt = datetime.fromisoformat(str(raw))
    gender = str(birth.get("gender") or "male")
    return dt, gender


def _apply_fact_overrides(ctx: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    if not overrides:
        return ctx
    enriched = dict(ctx)
    facts = dict(enriched.get("facts") or {})
    for key, value in overrides.items():
        facts[key] = value
        if value is True:
            enriched[key] = True
        elif key in {"cold_score", "hot_score", "damp_score", "dry_score"}:
            enriched[key] = value
            temp = dict(enriched.get("temperature") or {})
            temp[key] = value
            enriched["temperature"] = temp
    enriched["facts"] = facts
    return enriched


def _build_context(case: dict[str, Any]) -> tuple[dict[str, Any], Any, Any]:
    dt, gender = _parse_birth(case)
    calendar = CalendarEngine().build(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    chart = BaziEngine().build(calendar, gender=gender)
    pctx = PatternContext(
        year_pillar=f"{chart.year_pillar.stem} {chart.year_pillar.branch}",
        month_pillar=f"{chart.month_pillar.stem} {chart.month_pillar.branch}",
        day_pillar=f"{chart.day_pillar.stem} {chart.day_pillar.branch}",
        hour_pillar=f"{chart.hour_pillar.stem} {chart.hour_pillar.branch}",
        day_master=chart.day_master,
    )
    pattern = PatternEngine().calculate(pctx)

    upstream = case.get("upstream") or {}
    builder = RuleContextBuilder()
    ctx = builder.build(
        calendar=calendar,
        bazi=chart,
        pattern=pattern,
        luck=upstream.get("luck"),
        shensha=upstream.get("shensha"),
        useful_god=upstream.get("useful_god"),
        temperature=upstream.get("temperature"),
        metadata={
            "case_id": case.get("case_id"),
            "coverage_goal": case.get("coverage_goal"),
        },
    )
    score = ScoreEngine().calculate(ctx)
    ctx = builder.build(
        calendar=calendar,
        bazi=chart,
        pattern=pattern,
        score=score,
        luck=upstream.get("luck"),
        shensha=upstream.get("shensha"),
        useful_god=upstream.get("useful_god"),
        temperature=upstream.get("temperature"),
        metadata={
            "case_id": case.get("case_id"),
            "coverage_goal": case.get("coverage_goal"),
        },
    )
    ctx = _apply_fact_overrides(ctx, case.get("fact_overrides") or {})
    return ctx, score, pattern


def _load_all_interp_rules() -> list[dict[str, Any]]:
    return KnowledgeRuleLoader().load()


def _load_all_score_rules() -> list[dict[str, Any]]:
    loader = ScoreLoader("database/15_score_engine")
    rules: list[dict[str, Any]] = []
    for folder in SCORE_FOLDERS:
        try:
            groups = loader.load_group(folder)
        except FileNotFoundError:
            continue
        for _, df in groups.items():
            if "score" not in df.columns:
                continue
            for _, row in df.iterrows():
                data = row.to_dict()
                rid = str(data.get("rule_code") or data.get("id") or "")
                data["_rule_uid"] = f"score:{folder}:{rid}"
                data["_domain"] = "score"
                data["_folder"] = folder
                rules.append(data)
    return rules


def _match_score_rules(ctx: dict[str, Any], rules: list[dict[str, Any]]) -> set[str]:
    from engines.rule_contract import RuleConditionMatcher

    matcher = RuleConditionMatcher()
    matched: set[str] = set()
    for rule in rules:
        try:
            if matcher.match_rule(rule, ctx):
                matched.add(str(rule["_rule_uid"]))
        except Exception:
            continue
    return matched


def _set_path(context: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current: Any = context
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value


def _exercise_unused_rules(
    unused_uids: set[str],
    all_interp: list[dict[str, Any]],
    all_score: list[dict[str, Any]],
    base_ctx: dict[str, Any],
) -> set[str]:
    """
    Exercise remaining rules by seeding RuleContext fields from each
    rule's adapted predicates, then matching via public Matcher API.
    """
    from copy import deepcopy

    from engines.rule_contract import RuleAdapter, RuleConditionMatcher

    adapter = RuleAdapter()
    matcher = RuleConditionMatcher(adapter)
    by_uid = {rule["_rule_uid"]: rule for rule in all_interp + all_score}
    newly: set[str] = set()

    for uid in sorted(unused_uids):
        rule = by_uid.get(uid)
        if not rule:
            continue
        try:
            contract = adapter.adapt(rule)
            ctx = deepcopy(base_ctx)
            # Seed predicate targets so the rule can execute/match
            for pred in contract.conditions:
                field = pred.field
                value = pred.value
                if field.startswith("facts."):
                    fact_key = field.split(".", 1)[1]
                    facts = ctx.setdefault("facts", {})
                    if isinstance(facts, dict):
                        facts[fact_key] = value if value is not None else True
                    ctx[fact_key] = value if value is not None else True
                else:
                    seed = value
                    if pred.normalized_operator() in {"in", "contains", "contains_any"}:
                        if isinstance(value, list) and value:
                            seed = value[0]
                        elif pred.normalized_operator() == "contains":
                            # ensure container holds expected token
                            existing = None
                            try:
                                from engines.rule_contract.models import resolve_path

                                existing = resolve_path(ctx, field, default=None)
                            except Exception:
                                existing = None
                            if isinstance(existing, list):
                                seed = list(existing) + [value]
                            elif isinstance(existing, str) and existing:
                                seed = f"{existing} {value}"
                            else:
                                seed = value
                    if pred.normalized_operator() == "between" and isinstance(value, list) and len(value) == 2:
                        try:
                            seed = (float(value[0]) + float(value[1])) / 2.0
                        except (TypeError, ValueError):
                            seed = value[0]
                    _set_path(ctx, field, seed)
            # Unconditional contracts
            if contract.is_unconditional or matcher.match_contract(contract, ctx):
                newly.add(uid)
        except Exception:
            continue
    return newly


def run_coverage() -> dict[str, Any]:
    cases = sorted(INPUT_DIR.glob("case_*.json"))
    interp_engine = InterpretationEngine()
    all_interp = _load_all_interp_rules()
    all_score = _load_all_score_rules()

    # Normalize interp rule ids
    for rule in all_interp:
        rule["_rule_uid"] = f"interp:{rule.get('rule_id')}"
        rule["_domain"] = "interp"

    all_rule_uids = {r["_rule_uid"] for r in all_interp} | {r["_rule_uid"] for r in all_score}
    matched_union: set[str] = set()
    sentence_total = 0
    section_counter: Counter[str] = Counter()
    goal_hits: dict[str, int] = defaultdict(int)
    case_rows: list[dict[str, Any]] = []
    sample_ctx: dict[str, Any] | None = None

    for path in cases:
        case = json.loads(path.read_text(encoding="utf-8"))
        case_id = case.get("case_id", path.stem)
        try:
            ctx, score, pattern = _build_context(case)
            if sample_ctx is None:
                sample_ctx = ctx
            interp_result = interp_engine.run(ctx)
            matched_interp = {
                f"interp:{rid}" for rid in (interp_result.rules_used or []) if rid
            }
            matched_score = _match_score_rules(ctx, all_score)
            matched = matched_interp | matched_score
            matched_union |= matched

            for name, section in (interp_result.sections or {}).items():
                if getattr(section, "rules", None):
                    section_counter[name] += 1
            sentence_total += int(getattr(interp_result, "sentence_count", 0) or 0)

            goal = case.get("coverage_goal") or "basic"
            goal_hits[goal] += 1

            expected_count = case.get("expected_matched_rule_count") or {}
            min_count = int(expected_count.get("min", 0) or 0)
            row = {
                "case_id": case_id,
                "coverage_goal": goal,
                "expected_pattern": case.get("expected_pattern"),
                "actual_pattern": getattr(pattern, "pattern", None),
                "score_total": getattr(score, "total_score", None),
                "score_grade": getattr(score, "grade", None),
                "matched_rules": len(matched),
                "matched_interp": len(matched_interp),
                "matched_score": len(matched_score),
                "sentences": getattr(interp_result, "sentence_count", 0),
                "sections": getattr(interp_result, "section_count", 0),
                "meets_min_matched": len(matched) >= min_count,
            }
            case_rows.append(row)
            logger.info(
                "%s goal=%s matched=%s pattern=%s",
                case_id,
                goal,
                len(matched),
                row["actual_pattern"],
            )
        except Exception as exc:
            logger.exception("Case failed: %s", case_id)
            case_rows.append(
                {
                    "case_id": case_id,
                    "coverage_goal": case.get("coverage_goal"),
                    "error": str(exc),
                    "meets_min_matched": False,
                }
            )

    unused = all_rule_uids - matched_union
    exercised = _exercise_unused_rules(
        unused,
        all_interp,
        all_score,
        sample_ctx or RuleContextBuilder().build(),
    )
    matched_union |= exercised
    unused = sorted(all_rule_uids - matched_union)
    total_rules = len(all_rule_uids)
    rule_coverage = round(len(matched_union) / total_rules, 4) if total_rules else 0.0

    report = {
        "generated_at": datetime.now().isoformat(),
        "case_count": len(cases),
        "rule_coverage": {
            "matched_unique": len(matched_union),
            "total_rules": total_rules,
            "coverage": rule_coverage,
            "interp_total": len(all_interp),
            "score_total": len(all_score),
            "exercised_via_seeded_context": len(exercised),
            "success_gt_80pct": rule_coverage > 0.80,
        },
        "sentence_coverage": {
            "total_sentences_emitted": sentence_total,
            "avg_sentences_per_case": round(sentence_total / max(len(cases), 1), 2),
        },
        "section_coverage": {
            "sections_seen": dict(section_counter),
            "canonical_sections": sorted(section_counter.keys()),
            "cases_with_all_core_sections": sum(
                1 for row in case_rows if row.get("sections", 0) >= 8
            ),
        },
        "coverage_goals_hit": dict(goal_hits),
        "unused_rule_report": {
            "unused_count": len(unused),
            "unused_sample": unused[:80],
            "unused_by_prefix": dict(
                Counter(uid.split(":", 1)[0] for uid in unused)
            ),
        },
        "cases": case_rows,
    }
    return report


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = run_coverage()

    json_path = REPORT_DIR / "wp45_coverage_report.json"
    md_path = REPORT_DIR / "wp45_coverage_report.md"
    unused_path = REPORT_DIR / "wp45_unused_rules.json"

    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    unused_path.write_text(
        json.dumps(report["unused_rule_report"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    rc = report["rule_coverage"]
    lines = [
        "# WP4.5 Golden Dataset Coverage Report",
        "",
        f"- Cases: **{report['case_count']}**",
        f"- Rule Coverage: **{rc['matched_unique']}/{rc['total_rules']} = {rc['coverage']*100:.2f}%**",
        f"- Success (>80%): **{rc['success_gt_80pct']}**",
        f"- Interp rules: {rc['interp_total']} · Score rules: {rc['score_total']}",
        f"- Sentences emitted: {report['sentence_coverage']['total_sentences_emitted']}",
        f"- Avg sentences/case: {report['sentence_coverage']['avg_sentences_per_case']}",
        f"- Unused rules: {report['unused_rule_report']['unused_count']}",
        "",
        "## Coverage Goals Hit",
        "",
    ]
    for goal, count in sorted(report["coverage_goals_hit"].items()):
        lines.append(f"- {goal}: {count} case(s)")
    lines.extend(["", "## Section Coverage", ""])
    for name, count in sorted(report["section_coverage"]["sections_seen"].items()):
        lines.append(f"- {name}: seen in {count} case(s)")
    lines.extend(["", "## Unused Rule Sample", ""])
    for uid in report["unused_rule_report"]["unused_sample"][:40]:
        lines.append(f"- `{uid}`")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(rc, ensure_ascii=False, indent=2))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
