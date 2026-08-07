# FOUNDATION_COMPLIANCE_CHECKLIST.md

Version: 1.0  
Date: 2026-08-07  
Status: OFFICIAL  
Owner: BTE UI Architecture  
Use: PR review · Screen release · Epic acceptance

---

## How to use

Mark each item **PASS** / **FAIL** / **N/A**.

Any **FAIL** on a mandatory item blocks merge for UI work.

Foundation documents themselves must not be edited to make a checklist pass.

---

## 0. Meta

| Item | Status |
|------|--------|
| Change description recorded | □ |
| Foundation docs read before coding | □ |
| Result Page freeze respected (if touched) | □ |

---

## 1. Architecture

| Item | Status |
|------|--------|
| Dependency direction preserved (Screen → … → Tokens) | □ |
| No reverse Engine imports from UI | □ |
| Public API / wrappers respected | □ |
| Zone → Row → Grid → Card (analysis surfaces) | □ |
| No new unofficial layout architecture | □ |

---

## 2. Experience (Experience Principles)

| Item | Status |
|------|--------|
| Supports trust → understanding → action | □ |
| Explainable, not opaque prediction theatre | □ |
| Reading journey clear | □ |
| Cognitive load acceptable (preview/expand where needed) | □ |
| Empty / loading / error states usable | □ |

---

## 3. Brand (Brand Language)

| Item | Status |
|------|--------|
| Feels like professional consultant, not calculator | □ |
| Tone calm, precise, trustworthy | □ |
| No playful / consumer marketing chrome | □ |
| Vocabulary consistent with Brand Language | □ |
| Avoids “widget collage” appearance | □ |

---

## 4. Visual (Visual Language)

| Item | Status |
|------|--------|
| Visual hierarchy: primary → secondary → tertiary | □ |
| Borders used sparingly (whitespace first) | □ |
| Typography scale respected | □ |
| Color used for meaning, not decoration | □ |
| Elevation subtle; no deep shadows | □ |
| One primary CTA per major screen | □ |
| Matches Visual Reference Gallery intent | □ |

---

## 5. Design System

| Item | Status |
|------|--------|
| PACK_01 principles | □ |
| PACK_02 layout / spacing / breakpoints | □ |
| PACK_03 components reused where possible | □ |
| PACK_04 presentation (ViewModels, clamp, heights) | □ |
| PACK_05 accessibility | □ |
| PACK_06 / PACK_07 if Result Page | □ |
| Layout Gallery patterns preserved | □ |

---

## 6. Accessibility

| Item | Status |
|------|--------|
| Keyboard operable | □ |
| Visible focus | □ |
| ARIA / labels present | □ |
| Semantic structure | □ |
| Contrast sufficient | □ |
| Reduced motion respected | □ |

---

## 7. Performance

| Item | Status |
|------|--------|
| No unnecessary re-renders introduced | □ |
| No duplicate heavy assets | □ |
| Dead code not added | □ |
| Module tests pass (when required) | □ |
| TypeScript / build pass | □ |

---

## 8. Documentation

| Item | Status |
|------|--------|
| Depends-on / references point to Foundation chain | □ |
| No conflicting SSOT introduced | □ |
| Changelog / report updated when required by epic | □ |
| Screenshots for visual changes attached | □ |

---

## 9. Strict Prohibitions

| Item | Status |
|------|--------|
| Did **not** edit frozen Foundation documents | □ |
| Did **not** invent spacing / type / color systems | □ |
| Did **not** move Result Page zones/cards | □ |
| Did **not** mix Engine models into UI | □ |

---

## Sign-off

| Role | Name | Date | Decision |
|------|------|------|----------|
| Author | | | □ Ready |
| Reviewer | | | □ Approved / □ Rejected |
| Product (if release) | | | □ Approved / □ Deferred |

---

END
