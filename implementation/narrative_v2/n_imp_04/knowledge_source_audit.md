# N-IMP-04 Knowledge Source Audit

Sprint: N-IMP-04
Module: engines/narrative_v2/knowledge
Mode: Shadow Mode

Approval is taken only from explicit `metadata.status` on the source record.
Filename and directory are not treated as approval.

---

## Classification legend

| Status | Meaning |
|--------|---------|
| APPROVED_CANONICAL | Narrative V2 / CK architecture that defines the layer, not entity content |
| APPROVED_DOMAIN | KnowledgeEntity JSON with `metadata.status = approved` |
| LEGACY | Older narrative/package reasoning that is not this resolver's source |
| TECHNICAL_ONLY | Schema, reports, loader contracts — not customer meaning |
| DRAFT | `metadata.status` is draft/review/deprecated |
| UNSUITABLE | Customer UI prose, Pack05, Portal, invented rewrite |

---

## Sources considered

| Path | Approval status | Version | Domain | Fields usable | Fields rejected | Used | Reason |
|------|-----------------|---------|--------|---------------|-----------------|------|--------|
| `knowledge/interpretation/domains/strength/*.json` | APPROVED_DOMAIN (`metadata.status=approved`) | 1.0.0 | Strength | `id`, `key`, `meaning`, warnings/contraindications as boundaries, recommendation `action` copies | `applications` (career/relationship outcomes) | YES | Exact key match from `evidence.strength.level` |
| `knowledge/interpretation/domains/pattern/*.json` | APPROVED_DOMAIN | 1.0.0 | Pattern | same as above | `applications` | YES | Exact key match from `evidence.pattern.primary` |
| `knowledge/interpretation/domains/useful_god/*.json` | APPROVED_DOMAIN | 1.0.0 | UsefulGod | same as above | `applications` | YES | Exact key match from `evidence.useful_god.primary` |
| `knowledge/interpretation/domains/ten_gods/*.json` | APPROVED_DOMAIN | 1.0.0 | TenGods | same as above | `applications` | YES | Exact key match from `evidence.ten_gods.visible_labels` |
| `knowledge/interpretation/domains/shensha/*.json` | APPROVED_DOMAIN (`status=approved`; coverage label Expert Ready is quality, not a substitute token) | 1.0.0 | ShenSha | `meaning`, contraindications as boundaries | `applications.relationships`, romance/career inference | YES | Exact name match from `evidence.shensha.names` |
| `knowledge/interpretation/domains/temperature/` | — | — | Temperature | none | — | NO | Domain has 0 entities (`KNOWLEDGE_STATUS.md`) |
| `knowledge/interpretation/domains/luck/` | — | — | Luck | none | — | NO | Domain has 0 entities |
| `knowledge/interpretation/concepts/core/warming_cold_chart.json` | APPROVED_DOMAIN (concept) | 1.0.0 | Concept | `id`, `meaning` | prose `conditions` | NO | No exact key: evidence is `warming`/`cold`, concept id is `warming_cold_chart`. Guessing forbidden. |
| `knowledge/interpretation/concepts/**` | APPROVED_DOMAIN (concept layer) | 1.0.0 | Concept | — | — | NO | Not keyed to N-IMP-03 semantic keys |
| `knowledge/interpretation/schemas/*.json` | TECHNICAL_ONLY | — | — | schema only | all meaning fields | NO | Not knowledge content |
| `knowledge/interpretation/reports/*.json` | TECHNICAL_ONLY | — | — | coverage counts | — | NO | Missing entity `id`/`key`/`metadata.status` contract |
| `knowledge/interpretation/KNOWLEDGE_STATUS.md` | APPROVED_CANONICAL | — | inventory | domain inventory | — | YES (audit only) | Documents Temperature/Luck = 0 |
| `knowledge/interpretation/interaction/*.md` | APPROVED_CANONICAL | — | Interaction Truth | relation facts | customer prose | NO | Wrong layer (facts, not meaning catalog) |
| `knowledge/consulting_knowledge/*.md` | APPROVED_CANONICAL (CK-01 freeze docs) | CK-01 | commercial | architecture | customer wording / actions | NO | No per-item `metadata.status` JSON. Indexing would become Action Plan. |
| `knowledge/architecture/ck_01_consulting_knowledge/*` | APPROVED_CANONICAL | 1.0.0 | commercial | catalog shape | matching/runtime | NO | Matching runtime is not N-IMP-04. Do not compose actions. |
| `engines/consulting_knowledge/` | TECHNICAL_ONLY / LEGACY runtime | — | commercial | catalog loader | compose | NO | Would merge consulting into narrative. Forbidden this sprint. |
| `knowledge/commercial_dashboard/**` | UNSUITABLE | — | UI | — | all Dashboard copy | NO | Presentation, not knowledge |
| `engines/narrative_engine` (Pack05) | LEGACY / UNSUITABLE | — | narrative | — | customer prose | NO | Forbidden as knowledge source |
| `knowledge/packages/*/reasoning/*` | LEGACY | — | package graphs | — | pedagogical sentences | NO | Different relation vocabulary |
| Portal / report HTML / frontend adapters | UNSUITABLE | — | UI | — | all | NO | Out of scope |
| Narrative V2 semantic_key catalogs | — | — | — | — | — | NO | No files exist keyed to `core.pattern_context` etc. Honest parent-entity match used instead. |

---

## Matching actually used

Priority applied:

1. Exact `semantic_key` on the knowledge record — none published for N-IMP-03 keys
2. Documented alias (`id` suffix ↔ `key` on the same approved record)
3. Documented parent/related entity: reasoning semantic scope → evidence value → `(domain, key)` exact lookup
4. UNRESOLVED

No embeddings. No LLM. No approximate text matching.

---

## Draft inventory

No domain JSON in `knowledge/interpretation/domains/` currently has `metadata.status = draft`.
Draft rejection is enforced by the loader (skip) and by `KnowledgeValidator` (fail if a draft item is injected).
