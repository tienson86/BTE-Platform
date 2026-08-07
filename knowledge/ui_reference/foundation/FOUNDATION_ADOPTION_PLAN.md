# FOUNDATION_ADOPTION_PLAN.md

Version: 1.0  
Date: 2026-08-07  
Status: OFFICIAL  
Epic: Foundation V1.0 Adoption  
Constraint: Do **not** modify frozen Foundation documents, Design System packs, or Result Page architecture

---

## 1. Goal

Bring remaining BTE UI surfaces into compliance with Foundation V1.0 while preserving:

- Result Page UI V1.0 freeze
- Visual Language V2 on Result Page
- Engine / business logic boundaries

---

## 2. Current Compliant Modules

| Module | Compliance | Notes |
|--------|------------|-------|
| `screens/result/**` | High | PACK_06/07 + Visual V2 |
| `PortalPage` Result host | High | Official analysis entry |
| Foundation document set | Complete | Frozen SSOT |
| Adoption docs + Cursor rule | Complete | This epic |

---

## 3. Modules Requiring Migration

| ID | Module | Gap | Priority | Effort | Suggested order |
|----|--------|-----|----------|--------|-----------------|
| M01 | Dual SSOT docs (`knowledge/design_system`, `ui_blueprints`) | Conflicting guidance | P0 | S | Document deprecation pointers only |
| M02 | Legacy `canonical_desktop/sections` + `rows` | Parallel to Result zones | P0 | M | Stop new work; route to Result |
| M03 | `screens/bazi/**` + `BaZiResultScreen` | Pre-Foundation layout | P1 | L | Replace usage with Result Page |
| M04 | Standalone analysis screens (Executive*, FourPillars, Metrics, Explainable, Consultation, Appendix) | Not zone architecture | P1 | L | Consolidate behind Result / retire |
| M05 | Dashboard (`screens/dashboard/**`) | Widget density vs Brand | P2 | M | Visual + Experience pass |
| M06 | Navigation / shell chrome | Brand/Visual incomplete | P2 | M | Align with Visual Language surfaces |
| M07 | `components/business/**` | Pre-PACK cards | P2 | L | Rebuild on shared presentation primitives |
| M08 | Charts library consumers | A11y text uneven | P3 | S | Text summaries everywhere |
| M09 | Forms / display / navigation components | Brand review missing | P3 | M | Checklist-driven review |
| M10 | i18n / copy tone | Brand vocabulary | P3 | M | Editorial pass vs Brand Language |

Effort key: **S** ≤ 2 days · **M** ≤ 1–2 weeks · **L** multi-sprint

---

## 4. Suggested Migration Waves

### Wave 0 — Process (this epic) ✅

- Audit, developer guide, checklist, adoption plan
- Cursor Foundation rule
- Documentation dependency chain

### Wave 1 — Clarify SSOT (P0)

- Mark legacy design trees as **reference / deprecated**
- Ensure all new UI tickets cite Foundation chain
- Block PRs that extend legacy BaZi/S* analysis UIs

### Wave 2 — Analysis surface consolidation (P1)

- Make Result Page the only production analysis UI
- Migrate callers from `BaZiResultScreen` / standalone screens
- Do **not** redesign Result zones; only retire duplicates

### Wave 3 — Portal experience (P2)

- Dashboard Visual/Brand pass
- Shell chrome Visual Language alignment
- Business component library alignment

### Wave 4 — Polish & coverage (P3)

- Charts a11y
- Forms/display Brand review
- Copy tone pass

---

## 5. Definition of Done (per module)

A module is adopted when:

1. `FOUNDATION_COMPLIANCE_CHECKLIST.md` is PASS for mandatory items
2. No Engine models leak into UI
3. Visual hierarchy matches Visual Language
4. Brand tone matches Brand Language
5. Design System packs for that surface are respected
6. Tests/build for the module pass

---

## 6. Out of Scope (explicit)

- Editing Product Manifesto / Brand / Experience / Visual System / PACK_01–07 content
- Result Page architecture or Layout Pattern changes
- New product features
- Engine / Rule Database changes

---

## 7. Next Development Phase Recommendations

1. **Wave 1 immediately** — eliminate dual SSOT confusion.
2. **Declare Result Page the sole analysis UI** in portal routing.
3. Run Foundation checklist on Dashboard as first non-Result migration.
4. Schedule Brand copy review for customer-facing strings.
5. Keep Visual V3 (if any) as a separate epic after adoption waves.

---

END
