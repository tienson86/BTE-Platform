# NUMBER_ENERGY_INTERACTION_RULES_V1

Canonical interaction rules for BTE-Platform number-energy sequence analysis.

Version: `1.0`
Status: `FROZEN`
Depends on: `NUMBER_ENERGY_MASTER_KNOWLEDGE_V1.md`

---

## 1. Scope

This file defines how the BTE `number_energy` engine reads digit sequences after the base energy table has been frozen.

It covers:

- adjacent pair parsing;
- non-adjacent underlying pairs through `0` and `5`;
- states `NORMAL`, `HIDDEN`, `AMPLIFIED`, `REPEATED`, `CONTROLLED`, `NEUTRALIZED`;
- control and support relations;
- approved example interpretations;
- limits where the engine must not infer beyond V1.

Cursor MUST use this file together with `NUMBER_ENERGY_MASTER_KNOWLEDGE_V1.md`.

---

## 2. Parsing Layers

The engine should parse a sequence in layers.

### Layer 1: Raw Digits

Keep the original digit string exactly as entered.

Example:

```text
input: 141319
raw_digits: [1, 4, 1, 3, 1, 9]
```

### Layer 2: Ordinary Gua Digits And Modifiers

Classify each digit:

- ordinary gua digit: `1`, `2`, `3`, `4`, `6`, `7`, `8`, `9`;
- modifier digit: `0`, `5`.

`0` and `5` are never ordinary pair digits.

### Layer 3: Adjacent Ordinary Pairs

For every adjacent pair where both digits are ordinary gua digits, generate a `NORMAL` energy occurrence.

Example:

```text
14 -> Sinh Khí, NORMAL
41 -> Sinh Khí, NORMAL
13 -> Thiên Y, NORMAL
```

### Layer 4: Modifier-Bridged Underlying Pairs

For every three-digit window `A-M-B`, where:

- `A` is an ordinary gua digit;
- `M` is `0` or `5`;
- `B` is an ordinary gua digit;

generate the underlying pair `AB`.

If `M = 0`, assign state `HIDDEN`.

If `M = 5`, assign state `AMPLIFIED`.

Example:

```text
103 -> underlying pair 13 -> Thiên Y, HIDDEN
153 -> underlying pair 13 -> Thiên Y, AMPLIFIED
108 -> underlying pair 18 -> Ngũ Quỷ, HIDDEN
```

In V1, the engine SHOULD NOT also treat `10`, `03`, `15`, `53`, `50`, or `05` as ordinary Du Niên pairs.

---

## 3. Energy Occurrence Schema

Each detected occurrence SHOULD use this structure.

```yaml
occurrence_id: string
source_span: [start_index, end_index]
source_digits: string
pair_digits: string
energy_id: string
display_name: string
strength_rank: 1 | 2 | 3 | 4 | null
state: NORMAL | HIDDEN | AMPLIFIED | REPEATED | CONTROLLED | NEUTRALIZED
via_modifier: null | 0 | 5
notes: string
```

Indexes are zero-based unless the UI layer explicitly converts them for display.

---

## 4. Repetition Rules

### 4.1 Same Pair Repetition

If the same energy appears repeatedly in close sequence, mark the later occurrences or the group summary as `REPEATED`.

Example:

```text
1414
pairs: 14, 41, 14
energies: Sinh Khí, Sinh Khí, Sinh Khí
state: REPEATED
```

Interpretation:

- Sinh Khí is dominant;
- the sequence strongly emphasizes quý nhân, cơ hội, giao tiếp, mở đường;
- if excessive, it may create over-reliance on thuận duyên, lack of discipline, or weak decisiveness.

### 4.2 Same Energy, Different Pair

If different pairs belong to the same energy, the sequence may still be summarized as `REPEATED`.

Example:

```text
1493
pairs: 14, 49, 93
energies: Sinh Khí, Thiên Y, Sinh Khí
summary: Sinh Khí repeated with Thiên Y support
```

### 4.3 Repetition Is Not Automatic Neutralization

