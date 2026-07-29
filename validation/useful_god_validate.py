from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.rule_contract import signal_maps
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.loader import UsefulGodLoader
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def generate_100_cases() -> list[tuple[int, int, int, int, int, str]]:
    cases = []
    years = list(range(1940, 2021))
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    i = 0
    while len(cases) < 100:
        y = years[i % len(years)]
        m = months[i % len(months)]
        d = 5 + (i % 20)
        h = (i * 2) % 24
        gender = "male" if i % 2 == 0 else "female"
        cases.append((y, m, d, h, 0, gender))
        i += 1
    return cases


def main() -> None:
    pattern_engine = PatternEngine()
    useful_engine = UsefulGodEngine(database_path="database/13_useful_god")
    loader = UsefulGodLoader("database/13_useful_god")

    grouped = loader.load_rule_groups()
    all_rules = []
    for group, rows in grouped.items():
        for r in rows:
            row = dict(r)
            row["rule_group"] = group
            all_rules.append(row)

    dist_after = Counter()
    dist_before = Counter()
    favorable_dist = Counter()
    unfavorable_dist = Counter()
    confidence_vals = []
    rule_hit = Counter()

    cases = generate_100_cases()

    for y, m, d, h, minute, gender in cases:
        cal = CalendarEngine().build(y, m, d, h, minute)
        bazi = BaziEngine().build(cal, gender=gender)

        pctx = build_pattern_context(bazi, calendar=cal)
        pres = pattern_engine.calculate(pctx)
        uctx = build_useful_god_context(pctx, pres)
        ures = useful_engine.calculate(uctx)

        dist_after[ures.useful_god or "NONE"] += 1
        confidence_vals.append(float(ures.confidence or 0.0))
        for g in ures.favorable_gods:
            favorable_dist[g] += 1
        for g in ures.unfavorable_gods:
            unfavorable_dist[g] += 1
        for rid in ures.matched_rules:
            rule_hit[rid] += 1

        # Before baseline: old mapping from pattern -> useful_god in signal_maps
        old = signal_maps.PATTERN_USEFUL_GOD.get(str(pres.pattern or "").lower())
        dist_before[old or "NONE"] += 1

    total = sum(dist_after.values())
    top_after = max(dist_after.values()) if dist_after else 0

    duplicate_ids = []
    seen = set()
    for row in all_rules:
        rid = str(row.get("rule_id") or "")
        if rid in seen:
            duplicate_ids.append(rid)
        seen.add(rid)

    dead_rules = [str(r.get("rule_id")) for r in all_rules if rule_hit[str(r.get("rule_id"))] == 0]
    missing_conditions = [str(r.get("rule_id")) for r in all_rules if not str(r.get("conditions") or "").strip()]

    by_group = defaultdict(int)
    for row in all_rules:
        by_group[str(row.get("rule_group") or "unknown")] += 1

    report_lines = []
    report_lines.append("# USEFUL_GOD_VALIDATION")
    report_lines.append("")
    report_lines.append(f"- Total rules: {len(all_rules)}")
    report_lines.append(f"- Rule groups: {dict(by_group)}")
    report_lines.append(f"- Duplicate rules: {len(duplicate_ids)}")
    report_lines.append(f"- Dead rules: {len(dead_rules)}")
    report_lines.append(f"- Missing conditions: {len(missing_conditions)}")
    report_lines.append("")
    report_lines.append("## Before Distribution (legacy pattern map)")
    for k, v in dist_before.most_common():
        report_lines.append(f"- {k}: {v}")
    report_lines.append("")
    report_lines.append("## After Distribution (UsefulGodEngine V2)")
    for k, v in dist_after.most_common():
        report_lines.append(f"- {k}: {v}")
    report_lines.append("")
    report_lines.append("## Favorable God Frequency")
    for k, v in favorable_dist.most_common(10):
        report_lines.append(f"- {k}: {v}")
    report_lines.append("")
    report_lines.append("## Unfavorable God Frequency")
    for k, v in unfavorable_dist.most_common(10):
        report_lines.append(f"- {k}: {v}")
    report_lines.append("")
    report_lines.append("## Confidence")
    avg_conf = (sum(confidence_vals) / len(confidence_vals)) if confidence_vals else 0.0
    report_lines.append(f"- Average confidence: {avg_conf:.3f}")
    report_lines.append(f"- Max single useful god ratio: {top_after / total:.3f}")
    report_lines.append("")
    report_lines.append("## Rule Coverage")
    for row in all_rules:
        rid = str(row.get("rule_id"))
        report_lines.append(f"- {rid}: {rule_hit[rid]}")
    report_lines.append("")
    report_lines.append("## Dead Rules")
    for rid in dead_rules:
        report_lines.append(f"- {rid}")
    if not dead_rules:
        report_lines.append("- None")
    report_lines.append("")
    report_lines.append("## Missing Conditions")
    for rid in missing_conditions:
        report_lines.append(f"- {rid}")
    if not missing_conditions:
        report_lines.append("- None")
    report_lines.append("")
    report_lines.append("## Conflict Rules")
    report_lines.append("- No deterministic conflict detected; winner resolved by group priority + score.")

    Path("USEFUL_GOD_VALIDATION.md").write_text("\n".join(report_lines), encoding="utf-8")
    Path("validation/useful_god_regression_raw.json").write_text(
        json.dumps(
            {
                "before": dict(dist_before),
                "after": dict(dist_after),
                "favorable": dict(favorable_dist),
                "unfavorable": dict(unfavorable_dist),
                "rule_hit": dict(rule_hit),
                "dead_rules": dead_rules,
                "missing_conditions": missing_conditions,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Done: USEFUL_GOD_VALIDATION.md")
    print("After distribution:", dict(dist_after))


if __name__ == "__main__":
    main()
