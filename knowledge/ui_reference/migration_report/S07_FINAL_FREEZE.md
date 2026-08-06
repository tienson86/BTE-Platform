# S07 — FINAL FREEZE

| Item | Value |
|------|-------|
| Section | **S07 — THẦN SÁT** |
| Status | **FROZEN** |
| Freeze Date | **2026-08-06** |
| Canonical Version | **Desktop Canonical UI V1** |

---

## Approved Screenshot

`knowledge/ui_reference/migration_report/screenshots/s07_phase2/01_s07_only.png`

Supporting artifacts:

- Phase 1: `screenshots/s07_phase1/01_s07_only.png`
- Phase 1 report: `S07_PHASE1_COMPLETION_REPORT.md`
- Phase 2 report: `S07_PHASE2_COMPLETION_REPORT.md`

---

## Source of Truth

`knowledge/ui_master/sections/S07_SHEN_SHA/`

- `README.md`
- `S07_MASTER_LAYOUT.md`
- `S07_MASTER_GRID_VI.md`
- `S07_MASTER_ANNOTATION_VI.md`
- `S07_REVIEW_CHECKLIST.md`

Implementation:

- `applications/customer_portal/src/screens/canonical_desktop/sections/S07ShenSha.tsx`
- S07 styles in `applications/customer_portal/src/styles/canonical-desktop.css`
- Mock: `CANONICAL_DESKTOP_MOCK.s07`

---

## Review Notes

- S07 is an **Executive Summary of Shen Sha**, not a dashboard, KPI widget, chart, or analytics panel.
- Reading flow locked:

  Header → Executive Summary → Cát tinh → Divider → Hung tinh → Divider → Footer Summary → `Xem toàn bộ →`

- Exact lists frozen:
  - Cát tinh (5): Thiên Ất Quý Nhân · Thiên Đức Quý Nhân · Nguyệt Đức Quý Nhân · Văn Xương · Hoa Cái
  - Hung tinh (5): Kiếp Sát · Không Vong · Cô Thần · Quả Tú · Đại Hao
- Phase 2 polish accepted: compact card, `#FFF8EF` executive banner, 16px icons, 14px item text, inset dividers, BTE Red text link.

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Information lists only (✓ / ✕) | Fast recognition in under 5 seconds |
| No pie / donut / gauge / progress / KPI | Avoid dashboard language; stay executive |
| Two semantic groups only (Cát / Hung) | Answers “what is good?” and “what is risky?” immediately |
| Soft executive banner `#FFF8EF` | Summary is informational, not a metric card |
| Text link, not button | Secondary action; no CTA chrome |
| Inset 1px dividers | Separate groups without heavy decoration |
| Mock data only | Desktop Canonical V1 is visual freeze, not backend |

---

## Future Change Policy

**S07 is permanently frozen.**

Do **not** modify S07 unless Product Owner explicitly reopens the section.

If a change is required after freeze:

1. Product Owner must reopen S07 in writing.
2. Change must cite the master section docs under `S07_SHEN_SHA/`.
3. Scope must be limited to S07 only (do not touch S00–S06 or S08–S11).
4. Deliver updated screenshot + freeze amendment note before re-freeze.

Forbidden without reopen:

- Redesign or layout changes
- New widgets, charts, badges, chips, tooltips, accordions
- Data / reading-flow / component-tree changes
- Typography or color system changes outside an approved polish ticket

---

## FREEZE STATEMENT

**Status: FROZEN**

S07 — THẦN SÁT is locked for Desktop Canonical UI V1 as of **2026-08-06**.
