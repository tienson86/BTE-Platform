"""Markdown report generators for baseline build/validation/release/freeze."""

from __future__ import annotations

from typing import Any

from baseline.models import ValidationReport


def generate_build_report(
    context_dict: dict[str, Any],
    artifacts: list[str],
    statistics: dict[str, Any],
    validation_summary: dict[str, str],
) -> str:
    """Generate build_report.md content."""
    lines = [
        "# Pack 01 Baseline Build Report",
        "",
        f"- Pack: `{context_dict.get('pack_id')}`",
        f"- Version: `{context_dict.get('version')}`",
        f"- Timestamp: `{context_dict.get('timestamp')}`",
        "",
        "## Artifacts",
        "",
    ]
    for artifact in artifacts:
        lines.append(f"- `{artifact}`")
    lines.extend(
        [
            "",
            "## Validation Summary",
            "",
            "| Domain | Status |",
            "|---|---|",
        ]
    )
    for domain, status in sorted(validation_summary.items()):
        lines.append(f"| {domain} | {status} |")
    lines.extend(
        [
            "",
            "## Statistics",
            "",
            "```json",
            _mini_json(statistics),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def generate_validation_report_md(
    reports: dict[str, ValidationReport],
) -> str:
    """Generate validation_report.md content."""
    lines = [
        "# Pack 01 Baseline Validation Report",
        "",
    ]
    overall = (
        "PASS"
        if all(report.status == "PASS" for report in reports.values())
        else "FAIL"
    )
    lines.append(f"**Overall Status:** {overall}")
    lines.append("")
    for name, report in sorted(reports.items()):
        lines.extend(
            [
                f"## {name}",
                "",
                f"- Status: `{report.status}`",
                f"- Errors: `{report.error_count}`",
                f"- Warnings: `{report.warning_count}`",
                "",
            ]
        )
        if report.findings:
            lines.append("| Code | Severity | Message |")
            lines.append("|---|---|---|")
            for finding in report.findings:
                message = finding.message.replace("|", "\\|")
                lines.append(
                    f"| {finding.code} | {finding.severity} | {message} |"
                )
            lines.append("")
        else:
            lines.append("No findings.")
            lines.append("")
    return "\n".join(lines)


def generate_release_candidate_md(
    governance: dict[str, Any],
    statistics: dict[str, Any],
) -> str:
    """Generate release_candidate.md content."""
    overall = governance.get("overall_status", "NOT_READY")
    lines = [
        "# Pack 01 Release Candidate",
        "",
        f"**Status:** `{overall}`",
        "",
        f"- Version: `{governance.get('version')}`",
        f"- Timestamp: `{governance.get('timestamp')}`",
        "",
        "## Readiness Gates",
        "",
        "| Gate | Ready |",
        "|---|---|",
        f"| Freeze | {governance['freeze_readiness']['ready']} |",
        f"| Baseline | {governance['baseline_readiness']['ready']} |",
        f"| Compiler | {governance['compiler_readiness']['ready']} |",
        f"| Validation | {governance['validation_readiness']['ready']} |",
        f"| Release | {governance['release_readiness']['ready']} |",
        "",
        "## Inventory Snapshot",
        "",
        f"- Knowledge Records: `{statistics.get('knowledge_records')}`",
        f"- Registries: `{statistics.get('registry_count')}`",
        f"- Ontology Classes: `{statistics.get('ontology_classes')}`",
        f"- Graph Nodes: `{statistics.get('graph_nodes')}`",
        f"- Graph Edges: `{statistics.get('graph_edges')}`",
        "",
    ]
    return "\n".join(lines)


def generate_freeze_readiness_md(governance: dict[str, Any]) -> str:
    """Generate freeze_readiness.md content."""
    ready = governance.get("freeze_readiness", {}).get("ready", False)
    lines = [
        "# Pack 01 Freeze Readiness",
        "",
        f"**Freeze Ready:** `{ready}`",
        "",
        f"**Overall Status:** `{governance.get('overall_status')}`",
        "",
        "## Criteria",
        "",
    ]
    criteria = governance.get("freeze_readiness", {}).get("criteria", {})
    for key, value in sorted(criteria.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append(
        "Pack 01 may be frozen only when all readiness gates are true "
        "and no ERROR/CRITICAL validation findings remain."
    )
    lines.append("")
    return "\n".join(lines)


def _mini_json(payload: dict[str, Any]) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
