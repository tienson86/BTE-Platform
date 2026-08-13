# IMPLEMENTATION

| Field | Value |
|-------|-------|
| Step | 3 |
| Layer | CLL **runtime realization** only |
| Architecture | Unchanged |

---

## Surface (minimal)

| File | Change |
|------|--------|
| `applications/production/language/writer.py` | Theme / capacity / dual gates on rooms, balance, close, insight, pressure, environment, action |
| `applications/production/language/service.py` | Theme-gated `_memory_line`; cue pass-through; `_avoid_block` dedupe |
| `applications/production/language/plain_language.py` | Lived `structure_to_plain` (case-normalized) |

Not edited: engines, Product Context, Theme Library catalog, CLL markdown specs, tests, Golden.

---

## Shared rules (not case ids)

### Conserving (PB-001)

```text
conserving =
    capacity in {weak, very_weak}
    OR (primary_theme == BALANCE_DIRECTION AND capacity in {balanced, empty})
```

When conserving:

- Close: rest / bảo toàn — never “Bạn mạnh hơn khi…”
- Career close: được phép dừng và trả việc
- Pressure: reduce surface, do not prove
- Environment: light calendar
- Career balance: stop-list, not a production cycle

### Theme-gated memory and rooms (PB-002)

| Theme | Room kept | Room forbidden |
|-------|-----------|----------------|
| OPERATING_OUTPUT | Product / output week / visible result | — |
| OPERATING_SELF_CARRY | Load-boundary, refuse overflow | Output week, “vòng ra kết quả” |
| BALANCE_DIRECTION / conserving | Cool, cut, return work | Motivation + production cycle |
| OPERATING_STANDARDS | Scope and standard | Default OUTPUT dump |

UG cooling that says “tạo ra sản phẩm / kết quả cụ thể” is rewritten **off OUTPUT** to “cắt giảm phần thừa, làm rõ biên”. Helpers: `_lived_balance`, `_strip_output_leak`.

### Two published stories (PB-003)

```text
dual = capacity_cue published AND structure_cue published
```

When dual:

- Identity / Executive close keeps **both**
- Insight keeps **both**
- Condition: “Hai lớp đã công bố đều đúng… đừng chọn một nhãn”
- SELF_CARRY + dual names the lived structure (Ấn → chuẩn bị / hỗ trợ / ổn định nền)
- OUTPUT + follow unchanged (0002 hold)

### Lived structure (enabler)

`structure_to_plain` uses `.lower()` so “Chính Ấn” matches “ấn”. Maps: tòng, ấn, tài, quan|sát, thương|thực. Fallback is a usable hold-frame — never empty “khung lá số”.

### Avoid dedupe (PB-013)

`_avoid_block` skips identical realized lines.

---

## What was deliberately not done

| Temptation | Why not |
|------------|---------|
| CASE_0002-only memory string | Would break the hold chart and teach case-locking |
| P04-only conserving sentence | Conserving is a **band+theme rule** |
| Wire Theme Library catalog (PB-005) | Catalog frozen this iteration; consume is next |
| Change Product Context | Frozen · 0003 parent path must hold |
| Rename CLL section titles | Frozen CLL docs |

---

## Tests run (module only)

```text
py -3.14 -m pytest tests/production/test_commercial_language.py \
  tests/production/test_product_context.py \
  tests/production/test_case_0001_regression.py -q
```

**34 passed.**

---

END