Repeated supportive energy is not automatically a full remedy.

Repeated challenging energy is not automatically fatal.

The engine must evaluate:

- energy class;
- strength rank;
- position;
- modifier state;
- control relation;
- purpose context.

---

## 5. Modifier Rules For 0 And 5

### 5.1 Digit 0: HIDDEN

`0` creates a hidden or attenuated version of the underlying pair-energy.

Example:

```yaml
sequence: 103
window: 1-0-3
underlying_pair: 13
energy: Thiên Y
state: HIDDEN
meaning: Thiên Y vẫn có nền tài vận/phúc khí/tình duyên, nhưng biểu hiện kín, chậm, yếu hoặc bị che.
```

Example:

```yaml
sequence: 108
window: 1-0-8
underlying_pair: 18
energy: Ngũ Quỷ
state: HIDDEN
meaning: Ngũ Quỷ vẫn là nền biến động, nhưng bị âm trường che hoặc giảm biểu hiện; không được kết luận là mất hẳn.
```

V1 rule: `0` does not completely erase the underlying energy unless a later frozen rule says so.

### 5.2 Digit 5: AMPLIFIED

`5` creates an activated or amplified version of the underlying pair-energy.

Example:

```yaml
sequence: 153
window: 1-5-3
underlying_pair: 13
energy: Thiên Y
state: AMPLIFIED
meaning: Thiên Y được kích hoạt, biểu hiện rõ hơn về tài vận, phúc khí, chính đào hoa và hỗ trợ ổn định.
```

V1 rule: `5` amplifies the underlying energy. It does not become a normal gua digit and does not create ordinary Du Niên pairs by itself.

### 5.3 Consecutive Modifiers

In V1, multiple consecutive modifiers such as `1003`, `1553`, `1053`, `1503`, `505`, `000`, `555` are not fully frozen.

The engine may classify them as:

```yaml
state: UNKNOWN_OR_NOT_DEFINED
reason: consecutive modifiers are not frozen in V1
```

unless a later version defines them.

---

## 6. Control And Remedy Rules

### 6.1 Frozen Direct Control Relations

| Challenging Energy | Controlling Supportive Energy | Status Result |
|---|---|---|
| Ngũ Quỷ | Sinh Khí | `CONTROLLED` |
| Tuyệt Mệnh | Thiên Y | `CONTROLLED` |
| Lục Sát | Diên Niên | `CONTROLLED` |
| Họa Hại | needs cát tinh combination | no direct single-pair control in V1 |

### 6.2 CONTROLLED

Use `CONTROLLED` when a proper supportive energy appears in a relevant sequence relationship to a challenging energy.

Example:

```text
Tuyệt Mệnh + Thiên Y -> Tuyệt Mệnh is CONTROLLED
```

Do not call it `NEUTRALIZED` unless a catalog pattern or explicit rule allows stronger wording.

### 6.3 NEUTRALIZED

Use `NEUTRALIZED` only for frozen, approved remedy structures.

In V1, `NEUTRALIZED` is conservative. If unsure, use `CONTROLLED` or `PARTIALLY_CONTROLLED` in the narrative layer while keeping the state as `CONTROLLED`.

### 6.4 Họa Hại Requires Combination

Họa Hại is tied to speech, conflict, market interaction, argument, and social friction.

In V1:

- no single direct-control cát tinh is frozen for Họa Hại;
- Họa Hại should be softened by a combination of supportive energies;
- customer-facing copy should distinguish “khẩu tài có thể dùng được” from “thị phi cần kiểm soát”.

### 6.5 Phục Vị Support Rule

Phục Vị is stabilizing but can become stagnant.

In V1:

- Sinh Khí supports Phục Vị by adding movement, opportunity, and quý nhân;
- Thiên Y supports Phục Vị by adding tài khí, phúc khí, and relationship stability;
- Phục Vị alone does not neutralize strong challenging energy;
- Phục Vị may prolong whatever energy precedes it.

---

## 7. Approved Compound Pattern: Sinh Khí -> Thiên Y -> Diên Niên

