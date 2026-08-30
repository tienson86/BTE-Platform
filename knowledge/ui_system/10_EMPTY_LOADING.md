# 10_EMPTY_LOADING.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_04_UI_PRESENTATION_STANDARD.md §14
- PACK_02_LAYOUT_SYSTEM.md §23–25
- PACK_03_COMPONENT_STANDARD.md §28–31

---

# 1. Philosophy

Empty, loading, and error are normal product states.

The layout exists before data arrives.

Users never see a blank canvas.

Tone stays consulting: calm, clear, actionable.

---

# 2. Loading

Skeleton first.

Skeleton dimensions match the final Hero / Summary / Analysis layout.

No layout jump when data arrives.

Progressive load: executive summary before charts and tables.

Token: skeleton uses `--surface-section` on `--surface-report-paper`. Motion: `--motion-normal` pulse, disabled under reduced motion.

---

# 3. Empty

Structure:

Title (Card Title or Section)

↓

One sentence (Body)

↓

One next action (optional)

Examples: no analysis yet → go to Analyze. No history → calm explanation. Never joke. Never blame the user.

Icon optional, 24–32px, Neutral.

---

# 4. Error

Structure:

What happened (Body)

↓

What to do (Body)

↓

Action (retry / reanalyze / back)

Severity:

| Level | Color | Use |
|-------|-------|-----|
| Warning | `--feedback-warning` | Recoverable |
| Critical | `--feedback-danger` | Contract / corrupt / failed render |

Customer copy: no stack traces, no engine names, no Pack05 / pipeline language.

---

# 5. Status Card

Loading, empty, and inline error chips use Status Card rules (XS, Label + state).

Page-level failure uses the existing Result status gate. Do not invent a new gate in UI-13.

---

END
