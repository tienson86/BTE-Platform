# G1-X01 — Cross-Engine Refreeze Checklist

Canonical production remains:

```text
StrengthEngine.calculate
    → PatternContext.strength_level / strength_score
    → Follow eligibility gate (weak-follow vs Tòng Vượng)
    → FollowPatternCalculator + 03_follow_pattern.csv
    → PatternEngine winner
    → follow token published only if winner is fol_*
    → build_useful_god_context canonicalizes token
    → UsefulGodEngine (spc_001 only when token is tong_tai)
```

Do not refreeze if Follow Pattern can still publish against `strength=strong`.

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Strength weights / thresholds / season / root / drain unchanged | PASS |
| 2 | Tuyền Strength remains **0.66 / strong / raw 16** | PASS |
| 3 | Follow evaluation consumes canonical Strength (`strength_level`) | PASS |
| 4 | Ten-god ratio cannot override Strength | PASS |
| 5 | Weak-follow (Tòng Tài / Quan / Sát / Nhi / Ấn) cannot publish when `strong` | PASS |
| 6 | `balanced` is not automatic follow | PASS |
| 7 | `weak` is eligible only; still needs detector + CSV conditions | PASS |
| 8 | Tòng Vượng is **not** blocked by the cực-nhược gate; requires `strong` | PASS |
| 9 | Tuyền `fol_ttai_01` rejected `follow_strength_incompatible` | PASS |
| 10 | Tuyền replacement is normal selection (`pat_ktai_01` Kiếp Tài), not hard-coded | PASS |
| 11 | Customer Pattern/Interpretation/Narrative/Report have no `cực nhược` for Tuyền | PASS |
| 12 | Machine token `tong_tai` / display `Tòng Tài` SSOT | PASS |
| 13 | Useful God does not compare Vietnamese labels to `spc_*` tokens | PASS |
| 14 | Legitimate Tòng Tài still reaches `spc_001` | PASS |
| 15 | Tuyền does **not** win `spc_001` after token repair | PASS |
| 16 | Follow token is not leaked when a non-follow rule wins (Dung `sat_an`) | PASS |
| 17 | G1-05 occurrence `Mộc3 · Hỏa1 · Thổ4 · Kim3 · Thủy6` unchanged | PASS |
| 18 | `flo_004` uses unique-max (G1-06), not key-exists; no repair | PASS |
| 19 | Tuyền Useful God winner remains `sea_002` Nhâm via season priority | PASS |
| 20 | Nhâm not forced to Mộc to match external reference | PASS |
| 21 | Sơn / Huỳnh / Dung / Hưng Strength unchanged | PASS |
| 22 | Pattern changed only where invalid follow previously won (Tuyền) | PASS |
| 23 | Cross-engine semantic contract tests added and passing | PASS |
| 24 | Golden / snapshot / expected output not edited | PASS |
| 25 | Live API restarted; fresh Analyze for Tuyền (no ResultStore reuse) | PASS |
| 26 | Result / Report / Narrative agree with repaired Pattern | PASS |

Portal rebuild: **not required** (presentation contracts unchanged).

---

G1-X01 STATUS: **CROSS-ENGINE CONSISTENCY: REPAIRED — REFREEZE READY**

Stop: do **not** start G1-FINAL.
