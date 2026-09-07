# CONSULTING LANGUAGE PACK

# 04_VARIATION_ENGINE.md

Document ID: LANG-PACK-04

Version: 0.1.0-skeleton

Status: DRAFT

---

# 1. Purpose

Variation cho phép nhiều wording đã duyệt cho cùng một semantic key.

Variation không được làm wording không tái lập.

---

# 2. Allowed

Multiple approved variants per `language_key`.

Selection inputs (all deterministic):

- `language_key`
- `question_id`
- `semantic_signature` (stable Assessment/Decision signature string)
- `catalog_version`
- `entry.version`

---

# 3. Forbidden

- `random()`
- `secrets`
- LLM
- temperature
- wall-clock
- consultation_id as a variation seed if that would change wording across replays of the same semantic input

Same semantic input + same catalog version → same selected variant.

`consultation_id` may appear in traces. It must not change the selected variant.

---

# 4. Algorithm

Implementation: `consulting/language/selector.py`

```
material = language_key + "|" + semantic_signature + "|" + catalog_version + "|" + entry.version
digest = SHA-256(material)
index = int(digest[:8], 16) % len(variants)
selected = variants[index]
```

If `variants` is empty, the entry itself is the only wording. Index = 0.

Do not shuffle. Do not fall through to another `language_key`.

---

# 5. Semantic Signature

`semantic_signature` is a canonical string of already-approved Assessment meaning, for example:

```
Q1|average|conflict=present|rescue=present
```

The signature is derived from Assessment/Decision. The selector does not invent it.

LANG-01 tests pass a fixed signature. Live Assessment does not call the selector yet.

---

# 6. Variant Record

```yaml
variants:
  - id: v1
    headline: "__PRODUCT_OWNER_WORDING_REQUIRED__"
    meaning: "__PRODUCT_OWNER_WORDING_REQUIRED__"
    status: placeholder
  - id: v2
    headline: "__PRODUCT_OWNER_WORDING_REQUIRED__"
    meaning: "__PRODUCT_OWNER_WORDING_REQUIRED__"
    status: placeholder
```

Variant ids are stable. Deleting `v1` after freeze is a breaking catalog change.

---

# 7. Replay Rule

Golden / live replay of the same Assessment semantic_key, comparison facts, and catalog version must select the same variant id.
