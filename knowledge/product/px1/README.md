# PX-1 — Result Experience Blueprint V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1 · Result Experience Blueprint V2  
Owner: BTE Product  
Scope: **Architecture and blueprint only — no implementation**

---

## 1. Purpose

PX-1 is the canonical Product Experience blueprint for the BTE Result Page V2.

Future UI implementations must follow this pack.

This sprint produces **design documents only**.

No React. No CSS. No Tailwind. No HTML.  
No Portal changes. No engine changes. No API changes.

---

## 2. Product identity

BTE is **not** a dashboard.  
BTE is **not** an admin console.  
BTE is **not** a developer tool.

BTE **is** a professional consultation experience.

The Result Page must feel like an experienced consultant guiding the user step by step.

---

## 3. Dependency chain

Higher layers win conflicts.

```
Product Manifesto
        ↓
Experience Principles
        ↓
Brand Language
        ↓
PX-1 Result Experience Blueprint V2   ← this pack
        ↓
Visual Language (frozen tokens)
        ↓
Design System PACK_01–07 (frozen primitives)
        ↓
Future implementation (not this sprint)
```

Foundation V1.0 remains frozen. PX-1 does **not** edit Foundation, Visual Language, or Design System packs.

PX-1 **references** frozen tokens (type scale, spacing scale, color roles, accessibility).  
PX-1 does **not** invent new pixels, hex values, type sizes, or shadows.

---

## 4. Relationship to prior Result specs

| Pack | Status after PX-1 |
|------|-------------------|
| PACK_06 / PACK_07 | Foundation V1 layout freeze — unmodified |
| Product Polish V1 | Commercial V1 experience reference — unmodified |
| **PX-1 Blueprint V2** | **Canonical SoT for future Result Experience** |

V1 layout freeze described *how the current Portal is structured*.  
PX-1 describes *how the consultation must read and feel* in V2.

Until a later implementation sprint is authorized, Portal code stays unchanged.

---

## 5. Frozen surfaces (this sprint)

| Surface | Rule |
|---------|------|
| Portal / React / CSS / Tailwind | Do not modify |
| Engines / pipelines / APIs | Do not modify |
| Foundation / Design System / Visual Language source docs | Do not modify |
| Knowledge Units / Narrative Engine | Do not modify |
| Golden Dataset / snapshots | Do not modify |

---

## 6. Reading order of this pack

| Order | File | Role |
|------:|------|------|
| 0 | `README.md` | This index |
| 1 | `DESIGN_PRINCIPLES.md` | Experience laws |
| 2 | `RESULT_PAGE_BLUEPRINT_V2.md` | Master blueprint |
| 3 | `INFORMATION_ARCHITECTURE.md` | Section map |
| 4 | `USER_READING_FLOW.md` | Consultant journey |
| 5 | `SECTION_PRIORITY.md` | Attention ranking |
| 6 | `VISUAL_HIERARCHY.md` | Visual weight |
| 7 | `COMPONENT_TREE.md` | Full hierarchy |
| 8 | `CARD_SPECIFICATION.md` | Card types |
| 9 | `TYPOGRAPHY_SYSTEM.md` | Type roles |
| 10 | `SPACING_SYSTEM.md` | Rhythm |
| 11 | `COLOR_STRATEGY.md` | Color roles |
| 12 | `ICONOGRAPHY.md` | Icon rules |
| 13 | `ACTION_MODEL.md` | CTA model |
| 14 | `EXPANSION_MODEL.md` | Preview → Expand → Detail |
| 15 | `RESPONSIVE_STRATEGY.md` | Desktop / Tablet / Mobile |
| 16 | `ACCESSIBILITY_GUIDE.md` | A11y |
| 17 | `LANGUAGE_GUIDE.md` | Vietnamese-only UI |
| 18 | `COPYWRITING_GUIDE.md` | Consultant prose |
| 19 | `MICROCOPY_GUIDE.md` | Labels and controls |
| 20 | `EMPTY_STATE_GUIDE.md` | Empty states |
| 21 | `ERROR_STATE_GUIDE.md` | Error states |
| 22 | `UI_REVIEW_CHECKLIST.md` | Future review gate |
| 23 | `PX1_SUMMARY.md` | Sprint close |
| — | `wireframes/` | Layout sketches |
| — | `documentation/` | Philosophy and future |

---

## 7. Canonical reading order (user)

```
Hero
  ↓
Tóm tắt tư vấn
  ↓
Định hướng chính
  ↓
Lưu ý quan trọng
  ↓
Sự nghiệp
  ↓
Tài chính
  ↓
Quan hệ
  ↓
Sức khỏe
  ↓
Vận trình
  ↓
Biểu đồ minh họa
  ↓
Chi tiết kỹ thuật
  ↓
Kiến thức bổ sung
  ↓
Phụ lục
```

This order is mandatory for V2.  
Reading order is identical on Desktop, Tablet, and Mobile.

---

## 8. Success criteria (PX-1)

- [x] Complete blueprint pack created  
- [x] Information architecture defined  
- [x] Reading flow defined  
- [x] Component tree defined  
- [x] Card, type, space, color, icon rules defined  
- [x] Language = Vietnamese for all user-visible text  
- [x] No implementation artifacts  

---

## 9. Stop line

**PX-1 is design only.**

Do not implement from this pack until Product authorizes a later sprint.

END
