# N-IMP-07C APPROVED CUSTOMER LANGUAGE ASSETS REPORT

Sprint: N-IMP-07C
Module: `engines.narrative_v2.language`
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Runtime Sentence Library is an asset/service under Commercial Communication. CASE-0001 consulting narrative now uses approved customer sentences for the primary and supporting insights. Remaining wrap units and unresolved knowledge are reported, not invented.

---

## 2. Architectural role

```
Approved Knowledge
        ↓
Meaning
        ↓
Customer Language Assets
        ↓
Commercial Rewrite
        ↓
Conversation
        ↓
Consulting Style
```

Not a new top-level Engine.

---

## 3. Language asset architecture

Package `engines/narrative_v2/language/` loads JSON assets from `knowledge/narrative_v2/runtime_assets/vi/sentence_library/`.

`SentenceSelector` never generates prose. Missing match → `None`. Rewrite falls back to the existing Bạn-wrap.

---

## 4. Files created

```
engines/narrative_v2/language/__init__.py
engines/narrative_v2/language/sentence_asset.py
engines/narrative_v2/language/sentence_library.py
engines/narrative_v2/language/sentence_registry.py
engines/narrative_v2/language/sentence_selector.py
engines/narrative_v2/language/sentence_validator.py
engines/narrative_v2/language/semantic_mapping.py
engines/narrative_v2/language/language_asset_status.py
engines/narrative_v2/language/language_errors.py
knowledge/narrative_v2/runtime_assets/vi/sentence_library/manifest.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/pattern/chinh_an.meaning.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/pattern/chinh_an.meaning.draft.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/strength/strong.meaning.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/shensha/hong_loan.meaning.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/shensha/thien_at_quy_nhan.meaning.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/ten_gods/kiep_tai.meaning.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/ten_gods/that_sat.meaning.json
knowledge/narrative_v2/runtime_assets/vi/sentence_library/ten_gods/thien_an.meaning.json
tests/narrative_v2/test_language_assets.py
implementation/narrative_v2/n_imp_07c/sentence_asset_audit.md
implementation/narrative_v2/n_imp_07c/case0001_language_assets.md
implementation/narrative_v2/n_imp_07c/case0001_semantic_equivalence.md
implementation/narrative_v2/n_imp_07c/case0001_before_after.md
implementation/narrative_v2/n_imp_07c/case0001_language_trace.json
implementation/narrative_v2/n_imp_07c/language_asset_contract_gaps.md
implementation/narrative_v2/N_IMP_07C_REPORT.md
```

---

## 5. Files modified

```
engines/narrative_v2/rewrite/sentence_selector.py
engines/narrative_v2/rewrite/rewrite_engine.py
engines/narrative_v2/rewrite/rewrite_validator.py
engines/narrative_v2/interpretation/interpretation_builder.py
engines/narrative_v2/summary/summary_builder.py
engines/narrative_v2/communication/communication_engine.py
tests/narrative_v2/test_rewrite_engine.py
tests/narrative_v2/test_rewrite_context.py
tests/narrative_v2/test_interpretation_builder.py
tests/narrative_v2/test_consulting_style.py
tests/narrative_v2/test_consulting_semantics.py
```

Existing tests that encoded the N-IMP-05/07B “library missing / shorthand present” contract were updated to the 07C contract. Meaning fields remain on rewrite items.

---

## 6. SentenceAsset contract

Fields: sentence_id, semantic_key, domain, category, meaning_key, text, locale, audience, style, status, priority, source_knowledge_ids, references, version, metadata.

Runtime customer use requires `status=approved`.

---

## 7. Asset status model

draft / review / approved / deprecated

Only `approved` is customer-eligible.

---

## 8. Asset versioning

`sentence_library_version = 1.0.0`

Each asset carries `version`. Source knowledge version is not faked.

---

## 9. Initial asset scope

Golden set for CASE-0001 approved Meanings only:

- strength.strong
- pattern.chinh_an
- approved ShenSha hong_loan, thien_at_quy_nhan
- approved Ten Gods kiep_tai, that_sat, thien_an

Useful God / Temperature / Luck not authored.

---

## 10. Approved assets created

7 approved meaning assets. 1 draft (must not resolve).

---

## 11. Source Knowledge traceability

Every approved asset traces:

SentenceAsset → approved Meaning → KnowledgeItem id → source_path JSON.

Rewrite items keep `source_meaning` as the approved knowledge text.

---

## 12. Semantic equivalence review

See `n_imp_07c/case0001_semantic_equivalence.md`.

6 NONE. 1 REVIEW (kiep_tai “bứt phá”). 0 FAIL in approved runtime. Draft FAIL wording does not resolve.

---

## 13. Sentence selection strategy

