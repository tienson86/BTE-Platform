# EXAMPLE — CASE-0001 Prototype Run

| Field | Value |
|-------|-------|
| Document | EXAMPLE_CASE_0001 |
| Pack | PACK-01 Prototype |
| Case | CASE-0001 |
| Input | Strength Facts only |
| Output | Traced Dual Mode — not a real report |

---

# 0. What this file is

A step-by-step demonstration:

```text
Fact → Knowledge selected → Sentence job → Paragraph → Final interpretation
```

It answers:

1. Which knowledge units were selected?
2. Why were they selected?
3. Why were others rejected?
4. How were duplicate ideas removed?
5. How were contradictions handled?
6. How were transition sentences created?
7. How was the final narrative ordered?

It does **not** generate a customer PDF.

It does **not** invent a job, marriage, or luck decade for the subject.

Source of facts (read-only):

`knowledge/pilot/replay/root_cause/strength_calibration/evidence/CASE-0001.json` → `published_contract` + `strength_evidence_ledger` + `context_fields`.

Out of band (NOT S0 input): expert expected “Thân trung bình / thiên nhược”. The selector ignores it. A footnote at the end records that discrepancy so reviewers are not surprised.

---

# 1. S0 — Strength Facts received

Published contract:

| Field | Value |
|-------|-------|
| `strength_level` | `strong` |
| `strength_score` | `0.87` |
| `season_score` | `0.25` |
| `root_score` | `0.12` |
| `support_score` | `0.08` |
| `drain_score` | `0.0` |
| `control_score` | `-0.18` |
| engine `confidence` | `1.0` |
| engine `reasoning` | `Thân vượng` |
| `matched_rules` | `sea_002`, `root_003`, `sup_001`, `ctl_001`, `ctl_006`, `spc_004` |

Ledger (why rules fired — still Strength Facts):

| Rule | Group | Polarity | Fact that matched |
|------|-------|----------|-------------------|
| `sea_002` | season | strengthen | `month_status` = Tướng |
| `root_003` | root | strengthen | `root_level` = Thông căn 1 chi |
| `sup_001` | support | strengthen | `support_type` = Đồng hành trợ thân |
| `ctl_001` | control | weaken | `control_type` = Bị Quan Sát khắc |
| `ctl_006` | control | weaken | officer contains Thất Sát |
| `spc_004` | special | strengthen | month branch ten god Chính Ấn + season winter |
| `pri_level_strong` | level | classify | `strength_score` >= 0.65 |

Also published:

- `drain_type` = null, drain bucket 0
- combination bucket 0
- `hidden_stems` = NOT_EXPOSED
- special priority 102 — **not** an override (override in engine is priority >= 105)

Not received (must not be used):

- Pattern, Useful God, Temperature
- Public luck interaction
- Gender as customer text
- Expert strength label

---

# 2. S1 — Evidence Layer (summary)

Supporting: season Tướng, root 1 chi, companion support, special Ấn in cold season.

Weakening: control (Quan Sát + Thất Sát).

Inactive: drain, combination.

Classify: level rule → strong.

Missing: hidden stems, luck interaction.

Conflict C1: support-side vs control.

Leak class: scores, rule IDs, enums → `internal_only`. Lived polarities → `meaning_ok`.

---

# 3. S2 — Class map

```text
engine strong  →  interpretation class strong  →  Thân Vượng
```

Not upgraded to Very Strong (engine has no `very_strong`; root is thin).

Not downgraded to Balanced.

---

# 4. S3 — Mode A honesty (before knowledge)

**Final conclusion:** Strong / Thân Vượng.

**Interpretation confidence (declared prototype arithmetic, not a new scorer):**

```text
start 88     published class, 6 matched rules, score 0.87 far from 0.65
− 10         C1 control vs support-side
− 6          hidden stems not exposed
+ 0          luck missing does not reduce natal-class confidence
= 72%        band = high
```

Engine `1.0` is recorded as input. It is **not** copied to 100%.

Why 72% is still high: four strengthen groups agree; drain is inactive; the class is not at the 0.65 edge.

Why not canonical: control is material; hidden stems unknown.

**Alternative:**

```text
Primary    Strong     72%
Runner-up  Balanced   28%
```

Balanced would need control to be treated as equal to season + special. It did not win. Weak is not plausible (drain inactive; season and root present).

