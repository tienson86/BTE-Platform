# BTE Platform — Rule Authoring Standard

| Field | Value |
|-------|-------|
| **Governance version** | 1.0 |
| **Last updated** | 2026-07-27 |
| **Applies to** | `database/` CSV rules, interpretation conditions, score rule tables |

---

## Purpose

Standards for writing, naming, and validating executable rules. Rules are **data** — authors write CSV; engines match via loaders.

---

## General principles

1. **One rule, one intent** — each row expresses a single interpretive or scoring proposition.
2. **Commercial prose separate from logic** — `condition` column is logic; title/body columns are customer-facing Vietnamese.
3. **No internal codes in customer text** — no `FPR`, `rule_id`, or debug tokens in fields that reach Portal (interpretation `portal_view` sanitizes, but authors must not rely on it).
4. **Database first** — do not encode the same rule in Python.
5. **Stable IDs** — never change `rule_id` meaning; add new row instead.

---

## Naming

### Files

| Rule | Example |
|------|---------|
| Vietnamese concept, no diacritics | `career_rules.csv`, `strength_levels.csv` |
| snake_case | `useful_god_rules.csv` |
| One purpose per file | `pattern_priority.csv` not mixed with strength |
| Folder numbering | `15_score_engine/03_strength/` |

### Columns

- snake_case
- Vietnamese headers allowed in legacy files — prefer stable English snake_case for new files
- Document columns in folder `README.md` or `ghi_chu.md`

### rule_id

| Rule | Standard |
|------|----------|
| Unique globally within rule family | Prefix + numeric: `CA001`, `WR012`, `FPR045` |
| Prefix indicates family | `CA` = career, `WR` = wealth, etc. |
| Never reuse | Retired IDs stay reserved — see retirement |
| Case | Uppercase prefix + digits recommended |

### Categories and sections

Interpretation output maps to **section** keys consumed by Portal:

`summary`, `personality`, `career`, `wealth`, `relationship`, `health`, `useful_god`, `luck`, `pattern`, `conclusion`, `warning`, `strength`, `weakness`, etc.

Rule files should document which section(s) they populate.

---

## Priority

| Field | Usage |
|-------|--------|
| `priority` | Integer; higher = more important when multiple rules match |
| Scale | Document per module (common: 0–100) |
| Score submodules | Separate `*_priority.csv` where applicable |

**Authoring rules:**

- Default priority for generic rules: 50–70
- Critical warnings: 90+
- Background context: 20–40
- When two rules conflict, adjust priority — do not duplicate prose

**Resolution:** Engine priority resolver — not CSV row order.

---

## Conditions

Conditions express when a rule applies. They reference **RuleContext signals** (bazi, pattern, score, strength, etc.).

### Syntax (interpretation rules)

- Boolean expressions: `AND`, `OR`, `NOT`
- Comparisons: `>`, `<`, `=`, `>=`, `<=`
- Signal names: engine-defined (e.g. `that_sat>0`, `chinh_quan>0`, `kim_vuong=true`)

### Authoring rules

| Rule | Requirement |
|------|-------------|
| Testable | Condition must be evaluable from RuleContext |
| No free text in condition | Conditions are logic, not prose |
| Document signals | New signals require engine/RuleContext support — not author-only |
| Avoid overly broad | `true` as sole condition — only for intentional catch-all with low priority |

### Exceptions

- Use explicit negative conditions rather than implicit overlap
- Document exception rules in file header: "Applies only when pattern X absent"
- Higher-priority specific rules should override broad rules

---

## Content fields (interpretation CSV example)

Typical columns (family-specific):

| Column | Purpose |
|--------|---------|
| `rule_id` | Identifier |
| `condition` | Match logic |
| `title` | Short commercial heading (optional) |
| `ability`, `recommendation`, `risk`, … | Section body building blocks |
| `score` | Rule-level weight for interpretation scoring |

**Prose standards:**

- Vietnamese commercial tone
- Complete sentences
- No English debug fragments
- Align with `knowledge_base/` style guides for feng shui / domain terms

---

## Examples

### Good — career rule row

```csv
rule_id,career_type,condition,title,...,score
CA001,Lãnh đạo,that_sat>0 AND chinh_quan>0,Năng lực lãnh đạo,...,90
```

- Unique `CA001`
- Clear condition referencing signals
- Commercial Vietnamese in content columns
- Priority via score column + engine resolution

### Bad — do not

| Anti-pattern | Why |
|--------------|-----|
| Reuse `CA001` for different logic | Breaks audit and golden cases |
| `condition: "good career"` | Not evaluable logic |
| `recommendation: "See FPR012"` | Internal code in customer text |
| Duplicate row same prose, different id | Redundant — merge or differentiate conditions |
| Empty `condition` on high-priority rule | Unintended global match |

### Sentence library (JSON)

Follow `sentence_schema.json`:

```json
{
  "sentence_id": "career_012",
  "module": "07_career",
  "category": "opportunity",
  "priority": 75,
  "tone": "neutral",
  "text": "Commercial Vietnamese sentence here."
}
```

---

## Validation

Before merge, authors must verify:

| Check | Method |
|-------|--------|
| Unique `rule_id` | Script or `DATA_QUALITY_STANDARD.md` checklist |
| No empty required columns | CSV lint |
| Valid condition syntax | Interpretation module tests / loader dry-run |
| Enum references exist | Cross-check signal names with RuleContext docs |
| UTF-8 encoding | No mojibake in Vietnamese |
| No duplicate prose | Dedup review for near-identical `recommendation` text |

**Automated:**

- Engine loader unit tests (`pytest engines/interpretation_engine/tests -q`)
- Interpretation module tests (`pytest tests/interpretation -q` if present)
- Production smoke when output materially changes

**Manual:**

- Domain reviewer reads commercial prose
- Critical case 1987-01-21 remains valid for calendar/bazi changes

---

## Retirement

To retire a rule:

1. Add changelog entry with `rule_id` and reason
2. Option A: Remove row (patch) — only if never shipped to production
3. Option B: Set `status=deprecated` in metadata or move to `archive/` folder (minor)
4. Do not reuse `rule_id` for 12 months minimum

---

## Related documents

- [DATA_QUALITY_STANDARD.md](DATA_QUALITY_STANDARD.md)
- [KNOWLEDGE_REVIEW_PROCESS.md](KNOWLEDGE_REVIEW_PROCESS.md)
- [KNOWLEDGE_ARCHITECTURE.md](KNOWLEDGE_ARCHITECTURE.md)
- `.cursor/rules/database.mdc` — platform database rules

---

**BTE Rule Authoring Standard — 1.0 — 2026-07-27**
