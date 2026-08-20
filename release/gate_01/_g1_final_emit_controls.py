"""Emit G1_FINAL_CONTROL_CASES.md from frozen PREFINAL JSON. No analysis."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "G1_PREFINAL_CONTROL_CASES.json"
OUT = ROOT / "G1_FINAL_CONTROL_CASES.md"


def main() -> None:
    rows = json.loads(SRC.read_text(encoding="utf-8"))
    if len(rows) != 10:
        raise SystemExit(f"expected 10 control cases, got {len(rows)}")

    lines = [
        "# G1-FINAL — Control cases (locked from Frozen Truth)",
        "",
        "**Source:** `release/gate_01/G1_PREFINAL_CONTROL_CASES.json` (G1-PREFINAL production recompute).",
        "**Generated:** this file is emitted from that JSON. Values are not hand-edited.",
        "**Contract:** `analysis_result.UsefulGodView@1.5`",
        "",
        "Customer Hỷ = `favorable_display`. Pattern override authority = `ug_override_eligible`.",
        "LEVEL-1 detection (`detected_special_pattern`) is listed in Pattern and does not grant override.",
        "",
        "| Case | Four Pillars | Strength | Pattern | Pattern override authority | Điều hậu | Overall Dụng | Reason archetype | Customer Hỷ | Kỵ | Luck |",
        "|------|--------------|----------|---------|----------------------------|----------|--------------|------------------|-------------|-----|------|",
    ]
    for row in rows:
        spec = row.get("detected_special_pattern")
        q = row.get("qualification_level")
        pattern = str(row["pattern"])
        if spec:
            pattern = f"{pattern} [LEVEL-{q} token `{spec}`]"
        ov = "true" if row["ug_override_eligible"] else "false"
        strength = f"{float(row['strength_score']):.2f} {row['strength_level']}"
        luck = str(row["current_luck"]).replace(" ages ", " · ages ")
        cells = [
            row["case"],
            row["four_pillars"],
            strength,
            pattern,
            ov,
            row["dieu_hau"],
            row["overall_dung"],
            row["reason_archetype"],
            row["customer_hy"],
            row["ky"],
            luck,
        ]
        lines.append("| " + " | ".join(str(c) for c in cells) + " |")

    lines.extend(
        [
            "",
            "## Provenance",
            "",
            "| Item | Value |",
            "|------|-------|",
            "| Machine source | `release/gate_01/G1_PREFINAL_CONTROL_CASES.json` |",
            "| 101 dump | `release/gate_01/G1_PREFINAL_101_TRUTH.json` |",
            "| 101 SHA256 | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` |",
            "| Oracle | G1-PREFINAL live production; not old reference sheets |",
            "",
        ]
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
