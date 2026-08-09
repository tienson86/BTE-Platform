# Report to UI Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Purpose

Map Canonical Report surfaces onto UI Contract fields.

Detail tables live in `mapping/`. This file is the index and the ownership law.

---

## 2. Source precedence

For each `report.*` content path:

```
1. CanonicalReportResult.presentation.{path without report.}
2. Else null
```

Structural/page state may additionally read:

```
CanonicalReportResult.success
CanonicalReportResult.errors
layout_result.success
layout_result.sections[].status
layout_result.blocks[].block_type / status
canonical_report_artifact.{metadata fields only}
```

No other sources.

---

## 3. Section index

| PX-1 section | Mapping file | Report root | UI owner |
|--------------|--------------|-------------|----------|
| Hero | `mapping/hero_mapping.md` | `report.identity` | Hero |
| Tóm tắt tư vấn | `mapping/summary_mapping.md` | `report.summary` | ExecutiveSummary |
| Định hướng chính | `mapping/recommendation_mapping.md` | `report.recommendations[]` | Recommendation |
| Lưu ý quan trọng | `mapping/warning_mapping.md` | `report.warnings[]` | ImportantWarnings |
| Five domains | `mapping/domain_mapping.md` | `report.domains.*` | DomainSection |
| Biểu đồ minh họa | `mapping/chart_mapping.md` | `report.charts[]` | Charts |
| Chi tiết kỹ thuật | `mapping/technical_mapping.md` | `report.technical` + artifact metadata | TechnicalInfo |
| Kiến thức bổ sung | `mapping/knowledge_mapping.md` | `report.knowledge[]` | Knowledge |
| Phụ lục | `mapping/appendix_mapping.md` | `report.appendix` | Appendix |

---

## 4. Layout module → section (routing only)

Layout `module_id` is **not** a UI title. Adapter may use it only to test emptiness.

| module_id | May inform |
|-----------|------------|
| `cover` | Hero availability (not copy) |
| `summary` / `overview` | Summary availability |
| `decision` | Recommendation / warning availability |
| `luck` | Domain luck availability |
| `chart` | Chart availability |
| `analysis` | Technical / analysis preview availability |
| `interpretation` | Knowledge / domain depth availability |
| `appendix` | Appendix availability |

PX-1 reading order **overrides** layout module order for render sequence (`RENDERING_PRIORITY.md`).

---

## 5. Ownership

| Report path | Sole UI owner |
|-------------|----------------|
| `report.identity.*` | Hero |
| `report.summary.*` | ExecutiveSummary |
| `report.recommendations[]` | Recommendation |
| `report.warnings[]` | ImportantWarnings |
| `report.domains.{key}.*` | that DomainSection |
| `report.charts[]` | Charts |
| `report.technical.*` | TechnicalInfo |
| `report.knowledge[]` | Knowledge |
| `report.appendix.*` | Appendix |
| `report.cta.*` | Recommendation region (CTA) |
| `report.page.*` | ResultPage |

Domain sections **reference** recommendation ids; they do not re-own rec text.

---

## 6. Stop line

One path. One owner. Null if unpublished.

END
