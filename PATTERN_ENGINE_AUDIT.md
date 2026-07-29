# Pattern Engine Audit Report

**Date:** 2026-07-29  
**Auditor:** AI Agent (Sonnet 4.6)  
**Trigger:** Integration Verification — 20/20 lá số đều trả về "Chính Quan"  
**Scope:** Pattern Engine pipeline + Rule Database

---

## Executive Summary

**Root cause xác nhận:** `database/14_pattern/01_main_pattern.csv` chứa **5 rules**, tất cả đều có `conditions = []` (không có điều kiện nào). Mọi rule match với mọi lá số. Rule có `priority` cao nhất là `chinh_quan` (priority=100) → **100% lá số trả về Chính Quan**.

**Mức độ nghiêm trọng:** 🔴 **CRITICAL** — Pattern Engine không hoạt động đúng chức năng phân loại.

---

## I. Pipeline Trace

```
PatternContext (day_master, ten_gods, pillars, shensha, bazi, calendar)
        ↓
PatternCalculator.calculate(context)
        ↓
PatternLoader.load_rules()
  → database/14_pattern/01_main_pattern.csv  ← CHỈ 1 FILE, 5 RULES
        ↓
foreach rule in rules:
  PatternMatcher.match(context, rule)
    → conditions = []  ← LUÔN MATCH (empty conditions = True)
        ↓
Winner = rule có priority cao nhất
  → pattern_001, chinh_quan, priority=100  ← LUÔN THẮNG
        ↓
FollowPatternCalculator.detect(context)  ← Chạy riêng, không ghi đè pattern
        ↓
PatternResult(pattern="chinh_quan", cach_cuc="Chính Quan", score=91, priority=100)
```

---

## II. Phân tích từng lá số (mẫu)

| Label | Day Master | Month Branch | Ten Gods | Follow Detected | Selected Pattern |
|---|---|---|---|---|---|
| Chinh_Quan_Nam | Canh | Sửu | Thất Sát, Kiếp Tài, Nhật Chủ, Thiên Ấn | — | chinh_quan |
| That_Sat_Nu | Ất | Ngọ | Chính Ấn, Thất Sát, Nhật Chủ, Thương Quan | — | chinh_quan |
| Tong_Cach_Nam | Kỷ | Thìn | Tỷ Kiên, Thương Quan, Nhật Chủ, Tỷ Kiên | — | chinh_quan |
| 08_TQ_F_1988 | Mậu | Thân | Kiếp Tài, Thực Thần, Nhật Chủ, Thực Thần | **Tòng Tài** | chinh_quan |
| 11_CQ_M_2000 | Canh | Dần | Thất Sát, Thất Sát, Nhật Chủ, Thiên Ấn | **Tòng Sát** | chinh_quan |
| 19_HA_M_2001 | Bính | Ngọ | Thực Thần, Tỷ Kiên, Nhật Chủ, Thực Thần | **Tòng Quan** | chinh_quan |

> **Lưu ý:** `FollowPatternCalculator.detect()` hoạt động đúng (phát hiện 8/50 lá số là Tòng Cách), nhưng kết quả của nó chỉ được lưu vào `result.follow_type` — **không ghi đè `result.pattern`**. Orchestrator sau đó map `follow_type → tong_cach` qua `rule_context_bridge.py`, nhưng `pattern` và `cach_cuc` vẫn là `chinh_quan`.

---

## III. Rule Database Analysis

### Trạng thái hiện tại

| File | Tồn tại | Số rules | Conditions đầy đủ |
|---|---|---|---|
| `database/14_pattern/01_main_pattern.csv` | ✅ | 5 | ❌ tất cả `[]` |
| `05_special_case_rules` | ❌ **MISSING** | — | — |
| `06_follow_pattern_rules` | ❌ **MISSING** | — | — |
| `07_combination_rules` | ❌ **MISSING** | — | — |
| `08_priority_rules` | ❌ **MISSING** | — | — |

### Nội dung `01_main_pattern.csv`

