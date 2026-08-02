# 15 — VISUAL GRAMMAR (Addendum J)

| Field | Value |
|-------|--------|
| **Document** | `15_VISUAL_GRAMMAR.md` |
| **Addendum** | **J** |
| **Version** | `1.1.0` |
| **Status** | **Normative — Blueprint V1.1 Final** |
| **Owner** | Design Language + Visual Hierarchy |

---

## Purpose

Freeze the **visual grammar** of BTE Result so implementers do not invent spacing, rhythm, elevation, or accent usage.

Complements [VISUAL_HIERARCHY.md](VISUAL_HIERARCHY.md) and [DESIGN_LANGUAGE.md](DESIGN_LANGUAGE.md).

---

## 1. Grid & stream

| Token | Normative value |
|-------|-----------------|
| Rail width (Desktop) | 200–240px |
| Stream max content width | 960–1100px |
| Tier gap | 2.0–3.0 × card inner padding |
| Card inner padding | “comfortable” (≥ 1.25rem logical; exact px in Sprint 07) |
| Column gutter (pillars) | ≥ 1.0rem |

**Grammar rule:** One vertical stream. No competing multi-column “dashboard widgets” at page level.

---

## 2. Elevation (surface stack)

| Level | Surfaces | Shadow / border |
|-------|----------|-----------------|
| E0 | Page canvas | Flat |
| E1 | Tier backgrounds (optional) | None / hairline |
| E2 | Standard cards (charts, chapters) | Hairline + soft shadow |
| E3 | ExecutiveHero, Day pillar | Soft elevated shadow; may use soft primary wash |
| E4 | Modals/toasts (global) | Stronger; rare on Result |

**Forbidden:** Every card at E3 (admin tile wall).

---

## 3. Rhythm

| Pattern | Rule |
|---------|------|
| Label → Value | Caption above metric/body |
| Section head → body | Head band, then padded body |
| List | Compact; max ~6 bullets before “more in Analysis” |
| Callout | Full-width inside hero/chapter; left accent bar allowed (primary/warn-soft only) |

---

## 4. Accent grammar (scarce)

| Accent token | Allowed on |
|--------------|------------|
| `accent-day` | Nhật Chủ, Day pillar |
| `accent-dung` | Dụng Thần metric |
| `accent-hy` | Hỷ Thần metric |
| `accent-ky` | Kỵ Thần metric (warning-soft, not danger flood) |
| `accent-than` | Thân metric |
| `accent-rail` | Active NavigationRail item |

All other metrics/surfaces: **neutral**.

---

## 5. Icon grammar

- Single stroke family; one size per context (rail 20px, tier head 20–22px)
- Icons never replace text labels on rail or TOC
- No emoji as product chrome

---

## 6. Motion grammar

| Trigger | Duration | Effect |
|---------|----------|--------|
| Content replace skeleton | 200–350ms | Fade |
| Tier enter | ≤350ms | Fade + 4–8px rise once |
| Collapse | ≤250ms | Height/opacity |
| Rail active | ≤180ms | Color/background |
| Chart bars | ≤400ms | Width ease |

**Forbidden:** Looping pulse, parallax, confetti, auto-carousel of KPIs.

---

## 7. Density grammar by tier

| Tier | Density |
|------|---------|
| Executive | Low |
| Bazi / Charts | Medium |
| Analysis | Medium–high, sectioned |
| Interpretation | Reading density (Notion-like) |
| Knowledge expert panes | Higher OK |

---

## 8. Do / Don’t

| Do | Don’t |
|----|-------|
| One hero mass | Equal cards everywhere |
| Hairlines for structure | Heavy colored boxes for every fact |
| Muted captions | Bright labels competing with values |
| Calm caution for Kỵ | Blood-red doom panels |

---

## Version

`1.1.0`
