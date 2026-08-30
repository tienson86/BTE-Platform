# Sentence Asset Audit

Sprint: N-IMP-07C
Library version: `1.0.0`
Locale: `vi`
Audience: `customer`
Mode: Shadow

## Loader

`engines.narrative_v2.language.SentenceRegistry`

Root: `knowledge/narrative_v2/runtime_assets/vi/sentence_library/`

## Status model

| Status | Customer-eligible |
| --- | --- |
| draft | no |
| review | no |
| approved | yes |
| deprecated | no |

## Loaded assets

| sentence_id | status | domain | meaning_key | selected at runtime |
| --- | --- | --- | --- | --- |
| sentence.pattern.chinh_an.meaning.001 | approved | pattern | knowledge.pattern.chinh_an | yes |
| sentence.pattern.chinh_an.meaning.draft | draft | pattern | knowledge.pattern.chinh_an | no |
| sentence.strength.strong.meaning.001 | approved | strength | knowledge.strength.strong | yes |
| sentence.shensha.hong_loan.meaning.001 | approved | shensha | knowledge.shensha.hong_loan | yes |
| sentence.shensha.thien_at_quy_nhan.meaning.001 | approved | shensha | knowledge.shensha.thien_at_quy_nhan | yes |
| sentence.ten_gods.kiep_tai.meaning.001 | approved | ten_gods | knowledge.ten_gods.kiep_tai | yes |
| sentence.ten_gods.that_sat.meaning.001 | approved | ten_gods | knowledge.ten_gods.that_sat | yes |
| sentence.ten_gods.thien_an.meaning.001 | approved | ten_gods | knowledge.ten_gods.thien_an | yes |

## Not authored (by design)

| Target | Reason |
| --- | --- |
| useful_god | upstream Meaning not customer-safe / unresolved |
| temperature | knowledge unresolved |
| luck | knowledge unresolved |
| nguyet_duc_quy_nhan | lookup-only consultant jargon; no customer Meaning to map |
| thien_duc_quy_nhan | lookup-only consultant jargon; no customer Meaning to map |
| nhat_chu | axis/lookup Meaning; would leak Nhật chủ if expanded |
| Action category | N-IMP-08 |

## Validator

`SentenceAssetValidator` rejects missing semantic key, missing Knowledge trace, Action category, prediction, forbidden claims, engine leak, and consultant shorthand in approved text.

Draft assets are loaded for audit and never selected.
