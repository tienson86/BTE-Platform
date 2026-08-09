# Evidence Coverage Report

## Completeness

| Package | Rules | Evidence bundles | 1:1 | Required fields* |
| --- | --- | --- | --- | --- |
| bz_01 … bz_08 | 879 | 879 | Yes | Present |
| bz_09_luck_foundation | 0 | 0 | N/A | N/A (reference package) |
| bz_10 | 250 | 250 | Yes | Present |
| bz_11 | 280 | 280 | Yes | Present |
| bz_12 | 300 | 300 | Yes | Present |
| bz_13 | 400 | 400 | Yes | Present |
| bz_14 | 360 | 360 | Yes | Present |
| bz_15 | 380 | 380 | Yes | Present |
| **Total** | **2 849** | **2 849** | **Yes** | |

\*Checked: `explanation`, `rationale`, positive example, negative example, boundary case (list or singular keys).

## Confidence distribution

Across bundles that declare `confidence_level`:

| Level | Count | Notes |
| --- | --- | --- |
| canonical | 2 849 (analytical/decision packages sampled as canonical on Wave 1 KX packages) | Uniform Gold declaration |
| high / medium / low mix | Not used as bundle-level enum on KX-5/6 packages | Propagation lives in `reasoning/confidence/` |

Wave 1 evidence confidence is **declared canonical**, not empirically graded. Diversity of confidence is a Wave 2 / Golden Dataset item.

## Reference completeness

Every production rule on bz_10–bz_15 points at in-package `REF-*` targets. Foundation packages (bz_01–bz_08) use their own reference catalogs. No broken `REF` targets were required for KX-6D freeze (packages not modified). Luck has no rule-level references.

## Boundary coverage

| Package family | Boundary cases |
| --- | --- |
| bz_01–bz_08 | Present per bundle (package evidence framework) |
| bz_10–bz_15 | Explicit `boundary_cases` / `upstream_boundary` on every rule |
| bz_09 | None |

## Gaps

- No evidence for luck foundation (0 rules).
- Confidence not stratified (all canonical) — weak signal for RM risk heatmaps.
- Golden Dataset still `not_applicable` on every PVP-RELEASE report.