**Missing:** `hidden_stems`, `luck_interaction`.

**Conflicts:** C1 season/root/support/special vs control. Engine resolution: level rule still Strong. Residual: Why must name both weathers.

---

# 5. S4 — Knowledge selection

## 5.1 Selected

| Unit ID | Source | Why selected |
|---------|--------|----------------|
| IK-STR-MEAN-ST-01 | 01_MEANINGS §4 lived | `class_strong` |
| IK-STR-MEAN-ST-03 | 01_MEANINGS §4 tendency (endurance as proof) | `class_strong`; pairs with later challenge |
| IK-STR-CAUSE-SEASON-01 | 02_CAUSES §3 | `season_present` |
| IK-STR-CAUSE-ROOT-THIN-01 | 02_CAUSES §4 thin root | `root_present` AND `root_thin` |
| IK-STR-CAUSE-SUPPORT-01 | 02_CAUSES §5 | `support_present` |
| IK-STR-CAUSE-CONTROL-01 | 02_CAUSES §7 | `control_present` |
| IK-STR-CAUSE-SPECIAL-01 | 02_CAUSES special as feed | `special_present` AND NOT `special_override` |
| IK-STR-CAUSE-CLASS-ST-01 | 02_CAUSES §9 Strong cluster | class strong; drain does not win |
| IK-STR-ADV-ST-responsibility | 03_ADVANTAGES §4 | P4 Strong pick |
| IK-STR-ADV-ST-leadership | 03_ADVANTAGES §4 staying power | P4 |
| IK-STR-ADV-ST-decision | 03_ADVANTAGES §4 | P4 |
| IK-STR-CHAL-ST-endurance-as-proof | 04_CHALLENGES §4 | P3 C1-relevant typical mistake |
| IK-STR-CHAL-ST-receptivity | 04_CHALLENGES §4 | control present — closed ear / pressure |
| IK-STR-CHAL-ST-battery | 04_CHALLENGES §4 relational cost | for Marriage pairing |
| IK-STR-PERS-ST-working | 05_PERSONALITY §3 | class strong; cap 2 |
| IK-STR-PERS-ST-conflict | 05_PERSONALITY §3 | class strong |
| IK-STR-CAR-ST-load | 06_CAREER §3 suitable load | class strong |
| IK-STR-CAR-ST-employment | 06_CAREER §3 backbone + recovery as condition | domain novelty vs Meaning |
| IK-STR-WEA-ST-earn-by-carrying | 07_WEALTH §3 | class strong |
| IK-STR-MAR-ST-love-by-carrying | 08_MARRIAGE §3 | pairs with battery |
| IK-STR-HEA-ST-downshift | 09_HEALTH §3 scheduled downshift | domain: body, not stamina synonym |
| IK-STR-REC-ST-do-rest-calendar | 11_RECOMMENDATIONS §3 | pairs with battery / health |
| IK-STR-REC-ST-do-invite-revision | 11_RECOMMENDATIONS §3 | pairs with endurance-as-proof |
| IK-STR-REC-ST-avoid-difficulty-identity | 11_RECOMMENDATIONS §3 | pairs with endurance-as-proof |
| IK-STR-REC-ST-avoid-hear-without-revise | 11_RECOMMENDATIONS §3 | pairs with receptivity |
| IK-STR-EDGE-C1-qualifier | 12_EDGE_CASES §3–4 | `conflict_support_vs_control` AND `root_thin` |

## 5.2 Rejected (material)

| Unit ID | Reason |
|---------|--------|
| IK-STR-MEAN-VS-* | WRONG_CLASS |
| IK-STR-MEAN-BA-* | WRONG_CLASS (alternative only, not Meaning) |
| IK-STR-MEAN-WK-* / VW-* | WRONG_CLASS |
| IK-STR-CAUSE-DRAIN-* | CAUSE_ABSENT (`drain_score` 0, `drain_type` null) |
| IK-STR-CAUSE-COMB-* | CAUSE_ABSENT (combination 0) |
| IK-STR-CAUSE-ROOT-DEEP-* | PREDICATE_BLOCK (`root_thin`, not deep) |
| IK-STR-ADV-ST-adaptability | P6 / not Strong headline gift |
| IK-STR-ADV-ST-stress_tolerance | DUPLICATE family with Health downshift (dropped at S7) |
| IK-STR-LUCK-* | MISSING_LUCK |
| IK-STR-REC-VS-* / BA-* / WK-* | WRONG_CLASS |
| IK-STR-EX-* (13_EXAMPLES) | teaching only — never customer output |
| Any Useful God / Pattern / Temperature unit | out of S0 scope |

