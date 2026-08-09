# Accessibility Guide — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Source: PACK_05 · WCAG 2.2 AA · Visual Language contrast rules

---

## 1. Purpose

A consultation that cannot be read, focused, or announced is not a BTE consultation.

Stricter of PACK_05 vs WCAG 2.2 AA wins.

---

## 2. Contrast

- Body, headings, bullets, and button labels meet contrast on Background and Card  
- Warning / Danger surfaces keep readable text — color wash is not an excuse  
- Chart text and captions meet the same bar  
- Focus ring remains visible on all interactive components  
- Do not rely on color alone for status, warning, or chart series  

---

## 3. Typography and reading

- Minimum comfortable body is Visual Language Body 16px  
- Do not shrink Primary advice to Caption to fit a card  
- Line length 45–75 characters for prose  
- Line height Body 150%  
- Users must be able to zoom / enlarge without losing reading order  

---

## 4. Structure for assistive tech

Logical heading outline follows reading order:

```
(document / page title — Vietnamese)
  Hero identity (not an English “Hero” heading)
  Tóm tắt tư vấn
  Định hướng chính
    Sự nghiệp / Tài chính / Quan hệ / Sức khỏe / Vận trình (groups)
  Lưu ý quan trọng
  Sự nghiệp
  Tài chính
  Quan hệ
  Sức khỏe
  Vận trình
  Biểu đồ minh họa
  Chi tiết kỹ thuật
  Kiến thức bổ sung
  Phụ lục
```

Do not skip heading levels to style a card.

---

## 5. Keyboard

Users must be able to:

- Skip to main content  
- Move through sections in visual order  
- Expand / collapse  
- Activate Primary / Secondary / Tertiary  
- Reach charts, technical panel, and knowledge  

Focus order = reading order.  
No keyboard trap inside expand panels.

---

## 6. Expand / collapse

Each disclosure control must expose:

- Visible Vietnamese name  
- Expanded / collapsed state  
- What it controls  

When Technical or Knowledge is collapsed, the toggle remains discoverable.  
Do not remove collapsed content from the accessibility tree in a way that hides the toggle.

---

## 7. Screen reader

| Element | Announcement intent |
|---------|---------------------|
| Hero identity | Who the consultation is for |
| Status | Vietnamese status, not codes |
| Summary bullets | List of 5 or fewer |
| Recommendation | Title, domain, Why, Expected result, Action |
| Warning | Caution + mitigation |
| Chart | Title + caption; decorative SVG marked decorative if caption suffices |
| Technical fields | Vietnamese labels before values |
| Icons | Named if functional; silent if decorative |

Never announce internal IDs unless the user opened Chi tiết kỹ thuật.

---

## 8. Motion

Respect reduced motion.  
Expand does not require animation to be understandable.

---

## 9. Error and empty

- Empty is not announced as an error  
- Errors include recovery in Vietnamese  
- Status is not color-only  

See `EMPTY_STATE_GUIDE.md` and `ERROR_STATE_GUIDE.md`.

---

## 10. Checklist (future implementation)

- [ ] Keyboard-only complete read + act  
- [ ] Focus visible  
- [ ] Heading outline matches IA  
- [ ] Contrast AA+  
- [ ] Expand state exposed  
- [ ] Charts have text alternative  
- [ ] Vietnamese accessible names  
- [ ] Reduced motion honored  
- [ ] No English-only ARIA  

---

## 11. Stop line

Accessibility is part of the blueprint, not a later polish layer.

END
