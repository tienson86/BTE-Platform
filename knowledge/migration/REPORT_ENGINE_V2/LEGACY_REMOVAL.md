# LEGACY REMOVAL — Customer PDF path

Date: 2026-08-13

---

## Removed from the customer PDF

The production export no longer renders:

- Four pillars / hidden stems / nạp âm / trường sinh tables
- Five-element score table
- Strength score / level / seasonal / root rows
- Ten Gods raw lists
- Pattern / follow-pattern / confidence
- Useful God / favorable / unfavorable / temperature
- Shen Sha evidence table
- Đại vận cycle table and runtime-gap notes
- Empty wealth / marriage / health / children placeholders
- Domain chapters titled `Luận giải {domain}`
- Hide-markers (`CAREER_REPORT_HIDDEN_BY_PRODUCT_CONTEXT`, `*_NOT_AVAILABLE`)
- Engine footer (`Report V1 · engine_version`)
- Template filler and rule IDs

Technical rows move to **Advisor Appendix only** (`PACKAGE_D`, `reader_role=CONSULTANT`, or `options.advisor_mode`).

---

## What stayed (intentionally)

| Item | Why |
|------|-----|
| `report_sections_v1.py` | Existing Report Engine V1 tests still assert 17 headings |
| `ReportExportServiceV1` | Public API wrapper — not the production customer path |
| `build_report_input_v1` | Stage `report_input_v1` kept for pipeline diagnostics |
| `_enrich_report_with_composition` | Compatibility method; **not called** for customer PDF |
| Domain composers | Still feed CDR / features — not printed to customer |

---

## Leak filter (customer render)

`engines/report_engine/commercial/leak_filter.py` drops paragraphs containing:

- Rule / claim / theme raw IDs
- Engine dump titles
- Hide markers
- “Áp dụng bảng trạng thái”, “Tính cách phản ánh”, “Kích hoạt” + rule/engine
- `strength_score`, `runtime`, `ExecutiveClaimPlan`, `ba engine`

Hidden features are omitted as chapters — they are not printed as error strings.

---

## Customer body source after removal

| Chapter | Source |
|---------|--------|
| Identity | `delivery.identity` (Identity Feature + CLL, or parent development rewrite) |
| Career | `delivery.career` (Career Feature + CLL) — omitted if Product Context hides |
| Executive | `delivery.executive` (Executive Consulting + CLL, or parent executive) |

No engine output is copied into those chapters.

END
