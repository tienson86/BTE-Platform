# CONSULTING LANGUAGE PACK

# 02_LANGUAGE_CATALOG.md

Document ID: LANG-PACK-02

Version: 0.1.0-skeleton

Status: DRAFT

---

# 1. Purpose

Định nghĩa Language Catalog: tổ chức file, language keys, versioning, module isolation.

---

# 2. Catalog Identity

| Token | Example | Changes when |
|---|---|---|
| `language_pack_version` | `consulting.language.pack@0.1.0-skeleton` | Loader / schema / selector behavior |
| `catalog_version` | `consulting.language.marriage@0.1.0-skeleton` | Any marriage YAML wording/key set |
| `module_language_version` | `marriage.language@0.1.0-skeleton` | TV-01 language surface |
| `entry.version` | `0.1.0` | That `language_key` wording |

Live TV-01 Narrative version remains `marriage.narrative.v1@1.1.0` until a later integration ticket.

---

# 3. Language Key System

Form:

```
{module}.{question_id}.{semantic_state}
```

Lowercase. Dot-separated. Stable. No prose inside the key.

TV-01 Marriage keys (skeleton):

## Q1 Overall Compatibility

- `marriage.q1.supportive`
- `marriage.q1.mixed`
- `marriage.q1.pressured`
- `marriage.q1.needs_adjustment`
- `marriage.q1.insufficient`

## Q2 Mutual Support

- `marriage.q2.mutual_support`
- `marriage.q2.a_supports_b`
- `marriage.q2.b_supports_a`
- `marriage.q2.asymmetric_support`
- `marriage.q2.vuong_phu`
- `marriage.q2.vuong_the`
- `marriage.q2.insufficient`

## Q3 Personality Balance

- `marriage.q3.similar_temperament`
- `marriage.q3.complementary`
- `marriage.q3.balanced`
- `marriage.q3.role_pressure`
- `marriage.q3.insufficient`

## Q4 Marriage Stability

- `marriage.q4.stable_with_rescue`
- `marriage.q4.mixed_with_conflict`
- `marriage.q4.pressured`
- `marriage.q4.stable_if_kept`
- `marriage.q4.needs_management`
- `marriage.q4.insufficient`

## Q5 Children

- `marriage.q5.insufficient`
- `marriage.q5.parenting_support`

## Q6 Overall Marriage Assessment

- `marriage.q6.can_progress`
- `marriage.q6.needs_more_review`
- `marriage.q6.high_pressure`
- `marriage.q6.good_foundation`

Keys are identities. They are not customer sentences.

---

# 4. R02 Semantic Map (seam only)

Current Assessment `semantic_key` values stay frozen.

Binding seam maps them later. LANG-01 does not change Assessment.

| R02 `semantic_key` | Language key |
|---|---|
| `very_compatible`, `quite_compatible` | `marriage.q1.supportive` |
| `average` | `marriage.q1.mixed` |
| `high_pressure` | `marriage.q1.pressured` |
| `needs_adjustment` | `marriage.q1.needs_adjustment` |
| `insufficient` (Q1) | `marriage.q1.insufficient` |
| `mutual_support` | `marriage.q2.mutual_support` |
| `similar` | `marriage.q3.similar_temperament` |
| `complementary` | `marriage.q3.complementary` |
| `balanced` | `marriage.q3.balanced` |
| `conflict` | `marriage.q3.role_pressure` |
| `stable_with_rescue` | `marriage.q4.stable_with_rescue` |
| `stable_if_kept` | `marriage.q4.stable_if_kept` |
| `needs_management` | `marriage.q4.needs_management` |
| `maintainable` | `marriage.q4.mixed_with_conflict` |
| `family_support` | `marriage.q5.parenting_support` |
| `can_proceed` | `marriage.q6.can_progress` |
| `learn_more` | `marriage.q6.needs_more_review` |
| `resolve_first` | `marriage.q6.high_pressure` |
| `good_foundation` | `marriage.q6.good_foundation` |

File: `consulting/language/bindings/marriage.py`

Not imported by `decision_pipeline` or `projector` in LANG-01.

---

# 5. File Isolation

One YAML file → one question_id.

Cross-file duplicate `language_key` is a load error.

A marriage entry must not appear in a business catalog.

---

# 6. Placeholder Policy

Catalog YAML may contain:

- schema
- keys
- empty/optional fields
- `__PRODUCT_OWNER_WORDING_REQUIRED__`
- structural slot names

Catalog YAML must not contain Cursor-invented commercial Vietnamese paragraphs.
