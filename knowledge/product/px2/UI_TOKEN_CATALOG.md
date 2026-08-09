# UI Token Catalog

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Values: Visual Language + PACK_02 / PACK_05 (frozen) — **roles only**

PX-2 does not invent pixels or hex.

---

## 1. Type roles → components

| Token role | VL level | Components |
|------------|----------|------------|
| display | Display 40 Bold | Hero headline (optional) |
| heading | H1 32 Bold | Page title if any |
| section | H2 24 SemiBold | Section titles |
| cardTitle | H3 20 SemiBold | Rec / warning / chart / knowledge titles |
| group | H4 18 Medium | Domain group labels |
| body | Body 16 Regular | Bullets, why, action, analysis |
| caption | Caption 14 | Chart caption, expand hint |
| note | Meta 12 | Technical labels, appendix notes |
| button | DS button | Primary / Secondary |
| tag | Caption/Meta | Domain tag, status |

---

## 2. Space roles

| Token | Value source | Use |
|-------|--------------|-----|
| page.padding.desktop | 32 | Desktop shell |
| page.padding.tablet | 24 | Tablet |
| page.padding.mobile | 16 | Mobile |
| zone.gap | XL/XXL 48–64 | Between major sections |
| section.gap | 32 | Section blocks |
| card.gap | 24 | Card stack |
| card.padding | 24 | Card inner |
| inline.gap | 12 | Icon–label |

Scale: 4·8·12·16·24·32·40·48·64·80·96 only.

---

## 3. Color roles

| Role | Use |
|------|-----|
| primary | One accent + Primary CTA |
| secondary | Nav / secondary CTA |
| success | Sparse positive expected-result cue |
| warning | Warning cards |
| danger | Critical warning / page error |
| neutral | Body, captions, collapsed headers |
| background | Page canvas |
| card | Card surface |
| border | Last-resort separator |
| highlight | Focus |

---

## 4. Elevation / motion / a11y

| Token | Rule |
|-------|------|
| elevation.card | VL Level 1–2 |
| focus.ring | Visible · PACK_05 |
| contrast.text | WCAG 2.2 AA / PACK_05 stricter |
| motion.expand | Short; honor reduced motion |

---

## 5. Binding rule

Components reference **token roles**, never raw CSS values.  
Future implementation maps roles to existing Design System tokens only.

---

## 6. Stop line

Token catalog is a role index, not a new theme.

END
