# G2-FINAL — Known V1.0 limitations

These are product boundaries of the frozen Gate-2 layer. **They are not V1.0 blockers** unless already contractual.

## History persistence

- Browser-local only (`localStorage` + `sessionStorage`)
- Maximum **30** History records, newest first
- No cloud / server / database History in V1.0
- Clearing origin storage clears History
- No account synchronization of analyses

## Official PDF vs Print

- Official customer PDF = Report V1 + Playwright (`Tải PDF`)
- Browser **In** is convenience print of the selected view
- OS “Save as PDF” from Print is not the official file

## PDF searchable text

- Naive Unicode byte-grep of the `.pdf` is not authoritative (Playwright CID fonts)
- Rendered HTML source + DOCX paragraphs/tables are the inspectable text artifacts
- This matches the G2-04 / G2-06 accepted baseline (`pdf_searchable: false` on raw-byte grep)

## Hỷ / Kỵ

- Customer Hỷ follows HK-R1H (`favorable_display`)
- Deeper independent Hỷ/Kỵ chart reconciliation is deferred to V1.1
- Authoritative backlog: `release/gate_01/G1_FINAL_V1_1_BACKLOG.md` and `release/gate_01/HK_V1.1_RECONCILIATION_BACKLOG.md`

## Narrative

- V1.0 narrative is intentionally concise / non-deep
- Composer V2 → `pack05_narrative_result_v1` does not independently reinterpret analytics
- Enhanced narrative is V1.1+

## Five Elements / Score presentation

- Customer “Phân bố Ngũ hành” is structural occurrence only (not vượng/suy / Useful God score)
- Strength card (“Điểm thân” in G2-02) is `strength.strength_score`, not Score Engine composite total
- Score Engine values remain a distinct engine output

## Special Pattern wording

- LEVEL-1 special = detected only, not fully qualified Overall override
- “Chuyên cách ưu tiên Ấn” is not used for under-qualified special structures

## Preview / legacy

- Preview fixture is allowed only with explicit preview mode
- `/result?legacy=1` is explicit legacy only

Do not treat deferred V1.1 features as Gate-2 defects.
