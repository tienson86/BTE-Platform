# BTE Quality Gate System V1.0

| Field | Value |
|-------|-------|
| Document | README |
| System | Quality Gate System V1.0 |
| Status | **OFFICIAL — Release governance** |
| Date | 2026-08-13 |
| Authority | **Only authority** for advancing a BTE release stage |

This package upgrades quality from scattered documentation into the **official release governance system**.

It does **not** modify Engines, Knowledge packs, Reasoning, Commercial Language, Production Pipeline, or Golden Dataset.

---

## Purpose

Decide, with a frozen rule, whether BTE may advance to the next release stage.

No sprint, UI wave, Knowledge QC cycle, or engineering green build may override this system.

---

## Reading order

| Order | File | Section |
|------:|------|---------|
| 1 | This README | Index |
| 2 | [QUALITY_LEVELS.md](QUALITY_LEVELS.md) | Q0–Q4 |
| 3 | [QUALITY_GATES.md](QUALITY_GATES.md) | RC0 → Commercial V1.1 + metrics + roadmap |
| 4 | [QUALITY_SCORECARD.md](QUALITY_SCORECARD.md) | Official scorecard |
| 5 | [QUALITY_BACKLOG.md](QUALITY_BACKLOG.md) | Categorized issues |
| 6 | [RELEASE_BOARD.md](RELEASE_BOARD.md) | Current readiness |
| 7 | [RELEASE_POLICY.md](RELEASE_POLICY.md) | Pass policy |
| 8 | [RC_CHECKLIST.md](RC_CHECKLIST.md) | Gate-by-gate checklist |
| 9 | [VERSION_POLICY.md](VERSION_POLICY.md) | Version / freeze rules |
| 10 | [CHANGELOG.md](CHANGELOG.md) | History |

---

## Current official state (2026-08-13)

| Axis | Level | Status |
|------|-------|--------|
| Quality | **Q1 — Measured** | MET |
| Release | **RC1** | MET |
| Next | RC2 | NOT MET |

See [RELEASE_BOARD.md](RELEASE_BOARD.md).

---

## What this system governs

| Governs | Does not govern |
|---------|-----------------|
| Advance / hold of RC0, RC1, RC2, Commercial V1, Commercial V1.1 | Engine implementation |
| Mandatory commercial metrics | Knowledge pack authoring |
| Whether a case is shippable | Golden Dataset file contents |
| Categorization of quality issues | UI Foundation / Design System |
| Freeze of quality levels | QC1–QC4 Knowledge-infrastructure scans |

Evidence sources (read-only):

- `knowledge/validation/GOLDEN_DATASET_V1/`
- `knowledge/consulting_quality/`
- Existing case reviews (not rewritten here)

---

## Related systems (not release authority)

| System | Role |
|--------|------|
| Sprint 3C JSON in this folder (`quality_metrics.json`, scorecards, checklists) | Knowledge Record quality specification |
| `qc1/` `qc2/` `qc3/` `qc4/` | Knowledge-infrastructure QC cycles |
| `knowledge/roadmap/` | Delivery / UI sprint tracking |
| `knowledge/validation/GOLDEN_DATASET_V1/` | Ground-truth laboratory |

Those systems **feed evidence**. They do not declare a release.

---

END
