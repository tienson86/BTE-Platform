# Luck Timeline Foundation

| Field | Value |
|-------|-------|
| **Document** | LUCK_TIMELINE |
| **Sprint** | LE-1 |
| **Timeline version** | 1.0.0 |
| **Package** | `bz_09_luck_foundation` 1.0.0 |
| **Foundation** | 1.0.0 (frozen) |
| **Status** | Canonical |

---

## Timeline philosophy

Luck in BTE is a **time lattice**, not a fortune verdict.

LE-1 defines:

- who the natal chart is (identity)
- which time layers exist
- how periods nest and abut
- which fields future Luck packages may publish

LE-1 does **not**:

- score luck quality
- mark favorable / unfavorable years
- adjust Useful God
- interpret or report

Runtime Dayun/Liunian providers already in `engines/luck_engine/` remain unchanged. They are calendar conversion helpers. LE-1 adds the **canonical contract** those and future packages must publish into.

---

## Timeline hierarchy

```
Natal Chart
    ↓
Major Luck Cycle (Đại Vận)     active
    ↓
Annual Luck (Lưu Niên)         active
    ↓
Monthly Luck (Lưu Nguyệt)      active
    ↓
Daily Luck (Lưu Nhật)          reserved
    ↓
Hourly Luck (Lưu Thời)         reserved
```

Parent references are optional on a period only when that period is not nested. When `parent_period_id` is set, it MUST exist on the parent layer.

---

## Timeline contracts

Published outputs (`timeline_version` 1.0.0):

| Output | Meaning |
|--------|---------|
| `natal_chart` | Natal identity |
| `major_cycles` | Đại Vận slots |
| `annual_cycles` | Lưu Niên slots |
| `monthly_cycles` | Lưu Nguyệt slots |
| `timeline_metadata` | ids, reserved layers, events |
| `timeline_version` | `1.0.0` |

Engine contracts:

| Type | Role |
|------|------|
| `LuckTimeline` | Published timeline |
| `LuckCycle` | Ordered periods on one layer |
| `LuckPeriod` | One contiguous slot |
| `LuckEvent` | Boundary marker only |
| `contracts.LuckContext` | Timeline context (not runtime `context.LuckContext`) |
| `LuckResult` | Reserved — status always `reserved` |

Forbidden on the timeline: `score`, `quality`, `favorable`, `unfavorable`, `useful_god`, `judgment`, `interpretation`, `fortune`.

---

## Future extension strategy

Extend Foundation. Do not modify Foundation 1.0.0 or this timeline version in place.

| Future work | Lands as |
|-------------|----------|
| Luck Analysis packages | New `package_id`s consuming this timeline |
| Luck Decision packages | New decision packages; AX-3 reserved luck stages stay inactive until a Foundation bump |
| Daily / Hourly activation | New timeline minor/major + registry status change |
| AI explainers | Consume `LuckTimeline` + traces; do not bypass construction |

---

## Integration with Analysis Pipeline (AX-2)

AX-2 canonical order already reserves `luck_cycle` as **inactive**.

LE-1 does **not** enable that stage and does **not** edit Analysis Engine.

When a later sprint activates Luck Analysis:

1. Consume Canonical Analysis Result published fields only.
2. Consume `LuckTimeline` published outputs.
3. Do not recompute Strength / Pattern / Useful God.

---

## Integration with Decision Pipeline (AX-3)

AX-3 already reserves `luck_cycle`, `annual_luck`, `monthly_luck` as **inactive**.

LE-1 does **not** enable those stages and does **not** edit Decision Engine.

Future Luck Decision packages:

- consume `final_useful_god` and related Decision published fields
- consume `LuckTimeline`
- do not rewrite Useful God Foundation / Priority / Override sealed packages

---

## Future Luck Analysis

Later packages may attach quality or support/attack **as new published names**. They MUST NOT mutate `LuckTimeline` field meanings.

---

## Future Luck Decision

Later decision packages may resolve luck usefulness relative to frozen Useful God. They follow AX-3 extension rules: new package ids, optional Foundation catalog bump to activate reserved stages.
