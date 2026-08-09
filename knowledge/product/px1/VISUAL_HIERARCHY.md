# Visual Hierarchy — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Tokens: Visual Language System (frozen) · PACK_01–03 (frozen)

---

## 1. Purpose

Visual weight must match consulting importance.

The eye should land on judgment first, evidence later.

PX-1 defines **roles**.  
Sizes, colors, and elevation values come from frozen Visual Language — not from this file.

---

## 2. Hierarchy bands

| Band | Name | Visual job | Typical sections |
|------|------|------------|------------------|
| **H0** | Hero focus | First calm focal point | Hero headline + one-liner |
| **H1** | Primary reading | Highest content emphasis | Tóm tắt tư vấn · Định hướng chính |
| **H2** | Guided depth | Clear but subordinate | Lưu ý · five domains |
| **H3** | Confirmation | Quiet evidence | Biểu đồ minh họa |
| **H4** | Reference | Lowest on-load weight | Chi tiết kỹ thuật · Kiến thức · Phụ lục |

One H0.  
One primary commercial CTA in H1.  
H3/H4 must never shout.

---

## 3. Weight tools (in order)

Use emphasis in this order only:

```
Typography
  ↓
Spacing / whitespace
  ↓
Surface contrast
  ↓
Elevation
  ↓
Color
```

Color is the last emphasis tool.  
Decoration is not an emphasis tool.

---

## 4. First viewport composition

Must include:

- Hero (H0)  
- Start of Tóm tắt tư vấn (H1)  

Should include, if height allows:

- Remainder of Tóm tắt  
- Affordance toward Định hướng chính  

Must not include as visual competitors:

- Chart grids  
- Pillar tables  
- Knowledge panels  
- Multi-CTA toolbars  

---

## 5. Section visual rules

| Section | Band | Type role | Surface | Border strategy |
|---------|------|-----------|---------|-----------------|
| Hero | H0 | Display / Heading | Distinct but calm | Whitespace first |
| Tóm tắt tư vấn | H1 | Section + Body | Primary card | One boundary |
| Định hướng chính | H1 | Section + Card title | Primary cards | One boundary per card |
| Lưu ý quan trọng | H2 | Section + Body | Warning semantic, not alarmist | Meaning via Warning role |
| Life domains | H2 | Section + Body | Standard cards | Group by whitespace |
| Biểu đồ minh họa | H3 | Section + Caption | Quiet cards | No dashboard chrome |
| Chi tiết kỹ thuật | H4 | Section + Note | Collapsed header | Minimal |
| Kiến thức bổ sung | H4 | Section + Caption | Collapsed header | Minimal |
| Phụ lục | H4 | Body / Note | Flat | No elevation drama |

---

## 6. Signature visual order (V2)

```
Hero
  ↓
Tóm tắt tư vấn
  ↓
Định hướng chính
  ↓
Lưu ý quan trọng
  ↓
Life domains
  ↓
Charts (quiet)
  ↓
Technical / Knowledge (collapsed)
```

This replaces V1 “charts before recommendations” as the *experience* hierarchy.

Visual Language tokens still supply the scale.  
PX-1 supplies what those tokens emphasize.

---

## 7. Density vs hierarchy

| Band | Density intent |
|------|----------------|
| H0–H1 | Low density — readable in one breath |
| H2 | Medium — one question per card |
| H3 | Medium–high visuals, low prose |
| H4 | High allowed only after expand |

Never fill whitespace with chips, stat strips, or badge storms.

---

## 8. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Equal card walls | Restore H0/H1 dominance |
| Bright charts above muted summary | Quiet charts; strengthen summary type |
| Thick borders everywhere | Whitespace → type → surface |
| Multiple accent colors competing | One primary accent per view |
| Hero as metadata ribbon | Move metadata to Chi tiết kỹ thuật |

---

## 9. Stop line

Visual hierarchy V2 is an experience map over frozen tokens.

END
