# P-004 LIFE CONSULTING ENGINE REPORT

Status: **COMPLETE**

Date: 2026-09-04  
Case: CASE-0001  
Surface: Life Consulting section (`data-life-consulting`) above the frozen dashboard grid

---

## Status

The Result Page now answers life-domain questions before the customer reads astrology components.

Runtime, Narrative Engine, Presentation contract (`bte.presentation.v2.1`), and astrology calculations were not modified.

Only consulting assets, a published-token binder, and a section outside `DASHBOARD_CARDS` changed.

---

## Architecture

```
Published canonical data
        ↓
collectLifeConsultingEvidence (copy tokens only)
        ↓
LIFE_DOMAIN_PROFILES lookup (first match per domain)
        ↓
adaptLifeConsulting
        ↓
LifeConsultingSection  (not a data-card)
```

Placement: Identity Header → Life Consulting → frozen 9-card grid.

The section is **not** a tenth `DASHBOARD_CARDS` entry. Spans stay `[4, 8, 4, 4, 4, 6, 6, 12, 12]`.

Lookup keys (Ten Gods names, pattern labels, strength class, Useful God display, ShenSha names, climate, current luck) stay internal. Customer copy never lists those systems.

A domain is omitted when published evidence does not match an authored profile. Nothing is invented.

---

## Domains

Order: Marriage → Children → Health → Career → Finance → Property.

Each domain answers:

Current tendency → Strength → Risk → Opportunity → Recommendation

Rendered layout:

Domain → Executive Insight → Xu hướng hiện tại → Điểm mạnh → Cơ hội → Rủi ro → Hướng đi

Strength is shown because the consulting model requires it. Opportunity sits before Risk because that is the ticket layout.

| Domain | Published evidence used for lookup | CASE-0001 profile |
|--------|------------------------------------|-------------------|
| Hôn nhân | Gender + spouse-star tokens (Tài for male; Quan/Sát for female); ShenSha if published | `marriage_male_side_wealth` |
| Con cái | Useful God / output tokens (Thực Thần, Thương Quan) | `children_output` |
| Sức khỏe | Pattern + Strength; Temperature / Five Elements when published | `health_hold_load` |
| Sự nghiệp | Ten Gods + Pattern + Useful God | `career_pressure_skill` |
| Tài chính | Ten Gods + Useful God + Pattern | `finance_short_side` |
| Nhà đất | Pattern + Strength + current Luck when published | `property_foundation_current` |

Children is not given a dedicated evidence list in the ticket. Binding uses published Useful God / output stars only.

---

## CASE-0001

Published tokens used (no person hardcode in assets):

- Gender: male
- Visible: Thất Sát, Kiếp Tài, Thiên Ấn (Nhật Chủ ignored)
- Hidden: Thiên Tài, Chính Ấn
- Pattern: Chính Ấn
- Strength: Thân vượng
- Useful display: Thủy · Nhâm · Thực Thần
- Current luck: published cycle present in the P-004 fixture

Rendered domains: all six.

Customer text does not contain Thập Thần, Thần Sát, or the lookup god/pattern names.

---

## Screenshots

Preview: `docs/reports/p004_life_consulting/preview.html`

- `docs/reports/p004_life_consulting/screenshots/case0001_before.png`
- `docs/reports/p004_life_consulting/screenshots/case0001_after.png`
- `docs/reports/p004_life_consulting/screenshots/case0001_after_mobile.png`
- `docs/reports/p004_life_consulting/screenshots/case0001_before_after.png`

Desktop after: 2-column domain grid. Mobile after: stacked single column.

Live `/result` was not driven in a running app browser. Verification is tests + Playwright preview screenshots.

---

## Tests

`npx vitest run tests/js/p004_life_consulting.test.tsx`

- Test Files 1 passed
- Tests 5 passed

Coverage:

- CASE-0001 binds six domains and renders the consulting field order
- Section is not `data-card`; frozen spans unchanged
- Domain omitted when evidence is missing
- Female partnership lookup without listing officer/pressure stars
- Authored copy has no astrology labels and no cửa/khung/lối/món
- Adapter/assets do not import engines, do not hardcode CASE-0001, do not touch Presentation

Related frozen-grid checks run for safety: UI-18 pass, UI-20 pass, UI-07 T15 spans pass.

---

## Known gaps

1. Catalog is a first layer. Many published combinations still omit a domain rather than guess.
2. CASE-0001 typical payloads often lack ShenSha, Five Elements, and Temperature. Those profiles exist but did not bind on this case.
3. Children evidence was inferred from published Useful God / output stars; the ticket did not list a Children evidence set.
4. CK-01 `commercial_composer` / `data.commercial_consulting` is unchanged. P-004 is a customer-portal consulting layer, not that engine.
5. UI-07 T20 (`resultSource` empty vs current) remains a pre-existing `resolveResultBoot` issue. Not in P-004 scope.

---

## Verdict

**PASS**

Customers can read six life domains in consulting language, bound only from published canonical data, without a new astrology calculation and without changing the frozen card grid.

STOP.
