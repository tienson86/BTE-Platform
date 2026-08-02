# NAVIGATION SPEC

| Field | Value |
|-------|--------|
| **Document** | `NAVIGATION_SPEC.md` |
| **Version** | `1.1.0` |
| **Status** | Final Freeze — Blueprint V1.1 |

---

## Purpose

Define Result navigation so users **follow a story**, not hunt across peer tabs.

---

## Hard bans

| Pattern | Status | Reason |
|---------|--------|--------|
| Primary **Tab bar** for Executive / Bazi / Charts / Analysis / Interpretation / Knowledge | **Banned** | Equalizes tiers; destroys reading order |
| **Accordion-as-navigation** for the six tiers | **Banned** | Hides spine; users guess where content lives |
| Replacing scroll with SPA route per tier | **Banned** (this blueprint) | Breaks continuous report metaphor |

Accordion/collapse **inside** Analysis/Interpretation sections is allowed as progressive disclosure — not as tier navigation.

---

## Naming freeze (Addendum E)

| Canonical | Do not use as primary |
|-----------|------------------------|
| **NavigationRail** | NavRail |
| Rail label VI `Tóm tắt` | — |
| Eyebrow VI `Tóm tắt điều hành` | — |
| Anchor ids | `tier-executive` … `tier-knowledge` (frozen) |

---

## Required pattern: Sticky Navigation Rail

### Placement

- Desktop: left column, `position: sticky`, aligned to report stream
- Tablet: may become horizontal chip rail above stream (same anchors)

### Contents (fixed order)

1. Tóm tắt → `#tier-executive`  
2. Bát Tự → `#tier-bazi`  
3. Biểu đồ → `#tier-charts`  
4. Phân tích → `#tier-analysis`  
5. Luận giải → `#tier-interpretation`  
6. Kiến thức → `#tier-knowledge`  

Optional footer of rail: Reading Progress.

### Behavior

| Event | Behavior |
|-------|----------|
| Click rail item | Smooth scroll to tier; set active |
| Scroll stream | Scroll Spy updates active item |
| Deep link `/result#tier-knowledge` | Land on Knowledge after load |
| Keyboard | Focusable links; Enter activates |

---

## Scroll Spy

| Spec | Value |
|------|-------|
| Mechanism | IntersectionObserver (or equivalent) |
| Root margin | Prefer center-weighted (e.g. top 20% / bottom 55%) so active = reading focus |
| Tie-break | Highest intersection ratio among visible tiers |
| Initial | `tier-executive` active on load when payload exists |

---

## Anchors

| Tier | Anchor id (normative) |
|------|------------------------|
| Executive | `tier-executive` |
| Bazi | `tier-bazi` |
| Charts | `tier-charts` |
| Analysis | `tier-analysis` |
| Interpretation | `tier-interpretation` |
| Knowledge | `tier-knowledge` |

Sub-anchors (optional later): `analysis-pattern`, `interp-career`, etc. — must not replace tier anchors.

**Scroll margin:** Enough offset that tier title is not hidden under sticky chrome/rail.

---

## Section Jump

- Rail jumps = section jump
- In-page TOC inside Interpretation (optional) may jump to chapter cards
- Must not open a new “mode” that unmounts other tiers

---

## Reading Progress

| Option | Spec |
|--------|------|
| A (preferred) | Thin progress within rail (steps filled 1→6) |
| B | Top thin bar over stream |

Progress = scroll depth through report stream (0–100%) and/or highest tier reached.

---

## Global app nav vs Result nav

| Nav | Role |
|-----|------|
| App header (Dashboard, Analyze, Result, Reports, …) | Product areas |
| Result rail | **Within-report** reading aids |

Do not merge them into one mega-sidebar of mixed concerns (admin smell).

---

## Empty / error navigation

| State | Nav behavior |
|-------|--------------|
| No payload | Hide rail or disable jumps; show EmptyState |
| Partial payload | Rail still lists all tiers; empty tiers show Unavailable |

---

## Acceptance

- [ ] No primary tier tabs  
- [ ] Sticky rail + scroll spy specified  
- [ ] Anchor ids frozen  
- [ ] Progress specified  
- [ ] Collapse ≠ navigation  

---

## Version

`1.1.0`
