"""Shared sys.path bootstrap for Runtime entrypoints.

``python runtime/*.py`` puts ``.../runtime`` on ``sys.path[0]``.
That must be replaced by the repo root so third-party imports are not
shadowed by top-level modules living under ``runtime/``.
"""

from __future__ import annotations

import sys
from pathlib import Path


def project_root() -> Path:
    """Return the BTE repository root (parent of ``runtime/``)."""
    return Path(__file__).resolve().parents[1]


def ensure_project_root_on_sys_path() -> Path:
    """Put repo root at ``sys.path[0]`` and remove the ``runtime/`` script dir."""
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent
    root_s = str(root)
    script_s = str(script_dir)

    def key(entry: str) -> str:
        if not entry:
            return entry
        try:
            return str(Path(entry).resolve())
        except OSError:
            return entry

    skip = {root_s, script_s, str(root.resolve()), str(script_dir.resolve())}
    sys.path[:] = [p for p in sys.path if key(p) not in skip]
    sys.path.insert(0, root_s)
    return root
