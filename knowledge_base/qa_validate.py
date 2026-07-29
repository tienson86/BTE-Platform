"""
Knowledge Base QA — read-only validation for knowledge_base/.

Kiểm tra:
- JSON format
- UTF-8 encoding (no BOM)
- schema (theo schema.json gần nhất của module)
- duplicate id
- duplicate alias
- empty required field (scalar)
- references

Không sửa dữ liệu. Chỉ đọc và sinh validation_report.md.

Chạy:
    python knowledge_base/qa_validate.py
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:  # pragma: no cover
    jsonschema = None  # type: ignore[assignment]
    Draft7Validator = None  # type: ignore[misc, assignment]

KB_ROOT = Path(__file__).resolve().parent
REPORT_PATH = KB_ROOT / "validation_report.md"
REPO_ROOT = KB_ROOT.parent

SKIP_DIR_NAMES = {"__pycache__", ".git", ".pytest_cache"}
SCHEMA_NAME = "schema.json"
METADATA_NAME = "metadata.json"

URL_RE = re.compile(r"^https?://", re.IGNORECASE)
PATHISH_RE = re.compile(
    r"[/\\]|^(?:\.\.?/)|(?:\.(?:json|md|csv|ya?ml|txt|pdf)$)",
    re.IGNORECASE,
)


@dataclass(slots=True)
class Finding:
    """Một kết quả kiểm tra."""

    severity: str  # error | warning | info
    check: str
    path: str
    message: str


@dataclass(slots=True)
class QaState:
    """Trạng thái tích lũy khi quét knowledge_base."""

    findings: list[Finding] = field(default_factory=list)
    json_files: list[Path] = field(default_factory=list)
    data_files: list[Path] = field(default_factory=list)
    schema_files: list[Path] = field(default_factory=list)
    metadata_files: list[Path] = field(default_factory=list)
    # path -> parsed object (chỉ khi JSON hợp lệ)
    parsed: dict[str, Any] = field(default_factory=dict)
    # path -> nearest schema path
    schema_for: dict[str, Path | None] = field(default_factory=dict)


def rel(path: Path) -> str:
    """Đường dẫn tương đối so với repo root."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def add(
    state: QaState,
    *,
    severity: str,
    check: str,
    path: Path | str,
    message: str,
) -> None:
    """Ghi một finding."""
    state.findings.append(
        Finding(
            severity=severity,
            check=check,
            path=rel(Path(path)) if isinstance(path, Path) else path,
            message=message,
        )
    )


def discover_json_files(root: Path) -> list[Path]:
    """Thu thập mọi file .json dưới knowledge_base, bỏ thư mục cache."""
    files: list[Path] = []
    for path in sorted(root.rglob("*.json")):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return files


def classify(path: Path) -> str:
    """Phân loại file: schema | metadata | data."""
    name = path.name.lower()
    if name == SCHEMA_NAME:
        return "schema"
    if name == METADATA_NAME:
        return "metadata"
    return "data"


