# CASE-0001 — Nguyễn Tiến Sơn (Report V1)

## Canonical status

**CASE-0001** is the canonical Simple Report Export V1 validation case.

| Field | Canonical value |
|-------|-----------------|
| Case ID | `CASE-0001` |
| Họ tên | Nguyễn Tiến Sơn |
| Giới tính | Nam (`male`) |
| Ngày sinh dương lịch | 1987-01-21 |
| Giờ sinh | 04:30 |
| Timezone | `Asia/Bangkok` (UTC+07:00) |
| Nơi sinh | Hà Tây, Việt Nam |

### Expected pillars (validation)

| Trụ | Can Chi |
|-----|---------|
| Năm | Bính Dần |
| Tháng | Tân Sửu |
| Ngày | Canh Ngọ |
| Giờ | Mậu Dần |

## Files in this folder

| File | Purpose |
|------|---------|
| `input.json` | Canonical birth input for Report V1 tests |
| `expected_report_input.json` | Snapshot of runtime `ReportInputV1.to_dict()` |

## Conflict resolution (WP-RPT-002)

| Source | Birth time | Location | Status |
|--------|------------|----------|--------|
| **`tests/golden_dataset/report_v1/CASE-0001/`** | **04:30** | **Hà Tây** | **CANONICAL for Report V1** |
| `knowledge/pilot/cases/CASE-0001/input.json` | 04:30 | Hà Nội | Pilot reference — location differs |
| `tests/golden_dataset/inputs/case_0001.json` | 04:15 | Hà Tây/Ung Hoa | **LEGACY** — pre-Report-V1 harness |

`case_0001.json` (lowercase) is **not overwritten**. It remains the legacy golden harness case with different birth minute and ISO datetime schema.

## Regenerate snapshot

```bash
python -c "
import json
from pathlib import Path
from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Adapter
from tests.report_engine.case_0001_runtime import build_case_0001_source

source = build_case_0001_source()
report_input = ReportInputV1Adapter().build(source)
out = Path('tests/golden_dataset/report_v1/CASE-0001/expected_report_input.json')
out.write_text(json.dumps(report_input.to_dict(), indent=2, ensure_ascii=False, sort_keys=True) + chr(10), encoding='utf-8')
"
```

## Generate HTML preview (local only — not committed by default)

```bash
python -c "
from pathlib import Path
from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Adapter
from engines.report_engine.rendering.html_report_v1 import render_html
from tests.report_engine.case_0001_runtime import build_case_0001_source

report_input = ReportInputV1Adapter().build(build_case_0001_source())
out = Path('knowledge/report_v1_validation/previews/CASE-0001.html')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(render_html(report_input), encoding='utf-8')
print(out)
"
```