---

# 6. S5–S7 — Priority, conflict, duplicates

**Conflict C1:** Keep Strong as Conclusion. Keep control in Why. Do not load Balanced meaning. Mode B may use EDGE qualifier once.

**Duplicates dropped:**

| Dropped | Because |
|---------|---------|
| IK-STR-ADV-ST-stress_tolerance | full-tank / stamina family already in MEAN-ST-01; Health owns downshift |
| IK-STR-MEAN-ST-02 extra “pressure is familiar” if it clones MEAN-ST-01 | keep MEAN-ST-01 + MEAN-ST-03 only |
| Career “you persist” | CAR-ST-load must answer *where load sits*, not restating Meaning |

**Kept after rewrite-to-domain:**

- Career: ownership of a hard piece + recovery as a work condition
- Wealth: income tracks load — legitimacy trap
- Marriage: love shown by carrying — partner may be unseen
- Health: scheduled downshift, not “you are healthy because Strong”

---

# 7. S8 — Sentence jobs (before transitions)

## Conclusion

Not a knowledge unit.

**Job:** Name.

**Why this paragraph exists:** Customer must hear the standing.

**Text:** Nhật chủ của bạn thuộc nhóm Thân Vượng.

## Why (cause units, P2 order)

1. SPECIAL — Ấn in cold season feeds; not an override.
2. SEASON — Tướng: climate is not empty.
3. ROOT-THIN — there is ground, but one branch: floor exists, not a fortress.
4. SUPPORT — companion backup: not standing entirely alone.
5. CONTROL — Quan Sát / Thất Sát: something sits on you.

**Job:** Explain.

**Why this paragraph exists:** Question Framework WHY, using only present causes.

**Assembled (leak-free):**

> Điều này đứng vững vì bạn được khí mùa nâng, có căn (dù không dày), có đồng hành trợ thân, và Ấn trong mùa lạnh còn tiếp thêm lực — không phải vì bạn không bị kiểm. Phía kia, Quan Sát / áp lực vẫn ngồi trên Nhật chủ: lực có thật, và lực đó không đi một mình không phanh.

Drain omitted on purpose.

## Meaning

Units: MEAN-ST-01, MEAN-ST-03, EDGE qualifier.

**Job:** Interpret.

**Why this paragraph exists:** SO WHAT at identity level — not a definition of Thân Vượng.

**Assembled:**

> Bạn vào việc với nội lực sẵn có. Người khác thấy bạn chịu được áp lực. Chính bạn dễ lấy việc “mình chịu được” làm bằng chứng rằng cách làm không cần đổi. Đây là Thân Vượng, không phải dạng dư lực không bị kiểm.

## Advantages

Units: responsibility, leadership staying power, decision stays decided.

**Job:** Upside.

**Why this paragraph exists:** usable capacity, not a restatement of “full tank”.

**Assembled:**

> Người khác có thể giao việc nặng rồi yên tâm. Bạn dẫn bằng việc còn pin ở giờ thứ mười. Quyết định một khi đã chốt thì không đảo vì tâm trạng.

## Challenges

Units: endurance-as-proof, receptivity, battery.

**Job:** Cost.

**Why this paragraph exists:** operating cost of the same structure.

**Assembled:**

> Cùng một lực đó, bạn dễ coi sự bền là bằng chứng phương pháp đúng. Góp ý nghe được nhưng chưa chắc đã sửa. Trong hệ thống (cơ quan hay gia đình), bạn dễ thành pin cho người khác.

## Life Influence

**Personality** (working + conflict): Bạn hiện diện đều, thích giữ một mảnh việc đến hết. Trong xung đột bạn đứng vững — và có thể đứng quá lâu.

**Career:** Phù hợp chỗ cần người gánh một mảnh khó và hoàn tất. Điều kiện làm việc phải gồm nhịp phục hồi; nếu không, tổ chức sẽ dùng xương sống đến khi nứt.