def find_nearest_schema(path: Path, root: Path) -> Path | None:
    """Tìm schema.json gần nhất khi đi lên từ thư mục chứa file."""
    current = path.parent
    root = root.resolve()
    while True:
        candidate = current / SCHEMA_NAME
        if candidate.is_file():
            return candidate
        if current.resolve() == root or current.parent == current:
            return None
        current = current.parent


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_utf8(state: QaState, path: Path) -> bytes | None:
    """Validate UTF-8 encoding và không có BOM. Trả raw bytes nếu đọc được."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        add(
            state,
            severity="error",
            check="utf8",
            path=path,
            message=f"không đọc được file: {exc}",
        )
        return None

    if raw.startswith(b"\xef\xbb\xbf"):
        add(
            state,
            severity="error",
            check="utf8",
            path=path,
            message="file có UTF-8 BOM (yêu cầu UTF-8 không BOM)",
        )
        # vẫn decode phần còn lại để tiếp tục các check khác
        payload = raw[3:]
    else:
        payload = raw

    try:
        payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        add(
            state,
            severity="error",
            check="utf8",
            path=path,
            message=f"không phải UTF-8 hợp lệ: {exc}",
        )
        return None

    return raw if not raw.startswith(b"\xef\xbb\xbf") else b"\xef\xbb\xbf" + payload


def check_json_format(state: QaState, path: Path, raw: bytes | None) -> Any | None:
    """Parse JSON; ghi lỗi nếu format sai."""
    if raw is None:
        return None
    text = raw.decode("utf-8-sig")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        add(
            state,
            severity="error",
            check="json_format",
            path=path,
            message=f"JSON không hợp lệ: {exc}",
        )
        return None
    state.parsed[rel(path)] = data
    return data


def _type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _json_type_ok(expected: str | list[str], value: Any) -> bool:
    expected_list = [expected] if isinstance(expected, str) else list(expected)
    actual = _type_name(value)
    for item in expected_list:
        if item == "number" and actual in {"integer", "number"}:
            return True
        if item == actual:
            return True
    return False


def validate_against_schema_manual(
    state: QaState,
    path: Path,
    data: Any,
    schema: dict[str, Any],
) -> None:
    """Fallback schema check khi không có thư viện jsonschema."""
    if not isinstance(data, dict):
        add(
            state,
            severity="error",
            check="schema",
            path=path,
            message="root phải là object",
        )
        return

    required = list(schema.get("required", []))
    properties = dict(schema.get("properties", {}))
    additional = schema.get("additionalProperties", True)

    for key in required:
        if key not in data:
            add(
                state,
                severity="error",
                check="schema",
                path=path,
                message=f"thiếu field bắt buộc '{key}'",
            )

    if additional is False:
        for key in data:
            if key not in properties:
                add(
                    state,
                    severity="error",
                    check="schema",
                    path=path,
                    message=f"field thừa '{key}'",
                )

    for key, prop in properties.items():
        if key not in data:
            continue
        expected = prop.get("type")
        if expected is not None and not _json_type_ok(expected, data[key]):
            add(
                state,
                severity="error",
                check="schema",
                path=path,
                message=(
                    f"field '{key}' sai kiểu: mong đợi {expected}, "
                    f"nhận {_type_name(data[key])}"
                ),
            )
        if "enum" in prop and data[key] not in prop["enum"]:
            add(
                state,
                severity="error",
                check="schema",
                path=path,
                message=f"field '{key}' = {data[key]!r} không thuộc enum {prop['enum']}",
            )
        if (
            isinstance(data[key], str)
            and "pattern" in prop
            and re.search(prop["pattern"], data[key]) is None
        ):
            add(
                state,
                severity="error",
                check="schema",
                path=path,
                message=f"field '{key}' không khớp pattern {prop['pattern']!r}",
            )
        if expected == "array" and isinstance(data[key], list):
            item_schema = prop.get("items") or {}
            item_type = item_schema.get("type")
            if item_type:
                for idx, item in enumerate(data[key]):
                    if not _json_type_ok(item_type, item):
                        add(
                            state,
                            severity="error",
                            check="schema",
                            path=path,
                            message=(
                                f"field '{key}[{idx}]' sai kiểu: mong đợi {item_type}, "
                                f"nhận {_type_name(item)}"
                            ),
                        )


def check_schema(state: QaState, path: Path, data: Any, schema_path: Path | None) -> None:
    """Validate data object theo schema.json của module."""
    if schema_path is None:
        add(
            state,
            severity="warning",
            check="schema",
            path=path,
            message="không tìm thấy schema.json cho module này",
        )
        return

    schema_key = rel(schema_path)
    schema = state.parsed.get(schema_key)
    if schema is None:
        # schema chưa parse được → đã có lỗi json/utf8 riêng
        add(
            state,
            severity="error",
            check="schema",
            path=path,
            message=f"không dùng được schema {schema_key}",
        )
        return

    if not isinstance(schema, dict):
        add(
            state,
            severity="error",
            check="schema",
            path=path,
            message=f"schema {schema_key} không phải object",
        )
        return

    if Draft7Validator is not None:
        try:
            validator = Draft7Validator(schema)
            errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        except Exception as exc:  # noqa: BLE001 — schema có thể lỗi cấu trúc
            add(
                state,
                severity="error",
                check="schema",
                path=path,
                message=f"schema {schema_key} không dùng được: {exc}",
            )
            return
        for err in errors:
            loc = ".".join(str(p) for p in err.path) or "(root)"
            add(
                state,
                severity="error",
                check="schema",
                path=path,
                message=f"{loc}: {err.message}",
            )
        return

    validate_against_schema_manual(state, path, data, schema)


def check_empty_required(
    state: QaState,
    path: Path,
    data: Any,
    schema_path: Path | None,
) -> None:
    """Báo lỗi khi field bắt buộc kiểu scalar bị rỗng / null."""
    if not isinstance(data, dict):
        return

    required: list[str] = []
    properties: dict[str, Any] = {}
    if schema_path is not None:
        schema = state.parsed.get(rel(schema_path))
        if isinstance(schema, dict):
            required = list(schema.get("required", []))
            properties = dict(schema.get("properties", {}))

    if not required:
        # fallback tối thiểu khi không có schema
        required = [k for k in ("id", "name") if k in data]

    in_examples = "examples" in path.parts
    for key in required:
        if key not in data:
            continue  # thiếu field đã được check schema
        value = data[key]
        prop = properties.get(key, {})
        expected = prop.get("type")

        if value is None:
            severity = "warning" if in_examples else "error"
            add(
                state,
                severity=severity,
                check="empty_required",
                path=path,
                message=f"field bắt buộc '{key}' = null",
            )
            continue

        if expected == "string" or (expected is None and isinstance(value, str)):
            if isinstance(value, str) and value.strip() == "":
                severity = "warning" if in_examples else "error"
                add(
                    state,
                    severity=severity,
                    check="empty_required",
                    path=path,
                    message=f"field bắt buộc '{key}' đang rỗng",
                )


def check_references(state: QaState, path: Path, data: Any) -> None:
    """Validate mảng references (nếu có)."""
    if not isinstance(data, dict) or "references" not in data:
        return

    refs = data["references"]
    if not isinstance(refs, list):
        # schema check đã báo sai kiểu; tránh trùng lặp nặng
        return

    seen_local: set[str] = set()
    for idx, item in enumerate(refs):
        label = f"references[{idx}]"
        if not isinstance(item, str):
            add(
                state,
                severity="error",
                check="references",
                path=path,
                message=f"{label} phải là string",
            )
            continue
        if item.strip() == "":
            add(
                state,
                severity="error",
                check="references",
                path=path,
                message=f"{label} đang rỗng",
            )
            continue

        key = item.strip()
        if key in seen_local:
            add(
                state,
                severity="warning",
                check="references",
                path=path,
                message=f"{label} trùng trong cùng file: {item!r}",
            )
        seen_local.add(key)

        if URL_RE.match(item):
            parsed = urlparse(item)
            if not parsed.scheme or not parsed.netloc:
                add(
                    state,
                    severity="error",
                    check="references",
                    path=path,
                    message=f"{label} URL không hợp lệ: {item!r}",
                )
            continue

        if PATHISH_RE.search(item):
            candidates = [
                (path.parent / item).resolve(),
                (KB_ROOT / item).resolve(),
                (REPO_ROOT / item).resolve(),
            ]
            if not any(c.is_file() or c.is_dir() for c in candidates):
                add(
                    state,
                    severity="warning",
                    check="references",
                    path=path,
                    message=f"{label} trỏ tới đường dẫn không tồn tại: {item!r}",
                )


def check_duplicate_ids(state: QaState) -> None:
    """Phát hiện id trùng giữa các data file."""
    index: dict[str, list[str]] = {}
    for path in state.data_files:
        key = rel(path)
        data = state.parsed.get(key)
        if not isinstance(data, dict):
            continue
        if "id" not in data:
            continue
        ident = data["id"]
        if not isinstance(ident, str) or ident.strip() == "":
            continue
        index.setdefault(ident, []).append(key)

    for ident, paths in sorted(index.items()):
        if len(paths) > 1:
            joined = ", ".join(paths)
            add(
                state,
                severity="error",
                check="duplicate_id",
                path="(global)",
                message=f"id trùng {ident!r} tại: {joined}",
            )


def check_duplicate_aliases(state: QaState) -> None:
    """Phát hiện alias trùng trong một file và giữa các file."""
    global_index: dict[str, list[str]] = {}

    for path in state.data_files:
        key = rel(path)
        data = state.parsed.get(key)
        if not isinstance(data, dict):
            continue
        aliases = data.get("aliases")
        if not isinstance(aliases, list):
            continue

        local_seen: set[str] = set()
        for idx, alias in enumerate(aliases):
            if not isinstance(alias, str):
                continue
            normalized = alias.strip().casefold()
            if normalized == "":
                add(
                    state,
                    severity="error",
                    check="duplicate_alias",
                    path=path,
                    message=f"aliases[{idx}] đang rỗng",
                )
                continue
            if normalized in local_seen:
                add(
                    state,
                    severity="error",
                    check="duplicate_alias",
                    path=path,
                    message=f"alias trùng trong file: {alias!r}",
                )
            local_seen.add(normalized)
            global_index.setdefault(normalized, []).append(f"{key} ({alias!r})")

    for alias_key, locations in sorted(global_index.items()):
        unique_files = {loc.split(" (", 1)[0] for loc in locations}
        if len(unique_files) > 1:
            add(
                state,
                severity="error",
                check="duplicate_alias",
                path="(global)",
                message=f"alias trùng {alias_key!r} tại: {', '.join(locations)}",
            )


def check_schema_file_shape(state: QaState, path: Path, data: Any) -> None:
    """Kiểm tra sơ bộ schema.json là object schema hợp lệ."""
    if not isinstance(data, dict):
        add(
            state,
            severity="error",
            check="schema",
            path=path,
            message="schema.json phải là object",
        )
        return
    if "properties" not in data and "$ref" not in data:
        add(
            state,
            severity="warning",
            check="schema",
            path=path,
            message="schema.json thiếu 'properties'",
        )
    if Draft7Validator is not None:
        try:
            Draft7Validator.check_schema(data)
        except Exception as exc:  # noqa: BLE001
            add(
                state,
                severity="error",
                check="schema",
                path=path,
                message=f"schema.json không phải Draft-07 hợp lệ: {exc}",
            )


# ---------------------------------------------------------------------------
# Orchestration + report
# ---------------------------------------------------------------------------


def run_qa(root: Path = KB_ROOT) -> QaState:
    """Chạy toàn bộ kiểm tra read-only trên knowledge_base."""
    state = QaState()
    state.json_files = discover_json_files(root)

    for path in state.json_files:
        kind = classify(path)
        if kind == "schema":
            state.schema_files.append(path)
        elif kind == "metadata":
            state.metadata_files.append(path)
        else:
            state.data_files.append(path)

    # Pass 1: UTF-8 + JSON format cho mọi JSON
    for path in state.json_files:
        raw = check_utf8(state, path)
        data = check_json_format(state, path, raw)
        if data is None:
            continue
        if classify(path) == "schema":
            check_schema_file_shape(state, path, data)

    # Pass 2: schema / empty required / references cho data files
    for path in state.data_files:
        key = rel(path)
        data = state.parsed.get(key)
        if data is None:
            continue
        schema_path = find_nearest_schema(path, root)
        state.schema_for[key] = schema_path
        check_schema(state, path, data, schema_path)
        check_empty_required(state, path, data, schema_path)
        check_references(state, path, data)

    # Pass 3: cross-file uniqueness
    check_duplicate_ids(state)
    check_duplicate_aliases(state)

    return state


def _count(state: QaState, severity: str) -> int:
    return sum(1 for f in state.findings if f.severity == severity)


def _group_by_check(state: QaState) -> dict[str, list[Finding]]:
    grouped: dict[str, list[Finding]] = {}
    for finding in state.findings:
        grouped.setdefault(finding.check, []).append(finding)
    return grouped


def render_report(state: QaState) -> str:
    """Sinh nội dung Markdown cho validation_report.md."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    errors = _count(state, "error")
    warnings = _count(state, "warning")
    infos = _count(state, "info")
    status = "PASS" if errors == 0 else "FAIL"

    lines: list[str] = [
        "# Knowledge Base Validation Report",
        "",
        f"- Generated: `{now}`",
        f"- Root: `knowledge_base/`",
        f"- Status: **{status}**",
        f"- JSON files scanned: **{len(state.json_files)}**",
        f"- Data files: **{len(state.data_files)}**",
        f"- Schema files: **{len(state.schema_files)}**",
        f"- Metadata files: **{len(state.metadata_files)}**",
        f"- Errors: **{errors}**",
        f"- Warnings: **{warnings}**",
        f"- Info: **{infos}**",
        "",
        "## Checks",
        "",
        "| Check | Description |",
        "|-------|-------------|",
        "| `json_format` | File parse được như JSON |",
        "| `utf8` | Encoding UTF-8, không BOM |",
        "| `schema` | Khớp schema.json của module |",
        "| `duplicate_id` | Không trùng `id` giữa các file |",
        "| `duplicate_alias` | Không trùng `aliases` |",
        "| `empty_required` | Field bắt buộc scalar không rỗng |",
        "| `references` | Mục `references` hợp lệ / tồn tại nếu là path |",
        "",
        "## File inventory",
        "",
    ]

    if not state.json_files:
        lines.append("_Không tìm thấy file JSON nào._")
        lines.append("")
    else:
        lines.append("| File | Kind | Schema |")
        lines.append("|------|------|--------|")
        for path in state.json_files:
            kind = classify(path)
            schema = state.schema_for.get(rel(path))
            schema_cell = rel(schema) if schema else ("—" if kind != "data" else "missing")
            lines.append(f"| `{rel(path)}` | {kind} | `{schema_cell}` |")
        lines.append("")

    lines.extend(
        [
            "## Summary by check",
            "",
            "| Check | Errors | Warnings |",
            "|-------|--------|----------|",
        ]
    )
    check_names = [
        "json_format",
        "utf8",
        "schema",
        "duplicate_id",
        "duplicate_alias",
        "empty_required",
        "references",
    ]
    grouped = _group_by_check(state)
    for name in check_names:
        items = grouped.get(name, [])
        e = sum(1 for i in items if i.severity == "error")
        w = sum(1 for i in items if i.severity == "warning")
        mark = "OK" if e == 0 and w == 0 else ("FAIL" if e else "WARN")
        lines.append(f"| `{name}` ({mark}) | {e} | {w} |")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    if not state.findings:
        lines.append("Không có lỗi hoặc cảnh báo.")
        lines.append("")
    else:
        order = {"error": 0, "warning": 1, "info": 2}
        ordered = sorted(
            state.findings,
            key=lambda f: (order.get(f.severity, 9), f.check, f.path, f.message),
        )
        lines.append("| Severity | Check | Path | Message |")
        lines.append("|----------|-------|------|---------|")
        for finding in ordered:
            msg = finding.message.replace("|", "\\|")
            lines.append(
                f"| {finding.severity} | `{finding.check}` | `{finding.path}` | {msg} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Policy",
            "",
            "- Tool **chỉ đọc** `knowledge_base/`.",
            "- **Không** sửa dữ liệu nguồn.",
            "- Report được ghi đè mỗi lần chạy tại `knowledge_base/validation_report.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(state: QaState, report_path: Path = REPORT_PATH) -> Path:
    """Ghi validation_report.md (chỉ ghi report, không đụng data)."""
    report_path.write_text(render_report(state), encoding="utf-8", newline="\n")
    return report_path


def main() -> int:
    """Entry point CLI."""
    state = run_qa(KB_ROOT)
    out = write_report(state, REPORT_PATH)
    errors = _count(state, "error")
    warnings = _count(state, "warning")
    print(f"Report: {rel(out)}")
    print(f"Scanned: {len(state.json_files)} JSON file(s)")
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")
    print("Status:", "PASS" if errors == 0 else "FAIL")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
