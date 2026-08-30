# 12_VISUAL_VALIDATION.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- FOUNDATION_COMPLIANCE_CHECKLIST.md
- All Visual System V2 documents in this folder

Use before any later CSS migration (not this sprint).

---

# 1. Purpose

This is the Visual System V2 gate.

FAIL on a mandatory item blocks visual implementation.

Do not edit Foundation or this system to make a check pass.

---

# 2. Specification gate (UI-13)

| Item | Status |
|------|--------|
| Design standards live in `knowledge/ui_system/` | PASS |
| No CSS migration | PASS |
| No Dashboard redesign | PASS |
| No Card redesign | PASS |
| No PDF redesign | PASS |
| No Narrative change | PASS |
| No Runtime change | PASS |
| No Portal routing change | PASS |
| Tokens specified from Foundation / Design System, not invented | PASS |

---

# 3. Future implementation gate (not UI-13)

Mark PASS / FAIL / N/A when CSS work starts.

## Identity

| Item | |
|------|--|
| Feels commercial, not admin / spreadsheet / consumer widget | □ |
| Consultant, not calculator | □ |
| Premium, professional, readable, trustworthy, calm | □ |

## Tokens

| Item | |
|------|--|
| Spacing from PACK_02 scale only | □ |
| Type roles: Hero, Section, Card Title, Body, Caption, Label, Metric | □ |
| Color roles: Primary, Secondary, Accent, Surface, Background, Success, Warning, Critical, Neutral | □ |
| Radius 6 / 10 / 14 / 9999 | □ |
| Elevation subtle | □ |
| Motion 120 / 200 / 320ms; reduced motion 0 | □ |

## Structure

| Item | |
|------|--|
| Grid 12 / 8 / 4 | □ |
| Card types: Hero, Analysis, Reference, Summary, Status | □ |
| One purpose per card | □ |
| Equal height in a row | □ |
| Icons unified; badges unified; charts unified | □ |
| Empty / loading / error present | □ |
| Contrast, 44px targets, visible focus | □ |

## Forbidden

| Item | |
|------|--|
| No raw hex / px outside tokens | □ |
| No new Builder / Runtime / Narrative | □ |
| No Result architecture redesign | □ |

---

# 4. Verdict rule

Visual System V2 specification is complete when UI-13 files exist and out-of-scope work did not start.

Visual System V2 implementation is complete only after a later sprint passes section 3.

---

END
