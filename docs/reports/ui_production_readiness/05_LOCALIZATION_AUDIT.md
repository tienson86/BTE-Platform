# 05 — Localization Audit

| Field | Value |
|-------|--------|
| **Sprint** | UI Sprint 07 |
| **Date** | 2026-08-02 |
| **Default locale** | `vi` |

---

## Scan method

- Preview full Result HTML assert: no raw `report.*` keys.
- Catalog review of `report.kw_*` English chrome → Vietnamese.
- Copy-path hard-code `"priority "` → `report.kw_rule_priority`.
- Duplicate `ch_references` key removed (`Tham chiếu`).

---

## Findings → fixes

| Finding | Fix |
|---------|-----|
| Knowledge section titles in English | VI in `vi.json` |
| `Sao chép citation/rule` EN fragments | Vietnamese |
| Hard-coded `priority` in copy buffer | i18n |
| Empty strengths/weaknesses showed `--` | `report.unavailable` |
| `ch_references: Reference` | `Tham chiếu` |

---

## Remaining (domain data, not chrome)

Stem/branch → element maps in `report_model.js` are classical domain constants (Giáp/Mộc…), not product chrome — allowed.

---

## Verdict

**No raw i18n keys in Result preview.** Product chrome localized for VI Beta.
