# 17 — LOCALIZATION CONTRACT (Addendum L)

| Field | Value |
|-------|--------|
| **Document** | `17_LOCALIZATION_CONTRACT.md` |
| **Addendum** | **L** |
| **Version** | `1.1.0` |
| **Status** | **Normative — Blueprint V1.1 Final** |

---

## Purpose

Freeze how UI strings, locale, and classical terms are handled so implementers do not hard-code copy or invent translations mid-sprint.

---

## 1. Locale policy

| Rule | Normative |
|------|-----------|
| Default consumer locale | `vi` (Vietnamese) |
| String source | Portal i18n catalog (e.g. `static/i18n/vi.json`) — presentation layer |
| No inline English product chrome | Except proper nouns (BTE) and code/request ids |
| Architecture docs language | May remain EN+VI mixed; **UI copy** follows i18n keys |

---

## 2. Key ownership by region

| UI region | Key prefix (normative) |
|-----------|------------------------|
| App nav / common | `nav.*`, `common.*` |
| Result chrome | `result.*` |
| Report tiers / hero / charts / analysis | `report.*` |
| Executive legacy labels | `executive.*` (may alias into report) |
| Bazi field labels | `bazi.*` |
| Interpretation confidence | `interpretation.*` |
| Discussion / expert | `discussion.*` |
| Analyze form | `analyze.*` |
| Dashboard | `dashboard.*` |
| Empty/unavailable | `report.unavailable`, `result.empty`, etc. |

**New keys required for V1.1 (must exist before Sprint 02 UI ships):**

| Key | Purpose |
|-----|---------|
| `report.quality_verdict.high` | Calm high-band caption |
| `report.quality_verdict.mid` | Calm mid-band caption |
| `report.quality_verdict.low` | Calm attention-band caption |
| `report.quality_verdict.confidence_only` | When only confidence exists |
| `report.first_recommendation` | Callout title |
| `report.toc` | Interpretation mục lục |
| `report.callout_insight` | Optional insight callout label |
| `report.callout_caution` | Optional caution callout label |

Exact Vietnamese wording is editorial; keys are frozen.

---

## 3. Quality band thresholds (display only)

| Score | Band key |
|-------|----------|
| ≥ 70 | `report.quality_verdict.high` |
| 40–69 | `report.quality_verdict.mid` |
| < 40 | `report.quality_verdict.low` |

If PO supplies an alternate table later, **only thresholds/copy change** — not IA.

---

## 4. Classical / domain terms

| Term | UI display | Notes |
|------|------------|-------|
| Nhật Chủ | i18n + value | — |
| Dụng / Hỷ / Kỵ | Prefer VI labels from `executive.*` / `report.*` | |
| Pattern codes (`chinh_an`) | Human label via existing formatters | Never raw code alone if label exists |
| Rule ids | Hidden on consumer | See Knowledge addendum |

---

## 5. Interpolation

Use `{var}` placeholders only (existing BteI18n style).  
Do not concatenate sentences in code across locales.

---

## 6. Forbidden localization practices

- Hard-coded VI strings in new components when a key exists or is listed above  
- Machine-translating fear idioms  
- Showing English ban-class words (“disaster”) in UI  

Align with Interpretation Narrative / Terminology architecture docs.

---

## Version

`1.1.0`
