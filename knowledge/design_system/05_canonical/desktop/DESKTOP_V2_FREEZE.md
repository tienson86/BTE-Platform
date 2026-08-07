# DESKTOP_V2_FREEZE.md

> BTE Design System · Desktop Canonical UI
>
> Status: **FROZEN**
>
> Date: 2026-08-07
>
> Task: FINAL_DESKTOP_V2_POLISH

---

## Decision

Desktop V2 layout and structure are **frozen**.

No further visual redesign or polish iterations in this phase.

Remaining visual gaps are tracked in:

`DESKTOP_V2_VISUAL_POLISH_BACKLOG.md`

---

## What is frozen

- Row architecture (Row01–Row04)
- Section placement S00–S11
- Module card chrome (white card, shared header language for S01–S03)
- Grid spans and reading order as implemented
- Preview/demo fixture shape in `mockData.ts` (fixture only — not runtime SSOT)

---

## Polish completed in final pass

1. **Module headers (S01 / S02 / S03)** — titles moved inside white cards via shared `ModuleHeader` (`cd-module-header`, `#B91C1C`, uppercase, 24px card padding).
2. **S03 container redesign** — outer card wrapper; denser pillars (removed `min-height` void + footer `margin-top: auto`); larger Han glyphs; balanced column spacing.
3. **S02 container redesign** — single title `TỔNG QUAN LÁ SỐ`; removed spacer div; six tiles optically centered under the header.

---

## Engine integration phase

Starts immediately after this freeze.

Portal must consume `POST /analyze` (OrchestratorService) instead of static mock for S00–S11.

---

END
