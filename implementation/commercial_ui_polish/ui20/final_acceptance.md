# UI-20 Final acceptance

Commercial UI V2 freeze candidate. CASE-0001 live `/result` and `/report-preview`. Second existing case: CASE-0002 (Hoàng Thị Thu Phương) reviewed from the published editorial export only — no new astrology fixture.

## Journey

Birth Input → Analyze → Result → Dashboard → Interpretation → Action → Report Preview → Print → Mobile.

All surfaces used the approved Visual System. No new card types, palettes, type scales, motion tokens, or visualizations.

## Acceptance questions

| Question | Result |
|----------|--------|
| Trust in 3 seconds | PASS |
| Main conclusion quickly | PASS |
| Action Plan usable | PASS |
| Mobile feels designed | PASS |
| Report/print hand-to-customer | PASS |

## Token cleanup this sprint

- Replaced UI-18 magic `56px` bar offset with `var(--touch-target-min) + var(--space-3)`
- ShenSha chip radius uses `--bte-radius-12`
- Mobile `overflow-x: clip`
- Identity solar date displays as DD/MM/YYYY in the header (ISO payload unchanged)

Identity header density, 14px card radius, and print millimetre page metrics remain accepted exceptions from earlier frozen geometry.