The conversation established an important rule:

```text
Ngũ Quỷ should use the ordered sequence:
Sinh Khí -> Thiên Y -> Diên Niên
and the order must not be reversed.
```

V1 handling:

- Treat this as an approved catalog pattern, not a fully generalized generator.
- The order matters.
- Do not auto-generate all longer variants unless separately approved.
- If a candidate sequence contains this order with repeated bridge pairs, the engine may identify it as an ordered supportive chain.

Canonical example:

```yaml
sequence: 141319
pairs:
  - 14: Sinh Khí
  - 41: Sinh Khí
  - 13: Thiên Y
  - 31: Thiên Y
  - 19: Diên Niên
ordered_chain:
  - Sinh Khí
  - Thiên Y
  - Diên Niên
status: approved_supportive_chain
use: may be used as a structured control/remedy pattern for Ngũ Quỷ contexts
note: Do not reverse the chain. Do not assume unlisted extensions are valid.
```

Open V1 limit:

```text
14131914
14131319
286249
```

These are not approved unless separately frozen in a later catalog.

---

## 8. Approved Example Interpretations

### 8.1 `103`

```yaml
sequence: 103
rule: modifier-bridged pair
underlying_pair: 13
energy: Thiên Y
strength_rank: 1
state: HIDDEN
interpretation: Thiên Y rank 1 exists as underlying energy, but `0` makes it hidden, slower, weaker, or less obvious.
customer_copy: Dãy này có nền Thiên Y, thiên về tài khí/phúc khí/tình cảm ổn định, nhưng biểu hiện không lộ mạnh vì bị âm trường che.
```

### 8.2 `153`

```yaml
sequence: 153
rule: modifier-bridged pair
underlying_pair: 13
energy: Thiên Y
strength_rank: 1
state: AMPLIFIED
interpretation: Thiên Y rank 1 is activated by `5`.
customer_copy: Dãy này kích hoạt Thiên Y mạnh, phù hợp khi cần tăng tài khí, phúc khí và sự ổn định trong quan hệ.
```

### 8.3 `108`

```yaml
sequence: 108
rule: modifier-bridged pair
underlying_pair: 18
energy: Ngũ Quỷ
strength_rank: 1
state: HIDDEN
interpretation: Ngũ Quỷ rank 1 exists as hidden/attenuated volatility.
customer_copy: Dãy này có nền Ngũ Quỷ bị che bởi âm trường. Không nên kết luận là đã mất hẳn biến động; nên xem thêm các cặp sau đó có Sinh Khí chế ước hay không.
```

### 8.4 `141319`

```yaml
sequence: 141319
rule: approved ordered supportive chain
pairs:
  - 14: Sinh Khí rank 1
  - 41: Sinh Khí rank 1
  - 13: Thiên Y rank 1
  - 31: Thiên Y rank 1
  - 19: Diên Niên rank 1
state: REPEATED + approved_supportive_chain
interpretation: Chuỗi đi từ Sinh Khí sang Thiên Y rồi Diên Niên, tạo cấu trúc mở cơ hội -> ổn định tài/phúc -> củng cố sự nghiệp/trách nhiệm.
customer_copy: Đây là chuỗi cát tinh mạnh, đi theo trật tự hỗ trợ: mở cơ hội, tăng tài khí/phúc khí, rồi đưa về ổn định và trách nhiệm.
```

### 8.5 `1414`

```yaml
sequence: 1414
rule: repeated same energy
pairs:
  - 14: Sinh Khí rank 1
  - 41: Sinh Khí rank 1
  - 14: Sinh Khí rank 1
state: REPEATED
interpretation: Sinh Khí rất trội; tốt cho quý nhân, cơ hội, giao tiếp, mở đường, nhưng cần tránh quá tùy duyên hoặc thiếu quyết đoán.
customer_copy: Dãy này nhấn rất mạnh Sinh Khí, hợp để mở quan hệ và cơ hội. Nếu dùng quá nhiều, nên phối thêm trường tạo kỷ luật và ổn định.
```