**Wealth:** Tiền thường đi cùng tải. Cái bẫy là chỉ thấy mình đáng giá khi còn tăng ca cho hóa đơn.

**Marriage:** Bạn yêu bằng cách gánh. Đối phương có thể được chăm và vẫn thấy mình không được nhìn thấy.

**Health:** Đưa nhịp xuống lịch, đừng để nghỉ = “khi xong hết”.

Each child exists because HOW IT AFFECTS that domain — not because we needed more synonyms of Strong.

## Luck

**State:** insufficient_data.

**Reason (Mode A):** public luck interaction not in Strength Facts.

**Customer text:**

> Phần vận trình chưa có dữ liệu công bố để luận tương tác với thân vượng/nhược. Phần natal ở trên vẫn giữ.

No decade names.

## Recommendations

**Do:** Đưa nghỉ vào lịch. Cho phép một người được quyền sửa phương pháp.

**Avoid:** Sưu tầm việc khó như một bản sắc. Nghe góp ý mà không đổi.

**Why this paragraph exists:** DO / AVOID paired with kept challenges.

## Executive Summary (7 lines)

> Nhật chủ của bạn thuộc nhóm Thân Vượng.
> Bạn được mùa, có căn và có trợ — đồng thời vẫn bị áp lực ngồi lên.
> Bạn vào việc với nội lực sẵn có, nên gánh được tải.
> Cái giá là lấy sự bền làm bằng chứng không cần đổi cách.
> Hãy chừa nhịp phục hồi và một người được quyền chỉnh phương pháp.
> Đừng biến việc khó thành danh tính.
> Điểm then chốt: mạnh không có nghĩa là không cần phanh.

No new claims. No luck line (luck insufficient). No percents.

---

# 8. S9 — Transitions used

| Boundary | Stem used | Skipped? |
|----------|-----------|----------|
| Conclusion → Why | `Điều này đứng vững vì` | No — folded into Why first clause |
| Why → Meaning | (none) | Meaning already starts with lived consequence |
| Meaning → Advantages | `Lực này giúp` implied by “Người khác có thể giao việc” | Stem not duplicated |
| Advantages → Challenges | `Cùng một lực đó` | Used |
| Challenges → Influence | `Trong đời sống` | Optional; children have their own domain heads |
| Influence → Luck | honest-gap stem | Used |
| Luck → Recommendations | `Vì vậy` based on natal only | Used in rec pairing, not as a new fact |

No LLM. No extra causes in bridges.

---

# 9. S10 — Final interpretation (prototype object, condensed)

## Mode A (audit)

1. **Conclusion:** Strong / Thân Vượng (engine `strong`, unmapped-not-applicable)
2. **Evidence:** rules above; support-side vs control; drain inactive; scores internal
3. **Rule Trace:** six matched + level rule; special is feed not override
4. **Confidence:** engine input 100% recorded; interpretation **72% high** (why in §4)
5. **Alternative:** Strong 72% / Balanced 28% / Weak not plausible
6. **Missing:** hidden stems; luck interaction
7. **Conflicts:** C1 support-side vs control; class not flipped
8. **Appendix:** selected / rejected / duplicate logs in §5–§6

## Mode B (customer)

Sections in §7, leak-free, each with `why_this_paragraph_exists`.

This is **not** a Report Engine artifact.

---

# 10. The seven questions — answers for CASE-0001

1. **Which units?** See §5.1.
2. **Why selected?** Class `strong` + present causes + caps + pairing.
3. **Why rejected?** Wrong class, drain absent, luck missing, deep-root false, examples not for output, other packs out of scope.
4. **Duplicates?** Stamina family kept in Meaning; Health took downshift; Career rewritten to load-site.
5. **Contradictions?** C1 both polarities in Why; primary class unchanged; Balanced only in Mode A alternative.
6. **Transitions?** Closed catalog, §8.
7. **Order?** Conclusion → Why → Meaning → Advantages → Challenges → Influence children → Luck (insufficient) → Recommendations → Executive Summary.

---

# 11. Footnote — expert discrepancy (not an input)

Pilot replay records expert expected “Thân trung bình / thiên nhược” vs engine `strong` / 0.87.

This prototype **must not** consume that label as a Strength Fact.

It **must** still show Alternative Analysis from **control + thin root** inside the facts.

Fixing the engine class is out of scope (do not modify Strength algorithm).

---

END