```csv
rule_id,pattern,priority,conditions,score,description
pattern_001,chinh_quan,100,[],91,Chinh Quan cach (main pattern)
pattern_002,that_sat,80,[],72,That Sat cach
pattern_003,thuc_than,50,[],48,Thuc Than cach
pattern_004,chinh_tai,70,[],60,Chinh Tai cach
pattern_005,chinh_an,70,[],60,Chinh An cach
```

**Vấn đề:** Tất cả `conditions = []` → `PatternMatcher.match()` với empty conditions luôn trả `True` (vòng for không iterate, trả về `True` ngay).

---

## IV. Component Analysis

### PatternMatcher (`matcher.py`)

```python
def match(self, context, rule):
    conditions = rule.get("conditions", [])
    for cond in conditions:          # ← empty list → không iterate
        ...
        if not self.evaluate(current, op, value):
            return False
    return True                      # ← luôn True khi conditions = []
```

**Status:** ✅ Logic đúng. Empty conditions = "match anything" là hành vi hợp lý. Vấn đề không ở đây.

### PatternCalculator (`calculator.py`)

```python
if rule["priority"] >= result["priority"]:  # ← >= thay vì >
    result["priority"] = rule["priority"]
    result["pattern"] = rule["pattern"]
```

**Status:** ⚠️ Dùng `>=` thay vì `>` — nếu có 2 rules cùng priority, rule sau sẽ thắng (không deterministic). Nhưng vấn đề chính không phải ở đây.

### PriorityResolver (`rules/priority.py`)

```python
return max(rules, key=lambda x: (x.priority, x.score))
```

**Status:** ✅ Logic đúng. Tuy nhiên `PriorityResolver` **không được gọi** trong main pipeline — `PatternCalculator.calculate()` tự xử lý priority inline, không dùng `PriorityResolver`.

### FollowPatternCalculator (`calculators/follow_pattern.py`)

**Status:** ✅ Logic detection đúng — phát hiện 8/50 lá số là Tòng Cách (16%). Tuy nhiên kết quả chỉ được publish vào `follow_type`, không ghi đè `pattern`.

### PatternLoader (`loader.py`)

**Status:** ⚠️ Chỉ load `01_main_pattern.csv` (hoặc `rules.csv`). Không load bất kỳ file nào khác trong thư mục. Các file `05_special_case`, `06_follow_pattern`... nếu có cũng không được load.

---

## V. Distribution — 50 Charts

| Pattern | Count | % | Ghi chú |
|---|---|---|---|
| chinh_quan | 50 | **100%** | 🔴 DOMINANT — ROOT CAUSE CONFIRMED |

### Follow-type detected (hoạt động đúng nhưng không ảnh hưởng pattern):

| Follow Type | Count |
|---|---|
| Tòng Tài | 2 |
| Tòng Sát | 1 |
| Tòng Quan | 2 |
| Tòng Vượng | 1 |
| Tòng Nhi | 2 |
| **Total follow** | **8/50 (16%)** |

---

## VI. Root Cause Summary

| # | Nguyên nhân | Tầng | Severity |
|---|---|---|---|
| 1 | `01_main_pattern.csv` — tất cả conditions = [] | **Database** | 🔴 CRITICAL |
| 2 | Database thiếu 4 rule files (special, follow, combination, priority) | **Database** | 🔴 CRITICAL |
| 3 | `PatternCalculator` chỉ load 1 file duy nhất | **Engine** | 🟡 WARNING |
| 4 | `FollowPatternCalculator.detect()` kết quả không ghi đè `pattern` | **Engine Logic** | 🟡 WARNING |
| 5 | `PriorityResolver` tồn tại nhưng không được gọi trong main pipeline | **Engine** | 🟡 INFO |

---

## VII. Fix Proposal

### Fix 1 (CRITICAL — Cần làm ngay): Bổ sung conditions vào Rule Database

File `database/14_pattern/01_main_pattern.csv` cần được thay thế/bổ sung với conditions thực tế. Mỗi cách cục cần điều kiện xác định, ví dụ:

**Chính Quan Cách:** Thiên Can tháng là Chính Quan của Nhật Chủ, hoặc tàng trong Địa Chi tháng  
**Thất Sát Cách:** Thiên Can tháng là Thất Sát, hoặc Thất Sát cường vượng  
**Thực Thần Cách:** Tương tự  
**Thương Quan Cách:** Tương tự  
**Chính Tài / Thiên Tài Cách:** Tương tự  
**Tòng Cách:** Dùng `follow_type` từ `FollowPatternCalculator`

### Fix 2 (CRITICAL): Bổ sung các Rule Database files còn thiếu

Cần tạo:
- `database/14_pattern/05_special_case_rules.csv` — Chuyên Cách (Khúc Trực, Viêm Thượng...)
- `database/14_pattern/06_follow_pattern_rules.csv` — Tòng Cách (Tòng Tài, Tòng Sát...)
- `database/14_pattern/07_combination_rules.csv` — Hoá Cách
- `database/14_pattern/08_priority_rules.csv` — Priority override rules

### Fix 3 (Engine): Sử dụng follow_type khi xác định cách cục

Khi `FollowPatternCalculator.detect()` trả về giá trị, `PatternCalculator` nên ưu tiên đó làm `pattern` thay vì giữ nguyên `chinh_quan`.

### Fix 4 (Engine): Kết nối `PriorityResolver` vào main pipeline

`PriorityResolver.resolve()` hiện không được gọi. Nên refactor để pipeline sử dụng nó.

---

## VIII. Điều không cần sửa

- **`PatternMatcher.match()`** — Logic đúng
- **`FollowPatternCalculator.detect()`** — Logic đúng, phát hiện đúng
- **UI / Frontend** — Không liên quan đến bug này
- **API / Orchestrator** — Không liên quan

---

## IX. Kết luận và Đề xuất

| Hạng mục | Kết quả |
|---|---|
| Pattern Engine pipeline code | ✅ Đúng về cấu trúc |
| Rule Database completeness | 🔴 Chỉ có 1/5 files, tất cả conditions rỗng |
| Pattern discrimination | 🔴 100% Chính Quan — không có discrimination |
| Follow-type detection | ✅ Hoạt động đúng (16% detection rate) |
| Special pattern detection | ⚠️ Code tồn tại nhưng không được gọi |

**Pattern Engine hiện tại là một "stub"** — code infrastructure đúng nhưng Rule Database chưa được xây dựng đủ để phân loại lá số.

**Để đạt Beta/RC:** Cần xây dựng đầy đủ Rule Database với conditions thực tế cho từng loại cách cục. Đây là **task Data/Domain** không phải task Code.

**Mức độ sẵn sàng Pattern Engine:** 🟡 **Alpha (Infrastructure Ready, Data Incomplete)**

---

## X. Files liên quan

| File | Trạng thái |
|---|---|
| `engines/pattern_engine/engine.py` | ✅ OK |
| `engines/pattern_engine/calculator.py` | ⚠️ Minor: dùng `>=` thay `>`, không dùng PriorityResolver |
| `engines/pattern_engine/matcher.py` | ✅ OK |
| `engines/pattern_engine/loader.py` | ⚠️ Chỉ load 1 file |
| `engines/pattern_engine/rules/priority.py` | ⚠️ Tồn tại nhưng không được gọi |
| `engines/pattern_engine/calculators/follow_pattern.py` | ✅ Logic đúng |
| `engines/pattern_engine/calculators/special_pattern.py` | ⚠️ Tồn tại nhưng không được gọi |
| `database/14_pattern/01_main_pattern.csv` | 🔴 5 rules, conditions=[] tất cả |
| `database/14_pattern/05_special_case_rules.csv` | ❌ MISSING |
| `database/14_pattern/06_follow_pattern_rules.csv` | ❌ MISSING |
| `database/14_pattern/07_combination_rules.csv` | ❌ MISSING |
| `database/14_pattern/08_priority_rules.csv` | ❌ MISSING |

---

*Generated: 2026-07-29 | Script: validation/pattern_audit.py | 50 charts*
