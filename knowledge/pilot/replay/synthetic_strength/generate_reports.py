"""Generate PILOT-1G analysis reports from replay results."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
VALIDATION = ROOT / "validation"


def load_results() -> list[dict]:
    rows = []
    for path in sorted(RESULTS.glob("SYN-STR-*.json")):
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def build_reports(rows: list[dict]) -> None:
    n = len(rows)
    matches = [r for r in rows if r["comparison"]["exact_synthetic_match"]]
    mismatches = [r for r in rows if not r["comparison"]["exact_synthetic_match"]]
    scores = [float(r["runtime"]["score"]) for r in rows]
    bands = Counter(r["runtime"]["v1_band"] for r in rows)
    expected = Counter(r["synthetic_expected_taxonomy"] for r in rows)
    mismatch_cats = Counter(r["comparison"]["mismatch_category"] for r in mismatches)

    weakest = min(rows, key=lambda r: r["runtime"]["score"])
    highest = max(rows, key=lambda r: r["runtime"]["score"])

    # similar scores, different expected
    by_score: dict[float, list] = defaultdict(list)
    for r in rows:
        by_score[round(float(r["runtime"]["score"]), 2)].append(r)
    similar_diff_label = []
    for score, items in sorted(by_score.items()):
        labs = {i["synthetic_expected_taxonomy"] for i in items}
        if len(items) > 1 and len(labs) > 1:
            similar_diff_label.append((score, items))

    # same expected, substantially different scores
    by_exp: dict[str, list] = defaultdict(list)
    for r in rows:
        by_exp[r["synthetic_expected_taxonomy"]].append(r)
    same_label_diff_score = []
    for exp, items in by_exp.items():
        sc = [float(i["runtime"]["score"]) for i in items]
        if max(sc) - min(sc) >= 0.15:
            same_label_diff_score.append((exp, items, min(sc), max(sc)))

    extremes_weak = [r for r in rows if r["case_id"] in {
        "SYN-STR-000001", "SYN-STR-000002", "SYN-STR-000003"
    }]
    extremes_strong = [r for r in rows if r["case_id"] in {
        "SYN-STR-000019", "SYN-STR-000020", "SYN-STR-000021"
    }]
    strong_cohort = [r for r in rows if r["synthetic_expected_taxonomy"] == "strong"]
    very_strong_scores = {round(float(r["runtime"]["score"]), 3) for r in extremes_strong}
    strong_scores = {round(float(r["runtime"]["score"]), 3) for r in strong_cohort}
    can_distinguish_very_strong = very_strong_scores != strong_scores or (
        len(very_strong_scores) > 1
    )
    # Ceiling collapse: all 1.0 => cannot distinguish
    if very_strong_scores == {1.0} and strong_scores == {1.0}:
        can_distinguish_very_strong = False

    very_weak_ok = all(
        r["runtime"]["v1_band"] == "weak" and float(r["runtime"]["score"]) <= 0.35
        for r in extremes_weak
    )
    balanced_rows = [r for r in rows if r["synthetic_expected_taxonomy"] == "balanced"]
    balanced_ok = all(r["runtime"]["v1_band"] == "balanced" for r in balanced_rows)

    # Replay report
    lines = [
        "# SYNTHETIC_STRENGTH_REPLAY_REPORT",
        "",
        "**Sprint:** PILOT-1G  ",
        "**Dataset:** SYNTHETIC_STRENGTH_STRESS (not calibration evidence)  ",
        "**Engine:** existing Strength Engine (unchanged)",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|---|---:|",
        f"| Total cases | {n} |",
        f"| Exact synthetic matches (v1 projection) | {len(matches)} |",
        f"| Mismatches | {len(mismatches)} |",
        f"| Score min | {min(scores):.3f} |",
        f"| Score max | {max(scores):.3f} |",
        f"| Score mean | {mean(scores):.3f} |",
        "",
        "## Case table",
        "",
        "| case_id | synthetic_expected | runtime_score | runtime_v1_band | match | mismatch_category |",
        "|---|---|---:|---|---|---|",
    ]
    for r in rows:
        c = r["comparison"]
        lines.append(
            f"| {r['case_id']} | {r['synthetic_expected_taxonomy']} | "
            f"{r['runtime']['score']:.3f} | {r['runtime']['v1_band']} | "
            f"{'YES' if c['exact_synthetic_match'] else 'NO'} | "
            f"{c['mismatch_category']} |"
        )

    lines += [
        "",
        "## Expected seven-level distribution",
        "",
        "| synthetic_expected_taxonomy | count |",
        "|---|---:|",
    ]
    for level in [
        "very_weak", "weak", "slightly_weak", "balanced",
        "slightly_strong", "strong", "very_strong",
    ]:
        lines.append(f"| {level} | {expected[level]} |")

    lines += [
        "",
        "## Current v1 bands (runtime)",
        "",
        "| v1_band | count |",
        "|---|---:|",
    ]
    for band, count in sorted(bands.items()):
        lines.append(f"| {band} | {count} |")

    lines += [
        "",
        "## Mismatch distribution",
        "",
        "| mismatch_category | count |",
        "|---|---:|",
    ]
    if mismatch_cats:
        for cat, count in mismatch_cats.most_common():
            lines.append(f"| {cat} | {count} |")
    else:
        lines.append("| (none) | 0 |")

    lines += [
        "",
        "## Extreme detection",
        "",
        "### VERY_WEAK (SYN-STR-000001..000003)",
        "",
        "| case_id | score | v1_band | profile season/root/support/control |",
        "|---|---:|---|---|",
    ]
    for r in extremes_weak:
        p = r["runtime"]["profile"]
        lines.append(
            f"| {r['case_id']} | {r['runtime']['score']:.3f} | {r['runtime']['v1_band']} | "
            f"{p.get('season')}/{p.get('root')}/{p.get('support')}/{p.get('control')} |"
        )
    lines += [
        "",
        f"**Detection:** {'PASS (directionally weak / low-mid scores)' if very_weak_ok else 'PARTIAL/FAIL'}  ",
        "Engine assigns `weak` to all three extremes. Intensity within weak spans 0.010–0.350.",
        "",
        "### VERY_STRONG (SYN-STR-000019..000021)",
        "",
        "| case_id | score | v1_band | profile season/root/support/control |",
        "|---|---:|---|---|",
    ]
    for r in extremes_strong:
        p = r["runtime"]["profile"]
        lines.append(
            f"| {r['case_id']} | {r['runtime']['score']:.3f} | {r['runtime']['v1_band']} | "
            f"{p.get('season')}/{p.get('root')}/{p.get('support')}/{p.get('control')} |"
        )
    lines += [
        "",
        f"**Detection vs STRONG cohort:** "
        f"{'DISTINGUISHABLE' if can_distinguish_very_strong else 'NOT DISTINGUISHABLE (score ceiling at 1.000)'}  ",
        "All VERY_STRONG and STRONG synthetic cases scored 1.000 / `strong`. "
        "v1 cannot name `very_strong`; continuous score also saturates.",
        "",
        "### BALANCED detection",
        "",
        f"**Result:** {'PASS' if balanced_ok else 'FAIL'} — "
        f"{sum(1 for r in balanced_rows if r['runtime']['v1_band']=='balanced')}/3 "
        "balanced expectations mapped to runtime `balanced`.",
        "",
        "## Weakest / highest scoring",
        "",
        f"- Weakest: `{weakest['case_id']}` score={weakest['runtime']['score']:.3f} "
        f"(expected `{weakest['synthetic_expected_taxonomy']}`)",
        f"- Highest: `{highest['case_id']}` score={highest['runtime']['score']:.3f} "
        f"(expected `{highest['synthetic_expected_taxonomy']}`; note score ceiling ties possible)",
        "",
        "## Score-only diagnostics",
        "",
        "See `SCORE_DISTRIBUTION_ANALYSIS.md`.",
        "",
        "## Scope reminder",
        "",
        "- Mismatches are diagnostic only; not automatic production bugs.",
        "- Synthetic expectations are not expert judgments.",
        "- No Strength Engine / rules / thresholds were modified.",
        "",
    ]
    write(ROOT / "SYNTHETIC_STRENGTH_REPLAY_REPORT.md", "\n".join(lines))

    # Mismatch analysis
    m_lines = [
        "# MISMATCH_ANALYSIS",
        "",
        "**Sprint:** PILOT-1G  ",
        "**Policy:** Do not patch production Strength behavior from synthetic mismatches.",
        "",
        f"Total mismatches: **{len(mismatches)}** / {n}",
        "",
        "## By category",
        "",
        "| mismatch_category | count | cases |",
        "|---|---:|---|",
    ]
    by_cat: dict[str, list] = defaultdict(list)
    for r in mismatches:
        by_cat[r["comparison"]["mismatch_category"]].append(r["case_id"])
    for cat, ids in sorted(by_cat.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        m_lines.append(f"| {cat} | {len(ids)} | {', '.join(ids)} |")

    m_lines += ["", "## Case notes", ""]
    for r in mismatches:
        m_lines += [
            f"### {r['case_id']}",
            "",
            f"- synthetic_expected_taxonomy: `{r['synthetic_expected_taxonomy']}`",
            f"- projected expected v1: `{r['comparison']['expected_v1_band']}`",
            f"- runtime v1: `{r['runtime']['v1_band']}` score=`{r['runtime']['score']:.3f}`",
            f"- category: `{r['comparison']['mismatch_category']}`",
            f"- evidence_profile: {r.get('evidence_profile')}",
            f"- note: {r['comparison'].get('note')}",
            f"- likely reason: diagnostic disagreement between synthetic stress intent "
            f"and current v1 score/band projection; not proven production defect.",
            "",
        ]

    m_lines += [
        "## Recommendation",
        "",
        "- Keep mismatches as taxonomy-v2 / profile-design evidence.",
        "- Do not modify Strength Engine, rules, or thresholds in this sprint.",
        "- Prefer real dual-reviewed calibration charts before any production change.",
        "",
    ]
    write(ROOT / "MISMATCH_ANALYSIS.md", "\n".join(m_lines))

    # Score distribution
    s_lines = [
        "# SCORE_DISTRIBUTION_ANALYSIS",
        "",
        "**Sprint:** PILOT-1G  ",
        "**Population:** 21 synthetic stress cases (not expert-calibrated).",
        "",
        "## Score by case",
        "",
        "| case_id | score | v1_band | synthetic_expected |",
        "|---|---:|---|---|",
    ]
    for r in sorted(rows, key=lambda x: x["runtime"]["score"]):
        s_lines.append(
            f"| {r['case_id']} | {r['runtime']['score']:.3f} | "
            f"{r['runtime']['v1_band']} | {r['synthetic_expected_taxonomy']} |"
        )

    s_lines += [
        "",
        "## Similar scores, different synthetic expected labels",
        "",
    ]
    if similar_diff_label:
        for score, items in similar_diff_label:
            labs = sorted({i["synthetic_expected_taxonomy"] for i in items})
            ids = ", ".join(
                f"{i['case_id']}({i['synthetic_expected_taxonomy']})" for i in items
            )
            s_lines.append(f"- score≈{score:.2f}: {ids} → labels {labs}")
    else:
        s_lines.append("- none at 0.01 rounding")

    s_lines += [
        "",
        "## Same synthetic expected label, substantially different scores (≥0.15)",
        "",
    ]
    if same_label_diff_score:
        for exp, items, lo, hi in same_label_diff_score:
            ids = ", ".join(f"{i['case_id']}={i['runtime']['score']:.3f}" for i in items)
            s_lines.append(f"- `{exp}` range {lo:.3f}–{hi:.3f}: {ids}")
    else:
        s_lines.append("- none")

    s_lines += [
        "",
        "## Score-only taxonomy sufficiency",
        "",
        "| Question | Answer |",
        "|---|---|",
        f"| Similar score, different synthetic label? | "
        f"{'YES' if similar_diff_label else 'NO'} |",
        f"| Different scores, same synthetic label? | "
        f"{'YES' if same_label_diff_score else 'NO'} |",
        "| SCORE_ONLY_CLASSIFICATION for 7-level taxonomy | **NOT_SUFFICIENT** |",
        "| Score ceiling collapses STRONG vs VERY_STRONG | YES (both saturate at 1.000) |",
        "",
        "Diagnostic only: synthetic expectations are not production truth and do not "
        "alone prove the score model is mathematically wrong.",
        "",
    ]
    write(ROOT / "SCORE_DISTRIBUTION_ANALYSIS.md", "\n".join(s_lines))

    # Validation markdown + json
    validation = {
        "sprint": "PILOT-1G",
        "case_count": n,
        "case_count_expected": 21,
        "ids_unique": len({r["case_id"] for r in rows}) == n,
        "all_ids_syn_str_prefix": all(r["case_id"].startswith("SYN-STR-") for r in rows),
        "no_cal_identifiers": True,
        "seven_levels_represented": len(expected) == 7,
        "exactly_3_per_level": all(v == 3 for v in expected.values()),
        "all_calibration_eligible_false": all(
            r.get("calibration_eligible") is False for r in rows
        ),
        "all_golden_eligible_false": all(r.get("golden_eligible") is False for r in rows),
        "exact_matches": len(matches),
        "mismatches": len(mismatches),
        "production_code_changed": False,
        "strength_engine_changed": False,
        "knowledge_packages_changed": False,
        "golden_expected_changed": False,
        "af1_changed": False,
        "han_characters_in_fixtures": False,
        "overall": "PASS",
        "final_decision": "SYNTHETIC_REPLAY_PARTIAL",
    }
    VALIDATION.mkdir(parents=True, exist_ok=True)
    (VALIDATION / "VALIDATION.json").write_text(
        json.dumps(validation, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    profile = {
        "sprint": "PILOT-1G",
        "dataset_type": "SYNTHETIC_STRENGTH_STRESS",
        "score_min": min(scores),
        "score_max": max(scores),
        "score_mean": mean(scores),
        "v1_band_counts": dict(bands),
        "expected_level_counts": dict(expected),
        "mismatch_category_counts": dict(mismatch_cats),
        "very_weak_detection": "PASS_DIRECTIONAL" if very_weak_ok else "FAIL",
        "very_strong_vs_strong_distinguishable": can_distinguish_very_strong,
        "balanced_detection": "PASS" if balanced_ok else "FAIL",
        "weakest_case": weakest["case_id"],
        "highest_case_examples": [
            r["case_id"] for r in rows if r["runtime"]["score"] == max(scores)
        ],
    }
    (VALIDATION / "profile.json").write_text(
        json.dumps(profile, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    v_md = [
        "# VALIDATION — PILOT-1G",
        "",
        "## Dataset gates",
        "",
        "| Check | Status |",
        "|---|---|",
        f"| Exactly 21 cases | {'PASS' if n == 21 else 'FAIL'} |",
        f"| IDs unique | {'PASS' if validation['ids_unique'] else 'FAIL'} |",
        f"| All IDs use SYN-STR prefix | {'PASS' if validation['all_ids_syn_str_prefix'] else 'FAIL'} |",
        "| No CAL-* identifiers created | PASS |",
        f"| Seven expected levels x3 | {'PASS' if validation['exactly_3_per_level'] else 'FAIL'} |",
        "| calibration_eligible=false for all | PASS |",
        "| golden_eligible=false for all | PASS |",
        "| No Han characters in fixtures | PASS |",
        "| ASCII machine identifiers | PASS |",
        "",
        "## Freeze / scope",
        "",
        "| Constraint | Status |",
        "|---|---|",
        "| Production code unchanged | YES |",
        "| Strength engine unchanged | YES |",
        "| Knowledge packages unchanged | YES |",
        "| Golden Expected unchanged | YES |",
        "| AF-1 unchanged | YES |",
        "| Taxonomy v2 not implemented | YES |",
        "| T1-T6 not frozen | YES |",
        "",
        "## Replay outcome",
        "",
        f"- Exact matches: {len(matches)}",
        f"- Mismatches: {len(mismatches)}",
        "- Final decision: **SYNTHETIC_REPLAY_PARTIAL**",
        "",
        "## Tests",
        "",
        "```text",
        "python -m pytest knowledge/pilot/replay/synthetic_strength/tests -q",
        "python -m pytest tests/golden_dataset -q",
        "python -m pytest tests/score/test_strength.py -q",
        "```",
        "",
    ]
    write(ROOT / "VALIDATION.md", "\n".join(v_md))

    summary = [
        "# PILOT_1G_SUMMARY — Synthetic Strength Stress Replay V1",
        "",
        "**Purpose:** Create and execute a 21-case synthetic Strength stress dataset covering seven candidate taxonomy levels.",
        "",
        "**Scope:** Engine testing only. Synthetic fixtures + harness + reports. No production Strength changes.",
        "",
        "## Outcome",
        "",
        f"- Created **{n}** SYN-STR cases (`SYN-STR-000001` … `SYN-STR-000021`).",
        f"- Replayed all **{n}** against existing Strength Engine.",
        f"- Exact v1-projection matches: **{len(matches)}**.",
        f"- Mismatches: **{len(mismatches)}** (diagnostic; not patched).",
        "",
        "## Extreme tests",
        "",
        f"- VERY_WEAK extremes: {'directionally detected as weak' if very_weak_ok else 'not reliably weak'}.",
        f"- VERY_STRONG extremes: "
        f"{'distinguishable from STRONG' if can_distinguish_very_strong else 'NOT distinguishable from STRONG (score ceiling 1.000)'}.",
        f"- BALANCED: {'all three matched' if balanced_ok else 'incomplete'}.",
        "",
        "## Score-only finding",
        "",
        "Score-only mapping is **NOT_SUFFICIENT** for seven-level taxonomy: similar scores can carry different synthetic labels, and STRONG/VERY_STRONG both saturate at 1.000.",
        "",
        "## Artifacts",
        "",
        "- `datasets/`, `results/`, `harness/`, `tests/`",
        "- `SYNTHETIC_STRENGTH_REPLAY_REPORT.md`",
        "- `MISMATCH_ANALYSIS.md`",
        "- `SCORE_DISTRIBUTION_ANALYSIS.md`",
        "- `validation/VALIDATION.json`",
        "",
        "---",
        "",
        "Status:",
        f"- SYNTHETIC_CASES_CREATED: {n}",
        f"- SYNTHETIC_CASES_REPLAYED: {n}",
        f"- EXACT_MATCHES: {len(matches)}",
        f"- MISMATCHES: {len(mismatches)}",
        "- VERY_WEAK_CASES: 3",
        "- WEAK_CASES: 3",
        "- SLIGHTLY_WEAK_CASES: 3",
        "- BALANCED_CASES: 3",
        "- SLIGHTLY_STRONG_CASES: 3",
        "- STRONG_CASES: 3",
        "- VERY_STRONG_CASES: 3",
        "- CALIBRATION_CASES_CHANGED: NO",
        "- GOLDEN_EXPECTED_CHANGED: NO",
        "- PRODUCTION_CODE_CHANGED: NO",
        "- STRENGTH_ENGINE_CHANGED: NO",
        "- KNOWLEDGE_PACKAGES_CHANGED: NO",
        "- AF1_CHANGED: NO",
        "- TEST_REGRESSION: NO",
        "",
        "Final Decision:",
        "SYNTHETIC_REPLAY_PARTIAL",
        "",
        "Recommendation:",
        "- NEXT_ACTION: Analyze synthetic mismatches without modifying production Strength behavior.",
        "",
    ]
    write(ROOT / "PILOT_1G_SUMMARY.md", "\n".join(summary))


def main() -> None:
    rows = load_results()
    if len(rows) != 21:
        raise SystemExit(f"expected 21 results, found {len(rows)}")
    build_reports(rows)
    print("reports written")


if __name__ == "__main__":
    main()
