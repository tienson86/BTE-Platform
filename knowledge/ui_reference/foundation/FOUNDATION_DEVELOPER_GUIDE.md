# FOUNDATION_DEVELOPER_GUIDE.md

Version: 1.0  
Date: 2026-08-07  
Status: OFFICIAL  
Owner: BTE UI Architecture  
Audience: Developers, Cursor agents, reviewers

---

## 1. Purpose

This guide explains how to use **Foundation V1.0** when building or changing any BTE user interface.

Foundation V1.0 is frozen. Developers apply it; they do not rewrite it.

---

## 2. Official Dependency Chain

Every UI decision must respect this order. Higher layers win when conflict appears.

```
Product Manifesto
        ↓
Experience Principles
        ↓
Brand Language
        ↓
Visual Language
        ↓
Design System (PACK_01 → PACK_07)
        ↓
Implementation Guide
        ↓
Code
```

| Layer | Document | Answers |
|-------|----------|---------|
| Product | `knowledge/product/BTE_PRODUCT_MANIFESTO.md` | Why BTE exists; what must never be built |
| Experience | `knowledge/ui_reference/brand/BTE_EXPERIENCE_PRINCIPLES.md` | What users must feel and achieve |
| Brand | `knowledge/ui_reference/brand/BTE_BRAND_LANGUAGE.md` | Identity: consultant, not calculator |
| Visual | `knowledge/ui_reference/visual/*` | Appearance, hierarchy, transform rules |
| Design | `knowledge/ui_reference/design_system/PACK_*` | Structure, layout, components, a11y |
| How | `knowledge/ui_reference/design_system/UI_IMPLEMENTATION_GUIDE.md` | Implementation workflow |

---

## 3. Before Writing Any UI Code

1. Read the Product Manifesto (mission fit).
2. Confirm Experience Principles (trust → understanding → action).
3. Confirm Brand Language (tone, vocabulary, anti-patterns).
4. Confirm Visual Language (hierarchy, borders, typography).
5. Confirm Design System pack(s) for the surface (layout, components, presentation, a11y).
6. For Result analysis UI: also read PACK_06, PACK_07, Layout Gallery.
7. Only then implement.

Cursor agents must follow the same order (see `.cursor/rules/foundation_v1.mdc`).

---

## 4. How to Design a New Screen

```
Requirement
↓
Does it serve understanding & decisions? (Manifesto)
↓
Define reading journey (Experience)
↓
Choose Brand-appropriate language & density
↓
Apply Visual hierarchy (primary / secondary / tertiary)
↓
Compose with Design System Zones → Rows → Grid → Cards
↓
Wire ViewModels + Presentation Adapter only
↓
Accessibility + Responsive validation
↓
Foundation Compliance Checklist
```

### Rules

- Prefer extending the Result Page architecture over inventing a new analysis layout.
- Do not create marketing / widget dashboards for analytical content.
- One primary CTA per major screen.
- Preview → Expand → Detail for long text.

---

## 5. How to Implement a New Component

1. Check whether a PACK_03 / shared / base component already exists.
2. If new: define presentation-only props (ViewModel fields, not Engine models).
3. Use Design Tokens / Visual Language tokens — never invent spacing, type scale, or colors.
4. Prefer whitespace over borders; typography over decoration.
5. Export via barrel; no circular imports.
6. Add accessibility: labels, focus, contrast.
7. Add module tests only when requested / required by the work package.

### Forbidden

- Reading Engine models in UI components
- Hard-coded business rules
- Nested “card inside card inside card” chrome
- Multiple primary buttons competing for attention

---

## 6. How to Perform a UI Review

Reviewers use `FOUNDATION_COMPLIANCE_CHECKLIST.md`.

Minimum review questions:

1. Does this change still serve the Manifesto?
2. Does the experience still create trust and understanding?
3. Does Brand language remain consultant-grade?
4. Does Visual hierarchy guide the eye correctly?
5. Does Design System architecture remain intact?
6. Are a11y and responsive rules preserved?
7. Was any frozen Foundation document edited? (Must be **No**)

---

## 7. Result Page Specific Rules

Result Page UI V1.0 is frozen.

| May change | Must not change |
|------------|-----------------|
| Bug fixes that preserve contracts | Zone / Row / Grid order |
| Visual Language layers scoped under `data-visual` | Layout Pattern IDs |
| Presentation formatting helpers (no business logic) | Blueprint / Gallery structure |
| Tests for regressions | Engine / ViewModel contracts without wrappers |

Reference implementations:

- `applications/customer_portal/src/screens/result/`
- `result-page-visual-v2.css` (`data-visual="v2"`)

---

## 8. Related Adoption Documents

| Document | Role |
|----------|------|
| `FOUNDATION_AUDIT_REPORT.md` | Current compliance map |
| `FOUNDATION_COMPLIANCE_CHECKLIST.md` | Release / PR gate |
| `FOUNDATION_ADOPTION_PLAN.md` | Migration order |
| `FOUNDATION_INDEX.md` | Entry point |

---

END
