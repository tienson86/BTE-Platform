# CONSULTING LANGUAGE PACK

# 07_REVIEW_CHECKLIST.md

Document ID: LANG-PACK-07

Version: 0.1.0-skeleton

Status: DRAFT

---

# 1. Purpose

Checklist trước khi một Language Entry được Product Owner đánh `approved` / `frozen`.

LANG-01 entries are `placeholder`. This checklist is not yet applied to commercial copy.

---

# 2. Semantic Fidelity

- [ ] Wording matches `language_key` / `semantic_state`
- [ ] Wording does not upgrade mixed → supportive
- [ ] Wording does not invent a Decision the Assessment did not make
- [ ] Traceable to `language_key`
- [ ] Supporting facts have `source_fact` identities

---

# 3. Vietnamese Quality

- [ ] Natural Vietnamese
- [ ] Verdict first
- [ ] Short enough for 30-second reading
- [ ] No repetitive openers (`Hai người...` on every line)
- [ ] No generic labels (`có điểm hỗ trợ`, `cấu trúc cho thấy`)

---

# 4. Jargon

- [ ] No unexplained Bát Tự jargon in headline
- [ ] Technical terms only with customer meaning
- [ ] `plain_customer_text` and `technical_explanation` are separate

---

# 5. Safety

- [ ] No deterministic marriage claims
- [ ] No fear language
- [ ] No forbidden patterns (ly hôn chắc chắn, vô sinh, đại hung, khắc chết, không nên cưới, ngoại tình)
- [ ] No fertility / child-count / gender prediction
- [ ] No invented advice (that is Recommendation)
- [ ] No invented score or percentage

---

# 6. Surfaces

- [ ] Assessment Card wording does not copy-paste into Recommendation
- [ ] Detailed Analysis is not required to understand the card
- [ ] Customer can understand without Bát Tự knowledge

---

# 7. Versioning

- [ ] `entry.version` bumped if wording meaning/behavior changed
- [ ] `catalog_version` bumped if the key set changed
- [ ] Previous frozen wording not silently replaced

---

# 8. Approval Gate

- [ ] Product Owner authored or signed the Vietnamese copy
- [ ] Status moved `placeholder` → `draft` → `approved`
- [ ] Frozen only after approved
- [ ] LANG-01 must not mark entries `frozen`

Cursor cannot self-approve commercial wording.
