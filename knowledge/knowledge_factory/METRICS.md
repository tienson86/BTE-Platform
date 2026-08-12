# Metrics — V1.0

| Field | Value |
|-------|-------|
| Document | METRICS |
| Version | 1.0.0 |
| Section | 13 — Metrics |

---

# 13.1 Purpose

Official KPIs for Knowledge Factory health at pack and platform level.

---

# 13.2 Volume metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **Knowledge Units** | Total catalog units in pack | Count of unit files |
| **Topics** | Catalog topic folders | Count of catalog/* |
| **Library Chapters** | Prose source files | Count in interpretation_knowledge |

---

# 13.3 Lifecycle metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **Draft %** | Units in Draft | Draft / Total × 100 |
| **Reviewed %** | Units Reviewed | Reviewed / Total × 100 |
| **Validated %** | Units Validated | Validated / Total × 100 |
| **Frozen %** | Units Frozen | Frozen / Total × 100 |
| **Deprecated %** | Units Deprecated | Deprecated / Total × 100 |

Target before pack Freeze: **Frozen % = 100** of production scope.

---

# 13.4 Quality metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **QA Pass %** | Units PASS at last QA | PASS / QA'd × 100 |
| **QA Review %** | Units REVIEW | REVIEW / QA'd × 100 |
| **QA Fail %** | Units FAIL | FAIL / QA'd × 100 |
| **Avg QA Score** | Mean unit average | Sum(avg) / QA'd |
| **Criterion avg** | Mean per criterion | Per QA phase report |
| **Duplicate %** | Units in duplicate_cluster | Cluster members / Total × 100 |
| **Open REVIEW count** | Unresolved REVIEW | Count at gate time |

---

# 13.5 Coverage metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **Coverage %** | Topics with ≥1 Validated unit | Topics validated / Topics total × 100 |
| **Class coverage %** | Classes with MEANING + CAUSE + ADV | Classes complete / Classes total × 100 |
| **Golden coverage %** | Golden-pinned ids Validated | Pinned validated / Pinned total × 100 |
| **Source trace %** | Units with valid source_document | Traced / Total × 100 |

---

# 13.6 Process metrics

| Metric | Definition | Notes |
|--------|------------|-------|
| **Review Time** | Days from QA complete → Review sign-off | Per phase |
| **Validation Time** | Days from Review complete → Validated | Per pack |
| **Freeze Time** | Days from Validated → Frozen | Per pack |
| **Release Time** | Days from Freeze → Release | Per pack |
| **Review Cost** | Human hours per phase | Tracked manually V1.0 |
| **Re-QA rate** | Units re-QA'd / Total QA'd | Change quality indicator |

---

# 13.7 Gate metrics

| Metric | Definition |
|--------|------------|
| **QG pass rate** | Gates passed first attempt / Total gate attempts |
| **Waiver count** | Chief Reviewer waivers per pack |
| **Rollback count** | Production rollbacks per release |

---

# 13.8 PACK-01 baseline (2026-08-12)

| Metric | Value |
|--------|-------|
| Knowledge Units | 339 |
| Draft % | 100% |
| Validated % | 0% |
| Frozen % | 0% |
| QA'd units | 78 (23%) |
| QA Pass % (of QA'd) | 43% PASS (34/78) |
| QA Review % (of QA'd) | 57% REVIEW (44/78) |
| QA Fail % | 0% |
| Avg QA Score | ~8.8 (phases 01–03) |
| Duplicate clusters declared | 5 |
| Golden coverage | Not validated yet |

---

# 13.9 Reporting cadence

| Report | Owner | Frequency |
|--------|-------|-----------|
| Phase QA summary | QA Assistant | Per topic phase |
| Pack dashboard | Release Manager | Weekly during production |
| Platform rollup | Chief Reviewer | Monthly |

V1.0: manual from phase reviews and catalog index. Tooling future.

---

# 13.10 Target thresholds (guidance)

| Metric | Target at Freeze |
|--------|------------------|
| Frozen % | 100% production scope |
| QA Fail % | 0% |
| Source trace % | 100% |
| Golden coverage % | 100% pinned ids |
| Open REVIEW | 0 or waived |

---

END
