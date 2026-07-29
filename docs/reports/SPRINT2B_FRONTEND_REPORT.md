# Sprint 2B Frontend Report

| Item | Value |
|------|-------|
| Document | `SPRINT2B_FRONTEND_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 2B — Frontend Score Binding |
| Scope | Customer Portal Result page (Đánh Giá + related presenters) |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |
| Constraints | **No backend / scoring / RuleContext / Knowledge changes** |

---

## Executive Summary

Score cards on the Result **Đánh Giá** tab now bind to canonical API fields. Hidden dimensions (`useful_god_score`, `shensha_score`, `luck_score`, scalar `wuxing_score`, `ten_god_score`) are restored. Incorrect aliases (`overall_score`, bare `pattern`, `score`, …) were removed from the score presenter. Element-count series are shown only as **Phân bố** extras — never as `wuxing_score`.

Backend JSON for the critical case remains:

| Field | JSON value | Card shown |
|-------|------------|------------|
| `total_score` | 55.25 | 55.25 |
| `strength_score` | 45 | 45 |
| `pattern_score` | 100 | 100 |
| `wuxing_score` | 0 | **0** (numeric score, not counts) |
| `ten_god_score` | 100 | 100 |
| `useful_god_score` | 20 | **20** (was hidden) |
| `shensha_score` | 100 | **100** (was hidden) |
| `luck_score` | 0 | **0** (was hidden) |
| `confidence` | medium | badge (API has no `confidence_score`) |

Zero cards for `wuxing_score` / `luck_score` are correct because JSON is 0 — not binding loss.

---

## Files modified

| File | Change |
|------|--------|
| `applications/customer_portal/static/js/presenters/score.js` | Canonical SUMMARY cards; restore all 8 scores; confidence from `confidence` / `confidence_score`; series → balance panels only |
| `applications/customer_portal/static/i18n/vi.json` | Labels for new score cards + balance panel titles; updated subtitle |
| `applications/customer_portal/static/js/presenters/summary_builder.js` | Executive highlight uses `total_score` only; wuxing/ten_god bars prefer numeric `*_score` |
| `applications/customer_portal/tests/js/score_binding_verify.js` | Node verifier for Sprint 2B bindings (new) |

**Not modified:** Pattern (Cách Cục), Interpretation (Luận Giải) score-field bindings — they do not render `data.score` dimension cards. Backend untouched.

---

## Bindings fixed

| Field | Before | After |
|-------|--------|-------|
| `total_score` | Shown via aliases including `overall_score` | Canonical `total_score` only |
| `strength_score` | Shown (+ aliases) | Canonical only + gauge |
| `pattern_score` | Shown (+ risky `pattern` alias) | Canonical only |
| `wuxing_score` | Hidden behind `wuxing_series` counts | Summary card from **numeric** `wuxing_score` |
| `ten_god_score` | Only as series / fallback | Summary card from numeric score |
| `useful_god_score` | Not rendered | Summary card |
| `shensha_score` | Not rendered | Summary card |
| `luck_score` | Not rendered | Summary card |
| `confidence` / `confidence_score` | `confidence` badge; ignored `confidence_score` | Badge reads `confidence` then `confidence_score` |
| Removed aliases | `overall_score`, `overall`, `final_score`, `score`, `than_score`, `body_score`, `strength`, `cach_cuc_score`, `pattern`, `interpretation_score`, … | Removed from Đánh Giá SUMMARY |

---

## Verification

### Automated presenter check

```text
node applications/customer_portal/tests/js/score_binding_verify.js
→ 10 PASS (case JSON fixture)
```

Evidence HTML: `docs/reports/_s2b_score_render.html`

### Portal tests

```text
pytest applications/customer_portal/tests -q
→ 18 passed
```

### Runtime

| Check | Result |
|-------|--------|
| `GET http://127.0.0.1:8081/result` | **200** |
| Served `/static/js/presenters/score.js` | Sprint 2B header present |
| Orchestrator case scores | 55.25 / 45 / 100 / 0 / 100 / 20 / 100 / 0 / confidence=medium |

---

## Screenshots

Browser screenshots were not captured in this environment (no headed UI automation). Render evidence for the critical-case score payload:

**Artifact:** [`docs/reports/_s2b_score_render.html`](../reports/_s2b_score_render.html)

Rendered card values (from that HTML):

- Điểm tổng → **55.25**
- Điểm Thân → **45**
- Điểm Cách cục → **100**
- Điểm Ngũ hành → **0** (score)
- Điểm Thập thần → **100**
- Điểm Dụng thần → **20**
- Điểm Thần sát → **100**
- Điểm Đại vận → **0**
- Độ tin cậy → **medium**
- Phân bố Ngũ hành → counts 4 / 5… (separate from score)

Open the artifact in a browser for a visual of the Đánh Giá layout.

---

## Remaining UI issues

| Severity | Issue |
|----------|-------|
| Low | New `bte-tone-*` classes (wuxing/tengod/shensha/luck) may share default card styling if CSS lacks specific rules |
| Low | API field is `confidence` (string), not `confidence_score` — badge supports both; no numeric confidence_score from backend |
| Low | `wuxing_score=0` / `luck_score=0` remain legitimate zeros (upstream/calculator) — UI now shows them correctly |
| Medium (out of Sprint 2B FE scope) | Luận Giải still lacks dedicated Ngũ hành / Thập thần / Tài vận / Đại vận narrative sections (Sprint 2A PARTIAL) |
| Info | Cách Cục tab unchanged — still pattern fields, not score dimensions |

---

## Conclusion

Sprint 2B frontend score binding for **Đánh Giá** is complete for the verified API contract. Non-zero JSON values (`20`, `100`, `55.25`, …) are no longer dropped by the presenter. Zero values display as `0` when JSON is `0`.

---

END
