# Classical Knowledge Base (Epic 03)

Version: **0.1.0** (schema foundation)

Path: `database/20_knowledge/`

This folder holds the **classical BaZi knowledge corpus** used by the future Knowledge & AI Expert layer.

It is **not** a calculation rule database.

- Calculation engines continue to use `database/11_temperature` … `15_score_engine` and related folders.
- Interpretation engines continue to use `database/interpretation_rules/`.
- This corpus stores explainable classical / modern knowledge entries for retrieval and citation.

**Milestone 01 status:** standardized schema only. Content rows will be added in later milestones.

---

## Files

| File | Topic |
|------|--------|
| `01_five_elements.csv` | Ngũ hành |
| `02_yin_yang.csv` | Âm dương |
| `03_ten_gods.csv` | Thập thần |
| `04_hidden_stems.csv` | Tàng can |
| `05_growth_stage.csv` | Trường sinh / twelve stages |
| `06_nayin.csv` | Nạp âm |
| `07_patterns.csv` | Cách cục |
| `08_useful_god.csv` | Dụng thần / Hỷ / Kỵ |
| `09_strength.csv` | Thân vượng / nhược |
| `10_temperature.csv` | Hàn / nhiệt / táo / thấp |
| `11_shensha.csv` | Thần sát |
| `12_career.csv` | Sự nghiệp |
| `13_wealth.csv` | Tài vận |
| `14_marriage.csv` | Hôn nhân |
| `15_children.csv` | Con cái |
| `16_health.csv` | Sức khỏe |
| `17_parents.csv` | Cha mẹ |
| `18_luck_cycles.csv` | Đại vận / lưu niên |
| `19_feng_shui.csv` | Phong thủy gợi ý |
| `20_glossary.csv` | Thuật ngữ |

Supporting docs:

| File | Purpose |
|------|---------|
| `README.md` | This document |
| `CHANGELOG.md` | Version history |
| `COVERAGE.md` | Coverage report (row counts / readiness) |

---

## Schema

Every CSV uses the same header (column order is stable — do not reorder):

```text
id,topic,keyword,condition,classical_text,modern_interpretation,priority,confidence,reference
```

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Stable knowledge entry id (e.g. `KNW-FE-001`) |
| `topic` | string | Domain topic label (Vietnamese or English key) |
| `keyword` | string | Retrieval keywords (semicolon- or pipe-separated allowed) |
| `condition` | string | When this entry applies (signal / RuleContext-oriented condition text) |
| `classical_text` | string | Classical quotation or paraphrase |
| `modern_interpretation` | string | Modern consultant-facing explanation |
| `priority` | int | Higher = preferred when multiple entries match |
| `confidence` | float | 0.0–1.0 knowledge confidence |
| `reference` | string | Bibliography id (`SRC-*` / `REF-*`) or classical work name |

### Conventions

- **CSV first** — one topic family per file; do not mix unrelated domains.
- **Read-only for engines** — Knowledge Expert layer reads; no engine writes here.
- **No fabricated content** — empty body until curated rows are approved.
- **References** — prefer ids from `knowledge/bibliography/` and `knowledge/references/` when available.
- **Stable schema** — add rows later; do not rename or reorder columns without a version bump.

### Suggested `id` prefixes (future content)

| File | Prefix |
|------|--------|
| `01_five_elements` | `KNW-FE-` |
| `02_yin_yang` | `KNW-YY-` |
| `03_ten_gods` | `KNW-TG-` |
| `04_hidden_stems` | `KNW-HS-` |
| `05_growth_stage` | `KNW-GS-` |
| `06_nayin` | `KNW-NY-` |
| `07_patterns` | `KNW-PT-` |
| `08_useful_god` | `KNW-UG-` |
| `09_strength` | `KNW-ST-` |
| `10_temperature` | `KNW-TP-` |
| `11_shensha` | `KNW-SS-` |
| `12_career` | `KNW-CR-` |
| `13_wealth` | `KNW-WL-` |
| `14_marriage` | `KNW-MR-` |
| `15_children` | `KNW-CH-` |
| `16_health` | `KNW-HL-` |
| `17_parents` | `KNW-PR-` |
| `18_luck_cycles` | `KNW-LC-` |
| `19_feng_shui` | `KNW-FS-` |
| `20_glossary` | `KNW-GL-` |

---

## Pipeline position

```text
RuleContext (from engines)
        ↓
Knowledge Retriever  ←  database/20_knowledge/
        ↓
Evidence + Reasoning + Prompt
        ↓
Expert Answer (future)
```

This folder does **not** feed Score / Pattern / Useful God calculation.

---

## Compatibility

- No calculation engine imports this folder in Milestone 01.
- Existing rule databases remain unchanged.
- Schema is additive and backward-compatible for future loaders.
