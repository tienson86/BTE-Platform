# Reference Coverage Report

**Module:** `knowledge/references`  
**Library version:** 1.0.0  
**Date:** 2026-07-30  

---

## 1. V1.0 library seed coverage

| Reference ID | Work | In `references.json` | In `reference_index.json` | Category |
|--------------|------|----------------------|---------------------------|----------|
| REF-000001 | Huang Di Nei Jing | Yes | Yes | classic |
| REF-000002 | Zhou Yi | Yes | Yes | classic |
| REF-000003 | Yuan Hai Zi Ping | Yes | Yes | classic |
| REF-000004 | San Ming Tong Hui | Yes | Yes | classic |
| REF-000005 | Di Tian Sui | Yes | Yes | classic |
| REF-000006 | Zi Ping Zhen Quan | Yes | Yes | classic |
| REF-000007 | Qiong Tong Bao Jian | Yes | Yes | classic |

**Coverage of required initial classics: 7 / 7 (100%).**

Not yet in V1.0 seed (legacy Markdown placeholders only): Xie Ji Bian Fang Shu, Lan Tai Miao Xuan, Shen Feng Tong Kao, Xing Ping Hui Hai, Other Classics.

---

## 2. Legacy ID remapping (critical)

`classics/INDEX.md` used a different assignment. **Authority for V1.0 is `references.json`.**

| Work | Legacy placeholder ID | V1.0 SSOT ID |
|------|----------------------|--------------|
| Huang Di Nei Jing | _(not allocated)_ | **REF-000001** |
| Zhou Yi | _(not allocated)_ | **REF-000002** |
| Yuan Hai Zi Ping | REF-000001 | **REF-000003** |
| Di Tian Sui | REF-000002 | **REF-000005** |
| San Ming Tong Hui | REF-000003 | **REF-000004** |
| Qiong Tong Bao Jian | REF-000004 | **REF-000007** |
| Zi Ping Zhen Quan | REF-000005 | **REF-000006** |
| Xie Ji Bian Fang Shu | REF-000006 | _(not in V1.0 seed)_ |
| Lan Tai Miao Xuan | REF-000007 | _(not in V1.0 seed)_ |

---

## 3. Consumer impact (read-only observation)

Knowledge Canon was **not modified** in this sprint.

| Consumer | Current citations | Issue under V1.0 SSOT |
|----------|-------------------|------------------------|
| `knowledge_canon/.../wood.json` | REF-000001 → "Yuan Hai Zi Ping" | ID now means Huang Di Nei Jing |
| | REF-000002 → "Di Tian Sui" | ID now means Zhou Yi |
| | REF-000003 → "San Ming Tong Hui" | ID now means Yuan Hai Zi Ping |
| | REF-000005 → "Zi Ping Zhen Quan" | ID now means Di Tian Sui |

**Required remapping for Wood (follow-up; out of scope here):**

| Intended work | Correct V1.0 ID |
|---------------|-----------------|
| Yuan Hai Zi Ping | REF-000003 |
| Di Tian Sui | REF-000005 |
| San Ming Tong Hui | REF-000004 |
| Zi Ping Zhen Quan | REF-000006 |

Optional additions once Canon may cite cosmology/medicine classics: REF-000001 (Huang Di Nei Jing), REF-000002 (Zhou Yi), REF-000007 (Qiong Tong Bao Jian).

---

## 4. Module relationship coverage (seed)

| Module tag | Seed refs mentioning it |
|------------|-------------------------|
| knowledge_canon | all 7 |
| five_elements | 000001, 000002 |
| yin_yang | 000002 |
| ten_gods | 000003, 000004, 000006 |
| strength | 000003, 000005, 000007 |
| useful_gods | 000003, 000005, 000006, 000007 |
| patterns | 000003, 000004, 000005, 000006 |
| temperature | 000001, 000005, 000007 |
| seasonal_qi | 000001, 000007 |
| shensha | 000004 |
| luck_cycles | 000004 |
| rule_database | 000003–000007 |
| terminology | 000001, 000002 |

---

## 5. Gaps

1. Legacy `classics/INDEX.md` still lists old IDs — needs Architect sync after Canon remapping.
2. No modern / paper / internal records in V1.0 seed.
3. `chapter_support` empty for all seed records.
4. All seed records remain `canonical_status: draft`.
