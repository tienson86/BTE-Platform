# N-IMP-05 Sentence Library Runtime Audit

Sprint: N-IMP-05
Module: engines/narrative_v2/rewrite

## Verdict

**SENTENCE LIBRARY RUNTIME GAP**

Narrative V2 Rewrite does not select runtime sentences from an approved
library keyed to N-IMP-03 semantic keys. No library was invented.

---

## What the specification defines

`knowledge/narrative_v2/10_SENTENCE_LIBRARY.md` defines architecture:

Meaning → approved sentence units → Builder selects, does not author.

`knowledge/narrative_v2/13_COMMERCIAL_REWRITE_ENGINE.md` requires
Sentence Selection after Language Standard. If a step is unknown: do
not publish, do not guess.

---

## What approved sentence assets exist

| Path | Status | Why not used |
|------|--------|----------------|
| `knowledge/narrative_v2/10_SENTENCE_LIBRARY.md` | Specification only | No sentence records |
| `knowledge/packages/sentence_library/core/sentences/*.json` | Package `released` / sentence `official` | Texts are meta candidates (`Câu ứng viên chỉ nêu trạng thái đã công bố...`), placeholders `{{analysis.strength_score}}`, not customer units keyed to `core.pattern_context` |
| `engines/interpretation_engine/knowledge/07_sentence_library/` | Legacy interpretation library | Pack-adjacent / interpretation engine. Not Narrative V2 semantic_key. Forbidden as Pack05-adjacent prose source |
| `knowledge/sentence_library/**` | Templates / INDEX | Not runtime customer sentences |
| `engines/narrative_engine/sentence_library_loader.py` | Pack05 loader | Must not be read |

---

## What is specification-only

- Sentence category / variant decision tree
- Grammar assembly (conversation)
- Template assembly (full Narrative)

N-IMP-05 implements the selector **interface** (`SentenceSelector.select`
always returns `None`) and records the gap.

---

## What is missing

- Approved customer sentences keyed to Narrative V2 `semantic_key`
- Approved aliases from KnowledgeItem → sentence_id
- Variant selection without random / LLM
- A library whose `text` is customer language rather than library-meta description

---

## What was NOT invented

- No new sentence JSON catalog
- No hidden map `strong → "Bạn có nội lực tốt."`
- No Hỏa → màu đỏ sentences
- No luck-quality sentences for Ất Tỵ

Rewrite uses only:

1. `customer_meaning_candidate` when present (none on CASE-0001)
2. approved `positive_meaning` from the traced knowledge source file
3. otherwise UNRESOLVED
