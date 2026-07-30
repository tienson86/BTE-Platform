"""Unit tests for registry_cli."""

from __future__ import annotations

from pathlib import Path

import registry_cli


def test_cli_validate(registry_root: Path, project_root: Path) -> None:
    code = registry_cli.main(
        [
            "--project-root",
            str(project_root),
            "--registry-root",
            str(registry_root),
            "validate",
            "--include-samples",
        ]
    )
    assert code == 0


def test_cli_stats_list_search(registry_root: Path, project_root: Path) -> None:
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "stats",
            ]
        )
        == 0
    )
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "list",
                "--registry",
                "knowledge_registry",
            ]
        )
        == 0
    )
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "search",
                "KNO-000001",
            ]
        )
        == 0
    )


def test_cli_export_reindex(
    registry_root: Path,
    project_root: Path,
    tmp_path: Path,
) -> None:
    out = tmp_path / "export"
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "export",
                "--output",
                str(out),
                "--include-indexes",
            ]
        )
        == 0
    )
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "reindex",
                "--write",
            ]
        )
        == 0
    )


def test_cli_import_dry_run(
    registry_root: Path,
    tmp_path: Path,
) -> None:
    source = tmp_path / "incoming.json"
    source.write_text(
        '{"version":"1.0.0","registry_name":"report_registry","records":[]}',
        encoding="utf-8",
    )
    code = registry_cli.main(
        [
            "--registry-root",
            str(registry_root),
            "import",
            "--source",
            str(source),
            "--dry-run",
        ]
    )
    assert code == 0