### 8.6 `219`

```yaml
sequence: 219
rule: adjacent pair analysis
pairs:
  - 21: Tuyệt Mệnh rank 1
  - 19: Diên Niên rank 1
state: NORMAL
interpretation: Có Tuyệt Mệnh mạnh đi cùng Diên Niên mạnh. Diên Niên không phải cát tinh trực tiếp chế Tuyệt Mệnh trong V1; không được đánh dấu neutralized.
customer_copy: Dãy này có một phần quyết liệt/mạo hiểm rất mạnh, sau đó đi vào xu hướng ổn định và trách nhiệm. Tuy nhiên, theo V1, cần Thiên Y để chế Tuyệt Mệnh; Diên Niên chỉ giúp tăng kỷ luật, không thay thế vai trò Thiên Y.
```

### 8.7 `216`

```yaml
sequence: 216
rule: adjacent pair analysis
pairs:
  - 21: Tuyệt Mệnh rank 1
  - 16: Lục Sát rank 1
state: NORMAL
interpretation: Hai trường challenging mạnh xuất hiện liên tiếp. Không có Thiên Y để chế Tuyệt Mệnh và không có Diên Niên để chế Lục Sát.
customer_copy: Dãy này có tổ hợp quyết liệt/mạo hiểm đi cùng cảm xúc và quan hệ dễ biến động. Cần phối thêm cát tinh phù hợp nếu dùng trong ngữ cảnh quan trọng.
```

---

## 9. Purpose Context Rules

The same sequence can be interpreted differently depending on purpose.

Supported V1 contexts:

- `phone_number`;
- `car_plate`;
- `motorbike_plate`;
- `id_number`;
- `bank_account`;
- `house_number`;
- `generic_number`.

Context emphasis:

| Context | Interpretation Focus |
|---|---|
| `phone_number` | communication, relationship, wealth, career flow, daily use |
| `car_plate` | movement, safety symbolism, work mobility, asset stability, financial flow |
| `motorbike_plate` | mobility, daily movement, personal rhythm, practical safety symbolism |
| `id_number` | long-term identity imprint, life themes, owner compatibility |
| `bank_account` | wealth flow, retention, risk, transaction stability |
| `house_number` | family stability, rest, health symbolism, long-term field |
| `generic_number` | only intrinsic number-energy unless owner/context supplied |

Do not conclude final compatibility until owner data such as Cung Phi or Bát Tự is integrated by a later layer.

---

## 10. Aggregation Guidance

When summarizing a full sequence, consider:

- dominant energy by frequency;
- strongest rank occurrences;
- whether challenging energies are controlled;
- whether supportive energies are repeated to excess;
- modifier states from `0` and `5`;
- whether Phục Vị prolongs preceding fields;
- purpose context;
- owner compatibility if available.

V1 does not define numeric scoring.

Any UI score, grade, percentage, or traffic-light result must be defined in a later frozen scoring specification.

---

## 11. Narrative Safety Rules

Customer-facing output should:

- explain “vì sao” using visible pairs or patterns;
- mention both useful and risky sides of a field;
- avoid fatalistic statements;
- avoid medical diagnosis;
- distinguish intrinsic number energy from owner compatibility;
- say “theo hệ thống Bát Cực Linh Số” for sensitive claims.

Customer-facing output should not say:

- “số này chắc chắn gây bệnh”;
- “số này chắc chắn phá sản”;
- “số này chắc chắn ly hôn”;
- “0 triệt tiêu hoàn toàn nên không còn tác động”;
- “5 biến thành quái số bình thường”.

---

## 12. Cursor Compliance Rule

Cursor MUST NOT generate interaction behavior outside this file.

If an interaction is not defined in V1, return:

```yaml
state: UNKNOWN_OR_NOT_DEFINED
reason: rule not frozen in NUMBER_ENERGY_INTERACTION_RULES_V1
```

Future changes must be added through a new versioned file or an explicit patch approved by the project owner.