Exact match only, deterministic order:

semantic_key → category → domain → locale → audience → approved → priority → sentence_id

No fuzzy match. No generation.

---

## 14. Rewrite integration

`rewrite.SentenceSelector.select(...)` → `SentenceAsset | None`.

On hit: `customer_language = asset.text`, metadata `sentence_source=sentence_library`.

On miss: existing Bạn-wrap, `sentence_source=address_wrap`.

Library-backed items skip substring preservation of consultant shorthand. Source Meaning remains on the item.

CASE-0001 rewrite coverage: `partial` (7 library / 3 wrap / 3 unresolved).

---

## 15. Conversation integration

Conversation Composer unchanged semantically. It consumes the new rewrite wording. Duplicate closing still merged.

07C conversation flow:

Bạn thường làm việc tốt hơn khi có chỗ dựa ổn định và khi công việc cần xây từ nền tảng. Vì vậy, Bạn thường duy trì được sự ổn định tốt khi theo đuổi những việc cần thời gian và sự bền bỉ. Từ đó, Bạn cũng phù hợp với việc học có hệ thống và cần thời gian để ngấm dần. Đồng thời, Điều này hữu ích khi bạn có lối để thể hiện năng lực và khi giới hạn được giữ rõ.

---

## 16. Consulting Style integration

Consulting Style frames unchanged. Better input changed frame selection (meaning now `Ở mặt tích cực`, recommendation now `Điều đáng chú ý là`) because shorthand/gap classifiers no longer fire on the assembled insight.

Status: `styled`. Fluency / register / technical_density: pass. Meaning fingerprint conversation = consulting.

---

## 17. CASE-0001 before

N-IMP-07 Interpretation / 07A Conversation used wrap shorthand.

N-IMP-07B Consulting:

Điểm nổi bật ở đây là bạn có chỗ dưỡng, chịu được việc cần nền. Điều này cho thấy bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền. Trong thực tế, hữu ích khi cần ủ và học có khung. Tuy nhiên, cũng cần lưu ý, hữu ích khi kênh thoát và chế được giữ phép.

---

## 18. CASE-0001 after

Điểm nổi bật ở đây là bạn thường làm việc tốt hơn khi có chỗ dựa ổn định và khi công việc cần xây từ nền tảng. Điều này cho thấy bạn thường duy trì được sự ổn định tốt khi theo đuổi những việc cần thời gian và sự bền bỉ. Ở mặt tích cực, bạn cũng phù hợp với việc học có hệ thống và cần thời gian để ngấm dần. Điều đáng chú ý là điều này hữu ích khi bạn có lối để thể hiện năng lực và khi giới hạn được giữ rõ.

---

## 19. CASE-0001 phrases improved

Removed from consulting flow: chỗ dưỡng, việc cần nền, ủ và học có khung, nền lực, chịu tải, kênh thoát, chế được giữ phép.

---

## 20. Remaining awkward phrases

Still in rewrite wrap units, not in consulting flow:

- kênh nhu can / nhãn đủ / Tra cứu quý-đức tháng
- trục rõ / đồng khí (nhat_chu)

Consulting still contains “Điều này hữu ích khi…” as approved strength wording.

---

## 21. Product quality review

| Gate | Result |
| --- | --- |
| Correctness | PASS for assembled insight |
| Clarity | PASS for consulting flow |
| Conversation | PASS |
| Professional consulting tone | PASS |
| Meaning preservation | PASS (source_meaning unchanged; conversation fingerprint = consulting fingerprint) |
| Unsupported claims | NONE |

Rewrite remains `partial` because wrap fallbacks and unresolved Useful God / Temperature / Luck are not invented away.

---

## 22. Contract gaps

See `n_imp_07c/language_asset_contract_gaps.md`.

Partial library coverage. Meaning-only categories. No Action. No Useful God / Temperature / Luck assets.

---

## 23. Tests

`py -m pytest tests/narrative_v2 -q`

257 passed.

LA1–LA20 in `tests/narrative_v2/test_language_assets.py`.

---

## 24. Determinism verification

Same CASE-0001 input → same sentence_id and same consulting flow. Selection is sorted by priority then sentence_id. No variants.

---

## 25. Shadow mode verification

`shadow_mode=true`, `replaces_pack05=false`, `portal_connected=false`. Presentation remains None. Action stage not implemented.

---

## 26. Out-of-scope confirmation

No Action Builder implemented: YES
No Presentation published: YES
No Portal integration: YES
No Pack05 replacement: YES
No astrology engine modified: YES
No new astrology Meaning invented: YES
No LLM/network used: YES
Only approved sentence assets used: YES

---

## 27. Verdict

READY FOR PRODUCT OWNER REVIEW
