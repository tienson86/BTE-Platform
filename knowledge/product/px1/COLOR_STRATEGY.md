# Color Strategy — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Source of roles: Visual Language §10 (frozen) · PACK_05 contrast

---

## 1. Purpose

Color communicates meaning.  
It is never decoration.

PX-1 defines **when** each role is used on the Result Page.  
PX-1 does not publish new hex values.

---

## 2. Role catalog

| Role | Job on Result Page |
|------|--------------------|
| **Primary** | Brand identity · one accent · Primary CTA |
| **Secondary** | Quiet navigation / in-page TOC / secondary controls |
| **Success** | Positive findings · constructive expected results |
| **Warning** | Lưu ý quan trọng · caution that needs attention without panic |
| **Danger** | Critical issues · blocking errors · severe risk only |
| **Neutral** | Supporting text · captions · collapsed headers · technical labels |
| **Background** | Page canvas — supports content, never competes |
| **Cards** | Elevated reading surfaces |
| **Borders** | Last-resort separation after whitespace and surface contrast |
| **Highlight** | Temporary emphasis (focus, selected expand) — sparse |

Information colors from Visual Language (do not invent more):

| Meaning | Family |
|---------|--------|
| Positive | Green |
| Neutral | Gray |
| Negative | Red |
| Warning | Amber |
| Information | Blue |

---

## 3. Accent rule

Each Result view has **one primary accent**.

Primary accent belongs to:

- brand presence  
- the single Primary CTA  

It does **not** belong to every tag, chart series, and heading.

---

## 4. Surface stack

```
Background
  ↓
Section
  ↓
Card
  ↓
Interactive control
```

Distinguish surfaces mainly by spacing and subtle elevation.  
Avoid nested bordered boxes.

---

## 5. Section usage

| Section | Color intent |
|---------|--------------|
| Hero | Neutral surfaces · Primary only as quiet identity accent |
| Tóm tắt tư vấn | Neutral card · no traffic-light bullets |
| Định hướng chính | Neutral cards · Success may mark constructive outcome lines sparingly |
| Lưu ý quan trọng | Warning role on icon/tag — body stays readable Neutral |
| Life domains | Neutral · domain tags are Neutral or Secondary, not a rainbow |
| Charts | Semantic series only as needed · captions Neutral · no neon |
| Technical / Knowledge | Neutral · collapsed headers quieter than P1 |
| Empty | Neutral |
| Error | Danger for status + Neutral readable explanation |

---

## 6. Hierarchy vs color

Priority of emphasis:

```
Typography
  ↓
Spacing
  ↓
Contrast
  ↓
Color
```

Do not color a section “important” to fake P1.

---

## 7. Warnings vs danger

| Situation | Role |
|-----------|------|
| Decision caution, mitigable | Warning |
| Blocking failure, data missing critically, unsafe to proceed | Danger |
| Positive expected result | Success |
| Informational chart note | Information / Neutral |

Most consultations should use Warning more than Danger.  
Danger inflation destroys trust.

---

## 8. Charts

Charts inherit semantic colors only to encode meaning already explained in Vietnamese captions.

Rules:

- Color is never the only encoding (see Accessibility)  
- Do not assign a unique hue to each life domain as decoration  
- Background of chart cards stays Card/Neutral  

---

## 9. Contrast

Follow PACK_05 and WCAG 2.2 AA (stricter internal rule wins).

- Body text on Background/Card must remain readable in light and dark themes  
- Warning/Danger backgrounds must not reduce body contrast  
- Placeholder / disabled text is not used for primary advice  

---

## 10. Forbidden

- Rainbow dashboards  
- Hero as a colored marketing banner  
- English status chips in Primary color  
- Using Danger for empty states  
- Inventing extra semantic hues  
- Decorative gradients that compete with reading  

---

## 11. Stop line

Color strategy V2 is role-based. Implementation must use Design System tokens only.

END
